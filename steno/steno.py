# -*- coding: utf-8 -*-
"""
.. module:: steno
   :platform: Unix, Windows
   :synopsis: Arguments parsing and application definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""
# License: wxWidgets (wxWindows Library Licence) 3.1

import sys
import os.path as op
from argparse import ArgumentParser

import wx

from player import Player
from defaults import Defaults


class Steno(wx.App):
    """Steno application.

    """

    def __init__(self, pargs=None):
        """Steno application.

        :param pargs: Parsed command line arguments
        :type pargs: :class:`argparse.Namespace`

        """
        self.pargs = pargs
        super(Steno, self).__init__(0)

    def OnInit(self):
        """Creates a main frame of the application and sets it as top level
        window.

        """
        try:
            wx.InitAllImageHandlers()
        except:
            pass
        try:
            self.player_frame = Player(self, pargs=self.pargs)
        except NotImplementedError:
            wx.MessageBox(
                Defaults.MEDIACTRL_NOT_IMPLEMENTED_MESSAGE,
                Defaults.MEDIACTRL_NOT_IMPLEMENTED_TITLE,
                style=wx.ICON_ERROR | wx.OK,
            )
            return 0
        else:
            self.SetTopWindow(self.player_frame)
            self.player_frame.Show()
        return 1

    def _get_config(self):
        """Creates a configuration instance. If the configuration has already
        been created earlier, then it will be used.

        :returns: Configuration
        :rtype: :class:`wx.Config`

        """
        if getattr(self, '_config', None) is None:
            self._config = wx.Config(
                Defaults.NAME, Defaults.NAME, Defaults.LOCAL_CONFIG_FILE,
                Defaults.GLOBAL_CONFIG_FILE)
        return self._config

    def _get_filter_storage(self):
        """Creates a storage instance for regex filters. If it has been created
        earlier, it'll be used again.

        :returns: Storage for regex filters
        :rtype: :class:`wx.Config`

        """
        if getattr(self, '_filter_storage', None) is None:
            self._filter_storage = wx.Config(
                Defaults.NAME, Defaults.NAME,
                Defaults.FILTER_STORAGE_FILE,
                Defaults.FILTER_STORAGE_FILE)
        return self._filter_storage

    def get_setting(self, name, default=None):
        """Reads one configuration parameter. If the specified parameter isn't
        found, default value will be returned.

        :param name: Parameter name
        :type name: str or unicode
        :param default: Default value
        :type default: any

        """
        if name in Defaults.SETTINGS.keys():
            config = self._get_config()
            value = config.Read(name, u'')
            if value:
                value_type = Defaults.SETTINGS.get(name)[0]
                if value_type is bool:
                    value = True if value == u'true' else False
                else:
                    value = value_type(value)
                return value
            else:
                return default
        else:
            return default

    def set_setting(self, name, value):
        """Records one configuration parameter.

        :param name: Parameter name
        :type name: str or unicode
        :param value: Parameter value
        :type value: str, unicode, int, float, or bool

        """
        config = self._get_config()
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, (int, float)):
            value = unicode(value)
        config.Write(name, value)

    def dump_filters(self, filters):
        """Writes filters to the storage.

        :param filters: RegEx filters
        :param filters: dict

        """
        filter_storage = self._get_filter_storage()
        filter_storage.DeleteAll()
        [filter_storage.Write(ptrn, repl)
         for ptrn, repl in filters.iteritems()]

    def load_filters(self):
        """Loads all filters from the storage.

        :returns: Loaded filters or default filters
        :rtype: dict

        """
        filter_storage = self._get_filter_storage()
        more, key, index = filter_storage.GetFirstEntry()
        filters = {}
        while more:
            if more and key:
                filters[key] = filter_storage.Read(key, u'')
            more, key, index = filter_storage.GetNextEntry(index)
        return filters if len(filters) else Defaults.DEFAULT_FILTERS

    def get_img_path(self, name):
        """Returns path to image resource.

        :param name: Name of an image resource
        :type name: str or unicode
        :returns: Absolute path to the image resource
        :rtype: unicode

        """
        return op.join(Defaults.BASE_PATH, u'steno', u'resources', u'img',
                       u'{0}.png'.format(name))


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--mediafile", metavar="VIDEO_FILE",
                        help="load video from VIDEO_FILE")
    parser.add_argument("-s", "--subtitles", dest="subtitles",
                        metavar="SUBTITLES_FILE",
                        help="load subtitles from SUBTITLES_FILE")
    parser.add_argument("-l", "--learning", dest="learning",
                        action="store_true",
                        help="start in learning mode (providing of VIDEO_FILE"
                        " and SUBTITLES_FILE are required)")

    app = Steno(parser.parse_args())
    app.MainLoop()

if __name__ == "__main__":
    main()
