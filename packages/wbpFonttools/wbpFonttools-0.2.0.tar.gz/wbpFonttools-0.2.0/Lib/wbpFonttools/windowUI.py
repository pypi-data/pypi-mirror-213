# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May 29 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from .control import FontTableListCrtl, FontObjectView
#from workbench.control.filling import Filling
from wx.stc import StyledTextCtrl
import wx
import wx.xrc

###########################################################################
## Class FontToolsWindowUI
###########################################################################

class FontToolsWindowUI ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.FULL_REPAINT_ON_RESIZE|wx.NO_BORDER|wx.TAB_TRAVERSAL, name = u"TtxWindow" )
		
		mainSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.tableList = FontTableListCrtl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL )
		self.tableList.SetMinSize( wx.Size( 100,-1 ) )
		
		mainSizer.Add( self.tableList, 0, wx.EXPAND, 0 )
		
		rightSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.fontEditToolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT )
		self.fontEditToolBar.SetToolBitmapSize( wx.Size( 16,16 ) )
		self.fontEditToolBar.SetMargins( wx.Size( 5,5 ) )
		self.fontEditToolBar.SetToolPacking( 5 )
		self.toolXML = self.fontEditToolBar.AddTool( wx.ID_ANY, u"XML", wx.ArtProvider.GetBitmap( 'HTML_FILE', wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_RADIO, u"View table in XML viewer", u"View table in XML viewer", None ) 
		
		self.toolNameSpace = self.fontEditToolBar.AddTool( wx.ID_ANY, u"NameSpace", wx.ArtProvider.GetBitmap( 'NAMESPACE', wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_RADIO, u"View table in NameSpace viewer", u"View table in NameSpace viewer", None ) 
		
		self.fontEditToolBar.AddSeparator()
		
		self.toolReload = self.fontEditToolBar.AddTool( wx.ID_ANY, u"Reload table", wx.ArtProvider.GetBitmap( 'RESET', wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Reload TTX table", u"Reload TTX table", None ) 
		
		self.toolCompile = self.fontEditToolBar.AddTool( wx.ID_ANY, u"Compile XML to TTX table", wx.ArtProvider.GetBitmap( 'COMPILE', wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, u"Compile XML to TTX table", u"Compile XML to TTX table", None ) 
		
		self.fontEditToolBar.Realize() 
		
		rightSizer.Add( self.fontEditToolBar, 0, wx.EXPAND, 0 )
		
		self.filling = FontObjectView( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.CLIP_CHILDREN|wx.NO_BORDER )
		self.filling.Hide()
		
		rightSizer.Add( self.filling, 1, wx.EXPAND, 0 )
		
		self.textEditor = StyledTextCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
		rightSizer.Add( self.textEditor, 1, wx.EXPAND, 0 )
		
		
		mainSizer.Add( rightSizer, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( mainSizer )
		self.Layout()
		mainSizer.Fit( self )
		
		# Connect Events
		self.tableList.Bind( wx.EVT_LEFT_DOWN, self.OnLeftDown )
		self.tableList.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnTableSelected )
		self.Bind( wx.EVT_TOOL, self.OnToolXML, id = self.toolXML.GetId() )
		self.Bind( wx.EVT_UPDATE_UI, self.OnUpdateToolXML, id = self.toolXML.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolNameSpace, id = self.toolNameSpace.GetId() )
		self.Bind( wx.EVT_UPDATE_UI, self.OnUpdateToolNameSpace, id = self.toolNameSpace.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnTooReload, id = self.toolReload.GetId() )
		self.Bind( wx.EVT_TOOL, self.OnToolCompile, id = self.toolCompile.GetId() )
		self.Bind( wx.EVT_UPDATE_UI, self.OnUpdateToolCompile, id = self.toolCompile.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnLeftDown( self, event ):
		event.Skip()
	
	def OnTableSelected( self, event ):
		event.Skip()
	
	def OnToolXML( self, event ):
		event.Skip()
	
	def OnUpdateToolXML( self, event ):
		event.Skip()
	
	def OnToolNameSpace( self, event ):
		event.Skip()
	
	def OnUpdateToolNameSpace( self, event ):
		event.Skip()
	
	def OnTooReload( self, event ):
		event.Skip()
	
	def OnToolCompile( self, event ):
		event.Skip()
	
	def OnUpdateToolCompile( self, event ):
		event.Skip()
	

