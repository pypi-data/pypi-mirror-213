"""
window
===============================================================================

Implementation of the window for the view part of the doc/view framework 
used by the wbpFonttools plugin.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from io import StringIO
import traceback

from fontTools.ttLib import tagToXML
from fontTools.misc.xmlWriter import XMLWriter

import wx
import wx.stc as stc

from wbBase.document.notebook import DocumentPageMixin
from wbBase.control.textEditControl import TextEditCtrl, MARGIN_NUMBERS, MARGIN_SYMBOLS

from .control import FontTableListCrtl, FontObjectView
from .tools import TtxTableParser

if TYPE_CHECKING:
    from wbBase.application import App
    from .view import FontToolsView
    from .document import FontToolsDocument, TTFont


class FontToolsWindow(wx.Panel, DocumentPageMixin):
    def __init__(self, parent:wx.Window, doc: FontToolsDocument, view: FontToolsView):
        """
        Main window to view and edit fontTools font objects
        """
        # Args:
        #     parent : Parent window
        #     doc (:class:`~.document.FontToolsDocument`) : document which represents the font
        #     view (:class:~.view.FontToolsView) : view which shows the font

        # Attributes:
        #     tableList (:class:`~.control.FontTableListCrtl`):
        #             List of font table tags

        #     toolbar ( wx.ToolBar): The toolbar
        #     filling (:class:`~workbench.control.filling.Filling`): The table object inspector
        #     textEditor (StyledTextCtrl): Editor for XML representation of the current table
        # """
        wx.Panel.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.FULL_REPAINT_ON_RESIZE | wx.NO_BORDER | wx.TAB_TRAVERSAL,
            name="FontToolsWindow",
        )
        DocumentPageMixin.__init__(self, doc, view)
        self.document: FontToolsDocument
        self.view: FontToolsView
        mainSizer = wx.FlexGridSizer(2, 2, 0, 0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(1)
        mainSizer.SetFlexibleDirection(wx.BOTH)
        mainSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.listHeader = wx.ToolBar(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT
        )
        self.listHeader.SetToolBitmapSize(wx.Size(16, 16))
        self.listHeader.SetMargins(wx.Size(5, 5))
        self.listHeader.SetToolPacking(5)
        self.listHeader_label = wx.StaticText(
            self.listHeader,
            wx.ID_ANY,
            "   Table",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTRE,
        )
        self.listHeader_label.Wrap(-1)
        self.listHeader.AddControl(self.listHeader_label)
        self.listHeader.Realize()
        mainSizer.Add(self.listHeader, 0, wx.EXPAND, 0)

        # Add the toolbar
        self.toolbar = wx.ToolBar(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT
        )
        self.toolbar.SetToolBitmapSize(wx.Size(16, 16))
        self.toolbar.SetMargins(wx.Size(5, 5))
        self.toolbar.SetToolPacking(5)
        bitmap = lambda icon: wx.ArtProvider.GetBitmap(icon, wx.ART_TOOLBAR)
        self.toolXML = self.toolbar.AddTool(
            wx.ID_ANY,
            "XML",
            bitmap("HTML_FILE"),
            wx.NullBitmap,
            wx.ITEM_RADIO,
            "View table in XML viewer",
            "View table in XML viewer",
            None,
        )
        self.toolNameSpace = self.toolbar.AddTool(
            wx.ID_ANY,
            "NameSpace",
            bitmap("NAMESPACE"),
            wx.NullBitmap,
            wx.ITEM_RADIO,
            "View table in NameSpace viewer",
            "View table in NameSpace viewer",
            None,
        )
        self.toolbar.AddSeparator()
        self.toolReload = self.toolbar.AddTool(
            wx.ID_ANY,
            "Reload table",
            bitmap("RESET"),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Reload TTX table",
            "Reload TTX table",
            None,
        )
        self.toolCompile = self.toolbar.AddTool(
            wx.ID_ANY,
            "Compile XML to TTX table",
            bitmap("COMPILE"),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            "Compile XML to TTX table",
            "Compile XML to TTX table",
            None,
        )
        self.toolbar.Realize()
        mainSizer.Add(self.toolbar, 0, wx.EXPAND, 0)

        # Add the list for all font tables
        self.tableList = FontTableListCrtl(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.LC_NO_HEADER
            | wx.LC_REPORT
            | wx.LC_SINGLE_SEL
            | wx.LC_VIRTUAL
            | wx.NO_BORDER,
        )
        self.tableList.SetMinSize(wx.Size(100, -1))
        mainSizer.Add(self.tableList, 0, wx.EXPAND, 0)

        rightSizer = wx.BoxSizer(wx.VERTICAL)
        # Add the object view
        self.filling = FontObjectView(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.CLIP_CHILDREN | wx.NO_BORDER,
        )
        self.filling.Hide()
        rightSizer.Add(self.filling, 1, wx.EXPAND | wx.LEFT, 1)
        # Add the XML text editor
        self.textEditor = TextEditCtrl(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER
        )
        self.textEditor.SetLexer(stc.STC_LEX_XML)
        self.textEditor.SetProperty("fold", "1")
        self.textEditor.SetProperty("fold.html", "1")
        self.textEditor.SetProperty("lexer.xml.allow.scripts", "0")
        rightSizer.Add(self.textEditor, 1, wx.EXPAND, 0)

        mainSizer.Add(rightSizer, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        self.Layout()
        mainSizer.Fit(self)

        # Connect Events
        self.tableList.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.tableList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnTableSelected)
        self.Bind(wx.EVT_TOOL, self.OnToolXML, id=self.toolXML.GetId())
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateToolXML, id=self.toolXML.GetId())
        self.Bind(wx.EVT_TOOL, self.OnToolNameSpace, id=self.toolNameSpace.GetId())
        self.Bind(
            wx.EVT_UPDATE_UI, self.OnUpdateToolNameSpace, id=self.toolNameSpace.GetId()
        )
        self.Bind(wx.EVT_TOOL, self.OnTooReload, id=self.toolReload.GetId())
        self.Bind(wx.EVT_TOOL, self.OnToolCompile, id=self.toolCompile.GetId())
        self.Bind(
            wx.EVT_UPDATE_UI, self.OnUpdateToolCompile, id=self.toolCompile.GetId()
        )

        # ==============
        self.document.template.xlmEditorConfig.apply(self.textEditor)
        self.tableParser = TtxTableParser(self.font)
        self._currentTable = None

    # -----------------------------------------------------------------------------
    # properties
    # -----------------------------------------------------------------------------

    @property
    def app(self) -> App:
        return wx.GetApp()

    @property
    def font(self) -> TTFont:
        return self.document.font

    @property
    def currentTable(self) -> str:
        "TableTag of the currently selected table"
        return self._currentTable

    @currentTable.setter
    def currentTable(self, tableTag:str):
        if tableTag in self.font:
            if self._currentTable != tableTag:
                self._currentTable = tableTag
                self.showTable(self._currentTable)
        else:
            wx.LogError(f'Invalid tableTag: "{tableTag}"')

    # -----------------------------------------------------------------------------
    # public methods
    # -----------------------------------------------------------------------------

    def showTable(self, tableTag:str):
        wx.BeginBusyCursor()
        wx.LogDebug("FontToolsWindow.showTable(%r)" % tableTag)
        font = self.font

        # put xml in textEditor
        textBuffer = StringIO()
        writer = XMLWriter(textBuffer)
        xmlTag = tagToXML(tableTag)
        writer.begintag(xmlTag)
        writer.newline()
        font[tableTag].toXML(writer, font)
        writer.endtag(xmlTag)
        self.textEditor.ReadOnly = False
        self.textEditor.SetText(textBuffer.getvalue())
        self.textEditor.SetSavePoint()
        self.textEditor.ReadOnly = tableTag in ("GlyphOrder", "loca")

        # put table object in filling
        if tableTag == "GlyphOrder":
            table = font.glyphOrder
        else:
            table = font[tableTag]
        tree = self.filling.tree
        tree.DeleteAllItems()
        tree.rootIsNamespace = False
        tree.item = tree.root = tree.AddRoot(f"font['{tableTag}']", -1, -1, table)
        tree.SetItemHasChildren(tree.root, tree.objHasChildren(table))
        tree.SelectItem(tree.root)
        if tableTag != "GlyphOrder":
            tree.Expand(tree.root)
        tree.display()

        # update table list control
        self.tableList.Refresh()
        self.Layout()

        wx.EndBusyCursor()

    def compileTable(self, tableTag:str) -> bool:
        font = self.font
        self.tableParser.font = font
        tableSave = font[tableTag]
        try:
            self.tableParser.parse(self.textEditor.TextRaw, tableTag)
            table = font[tableTag]
            table.decompile(table.compile(font), font)
            return True
        except:
            traceback.print_exc()  # for debugging purposes
            wx.LogError(
                "Compiling of table %s failed!\n%s\nSee full traceback in Output panel"
                % (self.currentTable, traceback.format_exc().splitlines()[-1])
            )
            font[tableTag] = tableSave
            return False

    def _canDiscardChanges(self) -> bool:
        if self.textEditor.IsShown() and self.textEditor.Modify:
            answer = wx.MessageBox(
                "You have uncompiled chages in the current XML view, \nif you continue your changes will be lost",
                self.app.AppName,
                wx.ICON_QUESTION | wx.OK | wx.CANCEL,
            )
            if answer == wx.CANCEL:
                return False
        return True

    # -----------------------------------------------------------------------------
    # Event handler
    # -----------------------------------------------------------------------------

    def OnLeftDown(self, event):
        event.Skip()

    def OnTableSelected(self, event):
        tableTag = self.font.keys()[event.Index]
        wx.LogDebug(
            "FontToolsWindow.OnTableSelected() %s -> %s" % (self.currentTable, tableTag)
        )
        if tableTag != self.currentTable:
            self.currentTable = tableTag

    def OnToolXML(self, event):
        self.filling.Show(False)
        self.textEditor.Show(True)
        self.SendSizeEvent()

    def OnUpdateToolXML(self, event):
        event.Skip()

    def OnToolNameSpace(self, event):
        if self._canDiscardChanges():
            self.showTable(self.currentTable)
            self.filling.Show(True)
            self.textEditor.Show(False)
            self.SendSizeEvent()
        else:
            self.toolbar.ToggleTool(self.toolXML.Id, True)
        event.Skip()

    def OnUpdateToolNameSpace(self, event):
        event.Skip()

    def OnTooReload(self, event):
        if self._canDiscardChanges():
            self.showTable(self.currentTable)
        else:
            event.Veto()

    def OnToolCompile(self, event):
        with wx.BusyCursor():
            if self.compileTable(self.currentTable):
                self.font._modifiedTables.add(self.currentTable)
                self.document.modified = True
                self.showTable(self.currentTable)

    def OnUpdateToolCompile(self, event:wx.UpdateUIEvent):
        event.Enable(self.textEditor.IsShown() and self.textEditor.Modify)
