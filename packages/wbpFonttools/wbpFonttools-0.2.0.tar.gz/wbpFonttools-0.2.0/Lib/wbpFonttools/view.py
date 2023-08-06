"""
view
===============================================================================

Implementation of the view part of the doc/view framework 
used by the wbpFonttools plugin.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import wx

from wbBase.document import dbg
from wbBase.document.view import View
from .window import FontToolsWindow

if TYPE_CHECKING:
    from .document import TTFont, FontToolsDocument


class FontToolsView(View):
    frameType = FontToolsWindow

    def __init__(self):
        super().__init__()
        self.frame: FontToolsWindow
        self.document: FontToolsDocument

    @property
    def font(self) -> Optional[TTFont]:
        doc = self.document
        if doc:
            return doc.font

    def OnUpdate(self, sender, hint):
        result = False
        dbg(f"FontToolsView.OnUpdate(sender={sender}, hint={hint})", indent=1)
        font = self.font
        if hint and font:
            self.frame.tableList.SetItemCount(len(font))
            if hint[0] == "load" and sender == self.document:
                dbg("FontToolsView.OnUpdate() table tags into control")
                self.frame._currentTable = None
                selected = self.frame.tableList.GetFirstSelected()
                if selected != wx.NOT_FOUND:
                    self.frame.tableList.Select(selected, 0)
                self.frame.tableList.Select(0)
                self.frame.tableList.Refresh()
                result = True
            elif hint[0] == "modify":
                if len(hint) == 2 and hint[1] in font:
                    font._modifiedTables.add(hint[1])
                    self.document.modified = True
                self.frame.tableList.Refresh()
                self.frame.showTable(self.frame.currentTable)
                result = View.OnUpdate(self, sender, hint)
            elif hint[0] == "refresh":
                self.frame.tableList.Refresh()
                if self.frame.currentTable in font:
                    self.frame.showTable(self.frame.currentTable)
                else:
                    self.frame.showTable("GlyphOrder")
                result = True
            else:
                result = View.OnUpdate(self, sender, hint)
        dbg("FontToolsView.OnUpdate() -> done", indent=0)
        return result
