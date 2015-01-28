# -*- coding: utf-8 -*-
"""
.. module:: player
   :platform: Unix, Windows
   :synopsis: Main frame of the application "Steno"

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""
# License: wxWidgets (wxWindows Library Licence) 3.1

import os.path as op
import threading

import wx
try:
    from wx.media import EVT_MEDIA_LOADED
except:
    pass

import pysrt

from player_gui import PlayerGUI
from player_settings import PlayerSettingsMixin
from player_content import PlayerContentMixin
from verificator import Verificator
from droptargets import FileDropTarget
from translator import Translator
from dialogs import PreferencesDialog
from dialogs import UserManualDialog
from defaults import Defaults
import events as ev
import ids


class Player(PlayerGUI, PlayerSettingsMixin, PlayerContentMixin):
    """Main window of the application.

    """

    def __init__(self, app, pargs=None):
        """:class:`Player` implements graphical user interface of the
        application.

        :param app: Application instance
        :type app: :class:`wx.App`
        :param pargs: Command line arguments
        :type pargs: :class:`argparse.Namespace`

        """

        self.app = app
        super(Player, self).__init__(None, -1, "")
        self.SetMinSize(wx.Size(*Defaults.PLAYER_MIN_SIZE))
        self.word_translate.SetMinSize(
            wx.Size(*Defaults.WORD_TRANSLATE_MIN_SIZE))
        self.subtitle_translate.SetMinSize(
            wx.Size(*Defaults.SUBTITLE_TRANSLATE_MIN_SIZE))

        self._video_state = self._subtitles_state = False
        self._aspect_ratio = None
        self._filters = self.app.load_filters()
        self.enable_menu_actions(play=False, pause=False, hint=False,
                                 repeat=False, stop=False)

        self.playback_timer = wx.Timer(self, id=ids.PLAYBACK_TICK)

        filedroptarget = FileDropTarget(self)
        self.SetDropTarget(filedroptarget)

        self.Bind(ev.LOAD_VIDEO, self.load_video)
        self.Bind(ev.LOAD_SUBTITLES, self.load_subtitles)
        self.Bind(ev.CONTENT_LOADING_STATE,
                  self.on_content_loading_state_change)
        self.Bind(wx.EVT_TIMER, self.on_playback_timer, id=ids.PLAYBACK_TICK)
        self.Bind(ev.FRAGMENT_COMPLETE, self.on_fragment_completion)
        self.Bind(ev.FRAGMENT_STARTED, self.on_fragment_starting)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_MOVE, self.on_move)
        self.Bind(ev.SUBTITLES_SHIFT, self.on_subtitles_shift)
        self.Bind(ev.TRANSLATE_REQUEST, self.on_translate_request)
        self.Bind(ev.TRANSLATION_RESULT, self.on_translation_result)
        self.Bind(ev.CONFIG_UPDATE, self.on_config_update)
        self.Bind(ev.TRANSLATE_ANSWER, self.on_translate_answer)
        if globals().get(u'EVT_MEDIA_LOADED', False):
            self.Bind(EVT_MEDIA_LOADED, self.on_video_backend_response)

        video_widget_size = self._get_video_slot_size()
        self.answer_edit.SetMinSize(wx.Size(*Defaults.ANSWER_FIELD_MIN_SIZE))
        self.video.SetMinSize(video_widget_size)
        self.video.SetSize(video_widget_size)

        if pargs:
            self._accept_args(pargs)

        wx.PostEvent(self, ev.ConfigUpdate(apply_all=True))
        self.Layout()

    def on_config_update(self, event):
        """Stores user's configuration data and applies them to the graphical
        interface.

        :param event: Event which contains updated configuration values
        :type event: :class:`events.ConfigUpdate`

        """
        params = getattr(event, 'params', {})
        apply_updated = getattr(event, 'apply_updated', False)
        apply_all = getattr(event, 'apply_all', False)
        for name, value in params.iteritems():
            if (
                name is not None and value is not None
                and name in Defaults.SETTINGS.keys()
            ):
                try:
                    if not isinstance(value, Defaults.SETTINGS.get(name)):
                        value = Defaults.SETTINGS.get(name)(value)
                except (TypeError, ValueError):
                    value = None
                if value is not None:
                    self.app.set_setting(name, value)
        for group in set(par[1] for name, par in Defaults.SETTINGS.iteritems()
                         if apply_updated and name in params.keys()
                         or apply_all):
            getattr(self, u'apply_{0}_settings'.format(group))()

    def on_preferences(self, event):
        """Creates and shows :class:`dialogs.PreferencesDialog` to edit the
        configuration parameters.

        :param event: Event entailed execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        dialog = PreferencesDialog(player=self)
        if dialog.ShowModal() == wx.ID_OK:
            wx.PostEvent(
                self, ev.ConfigUpdate(params=dialog.get_preferences(),
                                      apply_updated=True))
            self._filters = dialog.get_filters()
            self.app.dump_filters(self._filters)
        dialog.Destroy()

    def on_translate_request(self, event):
        """Creates and starts a thread in which the translation request will be
        performed.

        :param event: Event which contains details of the translation request
        :type event: :class:`events.TranslateRequest`

        """
        src = getattr(event, 'src', None)
        if src:
            threading.Thread(
                target=self._translate_in_thread,
                args=(self.learning_language(), self.user_language(), src,
                      getattr(event, u'details', False))).start()

    def _translate_in_thread(self, src_lang, target_lang, text, details=False):
        """Performs the translation request in a thread.

        Language codes for `src_lang` and `target_lang` parameters can be
        found in :const:`defaults.Defaults.LANGUAGES`.

        :param src_lang: Source language of the text
        :type src_lang: unicode or str
        :param target_lang: Desired language for the text
        :type target_lang: unicode or str
        :param text: Original text for the translation
        :type text: unicode or str
        :param bool details: Verbosity of the translation result

        """
        with self.translator.lock:
            try:
                result = getattr(
                    self.translator, u'trans_{0}'.format(
                        u'details' if details else u'sentence')
                )(src_lang, target_lang, text)
            except:
                result = False
        if result:
            wx.CallAfter(wx.PostEvent, self,
                         ev.TranslationResult(result=result, details=details))

    def on_translation_result(self, event):
        """Handles the translation result.

        :param event: Event which contains a result of the translation
        :type event: :class:`events.TranslationResult`

        """
        result = getattr(event, 'result', None)
        if result:
            if getattr(event, 'details', False):
                self.word_translate.SetValue(result)
            else:
                self.subtitle_translate.SetValue(result)

    def on_playback_timer(self, event):
        """Supports actual values of widgets during playback.

        :param event: Event entailed execution of the callback
        :type event: :class:`wx.TimerEvent`

        """
        if self.video_slider.GetMax() != self.video.Length():
            self.video_slider.SetMax(self.video.Length())
            self.video_slider.SetPageSize(int(self.video.Length()/10))
            self.Layout()
        else:
            self.video_slider.SetValue(self.video.Tell())

        subtitle = self.find_subtitle()
        if subtitle and not self.is_learning():
            self.show_subtitle(subtitle)
        if self.is_learning():
            if self.verificator.set_subtitle(subtitle, replace=False):
                wx.PostEvent(self, ev.FragmentStarted())
                wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_TEXT.typeId,
                                                     ids.ANSWER))
            if self.verificator.is_passed(self.video.Tell() / 1000):
                if self.verificator.is_empty():
                    wx.PostEvent(self, ev.FragmentComplete())
                else:
                    wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId,
                                                         ids.PAUSE))
                    wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_TEXT.typeId,
                                                         ids.ANSWER))

    def on_repeat(self, event):
        """Rewinds a position in a video stream to the beginning of the current
        subtitle fragment.

        :param event: Event which entailed execution of the callback
        :type event: :class:`wx.ScrollEvent`

        """
        if self.verificator.has_subtitle():
            last = self.verificator.get_subtitle()
            self.video.Seek(int(
                (last.start.hours * 3600 + last.start.minutes * 60
                 + last.start.seconds) * 1000))
            wx.PostEvent(self, wx.PyCommandEvent(
                wx.EVT_BUTTON.typeId, ids.PLAY))

    def on_aspect_ratio(self, event):
        """Sets aspect ratio for video widget.

        :param event: Event which entailed execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        widget_id = event.GetId()
        aspect = None
        for width, height in Defaults.ASPECT_RATIO_LIST:
            if widget_id == getattr(
                ids, 'ASPECT_{0}x{1}'.format(width, height), None
            ):
                aspect = (width, height)
        self._aspect_ratio = aspect
        self.video.SetAspectRatio(self._aspect_ratio,
                                  slot_size=self._get_video_slot_size())
        self.Layout()

    def on_resize(self, event):
        """Handles frame resize event in order to save new sizes in
        configuration and to correctly resize the video widget.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.SizeEvent`

        """
        event.Skip()
        self.video.SetAspectRatio(self._aspect_ratio,
                                  slot_size=self._get_video_slot_size())
        self.Layout()
        self._after_resize_or_move()

    def _after_resize_or_move(self):
        """Saves new position and sizes of the window after a short delay.

        Delay is necessary to write new values in configuration when user
        will stop their changing. Otherwise it would be required to save sizes
        and position coordinates many times while user resizes the frame.

        """
        if hasattr(self, '_resize_params_save_held_call'):
            self._resize_params_save_held_call.Restart(
                Defaults.RESIZE_PARAMS_SAVE_DELAY * 1000)
        else:
            self._resize_params_save_held_call = wx.CallLater(
                Defaults.RESIZE_PARAMS_SAVE_DELAY * 1000,
                self._save_frame_size_and_position)

    def on_move(self, event):
        """Handles frame move event in order to save new position coordinates
        in configuration.

        :param event: Event that entailed an execution of the callback
        :type event: :defaults:`wx.MoveEvent`

        """
        event.Skip()
        self._after_resize_or_move()

    def on_playback_control(self, event):
        """Controls the video playback.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with types :const:`wx.EVT_BUTTON`
                     or :const:`wx.EVT_MENU`

        """
        widget_id = event.GetId()
        if widget_id == wx.ID_STOP or widget_id == ids.PAUSE:
            if widget_id == ids.PAUSE:
                self.video.Pause()
            elif widget_id == wx.ID_STOP:
                self.video.Stop()
                self.video_slider.SetValue(0)
                if self.is_learning():
                    self.mode_choice.SetSelection(ids.PREVIEW)
                    wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_CHOICE.typeId,
                                                         ids.MODE))
                    self.show_statistics_dialog()
            self.pause_button.Enable(False)
            self.play_button.Enable(True)
            if not self.is_learning():
                self.enable_menu_actions(pause=False, play=True)
            if self.playback_timer.IsRunning():
                self.playback_timer.Stop()
        elif widget_id == ids.PLAY:
            self.video.Play()
            self.pause_button.Enable(True)
            self.play_button.Enable(False)
            if not self.is_learning():
                self.enable_menu_actions(pause=True, play=False)
            if not self.playback_timer.IsRunning():
                if self.video.Length():
                    self.video_slider.SetRange(0, self.video.Length())
                    self.video_slider.SetPageSize(int(self.video.Length()/10))
                    self.Layout()
                self.playback_timer.Start(Defaults.PLAYBACK_TICK_INTERVAL)

    def on_seek(self, event):
        """Rewinds the video stream position to.

        .. note:: Rewind procedure implemented in
                  :meth:`Player.on_playback_timer`.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.ScrollEvent`

        """
        self.video.Seek(event.GetPosition())
        self.video_slider.SetValue(event.GetPosition())
        event.Skip()

    def on_hint(self, event):
        """Prints the hint requested by user in "learning" mode.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with types :const:`wx.EVT_BUTTON`
                     or :const:`wx.EVT_MENU`

        """
        if self.is_learning() and self.verificator.has_subtitle():
            self.answer_edit.SetValue(self.verificator.hint(
                self.answer_edit.GetValue()))
            self.answer_edit.SetInsertionPointEnd()

    def on_answer(self, event):
        """Checks the correctness of user's answer and its completeness.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_TEXT`

        """
        if self.is_learning() and len(self.answer_edit.GetValue()):
            if self.verificator.has_subtitle():
                self.edit_answer(self.verificator.verify_answer(
                    self.answer_edit.GetValue()))
                if self.verificator.is_complete(self.answer_edit.GetValue()):
                    wx.PostEvent(self, ev.FragmentComplete())

    def on_translate_answer(self, event):
        """Generates a request for translation of an answer.

        :param event: Event contains the source text for translation
        :type event: :class:`events.TranslateAnswer`

        """
        answer = getattr(event, 'answer', None)
        if answer:
            try:
                if answer[-1] == u' ':
                    wx.PostEvent(self, ev.TranslateRequest(src=answer))
                    last_word = self.verificator.get_last_word()
                    if last_word:
                        wx.PostEvent(self, ev.TranslateRequest(src=last_word,
                                                               details=True))
            except IndexError:
                pass

    def on_fragment_completion(self, event):
        """Clears the current subtitle and user's answer when current fragment
        was successfully complete.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`events.FragmentComplete`

        """
        self.progress_gauge.SetValue(self.verificator.fragment_length())
        self.verificator.clear_subtitle(complete=True)
        self.answer_edit.ChangeValue(u'')
        wx.PostEvent(self, wx.PyCommandEvent(
            wx.EVT_BUTTON.typeId, ids.PLAY))

    def on_fragment_starting(self, event):
        """Sets actual values for progress bar when new subtitle fragment
        starts.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`events.FragmentStarted`

        """
        if self.verificator.has_subtitle():
            self.progress_gauge.SetRange(self.verificator.fragment_length())
        self.progress_gauge.SetValue(0)

    def on_close_all(self, event):
        """Closes video and subtitles files.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, wx.ID_STOP))
        self.mode_choice.SetSelection(ids.PREVIEW)
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_CHOICE.typeId, ids.MODE))
        self.video.Close()
        self.video_slider.SetValue(0)
        self.progress_gauge.SetValue(0)
        del self.subtitles
        wx.PostEvent(self, ev.ContentLoadingState(video=False,
                                                  subtitles=False))

    def on_content_loading_state_change(self, event):
        """Handles loading/unloading of a content.

        :param event: Event that contains information about current
                      availability of a content
        :type event: :class:`events.ContentLoadingState`

        """
        video = getattr(event, 'video', None)
        subtitles = getattr(event, 'subtitles', None)
        if video is not None and video != self._video_state:
            self._video_state = video
            if self.video.Length():
                self.video_slider.SetRange(0, self.video.Length())
                self.video_slider.SetPageSize(int(self.video.Length()/10))
                self.Layout()
            for widget in ('play_button', 'stop_button', 'video_slider'):
                getattr(self, widget).Enable(video)
            self.enable_menu_actions(play=video, stop=video)
            self.video.SetVolume(self.volume_slider.GetValue() / 100.0)
            if video:
                wx.CallLater(
                    300, wx.PostEvent, self,
                    wx.PyCommandEvent(wx.EVT_BUTTON.typeId, ids.PLAY))
        if subtitles is not None:
            self._subtitles_state = subtitles
        both = self._video_state and self._subtitles_state
        for widget in ('mode_choice', 'delay_spin', 'answer_edit'):
            getattr(self, widget).Enable(both)
        if both:
            self.translator = Translator()
        else:
            try:
                del self.translator
            except AttributeError:
                pass

    def on_subtitles_shift(self, event):
        """Sets a shift value for subtitles.

        :param event: Event that contains new shift value
        :type event: :class:`events.SubtitlesShift`

        """
        shift = getattr(event, 'shift', None)
        if shift:
            if getattr(self, '_applied_shift', None):
                self.subtitles.shift(milliseconds=(-1*self._applied_shift))
            self._applied_shift = shift
            self.subtitles.shift(milliseconds=shift)

    def on_content_open(self, event):
        """Provides an opportunity for user to choose content files for
        loading.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        widget_id = event.GetId()
        workdir = self.app.get_setting(u'working_directory', None)
        if not workdir:
            workdir = wx.StandardPaths.Get().GetDocumentsDir()
        dialog = wx.FileDialog(
            self, message=Defaults.VIDEO_OPEN_DIALOG_TITLE
            if widget_id == wx.ID_OPEN
            else Defaults.SUBTITLES_OPEN_DIALOG_TITLE,
            defaultDir=workdir, wildcard=Defaults.VIDEO_WILDCARD
            if widget_id == wx.ID_OPEN else Defaults.SUBTITLES_WILDCARD,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            wx.PostEvent(self,
                         ev.LoadVideo(filepath=path)
                         if widget_id == wx.ID_OPEN else
                         ev.LoadSubtitles(filepath=path))
            newwd = op.split(path)[0] if op.isfile(path) else path
            if newwd != workdir:
                wx.PostEvent(
                    self, ev.ConfigUpdate(params={u'working_directory': newwd})
                )
        dialog.Destroy()

    def on_delay(self, event):
        """Handles editing of subtitles shift value.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.SpinEvent`

        """
        if isinstance(getattr(self, 'subtitles', None),
                      pysrt.srtfile.SubRipFile):
            shift = self.delay_spin.GetValue()
            wx.PostEvent(self, ev.SubtitlesShift(shift=shift))
            wx.PostEvent(self,
                         ev.ConfigUpdate(params={u'subtitles_shift': shift}))

    def on_volume(self, event):
        """Applies new volume level.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.ScrollEvent`

        """
        volume = event.GetPosition()
        self.video.SetVolume(volume / 100.0)
        ev.ConfigUpdate(params={u'volume': volume})

    def on_mode(self, event):
        """Changes the application working mode.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_CHOICE`

        """
        self._is_learning = None
        if self.is_learning():
            wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId,
                                                 ids.PLAY))
            self.play_button.Hide()
            self.pause_button.Hide()
            self.repeat_button.Show()
            self.hint_button.Show()
            self.Layout()
            self.video_slider.Enable(False)
            self.enable_menu_actions(play=False, pause=False, repeat=True,
                                     hint=True)
            self.verificator = Verificator(self)
            if self.verificator.set_subtitle(self.find_subtitle(first=True)):
                wx.PostEvent(self, ev.FragmentStarted())
        else:
            self.repeat_button.Hide()
            self.hint_button.Hide()
            self.play_button.Show()
            self.pause_button.Show()
            self.Layout()
            self.video_slider.Enable(True)
            self.enable_menu_actions(play=True, pause=True, repeat=False,
                                     hint=False)
            try:
                del self.verificator
            except AttributeError:
                pass
        self.answer_edit.ChangeValue(u'')
        self.word_translate.Clear()
        self.subtitle_translate.Clear()

    def on_exit(self, event):
        """Prepares for an application termination.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        self.video.Close()
        for component in (u'translator', u'verificator', u'subtitles'):
            if getattr(self, component, None) is not None:
                delattr(self, component)
        self.Close()

    def on_about(self, event):
        """Shows "About" dialog.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon(self.app.get_img_path(Defaults.ABOUT_ICON),
                             wx.BITMAP_TYPE_PNG))
        for attr in (u'Name', u'Version', u'Description', u'License',
                     u'WebSite', u'Copyright',):
            getattr(info, u'Set{0}'.format(attr))(
                getattr(Defaults, attr.upper(), u''))
        for dev in Defaults.ABOUT_DEVELOPERS:
            info.AddDeveloper(dev)
        wx.AboutBox(info)

    def on_user_manual(self, event):
        """Creates and shows "User Manual" dialog.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_MENU`

        """
        dialog = UserManualDialog(self)
        dialog.ShowModal()
        dialog.Destroy()

    def Layout(self):
        """Invokes the layout algorithm for the window and for its panels.

        """
        super(Player, self).Layout()
        self.panel.Layout()
        self.Refresh()
