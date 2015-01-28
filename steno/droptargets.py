# -*- coding: utf-8 -*-
"""
.. module:: droptargets
   :platform: Unix, Windows
   :synopsis: Drag'n'Drop behavior definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

import os.path as op

import wx

import events as ev


class FileDropTarget(wx.FileDropTarget):
    """Handles drag'n'drop files events.

    """

    def __init__(self, frame):
        """Implements loading of a content initiated by dragging.

        :param frame: Player window instance
        :type frame: :class:`player.Player`

        """
        super(FileDropTarget, self).__init__()
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        """Handles a file dropping to the frame.

        :param int x: X-coordinate of the dropping
        :param int y: Y-coordinate of the dropping
        :param list filenames: Paths to files

        """
        for filename in filenames:
            if op.isfile(filename):
                _, extension = op.splitext(filename)
                if extension.lower() == '.srt':
                    self._on_subtitles_drop(filename)
                else:
                    self._on_video_drop(filename)

    def _on_video_drop(self, filename):
        """Initializes loading of a video file.

        :param filename: Path to the file
        :type filename: str or unicode

        """
        wx.PostEvent(self.frame, ev.LoadVideo(filepath=filename))

    def _on_subtitles_drop(self, filename):
        """Initializes loading of a subtitles file.

        :param filename: Path to the file
        :type filename: str or unicode

        """
        wx.PostEvent(self.frame, ev.LoadSubtitles(filepath=filename))
