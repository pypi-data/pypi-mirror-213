"""
Custom version of CheckListBox
"""
import wx


class CheckAllListBox(wx.Panel):
    """
    Drop-In replacement for wx.CheckListBox with additional "Check All" option
    """
    def __init__(
        self,
        parent,
        id:int=wx.ID_ANY,
        pos:wx.Point=wx.DefaultPosition,
        size:wx.Size=wx.DefaultSize,
        choices=None,
        style:int=wx.TAB_TRAVERSAL,
        validator=wx.DefaultValidator,
        name:str="CheckAllListBox",
    ):
        wx.Panel.__init__(
            self, parent, id=id, pos=pos, size=size, style=wx.TAB_TRAVERSAL, name=name
        )

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.checkBox_all = wx.CheckBox(
            self,
            wx.ID_ANY,
            u"Check All",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.CHK_3STATE,
        )
        sizer.Add(self.checkBox_all, 0, wx.ALL | wx.EXPAND, 3)

        self.checkList = wx.CheckListBox(
            parent=self,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            choices=choices if choices else [],
            style=style,
            validator=validator,
        )
        sizer.Add(self.checkList, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        # Connect Events
        self.checkBox_all.Bind(wx.EVT_CHECKBOX, self.on_check_all)
        self.checkBox_all.Bind(wx.EVT_UPDATE_UI, self.onUpdate_check_all)

    def __del__(self):
        pass

    # =========================================================================
    # CheckListBox methods
    # =========================================================================

    def Set(self, items):
        self.checkList.Set(items)

    def GetItems(self):
        return self.checkList.GetStrings()

    def SetItems(self, items):
        self.checkList.Set(items)

    Items = property(GetItems, SetItems)

    @property
    def Count(self):
        return self.checkList.Count

    @property
    def CountPerPage(self):
        return self.checkList.CountPerPage

    def Check(self, item, check=True):
        self.checkList.Check(item, check)

    def IsChecked(self, item):
        return self.checkList.IsChecked(item)

    def GetCheckedItems(self):
        return self.checkList.GetCheckedItems()

    def SetCheckedItems(self, indexes):
        self.checkList.SetCheckedItems(indexes)

    CheckedItems = property(GetCheckedItems, SetCheckedItems)

    def GetCheckedStrings(self):
        return self.checkList.GetCheckedStrings()

    def SetCheckedStrings(self, strings):
        self.checkList.SetCheckedStrings(strings)

    CheckedStrings = property(GetCheckedStrings, SetCheckedStrings)

    # =========================================================================
    # Event Handler
    # =========================================================================
    def on_check_all(self, event):
        checked = event.IsChecked()
        for i in range(self.checkList.Count):
            self.checkList.Check(i, checked)

    def onUpdate_check_all(self, event):
        if len(self.checkList.CheckedItems) == self.checkList.Count:
            self.checkBox_all.Value = True
        elif len(self.checkList.CheckedItems) == 0:
            self.checkBox_all.Value = False
        else:
            self.checkBox_all.Set3StateValue(wx.CHK_UNDETERMINED)
