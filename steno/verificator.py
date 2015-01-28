# -*- coding: utf-8 -*-
"""
.. module:: verificator
   :platform: Unix, Windows
   :synopsis: Comparison of user's input and subtitles content

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""
# License: wxWidgets (wxWindows Library Licence) 3.1

import re
from datetime import datetime
from difflib import ndiff

from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime


class Verificator(object):
    """Checks user answers in the learning process, prepares the subtitle
    text.

    """

    def __init__(self, player):
        """:class:`Verificator` serves to check the correctness of user input.

        :param player: Player frame instance
        :type player: :class:`player.Player`

        """
        self.player = player
        self._subtitle = None
        self._complete = []
        self._created_at = datetime.now()
        self._hint_counter = 0
        self._mistakes_counter = 0

    def set_subtitle(self, subtitle, replace=True, force=False):
        """Sets the current subtitle which will be used to for comparison
        with user's answer.

        :param subtitle: Current subtitle
        :type subtitle: :class:`pysrt.srtitem.SubRipItem`
        :param replace: Overwrite previously set subtitle
        :param force: Set the subtitle even if it was completed previously
        :returns: Execution status
        :rtype: boolean

        """
        if isinstance(subtitle, SubRipItem):
            if not self.has_subtitle() or replace:
                if not self.whether_complete(subtitle) or force:
                    self.clear_subtitle(complete=False)
                    self._subtitle = subtitle
                    return True
        return False

    def get_subtitle(self):
        """Getter for the current subtitle attribute.

        :returns: Current subtitle or None if there isn't
        :rtype: :class:`pysrt.srtitem.SubRipItem` or None

        """
        return self._subtitle

    def clear_subtitle(self, complete=True):
        """Clears the current subtitle and related private attributes.

        :param complete: Mark the current subtitle as completed

        """
        if complete and self.has_subtitle():
            self._complete.append(self._subtitle)
        self._subtitle = None
        self._etalon = None
        self._prepared_origin_words = None

    def whether_complete(self, subtitle):
        """Checks whether current subtitle previously completed or not.

        :param subtitle: Suspicious subtitle
        :type subtitle: :class:`pysrt.srtitem.SubRipItem`
        :returns: State of completion
        :rtype: boolean

        """
        return bool(subtitle.text in [sub.text for sub in self._complete])

    def has_subtitle(self):
        """Checks the existence of current subtitle.

        :returns: Existence of the current subtitle
        :rtype: boolean

        """
        return isinstance(self._subtitle, SubRipItem)

    def is_passed(self, position):
        """Checks for the ending of the current subtitle.

        :param int position: Position in media stream (in seconds)
        :returns: Achievement of the subtitle ending
        :rtype: boolean

        """
        if (
            self.has_subtitle() and
            SubRipTime(seconds=int(position)) >= self._subtitle.end
        ):
            return True
        return False

    def _clean_includes(self):
        """Returns a collection of symbols which may pass the filter.

        :returns: "Safe" symbols
        :rtype: tuple

        """
        return (u' ', u"'",)

    def _accept_filters(self, src):
        """Applies regex filters to a text.

        :param src: Source grubby text
        :type src: str or unicode
        :returns: Filtered tidy text or None if `src` isn't a text
        :rtype: unicode or None

        """
        if isinstance(src, (int, float)):
            src = unicode(src)
        if isinstance(src, (str, unicode)):
            result = src
            for pattern, replacement in self.player.get_filters().iteritems():
                result = re.sub(pattern, replacement, result)
            return result
        else:
            return None

    def _clean_text(self, src):
        """Removes unwanted characters from a text.

        :param src: Source text
        :type src: str or unicode
        :returns: Clean text or None if `src` isn't a text
        :rtype: unicode or None

        """
        if isinstance(src, (int, float)):
            src = unicode(src)
        if isinstance(src, (str, unicode)):
            return u''.join(symbol for symbol in src.lower()
                            if symbol.isalpha() or symbol.isdigit()
                            or symbol in self._clean_includes())
        else:
            return None

    def get_etalon(self):
        """Prepares a filtered etalon phrase from the subtitle text.

        :returns: Filtered subtitle text
        :rtype: unicode

        """
        if getattr(self, '_etalon', None) is None:
            text = self.get_subtitle().text
            text = self._accept_filters(text)
            self._etalon = self._clean_text(text)
        return self._etalon

    def get_etalon_words(self):
        """Returns clean words prepared from the subtitle text

        :returns: Clean words or None if there isn't source for words
        :rtype: list of unicode or None

        """
        etalon = self.get_etalon()
        if isinstance(etalon, (str, unicode)):
            return etalon.split()
        else:
            return None

    def _prepare_answer_words(self, text):
        """Cleans user's answer and splits it into words.

        :param text: User's answer
        :type text: str or unicode
        :returns: Cleaned words or empty list
        :rtype: list of unicode

        """
        result = self._clean_text(text)
        return result.split() if result is not None else []

    def _prepare_origin_words(self):
        """Prepares the original subtitle text divided into words.

        :returns: Original subtitle text like a list of words
        :rtype: list of unicode

        """
        if getattr(self, '_prepared_origin_words', None) is None:

            def has_alpha_or_digit(word):
                for character in word:
                    if character.isalpha() or character.isdigit():
                        return True
                return False

            self._prepared_origin_words = filter(
                has_alpha_or_digit, self._accept_filters(
                    self.get_subtitle().text).split())
        return self._prepared_origin_words

    def get_last_word(self):
        """Returns last full word from user's answer.

        :returns: Last word from answer
        :rtype: unicode

        """
        return getattr(self, '_last_word', None)

    def verify_answer(self, answer):
        """Checks the correctness of every symbol in user's answer.

        :param answer: User's answer
        :type answer: str or unicode
        :returns: Estimation of the answer as a list of pairs where first value
                  is a symbol and second is an estimation of its correctness
        :rtype: list of tuples (list of pairs)

        """
        result = []
        if self.has_subtitle():
            origin_words = self._prepare_origin_words()
            etalon_words = self.get_etalon_words()
            answer_words = self._prepare_answer_words(answer)
            for idx in xrange(len(answer_words)):
                try:
                    if answer_words[idx] == etalon_words[idx]:
                        result.extend([(sym, True)
                                       for sym in origin_words[idx]])
                        result.append((u' ', True))
                        self._last_word = etalon_words[idx]
                    else:
                        all_next_incorrect = False
                        for cursor in ndiff(answer_words[idx],
                                            etalon_words[idx]):
                            if cursor[0] == u' ':
                                if all_next_incorrect:
                                    result.append((cursor[2], False))
                                    self._mistakes_counter += 1
                                    break
                                else:
                                    result.append((cursor[2], True))
                            elif cursor[0] == u'-':
                                result.append((cursor[2], False))
                                self._mistakes_counter += 1
                                break
                            elif cursor[0] == u'+':
                                all_next_incorrect = True
                except IndexError:
                    if len(answer_words[idx]):
                        result.append((answer_words[idx][0], False))
                        self._mistakes_counter += 1
        return result

    def hint(self, answer):
        """Prompt next word to the user. If user began to write next word it
        will complete this, else it will add full next word.

        :param answer: User's input in actual state
        :type answer: str or unicode
        :returns: Received input with completed or added next word
        :rtype: unicode

        """
        result = u''
        if self.has_subtitle():
            self._hint_counter += 1
            etalon_words = self.get_etalon_words()
            answer_words = self._prepare_answer_words(answer)
            if not len(answer_words):
                try:
                    return etalon_words[0]
                except IndexError:
                    return u''
            else:
                try:
                    if etalon_words[len(answer_words)-1] != answer_words[-1]:
                        answer_words[-1] = etalon_words[len(answer_words)-1]
                    else:
                        answer_words.append(etalon_words[len(answer_words)])
                except IndexError:
                    pass
                finally:
                    result = u' '.join(answer_words)
        return result

    def is_complete(self, answer):
        """Checks completeness of current subtitles fragment.

        :param answer: User's answer in actual state
        :type answer: unicode or str
        :returns: Whether the current fragment is finished or not
        :rtype: boolean

        """
        return bool(u' '.join(self._prepare_answer_words(answer)) ==
                    u' '.join(self.get_etalon_words()))

    def is_empty(self):
        """Checks the content existence in current subtitles fragment.

        Sometimes text ends after an application of filters.

        :returns: Existence of the text
        :rtype: boolean

        """
        return not bool(len(self.get_etalon_words()))

    def fragment_length(self):
        """Calculates the length of the subtitles fragment in symbols.

        :returns: Length of the fragment (in characters)
        :rtype: int

        """
        if self.has_subtitle():
            return len(u' '.join(self._prepare_origin_words()))
        else:
            return 0

    def get_statistics(self):
        """Returns a statistics information about learning process.

        :returns: Learning statistics
        :rtype: dict

        """
        return {
            u'completed_fragments': len(self._complete),
            u'learning_time':
                (datetime.now() - self._created_at).total_seconds(),
            u'hint_used': self._hint_counter,
            u'mistakes': self._mistakes_counter,
            u'total_chars': sum([len(sub.text) for sub in self._complete]),
        }
