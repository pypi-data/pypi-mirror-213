"""
dialog
===============================================================================

Controls used by the wbpFonttools plugin.
"""
from __future__ import annotations
import wx

from .selectFontsDialogUI import SelectFontsDialogUI


class SelectFontsDialog(SelectFontsDialogUI):
    """
    Dialog to select one or more fonts from the fonts open in the application.
    """

    def __init__(self, message: str = "Select fonts"):
        """
        :param message: Message shown in the dialog, defaults to 'Select fonts'
        """
        app = wx.GetApp()
        SelectFontsDialogUI.__init__(self, app.TopWindow)
        self.label_message.Label = message
        fontList = self.listCtrl_fonts
        currentDoc = app.documentManager.currentDocument
        for i in range(fontList.ItemCount):
            if fontList.allFonts[i] == currentDoc:
                fontList.SetItemState(i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    @property
    def selectedFonts(self):
        return self.listCtrl_fonts.getSelectedFonts()

    def on_KEY_DOWN(self, event):
        unicodeKey = event.GetUnicodeKey()
        if unicodeKey != wx.WXK_NONE:
            key = chr(unicodeKey)
            if key == "A" and (event.ControlDown() or event.CmdDown()):
                fontList = self.listCtrl_fonts
                for i in range(fontList.ItemCount):
                    fontList.SetItemState(
                        i, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED
                    )
        else:
            event.Skip()
