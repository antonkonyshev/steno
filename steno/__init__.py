#!/usr/bin/env python
# -*- coding: utf-8 -*-


from steno import Steno
from player import Player
from defaults import Defaults
from dialogs import PreferencesDialog, UserManualDialog
from droptargets import FileDropTarget
from translator import Translator
from verificator import Verificator
from widgets import VideoWidget, FilterList
from steno import main as start


__all__ = [
    'Steno',
    'Player',
    'Defaults',
    'PreferencesDialog',
    'UserManualDialog',
    'FileDropTarget',
    'Translator',
    'Verificator',
    'VideoWidget',
    'FilterList',
]

__license__ = "wxWidgets (wxWindows Library Licence) 3.1"
__version__ = Defaults.VERSION
__author__ = "Anton Konyshev <anton.konyshev@gmail.com>"
__copyright__ = "Copyright 2014 Anton Konyshev"
