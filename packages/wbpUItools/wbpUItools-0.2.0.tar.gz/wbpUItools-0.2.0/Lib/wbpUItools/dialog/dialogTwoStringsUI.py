# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class DialogTwoStringsUI
###########################################################################

class DialogTwoStringsUI ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Two Strings", pos = wx.DefaultPosition, size = wx.Size( 300,150 ), style = wx.CAPTION|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.Size( 300,150 ), wx.DefaultSize )

		sizer = wx.GridBagSizer( 0, 0 )
		sizer.SetFlexibleDirection( wx.BOTH )
		sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.lbl_Message = wx.StaticText( self, wx.ID_ANY, u"Enter two strings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_Message.Wrap( -1 )

		sizer.Add( self.lbl_Message, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.lbl_string_1 = wx.StaticText( self, wx.ID_ANY, u"String 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_string_1.Wrap( -1 )

		sizer.Add( self.lbl_string_1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_string_1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer.Add( self.textCtrl_string_1, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

		self.lbl_string_2 = wx.StaticText( self, wx.ID_ANY, u"String 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_string_2.Wrap( -1 )

		sizer.Add( self.lbl_string_2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.textCtrl_string_2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sizer.Add( self.textCtrl_string_2, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		button_sizer = wx.StdDialogButtonSizer()
		self.button_sizerOK = wx.Button( self, wx.ID_OK )
		button_sizer.AddButton( self.button_sizerOK )
		self.button_sizerCancel = wx.Button( self, wx.ID_CANCEL )
		button_sizer.AddButton( self.button_sizerCancel )
		button_sizer.Realize();

		sizer.Add( button_sizer, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 5 )


		sizer.AddGrowableCol( 1 )
		sizer.AddGrowableRow( 3 )

		self.SetSizer( sizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


