"""
dialogTwoStrings
===============================================================================

Get two strings from user.
"""
import wx
from .dialogTwoStringsUI import DialogTwoStringsUI


class DialogTwoStrings(DialogTwoStringsUI):
    """
    Dialog to get two strings from user.
    """

    def __init__(
        self,
        message: str = "Enter two strings",
        caption: str = "Two Strings",
        string1: str = "",
        string2: str = "",
        label1: str = "String 1",
        label2: str = "String 1",
    ):
        super().__init__(wx.GetApp().TopWindow)
        self.SetTitle(caption)
        self.lbl_Message.SetLabel(message)
        self.lbl_string_1.SetLabel(label1)
        self.textCtrl_string_1.SetValue(string1)
        self.lbl_string_2.SetLabel(label2)
        self.textCtrl_string_2.SetValue(string2)
        self.Layout()

    @property
    def string1(self):
        return self.textCtrl_string_1.GetValue()

    @property
    def string2(self):
        return self.textCtrl_string_2.GetValue()


def getTwoStrings(
    message: str = "Enter two strings",
    caption: str = "Two Strings",
    string1: str = "",
    string2: str = "",
    label1: str = "String 1",
    label2: str = "String 1",
):
    """
    Function to get two strings from user.
    """
    with DialogTwoStrings(
        message, caption, string1, string2, label1, label2
    ) as dialogTwoStrings:
        if dialogTwoStrings.ShowModal() == wx.ID_OK:
            return (dialogTwoStrings.string1, dialogTwoStrings.string2)
    return (None, None)
