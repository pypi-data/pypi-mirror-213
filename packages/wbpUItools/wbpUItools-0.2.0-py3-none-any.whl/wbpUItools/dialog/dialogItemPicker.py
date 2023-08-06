"""
dialogItemPicker
===============================================================================

Implementation of the ItemPicker dialog.
"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Iterable, List
import wx

from .dialogItemPickerUI import DialogItemPickerUI

if TYPE_CHECKING:
    from wbBase.application import App


class DialogItemPicker(DialogItemPickerUI):
    def __init__(
        self,
        parent: Optional[wx.Window] = None,
        title: str = "",
        message: str = "Select options",
        options: Optional[Iterable[str]] = None,
        selection: Optional[Iterable[str]] = None,
        optionsLabel: str = "Options",
        selectionLabel: str = "Selection",
        width: int = 500,
        height: int = 400,
    ):
        """
        :param parent: Parent window of the dialog, defaults to application TopWindow
        :param title: Title of the dialog, defaults to application AppDisplayName
        :param message: Shown message, defaults to "Select options"
        :param options: defaults to empty list
        :param selection: defaults to empty list
        :param optionsLabel: Options label, defaults to "Options"
        :param selectionLabel: Selection, defaults to "Selection"
        :param width: Width of the dialog, defaults to 500
        :param height: Height of the dialog, defaults to 400
        """
        app: App = wx.GetApp()
        if not parent:
            parent = app.TopWindow
        DialogItemPickerUI.__init__(self, parent)
        self.Size = (width, height)
        self.Title = title or app.AppDisplayName
        self.label_message.LabelText = message
        self.options = options or []
        self.selection = selection or []
        self.itemPicker.label_options.LabelText = optionsLabel
        self.itemPicker.label_selection.LabelText = selectionLabel

    @property
    def options(self) -> List[str]:
        """
        :return: selectable options
        """
        return self.itemPicker.listBox_options.Items

    @options.setter
    def options(self, value: Iterable[str]):
        self.itemPicker.listBox_options.Items = list(value)

    @property
    def selection(self) -> List[str]:
        """
        :return: actual selection of the user.
        """
        return self.itemPicker.listBox_selection.Items

    @selection.setter
    def selection(self, value: Iterable[str]):
        self.itemPicker.listBox_selection.Items = list(value)
