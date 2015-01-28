# -*- coding: utf-8 -*-
"""
.. module:: dialogs
   :platform: Unix, Windows
   :synopsis: Application dialogs definition

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""
# License: wxWidgets (wxWindows Library Licence) 3.1

import os.path as op

import wx

from player_gui import PreferencesDialogGUI
from player_gui import UserManualDialogGUI
import ids
from defaults import Defaults


class PreferencesDialog(PreferencesDialogGUI):
    """Dialog allows user to edit the configuration using a graphical
    interface.

    """

    def __init__(self, player=None):
        """Dialog for editing of the configuration data.

        :param player: Player frame instance
        :type player: :class:`player.Player`

        """
        self.player = player
        self.app = getattr(self.player, u'app', None)
        super(PreferencesDialog, self).__init__(None)
        self.SetMinSize(wx.Size(*Defaults.PREFERENCES_DIALOG_MIN_SIZE))
        self.SetSize(wx.Size(*Defaults.PREFERENCES_DIALOG_MIN_SIZE))

        self.ok_button.SetDefault()
        self.SetEscapeId(wx.ID_CANCEL)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_filter_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_filter_deselect)

        self._set_init_values()

    def on_filter_select(self, event):
        """Fills fields for filter editing by values of a selected filter.

        :param event: Event that contains an identifier of a selected filter
        :type event: :class:`wx.ListEvent` with type
                     :const:`wx.EVT_LIST_ITEM_SELECTED`

        """
        regex, repl = self.filter_list.get_filter(event.GetIndex())
        self.filter_regex_edit.ChangeValue(regex)
        self.filter_replace_edit.ChangeValue(repl)

    def on_filter_deselect(self, event):
        """Clears fields for filter editing when user clears selection.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.ListEvent` with type
                     :const: `wx.EVT_LIST_ITEM_DESELECTED`

        """
        self.filter_regex_edit.ChangeValue(u'')
        self.filter_replace_edit.ChangeValue(u'')

    def on_filter_action(self, event):
        """Adds, updates or removes a selected filter.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_BUTTON`

        """
        widget_id = event.GetId()
        if widget_id == ids.ADD_FILTER:
            regex = self.filter_regex_edit.GetValue()
            repl = self.filter_replace_edit.GetValue()
            if regex or repl:
                sel = self.filter_list.selected()
                if sel:
                    self.change_filter(ids.REMOVE_FILTER,
                                       *self.filter_list.get_filter(sel))
                index = self.filter_list.add_or_update_filter(regex, repl)
                self.change_filter(widget_id,
                                   *self.filter_list.get_filter(index))
        elif widget_id == ids.REMOVE_FILTER:
            self.change_filter(widget_id, *self.filter_list.remove_selected())

    def change_filter(self, action, regex=None, repl=None):
        """Changes values of a filter, adds a new filter or removes it.

        :param int action: Identifier of requested operation (may be one of
                           ids.ADD_FILTER, ids.REMOVE_FILTER)
        :param regex: RegEx pattern
        :type regex: str or unicode
        :param repl: Replacement data
        :type repl: str or unicode

        """
        if regex is not None and repl is not None:
            if action == ids.ADD_FILTER:
                self._filters[regex] = repl
            elif action == ids.REMOVE_FILTER:
                try:
                    del self._filters[regex]
                except KeyError:
                    pass

    def _set_filters(self):
        """Receives filters from the player instance and inserts them into
        filters list.

        """
        self._filters = self.player.get_filters(copy=True)
        for regex, repl in self._filters.iteritems():
            self.filter_list.add_or_update_filter(regex, repl)

    def get_filters(self):
        """Returns a collection of filters.

        :return: RegEx filters
        :rtype: dict

        """
        return self._filters.copy()

    def _set_languages(self):
        """Sets initial values of language selection widgets.

        """
        learning = self.player.app.get_setting(
            u'learning_language', Defaults.DEFAULT_LEARNING_LANGUAGE)
        native = self.player.app.get_setting(u'user_language', None)
        if native is None or native not in set(
                code for _, code in Defaults.LANGUAGES):
            native = Defaults.DEFAULT_USER_LANGUAGE
        idx = learning_idx = native_idx = 0
        for langname, langcode in Defaults.LANGUAGES:
            self.learning_language_choice.Append(langname)
            self.user_language_choice.Append(langname)
            if langcode == learning:
                learning_idx = idx
            if langcode == native:
                native_idx = idx
            idx += 1
        self.learning_language_choice.SetSelection(learning_idx)
        self.user_language_choice.SetSelection(native_idx)
        self.encoding_edit.SetValue(self.player.app.get_setting(
            u'encoding', Defaults.DEFAULT_ENCODING))

    def _set_init_values(self):
        """Sets initial values for widgets.

        """
        self._set_languages()
        self._set_filters()
        self.translation_cb.SetValue(
            self.player.app.get_setting(u'translation',
                                        Defaults.DEFAULT_TRANSLATION_ENABLE))
        [getattr(self, u'{0}_{1}_cp'.format(group, ground)).SetColour(
            getattr(getattr(self.player, widget),
                    u'Get{0}Colour'.format(method))())
         for ground, method in {
            u'fg': u'Foreground', u'bg': u'Background'}.iteritems()
         for group, widget in {
            u'answer': u'answer_edit', u'translation': u'word_translate'
        }.iteritems()]
        [getattr(self, u'answer_{0}_cp'.format(correctness)).SetColour(
            getattr(self.player, u'{0}_highlighting'.format(correctness))())
         for correctness in (u'correct', u'incorrect',)]
        self._answer_font = self.player.answer_edit.GetFont()
        self._translation_font = self.player.word_translate.GetFont()
        self._show_font_names()

    def _show_font_names(self):
        """Sets labels for buttons of font selection dialogs.

        """
        for group in (u'answer', u'translation',):
            getattr(self, u'{0}_font_button'.format(group)).SetLabel(
                u'{0} {1}'.format(
                    getattr(self, u'_{0}_font'.format(
                        group)).GetFaceName().title(),
                    getattr(self, u'_{0}_font'.format(group)).GetPointSize()))

    def on_font(self, event):
        """Creates and shows a font selection dialog with initial data.

        :param event: Event that entailed an execution of the callback
        :type event: :class:`wx.CommandEvent` with type :const:`wx.EVT_BUTTON`

        """
        widget_id = event.GetId()
        for group, font_id in {
            u'answer': ids.ANSWER_FONT, u'translation': ids.TRANSLATION_FONT
        }.iteritems():
            if widget_id == font_id:
                data = wx.FontData()
                data.SetInitialFont(getattr(self, u'_{0}_font'.format(group)))
                dialog = wx.FontDialog(None, data)
                if dialog.ShowModal() == wx.ID_OK:
                    setattr(self, u'_{0}_font'.format(group),
                            dialog.GetFontData().GetChosenFont())
                    self._show_font_names()
                return None

    def get_preferences(self):
        """Returns current configuration data.

        :returns: Configuration data
        :rtype: dict

        """
        prefs = {
            u'translation': self.translation_cb.GetValue(),
            u'learning_language': Defaults.LANGUAGES[
                self.learning_language_choice.GetSelection()][1],
            u'user_language': Defaults.LANGUAGES[
                self.user_language_choice.GetSelection()][1],
            u'answer_correct': self.answer_correct_cp.GetColour().GetRGB(),
            u'answer_incorrect': self.answer_incorrect_cp.GetColour().GetRGB(),
            u'answer_font': self._answer_font.GetNativeFontInfoDesc(),
            u'translation_font':
                self._translation_font.GetNativeFontInfoDesc(),
            u'encoding': self.encoding_edit.GetValue(),
        }
        prefs.update(dict(
            [(u'{0}_{1}'.format(group, ground), getattr(
                self,
                u'{0}_{1}_cp'.format(group, ground)).GetColour().GetRGB())
             for group in (u'answer', u'translation',)
             for ground in (u'fg', u'bg',)]))
        return prefs


class UserManualDialog(UserManualDialogGUI):
    """Dialog allows user to read user manual while working with the
    application.

    """
    def __init__(self, player=None):
        """Dialog to showing of the user manual text.

        :param player: Player window instance
        :type player: :class:`player.Player`

        """
        self.player = player
        self.app = getattr(self.player, u'app', None)
        super(UserManualDialog, self).__init__(None)
        self.SetMinSize(wx.Size(*Defaults.USER_MANUAL_DIALOG_MIN_SIZE))
        self.SetSize(wx.Size(*Defaults.USER_MANUAL_DIALOG_MIN_SIZE))
        self.html_widget.SetPage(self._load_html())
        self.close_button.SetDefault()
        self.SetEscapeId(wx.ID_CANCEL)

    def _load_html(self):
        """Loads the content of User Manual from html file.

        :returns: Content of User Manual
        :rtype: unicode

        """
        if op.isfile(Defaults.USER_MANUAL_FILEPATH):
            try:
                with open(Defaults.USER_MANUAL_FILEPATH) as handler:
                    html = handler.read()
                    handler.close()
            except IOError as err:
                html = Defaults.USER_MANUAL_IOERROR.format(err.message)
        else:
            html = Defaults.USER_MANUAL_IS_NOT_A_FILE
        return html
