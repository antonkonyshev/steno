# -*- coding: utf-8 -*-
"""
.. module:: translator
   :platform: Unix, Windows
   :synopsis: Language translation behavior

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import threading

import google_translate_api as gtapi


class Translator(gtapi.TranslateService):
    """Customization of :class:`google_translate_api.TranslateService`
    mainly for output formatting.

    """

    def __init__(self):
        """:class:`Translator` serves to interact with Google Translate API."""
        super(Translator, self).__init__()
        self.lock = threading.Lock()

    def trans_details(self, source_lang, target_lang, value):
        """Performs translation and formats detailed output.

        Suitable options for `source_lang` and `target_lang` parameters stored
        in :const:`defaults.Config.LANGUAGES`.

        :param source_lang: Source language of the `value`
        :type source_lang: str or unicode
        :param target_lang: Language of the translation
        :type target_lang: str or unicode
        :param value: Text or word
        :returns: Translation with details
        :rtype: unicode

        """
        response = super(Translator, self).trans_details(source_lang,
                                                         target_lang, value)
        result = u''
        if response:
            try:
                sentence = response.get(u'sentences', [])[0]
            except IndexError:
                sentence = {}
            details = response.get(u'dict', [])
            result = u'\n'.join([
                sentence.get(u'orig', u''),
                sentence.get(u'trans', u''), u'',
                u'Translit: {0}'.format(sentence.get(u'translit', u'')),
            ])
            for form in details:
                result = u'\n'.join([
                    result, u'',
                    u'{0} | {1}'.format(form.get(u'base_form', u''),
                                        form.get(u'pos', u'')),
                ])
                for entry in form.get(u'entry', []):
                    result = u' '.join([
                        result, u'\n',
                        u' {0}: '.format(entry.get(u'word', u'')),
                        u', '.join(entry.get(u'reverse_translation', [])),
                        u'[{0}]'.format(int(entry.get(u'score', 0.0) * 10000)),
                    ])
                result = u'\n'.join([result, u'', u'  Phrases:'])
                for term in form.get(u'terms', []):
                    result = u'\n    '.join([result, term])
        return result
