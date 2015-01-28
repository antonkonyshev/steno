# -*- coding: utf-8 -*-
"""
.. module:: widgets
   :platform: Unix, Windows
   :synopsis: Widgets customization

.. moduleauthor:: Anton Konyshev <anton.konyshev@gmail.com>

"""

from sys import maxint

import wx
from wx.media import MediaCtrl

from defaults import Defaults


class VideoWidget(MediaCtrl):
    """Customization of MediaCtrl widget.

    """

    def SetAspectRatio(self, aspect, slot_size):
        """Sets video widget size in according to a selected aspect ratio.

        :param tuple aspect: Aspect ratio value
        :param tuple slot_size: Maximum size available for a widget

        """
        if aspect is None:
            src_width, src_height = self.GetBestSize()
            try:
                aspect = (src_width / float(src_height), 1)
            except ZeroDivisionError:
                aspect = (4, 3)
        size = self._calculate_size(slot_size, aspect)
        self.SetMinSize(size)
        self.SetSize(size)

    @classmethod
    def _calculate_size(cls, slot_size, aspect):
        """Calculates video widget size in according to a selected aspect ratio
        and a maximum size available for a widget.

        :param tuple slot_size: Maximum size available for a widget
        :param tuple aspect: Aspect ratio

        """
        slot_width, slot_height = slot_size
        width_prop, height_prop = aspect
        width_prop_by_one = width_prop / float(height_prop)
        slot_width_prop_by_one = slot_width / float(slot_height)
        if slot_width_prop_by_one > width_prop_by_one:
            own_height = int(slot_height)
            own_width = int((own_height / float(height_prop)) * width_prop)
        else:
            own_width = int(slot_width)
            own_height = int((own_width / float(width_prop)) * height_prop)
        return wx.Size(own_width, own_height)


class FilterList(wx.ListCtrl):
    """Implements the logics of a list of regex filters.

    """

    def __init__(self, parent=None, widget_id=wx.ID_ANY):
        """Serves to edit a list of regex filters.

        :param parent: Parent object, usually: panel, dialog or frame
        :type parent: subclass of :class:`wx.Window`
        :param int widget_id: Identifier of the widget

        """
        super(FilterList, self).__init__(parent, widget_id, style=wx.LC_REPORT
                                         | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN)
        self._init_columns()

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_deselect)

    def on_select(self, event):
        """Preserves an index of a filter selected by user.

        :param event: Event that contains an index of a selected filter
        :type event: :class:`wx.ListEvent` with type
                     :const:`wx.EVT_LIST_ITEM_SELECTED`

        """
        self._selected = event.GetIndex()
        event.Skip()

    def on_deselect(self, event):
        """Clears an index of a selected filter when user clears
        a selection.

        :param event: Event that entails an execution of the callback
        :type event: :class:`wx.ListEvent` with type
                     :const:`wx.EVT_LIST_ITEM_DESELECTED`

        """
        self._selected = None
        event.Skip()

    def selected(self):
        """Returns an index of a selected filter.

        :returns: Index of a selected filter or None if no one is selected
        :rtype: int or None

        """
        return getattr(self, u'_selected', None)

    def _init_columns(self):
        """Creates columns of the list of filters.

        """
        self.InsertColumn(0, Defaults.FILTERS_REGEX_HEADER)
        self.InsertColumn(1, Defaults.FILTERS_REPLACEMENT_HEADER)

    def on_resize(self, event):
        """Resizes columns of the list of filters proportionally to a width of
        the widget.

        :param event: Event which entails an execution of the callback
        :type event: :class:`wx.SizeEvent`

        """
        event.Skip()
        for col in xrange(2):
            self.SetColumnWidth(col, int(self.GetSize().GetWidth() / 2.05))

    def add_or_update_filter(self, regex, repl):
        """Adds or updates a filter data.

        :param regex: RegEx pattern
        :type regex: str or unicode
        :param repl: Replacement data
        :type repl: str or unicode
        :returns: Index of a filter which was modified
        :rtype: int

        """
        index = self.selected()
        if index >= 0:
            self.SetStringItem(index, 0, regex)
            self.SetStringItem(index, 1, repl)
            return index
        index = self.get_index_of(regex)
        if index:
            self.SetStringItem(index, 1, repl)
            return index
        index = self.InsertStringItem(maxint, regex)
        self.SetStringItem(index, 1, repl)
        return index

    def remove_selected(self):
        """Removes a selected filter from the list.

        :returns: Filter data or None
        :rtype: tuple or None

        """
        index = self.selected()
        if index >= 0:
            regex, repl = self.get_filter(index)
            self.DeleteItem(index)
            return regex, repl
        return None

    def get_filter(self, idx):
        """Returns data of a filter with specified index.

        :param int idx: Index of a filter
        :returns: Filter data
        :rtype: tuple

        """
        return self.GetItem(idx, 0).GetText(), self.GetItem(idx, 1).GetText()

    def get_index_of(self, regex):
        """Returns index of a filter by its regex pattern.

        :param regex: RegEx pattern
        :type regex: str or unicode
        :returns: Index of a filter or None if such filter isn't found
        :rtype: int or None

        """
        for index in xrange(self.GetItemCount()):
            if self.GetItem(index, 0).GetText() == regex:
                return index
        return None
