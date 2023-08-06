from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING, Iterable, List, Union

import wx

from .dialog.checkListDialogUI import CheckListDialogUI
from .dialog.dialogItemPicker import DialogItemPicker

if TYPE_CHECKING:
    from wbBase.application import App

__version__ = "0.2.0"


def AskString(message: str, value: str = "", title: str = "") -> Optional[str]:
    app: App = wx.GetApp()
    return wx.GetTextFromUser(
        message,
        caption=title or app.AppDisplayName,
        default_value=value,
        parent=app.TopWindow,
    )


def AskYesNoCancel(message:str, title:str="", default=0, informativeText:str="") -> Union[bool, None]:
    """
    :param message: Shown message
    :param title: Title of the dialog, defaults to application AppDisplayName
    :param default: Not used
    :param informativeText: Additional information, defaults to ""
    :return: Yes = True, No = False, Cancel = None
    """
    app: App = wx.GetApp()
    if informativeText:
        messageText = message.strip() + "\n\n" + informativeText.strip()
    else:
        messageText = message
    result = wx.MessageBox(
        message=messageText,
        caption=title or app.AppDisplayName,
        style=wx.YES_NO | wx.CANCEL,
        parent=app.TopWindow,
    )
    if result == wx.YES:
        return True
    if result == wx.NO:
        return False


def Message(message, title="Workbench", informativeText="") -> None:
    if informativeText:
        messageText = message.strip() + "\n\n" + informativeText.strip()
    else:
        messageText = message
    wx.MessageBox(
        message=messageText, caption=title, style=wx.OK, parent=wx.GetApp().TopWindow
    )


def GetFile(
    message: str = "",
    title: str = "",
    directory: str = "",
    fileName: str = "",
    allowsMultipleSelection: bool = False,
    fileTypes: str = "",
) -> Optional[str]:
    if not fileTypes:
        wildcardStr = "Any files (*.*)|*.*"
    else:
        wildcardStr = fileTypes
    app: App = wx.GetApp()
    return wx.FileSelector(
        message=message,
        default_path=directory,
        default_filename=fileName,
        default_extension="",
        wildcard=wildcardStr,
        flags=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        parent=app.TopWindow,
    )


def PutFile(message: str = "", fileName: str = "") -> Optional[str]:
    if fileName:
        default_path, default_filename = os.path.split(fileName)
    else:
        default_path, default_filename = "", ""
    return wx.FileSelector(
        message=message,
        default_path=default_path,
        default_filename=default_filename,
        default_extension="",
        wildcard="Any files (*.*)|*.*",
        flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        parent=wx.GetApp().TopWindow,
    )


class CheckListDialog(CheckListDialogUI):
    def __init__(self, message, title="Workbench", choices=None, checked=None):
        super().__init__(wx.GetApp().TopWindow)
        self.Title = title
        self.message.Label = message
        if isinstance(choices, Iterable):
            self.checkList.SetItems([c for c in choices])
            if isinstance(checked, Iterable):
                self.checkList.SetCheckedStrings([i for i in checked if i in choices])


def getCheckList(message, title="Workbench", choices=None, checked=None):
    with CheckListDialog(message, title, choices, checked) as dialog:
        if dialog.ShowModal() == wx.ID_OK:
            return dialog.checkList.GetCheckedStrings()


def pickItems(
    message: str = "Select options",
    title: str = "",
    options: Optional[Iterable[str]] = None,
    selection: Optional[Iterable[str]] = None,
    optionsLabel: str = "Options",
    selectionLabel: str = "Selection",
    width: int = 500,
    height: int = 400,
) -> List[str]:
    """
    Show the :class:`~.dialog.dialogItemPicker.DialogItemPicker`
    with the given parameters and return the selected items.

    :param message: Shown message, defaults to "Select options"
    :param title: Title of the dialog, defaults to application AppDisplayName
    :param options: defaults to empty list
    :param selection: defaults to empty list
    :param optionsLabel: Options label, defaults to "Options"
    :param selectionLabel: Selection, defaults to "Selection"
    :param width: Width of the dialog, defaults to 500
    :param height: Height of the dialog, defaults to 400
    :return: Items selected by the user
    """
    with DialogItemPicker(
        wx.GetApp().TopWindow,
        title,
        message,
        options,
        selection,
        optionsLabel,
        selectionLabel,
        width,
        height,
    ) as dialog:
        if dialog.ShowModal() == wx.ID_OK:
            return dialog.selection
    return []


globalObjects = [
    "AskString",
    "AskYesNoCancel",
    "Message",
    "GetFile",
    "PutFile",
    "getCheckList",
]
