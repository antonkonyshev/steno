#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri Dec  5 14:35:05 2014

import wx

# begin wxGlade: extracode
import wx.html

import ids
from widgets import VideoWidget
from widgets import FilterList
# end wxGlade



class UserManualDialogGUI(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: UserManualDialogGUI.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.html_widget = wx.html.HtmlWindow(self, -1)
        self.close_button = wx.Button(self, wx.ID_CANCEL, "Close")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: UserManualDialogGUI.__set_properties
        self.SetTitle("User Manual")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(self.app.get_img_path(u'icon_64x64'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: UserManualDialogGUI.__do_layout
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_14.Add(self.html_widget, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_14.Add(self.close_button, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(sizer_14)
        sizer_14.Fit(self)
        self.Layout()
        # end wxGlade

# end of class UserManualDialogGUI


class PreferencesDialogGUI(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PreferencesDialogGUI.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.notebook = wx.Notebook(self, -1, style=0)
        self.filters_panel = wx.Panel(self.notebook, -1)
        self.fonts_panel = wx.Panel(self.notebook, -1)
        self.colors_panel = wx.Panel(self.notebook, -1)
        self.translation_panel = wx.Panel(self.notebook, -1)
        self.translation_cb = wx.CheckBox(self.translation_panel, -1, "Enable translation")
        self.learning_language_label = wx.StaticText(self.translation_panel, -1, "Learning language")
        self.learning_language_choice = wx.Choice(self.translation_panel, -1, choices=[])
        self.user_language_label = wx.StaticText(self.translation_panel, -1, "Your language")
        self.user_language_choice = wx.Choice(self.translation_panel, -1, choices=[])
        self.encoding_label = wx.StaticText(self.translation_panel, -1, "Default subtitles encoding")
        self.encoding_edit = wx.TextCtrl(self.translation_panel, -1, "")
        self.answer_correct_label = wx.StaticText(self.colors_panel, -1, "Highlighting of correct answers")
        self.answer_correct_cp = wx.ColourPickerCtrl(self.colors_panel, -1)
        self.answer_incorrect_label = wx.StaticText(self.colors_panel, -1, "Highlighting of incorrect answers")
        self.answer_incorrect_cp = wx.ColourPickerCtrl(self.colors_panel, -1)
        self.answer_fg_label = wx.StaticText(self.colors_panel, -1, "Subtitles text color")
        self.answer_fg_cp = wx.ColourPickerCtrl(self.colors_panel, -1)
        self.answer_bg_label = wx.StaticText(self.colors_panel, -1, "Subtitles background color")
        self.answer_bg_cp = wx.ColourPickerCtrl(self.colors_panel, -1)
        self.translation_fg_label = wx.StaticText(self.colors_panel, -1, "Translation text color")
        self.translation_fg_cp = wx.ColourPickerCtrl(self.colors_panel, -1)
        self.translation_bg_color = wx.StaticText(self.colors_panel, -1, "Translation background color")
        self.translation_bg_cp = wx.ColourPickerCtrl(self.colors_panel, -1)
        self.answer_font_label = wx.StaticText(self.fonts_panel, -1, "Subtitles font")
        self.answer_font_button = wx.Button(self.fonts_panel, ids.ANSWER_FONT, "Select font")
        self.translation_font_label = wx.StaticText(self.fonts_panel, -1, "Translation font")
        self.translation_font_button = wx.Button(self.fonts_panel, ids.TRANSLATION_FONT, "Select font")
        self.filter_list = FilterList(self.filters_panel, ids.FILTER_LIST)
        self.filter_regex_edit = wx.TextCtrl(self.filters_panel, -1, "")
        self.filter_replace_edit = wx.TextCtrl(self.filters_panel, -1, "")
        self.add_filter_button = wx.Button(self.filters_panel, ids.ADD_FILTER, "Add / Update")
        self.remove_filter_button = wx.Button(self.filters_panel, ids.REMOVE_FILTER, "Remove")
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, "Cancel")
        self.ok_button = wx.Button(self, wx.ID_OK, "OK")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_font, id=ids.ANSWER_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_font, id=ids.TRANSLATION_FONT)
        self.Bind(wx.EVT_BUTTON, self.on_filter_action, id=ids.ADD_FILTER)
        self.Bind(wx.EVT_BUTTON, self.on_filter_action, id=ids.REMOVE_FILTER)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: PreferencesDialogGUI.__set_properties
        self.SetTitle("Preferences")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(self.app.get_img_path(u'icon_64x64'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.translation_cb.SetValue(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PreferencesDialogGUI.__do_layout
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_30 = wx.BoxSizer(wx.VERTICAL)
        sizer_31 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_32 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_27 = wx.BoxSizer(wx.VERTICAL)
        sizer_29 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_28 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_20 = wx.BoxSizer(wx.VERTICAL)
        sizer_26 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_24 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_33 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17.Add(self.translation_cb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.learning_language_label, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_18.Add(self.learning_language_choice, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(sizer_18, 0, wx.EXPAND, 0)
        sizer_19.Add(self.user_language_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_19.Add(self.user_language_choice, 0, wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(sizer_19, 0, wx.EXPAND, 0)
        sizer_33.Add(self.encoding_label, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_33.Add(self.encoding_edit, 0, wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_17.Add(sizer_33, 0, wx.EXPAND, 0)
        self.translation_panel.SetSizer(sizer_17)
        sizer_21.Add(self.answer_correct_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_21.Add(self.answer_correct_cp, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_21, 0, wx.EXPAND, 0)
        sizer_22.Add(self.answer_incorrect_label, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_22.Add(self.answer_incorrect_cp, 0, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_22, 0, wx.EXPAND, 0)
        sizer_23.Add(self.answer_fg_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_23.Add(self.answer_fg_cp, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_23, 0, wx.EXPAND, 0)
        sizer_24.Add(self.answer_bg_label, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_24.Add(self.answer_bg_cp, 0, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_24, 0, wx.EXPAND, 0)
        sizer_25.Add(self.translation_fg_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_25.Add(self.translation_fg_cp, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_25, 0, wx.EXPAND, 0)
        sizer_26.Add(self.translation_bg_color, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_26.Add(self.translation_bg_cp, 0, wx.RIGHT|wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_20.Add(sizer_26, 0, wx.EXPAND, 0)
        self.colors_panel.SetSizer(sizer_20)
        sizer_28.Add(self.answer_font_label, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_28.Add(self.answer_font_button, 1, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_27.Add(sizer_28, 0, wx.EXPAND, 0)
        sizer_29.Add(self.translation_font_label, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_29.Add(self.translation_font_button, 1, wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_27.Add(sizer_29, 0, wx.EXPAND, 0)
        self.fonts_panel.SetSizer(sizer_27)
        sizer_30.Add(self.filter_list, 1, wx.ALL|wx.EXPAND, 5)
        sizer_32.Add(self.filter_regex_edit, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        sizer_32.Add(self.filter_replace_edit, 1, wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        sizer_30.Add(sizer_32, 0, wx.EXPAND, 0)
        sizer_31.Add(self.add_filter_button, 0, wx.LEFT|wx.BOTTOM, 5)
        sizer_31.Add(self.remove_filter_button, 0, wx.RIGHT|wx.BOTTOM, 5)
        sizer_31.Add((0, 0), 1, 0, 0)
        sizer_30.Add(sizer_31, 0, wx.EXPAND, 0)
        self.filters_panel.SetSizer(sizer_30)
        self.notebook.AddPage(self.translation_panel, "Translation")
        self.notebook.AddPage(self.colors_panel, "Colors")
        self.notebook.AddPage(self.fonts_panel, "Fonts")
        self.notebook.AddPage(self.filters_panel, "Filters")
        sizer_15.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        sizer_16.Add((0, 0), 1, 0, 0)
        sizer_16.Add(self.cancel_button, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_16.Add(self.ok_button, 0, wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_15.Add(sizer_16, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_15)
        sizer_15.Fit(self)
        self.Layout()
        # end wxGlade

    def on_font(self, event): # wxGlade: PreferencesDialogGUI.<event_handler>
        print "Event handler `on_font' not implemented!"
        event.Skip()

    def on_cancel(self, event): # wxGlade: PreferencesDialogGUI.<event_handler>
        print "Event handler `on_cancel' not implemented!"
        event.Skip()

    def on_ok(self, event): # wxGlade: PreferencesDialogGUI.<event_handler>
        print "Event handler `on_ok' not implemented!"
        event.Skip()

    def on_add_filter(self, event): # wxGlade: PreferencesDialogGUI.<event_handler>
        print "Event handler `on_add_filter' not implemented"
        event.Skip()

    def on_remove_filter(self, event): # wxGlade: PreferencesDialogGUI.<event_handler>
        print "Event handler `on_remove_filter' not implemented"
        event.Skip()

    def on_filter_action(self, event): # wxGlade: PreferencesDialogGUI.<event_handler>
        print "Event handler `on_filter_action' not implemented"
        event.Skip()

# end of class PreferencesDialogGUI


class PlayerGUI(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: PlayerGUI.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel = wx.Panel(self, -1)
        
        # Menu Bar
        self.menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.file_menu.Append(wx.ID_OPEN, "&Open Video\tCtrl+O", "", wx.ITEM_NORMAL)
        self.file_menu.Append(ids.OPEN_SUBTITLES, "Open &Subtitles\tCtrl+S", "", wx.ITEM_NORMAL)
        self.file_menu.AppendSeparator()
        self.file_menu.Append(wx.ID_CLOSE_ALL, "&Close All\tCtrl+W", "", wx.ITEM_NORMAL)
        self.file_menu.AppendSeparator()
        self.file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q", "", wx.ITEM_NORMAL)
        self.menubar.Append(self.file_menu, "&File")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(ids.PREFERENCES, "&Preferences\tCtrl+P", "", wx.ITEM_NORMAL)
        self.menubar.Append(wxglade_tmp_menu, "&Edit")
        self.playback_menu = wx.Menu()
        self.playback_menu.Append(ids.PLAY, "P&lay\tCtrl+L", "", wx.ITEM_NORMAL)
        self.playback_menu.Append(ids.PAUSE, "Pa&use\tCtrl+U", "", wx.ITEM_NORMAL)
        self.playback_menu.AppendSeparator()
        self.playback_menu.Append(ids.REPEAT, "&Repeat\tCtrl+R", "", wx.ITEM_NORMAL)
        self.playback_menu.Append(ids.HINT, "&Hint\tCtrl+H", "", wx.ITEM_NORMAL)
        self.playback_menu.AppendSeparator()
        self.playback_menu.Append(wx.ID_STOP, "&Stop", "", wx.ITEM_NORMAL)
        self.playback_menu.AppendSeparator()
        aspect_ratio_menu = wx.Menu()
        aspect_ratio_menu.Append(ids.ASPECT_AUTO, "Auto", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_4x3, "4 : 3", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_3x2, "3 : 2", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_5x3, "5 : 3", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_16x9, "16 : 9", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_14x9, "14 : 9", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_16x10, "16 : 10", "", wx.ITEM_RADIO)
        aspect_ratio_menu.Append(ids.ASPECT_21x9, "21 : 9", "", wx.ITEM_RADIO)
        self.playback_menu.AppendMenu(ids.ASPECT_RATIO, "&Aspect Ratio", aspect_ratio_menu, "")
        self.menubar.Append(self.playback_menu, "&Playback")
        self.help_menu = wx.Menu()
        self.help_menu.Append(ids.MANUAL, "User &Manual", "", wx.ITEM_NORMAL)
        self.help_menu.Append(wx.ID_ABOUT, "&About", "", wx.ITEM_NORMAL)
        self.menubar.Append(self.help_menu, "&Help")
        self.SetMenuBar(self.menubar)
        # Menu Bar end
        self.statusbar = self.CreateStatusBar(2, 0)
        self.mode_label = wx.StaticText(self.panel, -1, "Mode", style=wx.ALIGN_RIGHT)
        self.mode_choice = wx.Choice(self.panel, ids.MODE, choices=["Preview", "Learning"])
        self.play_button = wx.BitmapButton(self.panel, ids.PLAY, wx.Bitmap(self.app.get_img_path(u'play'),wx.BITMAP_TYPE_ANY))
        self.pause_button = wx.BitmapButton(self.panel, ids.PAUSE, wx.Bitmap(self.app.get_img_path(u'pause'),wx.BITMAP_TYPE_ANY))
        self.repeat_button = wx.BitmapButton(self.panel, ids.REPEAT, wx.Bitmap(self.app.get_img_path(u'repeat'),wx.BITMAP_TYPE_ANY))
        self.hint_button = wx.BitmapButton(self.panel, ids.HINT, wx.Bitmap(self.app.get_img_path(u'help'),wx.BITMAP_TYPE_ANY))
        self.stop_button = wx.BitmapButton(self.panel, wx.ID_STOP, wx.Bitmap(self.app.get_img_path(u'stop'),wx.BITMAP_TYPE_ANY))
        self.delay_label = wx.StaticText(self.panel, -1, "Subtitles shift", style=wx.ALIGN_RIGHT)
        self.delay_spin = wx.SpinCtrl(self.panel, ids.DELAY, "0", min=-999999, max=999999)
        self.delay_units_label = wx.StaticText(self.panel, -1, "ms")
        self.video_slider = wx.Slider(self.panel, ids.SEEK, 0, 0, 10)
        self.volume_label = wx.StaticText(self.panel, -1, "Volume", style=wx.ALIGN_CENTRE)
        self.volume_slider = wx.Slider(self.panel, ids.VOLUME, 50, 0, 100)
        self.video = VideoWidget(self.panel, ids.VIDEO)
        self.word_translate = wx.TextCtrl(self.panel, ids.WORD_TRANSLATE, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.subtitle_translate = wx.TextCtrl(self.panel, ids.SUBTITLE_TRANSLATE, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.answer_edit = wx.TextCtrl(self.panel, ids.ANSWER, "", style=wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_CENTRE)
        self.progress_gauge = wx.Gauge(self.panel, ids.PROGRESS, 100, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.on_content_open, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.on_content_open, id=ids.OPEN_SUBTITLES)
        self.Bind(wx.EVT_MENU, self.on_close_all, id=wx.ID_CLOSE_ALL)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_preferences, id=ids.PREFERENCES)
        self.Bind(wx.EVT_MENU, self.on_playback_control, id=ids.PLAY)
        self.Bind(wx.EVT_MENU, self.on_playback_control, id=ids.PAUSE)
        self.Bind(wx.EVT_MENU, self.on_repeat, id=ids.REPEAT)
        self.Bind(wx.EVT_MENU, self.on_hint, id=ids.HINT)
        self.Bind(wx.EVT_MENU, self.on_playback_control, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_AUTO)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_4x3)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_3x2)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_5x3)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_16x9)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_14x9)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_16x10)
        self.Bind(wx.EVT_MENU, self.on_aspect_ratio, id=ids.ASPECT_21x9)
        self.Bind(wx.EVT_MENU, self.on_user_manual, id=ids.MANUAL)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_CHOICE, self.on_mode, id=ids.MODE)
        self.Bind(wx.EVT_BUTTON, self.on_playback_control, id=ids.PLAY)
        self.Bind(wx.EVT_BUTTON, self.on_playback_control, id=ids.PAUSE)
        self.Bind(wx.EVT_BUTTON, self.on_repeat, id=ids.REPEAT)
        self.Bind(wx.EVT_BUTTON, self.on_hint, id=ids.HINT)
        self.Bind(wx.EVT_BUTTON, self.on_playback_control, id=wx.ID_STOP)
        self.Bind(wx.EVT_SPINCTRL, self.on_delay, id=ids.DELAY)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.on_seek, id=ids.SEEK)
        self.Bind(wx.EVT_COMMAND_SCROLL, self.on_volume, id=ids.VOLUME)
        self.Bind(wx.EVT_TEXT, self.on_answer, id=ids.ANSWER)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: PlayerGUI.__set_properties
        self.SetTitle("Steno")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(self.app.get_img_path(u'icon_64x64'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((933, 747))
        self.statusbar.SetStatusWidths([0, 0])
        # statusbar fields
        statusbar_fields = ["", ""]
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        self.mode_choice.Enable(False)
        self.mode_choice.SetSelection(0)
        self.play_button.Enable(False)
        self.play_button.SetSize(self.play_button.GetBestSize())
        self.pause_button.Enable(False)
        self.pause_button.SetSize(self.pause_button.GetBestSize())
        self.repeat_button.SetToolTipString("Repeat the last fragment")
        self.repeat_button.Hide()
        self.repeat_button.SetSize(self.repeat_button.GetBestSize())
        self.hint_button.SetToolTipString("Use a hint")
        self.hint_button.Hide()
        self.hint_button.SetSize(self.hint_button.GetBestSize())
        self.stop_button.Enable(False)
        self.stop_button.SetSize(self.stop_button.GetBestSize())
        self.delay_spin.SetToolTipString("Subtitles delay in milliseconds")
        self.delay_spin.Enable(False)
        self.video_slider.Enable(False)
        self.word_translate.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.subtitle_translate.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.answer_edit.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.answer_edit.Enable(False)
        self.progress_gauge.SetToolTipString("Shows your progress in the fragment")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PlayerGUI.__do_layout
        panels_sizer = wx.BoxSizer(wx.HORIZONTAL)
        topbox = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_1_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7.Add(self.mode_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_7.Add(self.mode_choice, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_6.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_8.Add(self.play_button, 0, wx.LEFT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.pause_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.repeat_button, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.hint_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_8.Add(self.stop_button, 0, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_6.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_9.Add((0, 0), 1, 0, 0)
        sizer_9.Add(self.delay_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_9.Add(self.delay_spin, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_9.Add(self.delay_units_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_6.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_3.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_3.Add(self.video_slider, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        sizer_1_copy.Add(sizer_3, 5, wx.EXPAND, 0)
        sizer_12.Add((0, 0), 1, 0, 0)
        sizer_12.Add(self.volume_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_12.Add((0, 0), 1, 0, 0)
        sizer_5.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_5.Add(self.volume_slider, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_1_copy.Add(sizer_4, 1, wx.EXPAND, 0)
        topbox.Add(sizer_1_copy, 0, wx.EXPAND, 0)
        sizer_11.Add(self.video, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_13.Add(self.word_translate, 3, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        sizer_13.Add(self.subtitle_translate, 1, wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        sizer_11.Add(sizer_13, 1, wx.EXPAND, 0)
        topbox.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_10.Add(self.answer_edit, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        sizer_10.Add(self.progress_gauge, 0, wx.ALL|wx.EXPAND, 5)
        sizer_2.Add(sizer_10, 1, wx.EXPAND, 0)
        topbox.Add(sizer_2, 0, wx.EXPAND, 0)
        self.panel.SetSizer(topbox)
        panels_sizer.Add(self.panel, 1, wx.EXPAND, 0)
        self.SetSizer(panels_sizer)
        self.Layout()
        # end wxGlade

    def on_video_open(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_video_open' not implemented!"
        event.Skip()

    def on_subtitles_open(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_subtitles_open' not implemented!"
        event.Skip()

    def on_close_all(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_close_all' not implemented!"
        event.Skip()

    def on_exit(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_exit' not implemented!"
        event.Skip()

    def on_about(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_about' not implemented!"
        event.Skip()

    def on_mode(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_mode' not implemented!"
        event.Skip()

    def on_play(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_play' not implemented!"
        event.Skip()

    def on_stop(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_stop' not implemented!"
        event.Skip()

    def on_delay(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_delay' not implemented!"
        event.Skip()

    def on_seek(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_seek' not implemented!"
        event.Skip()

    def on_volume(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_volume' not implemented!"
        event.Skip()

    def on_answer(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_answer' not implemented!"
        event.Skip()

    def on_hint(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_hint' not implemented!"
        event.Skip()

    def on_repeat(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_repeat' not implemented!"
        event.Skip()

    def on_pause(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_pause' not implemented"
        event.Skip()

    def on_playback_control(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_playback_control' not implemented"
        event.Skip()

    def on_content_open(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_content_open' not implemented"
        event.Skip()

    def on_proportion(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_proportion' not implemented"
        event.Skip()

    def on_aspect_ratio(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_aspect_ratio' not implemented"
        event.Skip()

    def on_user_manual(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_user_manual' not implemented"
        event.Skip()

    def on_license(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_license' not implemented"
        event.Skip()

    def on_preferences(self, event): # wxGlade: PlayerGUI.<event_handler>
        print "Event handler `on_preferences' not implemented"
        event.Skip()

# end of class PlayerGUI

