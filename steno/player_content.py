# -*- coding: utf-8 -*-
"""
.. module:: player_content
   :platform: Unix, Windows
   :synopsis: Behavior of the player related to the content

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import sys

import wx

import pysrt
from pysrt.srtitem import SubRipItem

import events as ev
import ids
from defaults import Defaults


class PlayerContentMixin(object):
    """Interaction with video and subtitles.

    """

    def show_subtitle(self, subtitle=None):
        """Shows subtitle text in "preview" mode.

        :param subtitle: Subtitle to showing
        :type subtitle: :class:`pysrt.srtitem.SubRipItem`

        """
        if (
            isinstance(subtitle, SubRipItem)
            and subtitle.text != self.answer_edit.GetValue()
        ):
            self.answer_edit.ChangeValue(subtitle.text)
            if self.need_translation():
                wx.PostEvent(self, ev.TranslateRequest(src=subtitle.text))
        elif subtitle is None:
            self.answer_edit.ChangeValue(u'')
            self.subtitle_translate.Clear()

    def edit_answer(self, output):
        """Prints content of an answer after verification and ephasizes its
        words with appropriate colors.

        :param output: Result of verification. List of pairs where first value
                       is a symbol and second is an estimation of its
                       correctness
        :type output: list of tuples

        """
        answer = u''.join([symbol for symbol, _ in output])
        self.answer_edit.ChangeValue(answer)
        start = end = value = None
        for index in xrange(len(output) + 1):
            try:
                charvalue = output[index][1]
            except IndexError:
                charvalue = None
            if start is None:
                start = index
                value = charvalue
            if value == charvalue:
                end = index + 1
            else:
                self.answer_edit.SetStyle(start, end, wx.TextAttr(
                    self.correct_highlighting() if value
                    else self.incorrect_highlighting()))
                start = index
                value = charvalue
                end = index + 1
        self.answer_edit.SetInsertionPointEnd()
        self.progress_gauge.SetValue(len([sym for sym, correctness in output
                                          if correctness]))
        if self.need_translation():
            wx.PostEvent(self, ev.TranslateAnswer(answer=answer))

    def load_video(self, event):
        """Loads video file.

        :param event: Event that contains path to video file
        :type event: events.LoadVideo

        """
        wx.PostEvent(self, wx.PyCommandEvent(wx.EVT_BUTTON.typeId, ids.PAUSE))
        self._video_loading_handled = False
        if not self.video.Load(event.filepath):
            wx.MessageBox(
                Defaults.VIDEO_LOADING_ERROR_MESSAGE.format(event.filepath),
                Defaults.VIDEO_LOADING_ERROR_TITLE,
                style=wx.ICON_ERROR | wx.OK,
            )
        else:
            # Different platforms and versions of wx framework show different
            # behavior here, because the framework uses platform dependent
            # backends in order to play media. For example, under Windows 7
            # with DirectShow backend the EVT_MEDIA_LOADED event isn't
            # generated, but under XP, where WMP10 backend is used, or Linux,
            # where GStreamer backend is used, EVT_MEDIA_LOADED
            # generates well. Handling of the media loading by catching the
            # EVT_MEDIA_LOADED event is the preferred way, but we should handle
            # it in any case, even if the event will never be generated.
            # Therefore we use timeout, if EVT_MEDIA_LOADED was generated
            # the timeout callback will do nothing, else it will try to run
            # the handling without the backend response receiving.
            wx.CallLater(Defaults.VIDEO_BACKEND_LOADING_TIMEOUT,
                         self.on_video_backend_timeout)

    def on_video_backend_timeout(self):
        """Runs the video handling without backend's response.

        """
        if not getattr(self, u'_video_loading_handled', False):
            self.on_video_backend_response(None)

    def on_video_backend_response(self, event):
        """Notifies the player of the successful loading of a video.

        """
        self._video_loading_handled = True
        wx.PostEvent(self, ev.ContentLoadingState(video=True))

    def load_subtitles(self, event):
        """Loads subtitles file.

        :param event: Event that contains path to subtitles file
        :type event: events.LoadSubtitles

        """
        try:
            try:
                self.subtitles = pysrt.open(event.filepath)
            except UnicodeDecodeError:
                default_encoding = self.app.get_setting(
                    u'encoding', Defaults.DEFAULT_ENCODING)
                try:
                    self.subtitles = pysrt.open(
                        event.filepath, encoding=default_encoding)
                except UnicodeDecodeError:
                    msg = Defaults.SUBTITLES_DECODE_ERROR_MESSAGE
                    wx.MessageBox(msg.format(event.filepath, default_encoding),
                                  Defaults.SUBTITLES_DECODE_ERROR_TITLE,
                                  style=wx.ICON_ERROR | wx.OK)
                    return
            if isinstance(getattr(self, u'subtitles', None),
                          pysrt.srtfile.SubRipFile):
                wx.PostEvent(self, ev.SubtitlesShift(
                             shift=self.delay_spin.GetValue()))
                wx.PostEvent(self, ev.ContentLoadingState(subtitles=True))
        except IOError as err:
            wx.MessageBox(
                Defaults.SUBTITLES_LOADING_ERROR_MESSAGE.format(event.filepath,
                                                                err.message),
                Defaults.SUBTITLES_LOADING_ERROR_TITLE,
                style=wx.ICON_ERROR | wx.OK,
            )

    def find_subtitle(self, first=False):
        """Find an actual subtitle.

        Method searches for a subtitle which is appropriate to a current
        position in the video stream. If there isn't such subtitle, None will
        be returned.

        :param bool first: If True first subtitle will be returned
        :returns: An actual subtitle or None if there isn't subtitles
        :rtype: :class:`pysrt.srtitem.SubRipItem`

        """
        if isinstance(getattr(self, 'subtitles', None),
                      pysrt.srtfile.SubRipFile):
            position = int(self.video.Tell() / 1000)
            try:
                return self.subtitles.slice(
                    starts_before={'seconds': position},
                    ends_after={'seconds': position},
                )[0]
            except IndexError:
                pass
            if first:
                try:
                    return self.subtitles.slice(
                        starts_after={'seconds': position},
                    )[0]
                except IndexError:
                    pass
        return None

    def _total_subtitle_fragments(self):
        """Calculates the total number of subtitle.

        :returns: Number of subtitles
        :rtype: int

        """
        if isinstance(getattr(self, 'subtitles', None),
                      pysrt.srtfile.SubRipFile):
            return len(self.subtitles)
        return 0

    def get_statistics(self):
        """Calculates a part of generic statistical values.

        This values are used with values received from
        :meth:`verificator.Verificator.get_statistics` to show lesson
        statistics for user at the end of a lesson.

        :returns: Several statistical values
        :rtype: dict

        """
        return {
            u'total_fragments': self._total_subtitle_fragments(),
        }

    def _seconds_to_readable(self, src):
        """Converts an interval in seconds into a human readable interval
        value.

        :param src: Value of time interval in seconds
        :type src: int or float
        :returns: Human readable interval value
        :rtype: unicode

        """
        if isinstance(src, (int, float)):
            mins, secs = divmod(src, 60)
            hour, mins = divmod(mins, 60)
            result = u':'.join([unicode(int(val)).zfill(2)
                                for val in [mins, secs]])
            if hour:
                result = u':'.join([unicode(int(hour)).zfill(2), result])
            return result
        else:
            return u''

    def show_statistics_dialog(self):
        """Shows dialog with statistics of the lesson.

        """
        if getattr(self, 'verificator', None):
            stats = self.get_statistics()
            stats.update(self.verificator.get_statistics())
            for value in (u'learning_time', u'seek_position'):
                stats[value] = self._seconds_to_readable(stats.get(value,
                                                                   None))
            msg = Defaults.LESSON_STATISTICS_REPORT
            wx.MessageBox(msg.format(**stats),
                          Defaults.LESSON_STATISTICS_TITLE,
                          wx.OK | wx.ICON_INFORMATION)
