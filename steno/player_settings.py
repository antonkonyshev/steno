# -*- coding: utf-8 -*-
"""
.. module:: player_settings
   :platform: Unix, Windows
   :synopsis: Usage of settings of the player window

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import os.path as op

import wx

from defaults import Defaults
import ids
import events as ev


class PlayerSettingsMixin(object):
    """Settings of the application graphical interface.

    """

    def correct_highlighting(self):
        """Returns a highlighting color for a correct part of user's answer.

        :returns: Highlighting color for correct text
        :rtype: :class:`wx.Colour`

        """
        if getattr(self, u'_correct_highlighting', None) is None:
            color = wx.Colour(*Defaults.DEFAULT_CORRECT_HIGHLIGHTING)
            color.SetRGB(self.app.get_setting(u'answer_correct',
                                              color.GetRGB()))
            self._correct_highlighting = color
        return self._correct_highlighting

    def incorrect_highlighting(self):
        """Returns a highlighting color for an incorrect part of user's answer.

        :returns: Highlighting color for incorrect text
        :rtype: :class:`wx.Colour`

        """
        if getattr(self, u'_incorrect_highlighting', None) is None:
            color = wx.Colour(*Defaults.DEFAULT_INCORRECT_HIGHLIGHTING)
            color.SetRGB(self.app.get_setting(u'answer_incorrect',
                                              color.GetRGB()))
            self._incorrect_highlighting = color
        return self._incorrect_highlighting

    def learning_language(self):
        """Returns a code of the language which is studied by user.

        :returns: Language code from :const:`defaults.Defaults.LANGUAGES`
        :rtype: unicode

        """
        if getattr(self, '_learning_language', None) is None:
            self._learning_language = self.app.get_setting(
                u'learning_language', u'en')
        return self._learning_language

    def user_language(self):
        """Returns a code of the language which is native for user.

        :returns: Language code from :const:`defaults.Defaults.LANGUAGES`
        :rtype: unicode

        """
        if getattr(self, '_user_language', None) is None:
            self._user_language = self.app.get_setting(u'user_language', u'ru')
        return self._user_language

    def need_translation(self):
        """Indicates the need for a translation.

        :returns: Need for a translation.
        :rtype: bool

        """
        if getattr(self, '_need_translation', None) is None:
            self._need_translation = self.app.get_setting(u'translation', True)
        return self._need_translation

    def is_learning(self):
        """Clarifies current working mode of the application.

        :returns: True if application works in "learning" mode else False
        :rtype: bool

        """
        if getattr(self, '_is_learning', None) is None:
            self._is_learning = bool(
                self.mode_choice.GetSelection() == ids.LEARNING)
        return self._is_learning

    def get_filters(self, copy=False):
        """Returns actual regex filters.

        :param bool copy: To copy dictionary with filters or not
        :returns: Regex filters
        :rtype: dict

        """
        return self._filters.copy() if copy else self._filters

    def enable_menu_actions(self, **kwargs):
        """Changes the availability of menu items in the playback menu.

        Default values of every keyword argument is None, i.e. availability of
        menu item will remain the same if you will not pass argument for it.

        :param bool play: Availability of "Play" menu item.
        :param bool pause: Availability of "Pause" menu item.
        :param bool stop: Availability of "stop" menu item.
        :param bool hint: Availability of "hint" menu item.
        :param bool repeat: Availability of "repeat" menu item.

        """
        for action, availability in kwargs.iteritems():
            menuitem_id = getattr(ids, action.upper(), None)
            if menuitem_id is None:
                menuitem_id = getattr(wx, ''.join(['ID_', action.upper()]),
                                      None)
            if menuitem_id:
                self.playback_menu.Enable(menuitem_id, availability)

    def apply_color_settings(self):
        """Applies color settings for widgets of player frame: text colors,
        background colors.

        """
        self._correct_highlighting = None
        self._incorrect_highlighting = None
        for group, widgets in {
            u'answer': [u'answer_edit'],
            u'translation': [u'word_translate', u'subtitle_translate'],
        }.iteritems():
            for widget in widgets:
                for place in (u'Fore', u'Back',):
                    color = getattr(getattr(self, widget),
                                    u'Get{0}groundColour'.format(place))()
                    rgb = self.app.get_setting(u'_'.join([group, u''.join([
                        place[0].lower(), u'g'])]), color.GetRGB())
                    if color.GetRGB() != rgb:
                        color.SetRGB(rgb)
                        getattr(getattr(self, widget),
                                u'Set{0}groundColour'.format(place))(color)

    def apply_font_settings(self):
        """Applies font settings for widgets of player frame.

        """
        answer_font = self.answer_edit.GetFont()
        answer_font.SetNativeFontInfoFromString(
            self.app.get_setting(u'answer_font',
                                 answer_font.GetNativeFontInfoDesc()))
        if (
            self.answer_edit.GetFont().GetNativeFontInfoDesc() !=
            answer_font.GetNativeFontInfoDesc()
        ):
            self.answer_edit.SetFont(answer_font)
        translation_font = self.word_translate.GetFont()
        translation_font.SetNativeFontInfoFromString(
            self.app.get_setting(u'translation_font',
                                 translation_font.GetNativeFontInfoDesc()))
        if (
            self.word_translate.GetFont().GetNativeFontInfoDesc() !=
            translation_font.GetNativeFontInfoDesc() or
            self.subtitle_translate.GetFont().GetNativeFontInfoDesc() !=
            translation_font.GetNativeFontInfoDesc()
        ):
            self.word_translate.SetFont(translation_font)
            self.subtitle_translate.SetFont(translation_font)

    def apply_frame_settings(self):
        """Applies common and window settings for player frame: languages,
        window size, window position.

        """
        self._learning_language = None
        self._user_language = None
        size = self.GetSize()
        newsize = wx.Size(
            self.app.get_setting(u'player_width', size.GetWidth()),
            self.app.get_setting(u'player_height', size.GetHeight()))
        if (
            size.GetWidth() != newsize.GetWidth() or
            size.GetHeight() != newsize.GetHeight()
        ):
            self.SetSize(newsize)
        pos = self.GetPosition()
        newpos = wx.Point(
            self.app.get_setting(u'player_position_x', pos.x),
            self.app.get_setting(u'player_position_y', pos.y))
        if newpos.x != pos.x or newpos.y != pos.y:
            self.SetPosition(newpos)

    def apply_playback_settings(self):
        """Applies playback settings for player frame: real time translation,
        volume level, subtitles shift.

        """
        self._need_translation = None
        volume = self.volume_slider.GetValue()
        newvol = self.app.get_setting(u'volume', volume)
        if newvol != volume:
            self.volume_slider.SetValue(newvol)
        shift = self.delay_spin.GetValue()
        newshift = self.app.get_setting(u'subtitles_shift', shift)
        if shift != newshift:
            self.delay_spin.SetValue(newshift)

    def _accept_args(self, pargs):
        """Handles command line arguments on application start.

        :param pargs: Arguments
        :type pargs: :class:`argparse.Namespace`

        """
        media_provided = subtitles_provided = False

        def resolve_path(path):
            if u'~' in path:
                path = path.replace(u'~', op.expanduser(u'~'))
            return op.abspath(path)

        if pargs.mediafile:
            mediafile = resolve_path(pargs.mediafile)
            if op.isfile(mediafile):
                media_provided = True
                wx.PostEvent(self, ev.LoadVideo(filepath=mediafile))
        if pargs.subtitles:
            subtitlesfile = resolve_path(pargs.subtitles)
            if op.isfile(subtitlesfile):
                subtitles_provided = True
                wx.PostEvent(self, ev.LoadSubtitles(filepath=subtitlesfile))
        if pargs.learning and media_provided and subtitles_provided:
            self.mode_choice.SetSelection(ids.LEARNING)
            wx.PostEvent(self,
                         wx.PyCommandEvent(wx.EVT_CHOICE.typeId, ids.MODE))

    def _save_frame_size_and_position(self):
        """Saves player window size and position coordinates.

        """
        pos = self.GetPosition()
        size = self.GetSize()
        wx.PostEvent(self, ev.ConfigUpdate(params={
            u'player_width': size.GetWidth(),
            u'player_height': size.GetHeight(),
            u'player_position_x': pos.x, u'player_position_y': pos.y,
        }))

    def _get_video_slot_size(self):
        """Calculates sizes available for video widget on the frame.

        :returns: Pair of values where first is available width and seconds is
                  available height
        :rtype: tuple

        """
        slot_width = (self.GetSize()[0] - self.word_translate.GetMinSize()[0]
                      - 15)
        slot_height = (self.word_translate.GetSize()[1] +
                       self.subtitle_translate.GetSize()[1] + 5)
        return slot_width, slot_height
