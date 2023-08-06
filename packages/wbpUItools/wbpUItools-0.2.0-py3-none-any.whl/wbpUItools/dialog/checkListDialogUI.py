# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from ..control.checkAllListBox import CheckAllListBox
import wx
import wx.xrc

###########################################################################
## Class CheckListDialogUI
###########################################################################

class CheckListDialogUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 250,300 ), style = wx.CAPTION|wx.RESIZE_BORDER )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        sizer = wx.BoxSizer( wx.VERTICAL )

        self.message = wx.StaticText( self, wx.ID_ANY, u"Message", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.message.Wrap( -1 )

        sizer.Add( self.message, 0, wx.ALL|wx.EXPAND, 5 )

        checkListChoices = []
        self.checkList = CheckAllListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, checkListChoices, wx.LB_NEEDED_SB )
        sizer.Add( self.checkList, 1, wx.ALL|wx.EXPAND, 5 )

        buttons = wx.StdDialogButtonSizer()
        self.buttonsOK = wx.Button( self, wx.ID_OK )
        buttons.AddButton( self.buttonsOK )
        self.buttonsCancel = wx.Button( self, wx.ID_CANCEL )
        buttons.AddButton( self.buttonsCancel )
        buttons.Realize();

        sizer.Add( buttons, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( sizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


