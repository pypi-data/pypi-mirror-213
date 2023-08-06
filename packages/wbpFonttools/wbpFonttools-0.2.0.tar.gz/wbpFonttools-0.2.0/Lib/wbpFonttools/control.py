"""
control
===============================================================================

Controls used by wbpFonttools components.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import wx
from wbBase.control.filling import Filling
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

if TYPE_CHECKING:
    from wbBase.application import App
    from wbBase.control.textEditControl import PyTextEditConfig

    from .document import TTFont
    from .window import FontToolsWindow


class FontTableListCrtl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    """
    List control to show all table tags of a font.
    """

    def __init__(
        self,
        parent: wx.Window,
        id: int = wx.ID_ANY,
        pos=wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VIRTUAL,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = "TTXtableListCrtl",
    ):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)
        ListCtrlAutoWidthMixin.__init__(self)
        self.Parent: FontToolsWindow
        imgSize = 16
        self.imglist = wx.ImageList(imgSize, imgSize)
        self.imgDefault = self.imglist.Add(
            wx.Bitmap.FromRGBA(
                imgSize, imgSize, red=0x00, green=0xFF, blue=0x00, alpha=wx.ALPHA_OPAQUE
            )
        )
        self.imgLoaded = self.imglist.Add(
            wx.Bitmap.FromRGBA(
                imgSize, imgSize, red=0xFF, green=0xFF, blue=0x00, alpha=wx.ALPHA_OPAQUE
            )
        )
        self.imgModified = self.imglist.Add(
            wx.Bitmap.FromRGBA(
                imgSize, imgSize, red=0xFF, green=0x00, blue=0x00, alpha=wx.ALPHA_OPAQUE
            )
        )
        self.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)

        self.InsertColumn(0, "Table")
        self.SetItemCount(0)

    @property
    def font(self) -> TTFont:
        return self.Parent.document.font

    def OnGetItemText(self, item: int, col: int) -> str:
        """
        :return: table tag of the specified item
        """
        return self.font.keys()[item]

    def OnGetItemImage(self, item) -> int:
        """
        :return: the index of the items image in the controls image list
        """
        tag = self.font.keys()[item]
        if tag in self.font._modifiedTables:
            return self.imgModified
        if self.font.isLoaded(tag):
            return self.imgLoaded
        else:
            return self.imgDefault


class FontObjectView(Filling):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.SP_LIVE_UPDATE | wx.SP_NOBORDER | wx.SP_NO_XP_THEME | wx.NO_BORDER,
    ):
        super().__init__(
            parent,
            id,
            pos,
            size,
            style,
            name="FontObjectView",
            rootObject=None,
            rootLabel=None,
            rootIsNamespace=True,
            static=False,
        )
        self.Parent: FontToolsWindow

    @property
    def config(self) -> PyTextEditConfig:
        return self.Parent.document.template.objectViewConfig


class FontSelectListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    #                        CheckListCtrlMixin):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.LC_REPORT | wx.LC_VIRTUAL,
        validator=wx.DefaultValidator,
        name="FontSelectListCtrl",
    ):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style, validator, name)
        ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0, "File Name")
        self.InsertColumn(1, "Path")
        self.SetColumnWidth(0, 200)
        self.allFonts = self.getAllFonts()
        self.SetItemCount(len(self.allFonts))

    @property
    def app(self) -> App:
        return wx.GetApp()

    def getAllFonts(self):
        from .template import FontToolsTemplate

        allFonts = []
        for doc in self.app.TopWindow.documentManager.documents:
            if isinstance(doc.template, FontToolsTemplate):
                allFonts.append(doc)
        allFonts.sort(key=lambda f: f.path)
        return allFonts

    def getSelectedFonts(self):
        fonts = []
        for i in range(self.ItemCount):
            if self.GetItemState(i, wx.LIST_STATE_SELECTED):
                fonts.append(self.allFonts[i].font)
        return fonts

    def OnGetItemText(self, item, col):
        if col == 0:
            return self.allFonts[item].printableName
        elif col == 1:
            return self.allFonts[item].path


class DlgFontNumber(wx.Dialog):
    def __init__(self, numFonts):
        parent = wx.GetApp().TopWindow
        id = wx.ID_ANY
        title = "Open TrueType Collection"
        pos = wx.DefaultPosition
        size = wx.DefaultSize
        style = wx.CAPTION | wx.RESIZE_BORDER
        message = (
            f"This Font Collection contains {numFonts} fonts.\n"
            + "Please specify the font you want to open.\n"
            + f"Enter a font number between 0 and {numFonts - 1} (inclusive)."
        )
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.lbl_Message = wx.StaticText(
            self, wx.ID_ANY, message, wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.lbl_Message.Wrap(-1)
        sizer.Add(self.lbl_Message, 0, wx.ALL | wx.EXPAND, 5)
        self.spinCtrl_fontNumber = wx.SpinCtrl(
            self,
            wx.ID_ANY,
            "0",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SP_ARROW_KEYS | wx.SP_WRAP,
            0,
            numFonts - 1,
            0,
        )
        sizer.Add(self.spinCtrl_fontNumber, 0, wx.ALL, 5)
        sizer.Add((0, 0), 1, wx.EXPAND, 5)
        sdbSizer = wx.StdDialogButtonSizer()
        self.sdbSizerOK = wx.Button(self, wx.ID_OK)
        sdbSizer.AddButton(self.sdbSizerOK)
        # self.sdbSizerCancel = wx.Button(self, wx.ID_CANCEL)
        # sdbSizer.AddButton(self.sdbSizerCancel)
        sdbSizer.Realize()
        sdbSizer.SetMinSize(wx.Size(10, -1))
        sizer.Add(sdbSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)
        self.Centre(wx.BOTH)

    @property
    def fontNumber(self):
        return int(self.spinCtrl_fontNumber.Value)


def getFontNumber(numFonts: int) -> int:
    with DlgFontNumber(numFonts) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.fontNumber
    return -1
