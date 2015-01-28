# -*- coding: utf-8 -*-
"""
.. module:: events
   :platform: Unix, Windows
   :synopsis: Custom events definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from wx.lib.newevent import NewEvent


newevent = NewEvent()
LoadVideo = newevent[0]
"""Command to load chosen video file.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    filepath (str): path to the video file.

"""
LOAD_VIDEO = newevent[1]

newevent = NewEvent()
LoadSubtitles = newevent[0]
"""Command to load chosen subtitles file.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    filepath (str): path to the subtitles file.

"""
LOAD_SUBTITLES = newevent[1]

newevent = NewEvent()
ContentLoadingState = newevent[0]
"""Notification about successful video or subtitles file opening and loading.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    video (bool): video loading state::

        True -- Chosen video successful loaded.
        False -- Video is not loaded.
        None -- Video loading state without changes.

    subtitles (bool): subtitles loading state::

        True -- Chosen subtitles successful loaded.
        False -- Subtitles is not loaded.
        None -- Subtitles loading state without changes.

"""
CONTENT_LOADING_STATE = newevent[1]

newevent = NewEvent()
FragmentComplete = newevent[0]
"""Notification about successful completion of current subtitles fragment.

Receivers:
    Player (wx.Frame): player window.

"""
FRAGMENT_COMPLETE = newevent[1]

newevent = NewEvent()
FragmentStarted = newevent[0]
"""Notification about beginning of a next subtitles fragment learning.

Receivers:
    Player (wx.Frame): player window.

"""
FRAGMENT_STARTED = newevent[1]

newevent = NewEvent()
SubtitlesShift = newevent[0]
"""Command to shift subtitles.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    shift (int): shift in milliseconds.

"""
SUBTITLES_SHIFT = newevent[1]

newevent = NewEvent()
TranslateRequest = newevent[0]
"""Command to translate a subtitles fragment or word.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    src (str or unicode): source text or word.
    details (bool): request detailed result or not (default is False)::

        True -- Details requested.
        False -- Only translation.

"""
TRANSLATE_REQUEST = newevent[1]

newevent = NewEvent()
TranslationResult = newevent[0]
"""Notification about successful translation.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    result (str or unicode): translated text.
    details (bool): is result detailed or not (default is False)::

        True -- Detailed result.
        False -- Only translation.

"""
TRANSLATION_RESULT = newevent[1]

newevent = NewEvent()
TranslateAnswer = newevent[0]
"""Command to translate an answer entered by user.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    answer (str or unicode): user's answer.

"""
TRANSLATE_ANSWER = newevent[1]

newevent = NewEvent()
ConfigUpdate = newevent[0]
"""Notification about settings changing.

Receivers:
    Player (wx.Frame): player window.

Kwargs:
    params (dict): changes (format: parameter_name-parameter_value).
    name (str or unicode): parameter name.
    value (str or unicode or bool or int or float): new parameter value.
    apply_updated (bool): apply changed settings now (default: False).
    apply_all (bool): apply all settings now (default: False).

"""
CONFIG_UPDATE = newevent[1]
