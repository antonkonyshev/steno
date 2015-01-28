# -*- coding: utf-8 -*-
"""
.. module:: defaults
   :platform: Unix, Windows
   :synopsis: Default configuration values definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import sys
import os.path as op


class Defaults(object):

    # Name, version, author, copyright
    NAME = u"Steno"
    VERSION = u"0.1b3"
    LICENSE = u"wxWidgets (wxWindows Library Licence) 3.1"
    COPYRIGHT = u"Copyright 2014 Anton Konyshev"
    AUTHOR = u"Anton Konyshev <anton.konyshev@gmail.com>"
    WEBSITE = "https://github.com/antonkonyshev/steno"
    DESCRIPTION = (u"Steno is an application that helps people learning "
                   u"a foreign language to train listening skills.")

    # File Dialogs
    VIDEO_OPEN_DIALOG_TITLE = "Choose a video file"
    VIDEO_WILDCARD = ("Video files (*.avi, *.mp4, *.mpg, *.mpeg, "
                      "*.flv, *.3gp, *.mov, *.wmv, *.mkv) |*.avi;"
                      "*.mp4;*.mpg;*.mpeg;*.flv;*.3gp;*.mov;"
                      "*.wmv;*.mkv")
    SUBTITLES_OPEN_DIALOG_TITLE = "Choose a subtitles file"
    SUBTITLES_WILDCARD = "Subtitles files (*.srt) |*.srt"

    # Errors
    VIDEO_LOADING_ERROR_TITLE = "File loading error"
    VIDEO_LOADING_ERROR_MESSAGE = "Unable to open {0}."
    SUBTITLES_LOADING_ERROR_TITLE = "File loading error"
    SUBTITLES_LOADING_ERROR_MESSAGE = "Unable to open {0}:\n{1}"
    SUBTITLES_DECODE_ERROR_TITLE = "Unable to decode subtitles"
    SUBTITLES_DECODE_ERROR_MESSAGE = ("Subtitles file {0} doesn't "
                                      "contain a byte order mark and "
                                      "it's not in {1} (that is "
                                      "specified as default). "
                                      "Please, set valid default "
                                      "encoding in preferences or "
                                      "convert subtitles file to {1}.")
    MEDIACTRL_NOT_IMPLEMENTED_TITLE = "Error. Dependencies are not satisfied."
    MEDIACTRL_NOT_IMPLEMENTED_MESSAGE = (
        "Your instance of wxWidgets library does not provide support of "
        "MediaCtrl. Please, use the \"--enable-mediactrl\" flag when building "
        "the wxWidgets or install the full version of the library from the "
        "maintainer website.")

    PLAYBACK_TICK_INTERVAL = 1000

    # Local configuration
    LOCAL_CONFIG_FILE = u'.steno.conf'
    GLOBAL_CONFIG_FILE = u'.steno.rc'
    FILTER_STORAGE_FILE = u'.steno.filters'
    SETTINGS = {
        # u'parameter_name': (type, parameter_group),
        u'subtitles_shift': (int, u'playback'),
        u'volume': (int, u'playback'),
        u'player_width': (int, u'frame'),
        u'player_height': (int, u'frame'),
        u'player_position_x': (int, u'frame'),
        u'player_position_y': (int, u'frame'),
        u'working_directory': (unicode, u'frame'),
        u'translation': (bool, u'playback'),
        u'translation_font': (unicode, u'font'),
        u'translation_fg': (int, u'color'),
        u'translation_bg': (int, u'color'),
        u'learning_language': (unicode, u'frame'),
        u'user_language': (unicode, u'frame'),
        u'encoding': (unicode, u'frame'),
        u'answer_font': (unicode, u'font'),
        u'answer_fg': (int, u'color'),
        u'answer_correct': (int, u'color'),
        u'answer_incorrect': (int, u'color'),
        u'answer_bg': (int, u'color'),
    }

    # Colors
    DEFAULT_CORRECT_HIGHLIGHTING = (0, 180, 0)
    DEFAULT_INCORRECT_HIGHLIGHTING = (180, 0, 0)

    # Default preferences
    DEFAULT_TRANSLATION_ENABLE = True

    # Languages
    DEFAULT_LEARNING_LANGUAGE = u'en'
    DEFAULT_USER_LANGUAGE = u'ru'
    LANGUAGES = (
        (u'Afrikaans', u'af'), (u'Albanian', u'sq'), (u'Arabic', u'ar'),
        (u'Azerbaijani', u'az'), (u'Basque', u'eu'), (u'Bengali', u'bn'),
        (u'Belarusian', u'be'), (u'Bulgarian', u'bg'), (u'Catalan', u'ca'),
        (u'Chinese Simplified', u'zh-CN'), (u'Chinese Traditional', u'zh-TW'),
        (u'Croatian', u'hr'), (u'Czech', u'cs'), (u'Danish', u'da'),
        (u'Dutch', u'nl'), (u'English', u'en'), (u'Esperanto', u'eo'),
        (u'Estonian', u'et'), (u'Filipino', u'tl'), (u'Finnish', u'fi'),
        (u'French', u'fr'), (u'Galician', u'gl'), (u'Georgian', u'ka'),
        (u'German', u'de'), (u'Greek', u'el'), (u'Gujarati', u'gu'),
        (u'Haitian Creole', u'ht'), (u'Hebrew', u'iw'), (u'Hindi', u'hi'),
        (u'Hungarian', u'hu'), (u'Icelandic', u'is'), (u'Indonesian', u'id'),
        (u'Irish', u'ga'), (u'Italian', u'it'), (u'Japanese', u'ja'),
        (u'Kannada', u'kn'), (u'Korean', u'ko'), (u'Latin', u'la'),
        (u'Latvian', u'lv'), (u'Lithuanian', u'lt'), (u'Macedonian', u'mk'),
        (u'Malay', u'ms'), (u'Maltese', u'mt'), (u'Norwegian', u'no'),
        (u'Persian', u'fa'), (u'Polish', u'pl'), (u'Portuguese', u'pt'),
        (u'Romanian', u'ro'), (u'Russian', u'ru'), (u'Serbian', u'sr'),
        (u'Slovak', u'sk'), (u'Slovenian', u'sl'), (u'Spanish', u'es'),
        (u'Swahili', u'sw'), (u'Swedish', u'sv'), (u'Tamil', u'ta'),
        (u'Telugu', u'te'), (u'Thai', u'th'), (u'Turkish', u'tr'),
        (u'Ukrainian', u'uk'), (u'Urdu', u'ur'), (u'Vietnamese', u'vi'),
        (u'Welsh', u'cy'), (u'Yiddish', u'yi'),
    )

    # Filters
    FILTERS_REGEX_HEADER = u'Regular expression'
    FILTERS_REPLACEMENT_HEADER = u'Replacement'
    DEFAULT_FILTERS = {
        r'\[.*?\]': u'', r'\n': u' ', r'\s{1,}': u' ', r'^[A-Z ]{2,}:': u'',
        r'<.*?>': u'',
    }

    # Min sizes
    PLAYER_MIN_SIZE = (800, 550)
    WORD_TRANSLATE_MIN_SIZE = (300, 100)
    SUBTITLE_TRANSLATE_MIN_SIZE = (300, 50)
    PREFERENCES_DIALOG_MIN_SIZE = (500, 400)
    USER_MANUAL_DIALOG_MIN_SIZE = (700, 500)
    ANSWER_FIELD_MIN_SIZE = (700, 50)

    # Other
    DEFAULT_ENCODING = u'utf-8'
    RESIZE_PARAMS_SAVE_DELAY = 5
    ASPECT_RATIO_LIST = ((4, 3), (3, 2), (5, 3), (16, 9), (14, 9), (16, 10),
                         (21, 9),)
    BASE_PATH = getattr(sys, u'_MEIPASS',
                        op.abspath(op.join(op.dirname(__file__), op.pardir)))
    USER_MANUAL_RELATIVE_PATH = op.join(u'steno', u'resources', u'html',
                                        u'user_manual.html')
    USER_MANUAL_FILEPATH = op.join(BASE_PATH, USER_MANUAL_RELATIVE_PATH)
    VIDEO_BACKEND_LOADING_TIMEOUT = 3000

    # Texts
    LESSON_STATISTICS_TITLE = u"Lesson statistics"
    LESSON_STATISTICS_REPORT = (u"Duration of the lesson: {learning_time}\n"
                                u"Hint used: {hint_used}\n"
                                u"Mistakes: {mistakes}\n"
                                u"Total number of characters: {total_chars}\n")
    ABOUT_ICON = u'icon_128x128'
    ABOUT_DEVELOPERS = (
        AUTHOR,
    )
    USER_MANUAL_IS_NOT_A_FILE = u''.join([
        u"<html><head><title>Error</title></head><body>Can't find a file ",
        u"with User Manual content. Please, check the existence of<br />",
        u"{0}.".format(USER_MANUAL_FILEPATH), u"</body></html>"])
    USER_MANUAL_IOERROR = u''.join([
        u"<html><head><title>Error</title></head><body>Can't open a file ",
        u"with User Manual content. Please, check the permissions on <br />",
        u"{0}.".format(USER_MANUAL_FILEPATH), u"<br />Error message: {0}",
        u"</body></html>"])
