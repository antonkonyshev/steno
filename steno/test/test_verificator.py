# -*- coding: utf-8 -*-
"""
.. module:: test_verificator
   :platform: Unix, Windows
   :synopsis: Testing of verificator module

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import unittest

import mock

from pysrt.srtitem import SubRipItem

from player import Player
from verificator import Verificator
from defaults import Defaults


class VerificatorTestCase(unittest.TestCase):
    def setUp(self):
        mock_player_attrs = {
            u'get_filters.return_value': Defaults.DEFAULT_FILTERS,
        }
        mock_player = mock.Mock(spec=Player, **mock_player_attrs)
        self.verificator = Verificator(mock_player)
        self.verificator.set_subtitle(SubRipItem(
            text=u"Hello! \n[emotions]\nWorld! It's...\n testing."))

    def tearDown(self):
        del self.verificator

    def test_text_cleaning(self):
        data = {
            u'Hello! \n[emotions]\nWorld.': [u'hello', u'world'],
            u'Hello \nworld!': [u'hello', u'world'],
            u"It's ...\n testing.": [u"it's", u'testing'],
            u"It's\ntesting!": [u"it's", u'testing'],
            u"Word": [u'word'],
        }
        for src, result in data.iteritems():
            self.verificator.set_subtitle(SubRipItem(text=src))
            self.assertEqual(self.verificator.get_etalon_words(), result,
                             msg=u'On cleaning of {0}'.format(src))

    def test_verify_answer_and_statistics(self):
        data = {
            u'hel': [(sym, True) for sym in u'hel'],
            u'hello': [(sym, True) for sym in u'Hello! '],
            u'hez': [(sym, False if sym == u'z' else True) for sym in u'hez'],
            u'hezl': [(sym, False if sym == u'z' else True) for sym in u'hez'],
            u'hezlo': [(sym, False if sym == u'z' else True)
                       for sym in u'hez'],
            u'hello ': [(sym, True) for sym in u'Hello! '],
            u'tests': [(u't', False)],
            u'hello worl': [(sym, True) for sym in u'Hello! worl'],
            u'hello world': [(sym, True) for sym in u'Hello! World! '],
            u"Hello! World! It's testing": [
                (sym, True) for sym in u"Hello! World! It's... testing. "],
            u'hello wordm': [(sym, True if sym != u'd' else False)
                             for sym in u'Hello! word'],
            u"Hello! World! it'": [(sym, True)
                                   for sym in u"Hello! World! it'"],
            u"mello!": [(u'm', False)],
        }
        msg = u"On verifying of {0}.\nExpected: {1}.\nReturned: {2}."
        for src, result in data.iteritems():
            returned = self.verificator.verify_answer(src)
            self.assertEqual(returned, result,
                             msg=msg.format(src, result, returned))
        msg = u'\n'.join([u'For question: {3}.', msg])
        question = u'PERSON: Hello, [ emotions ] world! ! !'
        self.verificator.clear_subtitle(complete=True)
        self.verificator.set_subtitle(
            SubRipItem(text=question))
        data = {
            u'hel': [(sym, True) for sym in u'hel'],
            u'per': [(u'p', False)],
            u'hello': [(sym, True) for sym in u'Hello, '],
            u'hello world': [(sym, True) for sym in u'Hello, world! '],
            u'Hello, world': [(sym, True) for sym in u'Hello, world! '],
        }
        for src, result in data.iteritems():
            returned = self.verificator.verify_answer(src)
            self.assertEqual(returned, result,
                             msg=msg.format(src, result, returned, question))
        question = u'. . .Hello . . . world. . .'
        self.verificator.clear_subtitle(complete=True)
        self.verificator.set_subtitle(
            SubRipItem(text=question))
        data = {
            u'hel': [(sym, True) for sym in u'hel'],
            u'hello': [(sym, True) for sym in u'.Hello '],
            u'Hello wor': [(sym, True) for sym in u'.Hello wor'],
            u'Hello world': [(sym, True) for sym in u'.Hello world. '],
            u"Hello world. it's": [(sym, False if sym == u'i' else True)
                                   for sym in u'.Hello world. i'],
        }
        for src, result in data.iteritems():
            returned = self.verificator.verify_answer(src)
            self.assertEqual(returned, result,
                             msg=msg.format(src, result, returned, question))
        [self.verificator.hint(ans) for ans in (u'hel', u'hello w')]
        self.verificator.clear_subtitle(complete=True)
        stats = self.verificator.get_statistics()
        self.assertTrue(stats.get(u'learning_time', 0) > 0)
        for param, value in {
            u'completed_fragments': 3, u'hint_used': 2, u'mistakes': 8,
            u'total_chars': 108
        }.iteritems():
            self.assertEqual(stats.get(param, None), value,
                             msg=u'On verifying of {0}.'.format(param))

    def test_last_word(self):
        data = {
            u'hel': None, u'hello': u'hello', u'Hello! wo': u'hello',
            u'Hello! World': u'world', u'Hello! World! ': u'world',
            u"Hello! World! It's": u"it's",
            u"Hello! World! It's... testin": u"it's",
            u"Hello! World! It's... testing": u'testing',
            u"hello world": u'world', u"hello world it's testin": u"it's",
            u"hello world it's testing": u'testing',
        }
        for src, result in data.iteritems():
            self.verificator.verify_answer(src)
            last_word = self.verificator.get_last_word()
            self.assertEqual(
                last_word, result, msg=u'On verifying of {0}.\nExpected: {1}.'
                '\nReceived: {2}.'.format(src, result, last_word))
            if hasattr(self.verificator, u'_last_word'):
                delattr(self.verificator, u'_last_word')

    def test_hint(self):
        data = {
            u'': u'hello', u'h': u'hello', u'z': u'hello',
            u'hello': u'hello world', u'hello wo': u'hello world',
            u'hello wz': u'hello world',
            u'Hello! World! ': u"hello world it's",
            u"Hello! World! It's": u"hello world it's testing",
            u"Hello! World! It's ": u"hello world it's testing",
            u"hello world it's te": u"hello world it's testing",
            u"Hello! World! It's... testing ": u"hello world it's testing",
        }
        for src, result in data.iteritems():
            hint = self.verificator.hint(src)
            self.assertEqual(
                hint, result, msg=u'On verifying of {0}.\nExpected: {1}.'
                '\nReceived: {2}.'.format(src, result, hint))

    def test_is_complete_simple(self):
        data = {
            u'': False, u'hello': False, u"hello world it's": False,
            u"Hello! World! It's... t": False,
            u"Hello! World! It's... testing. ": True,
            u"Hello! World! It's... testing.": True,
        }
        for src, result in data.iteritems():
            self.assertEqual(self.verificator.is_complete(src), result,
                             msg=u'On verifying of "{0}".'.format(src))

    def test_is_empty(self):
        data = {
            u'[emotions]': True, u' [ emotions ] ': True,
            u'PERSON: [ emotions ]': True, u'. . .': True,
            u'PERSON: Hi': False, u'[emotions] Hi': False,
        }
        for src, result in data.iteritems():
            self.verificator.set_subtitle(SubRipItem(text=src))
            self.assertEqual(self.verificator.is_empty(), result,
                             msg=u'On verifying of {0}.'.format(src))

    def test_sequential_answering(self):
        data = (
            (u'he', [(sym, True) for sym in u'he']),
            (u'hen', [(sym, False if sym == u'n' else True)
                      for sym in u'hen']),
            (u'henl', [(sym, False if sym == u'n' else True)
                       for sym in u'hen']),
            (u'Hello! word', [(sym, False if sym == u'd' else True)
                              for sym in u'Hello! word']),
            (u'Hello! wormd', [(sym, False if sym == u'm' else True)
                               for sym in u'Hello! worm']),
            (u'Hello! World! ti', [(sym, False if sym == u't' else True)
                                   for sym in u'Hello! World! t']),
            (u"Hello! World! i't", [(sym, False if sym == u"'" else True)
                                    for sym in u"Hello! World! i'"]),
        )
        for answer, result in data:
            returned = self.verificator.verify_answer(answer)
            self.assertEqual(
                returned, result, msg=u'On verifying of {0}.\nExpected: {1}.'
                u'\nReceived: {2}.'.format(answer, result, returned))

    def test_is_complete_with_punctuation(self):
        data = {
            u'Hello!': u'hello', u'Hello...': u'hello',
            u'. . .Hello!': u'hello', u'Hello. . .': u'hello',
            u'[emotions]': u'', u'Hello [ emotions ] .': u'hello',
            u'PERSON: Hello, people. . .': u'hello people',
            u'PERSON:\nHello [ emotions ]\n, World ! ! !': u'Hello, world',
            u'Say: " Hello, World! "': u'say hello world',
            u'. . . World!': u'world',
        }
        for question, answer in data.iteritems():
            self.verificator.set_subtitle(SubRipItem(text=question))
            self.assertTrue(self.verificator.is_complete(answer),
                            msg=u'On verifying of {0}.'.format(question))
