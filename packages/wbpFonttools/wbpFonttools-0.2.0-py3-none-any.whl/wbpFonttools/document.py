"""
document
===============================================================================

Implementation of the document part of the doc/view framework 
used by the wbpFonttools plugin.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO, Optional, Union

import wx
from fontTools.misc import sstruct
from fontTools.ttLib import TTFont as TTFontBase
from fontTools.ttLib import TTLibError
from fontTools.ttLib.sfnt import ttcHeaderFormat, ttcHeaderSize
from wbBase.document import Document, dbg

from .control import getFontNumber

if TYPE_CHECKING:
    from wbBase.document.template import DocumentTemplate

    from .template import FontToolsTemplate

TYPENAME = "FontTools Font"


class TTFont(TTFontBase):
    def __init__(
        self,
        document: FontToolsDocument,
        file: Optional[Union[str, BinaryIO]] = None,
        res_name_or_index=None,
        sfntVersion: str = "\x00\x01\x00\x00",
        flavor: Optional[str] = None,
        checkChecksums: int = 0,
        verbose=None,
        recalcBBoxes: bool = True,
        allowVID:bool=False,
        ignoreDecompileErrors: bool = False,
        recalcTimestamp: bool = False,
        fontNumber: int = -1,
        quiet=None,
        _tableCache=None,
    ):
        lazy = False
        TTFontBase.__init__(
            self,
            file,
            res_name_or_index,
            sfntVersion,
            flavor,
            checkChecksums,
            verbose,
            recalcBBoxes,
            allowVID,
            ignoreDecompileErrors,
            recalcTimestamp,
            fontNumber,
            lazy,
            quiet,
            _tableCache,
        )
        self.document: Document = document
        self._modifiedTables = set()

    def __repr__(self):
        return f'<TTFont object: "{self.document.printableName}">'

    def save(self, file, reorderTables=True):
        TTFontBase.save(self, file, reorderTables)
        self._modifiedTables = set()

    def updateUI(self, table:Optional[str]=None):
        if hasattr(self, "document"):
            if table:
                self.document.UpdateAllViews(self.document, ("modify", table))
            else:
                self.document.UpdateAllViews(self.document, ("refresh",))


class FontToolsDocument(Document):
    binaryData = True
    canReload = True

    def __init__(self, template: FontToolsTemplate):
        super().__init__(template)
        self.font: Optional[TTFont] = None

    def LoadObject(self, fileObject: BinaryIO) -> bool:
        dbg(f"FontToolsDocument.LoadObject({fileObject})", indent=1)
        # check for TrueType Collections
        sfntVersion = fileObject.read(4)
        fileObject.seek(0)
        if sfntVersion == b"ttcf":
            ttcHeaderData = fileObject.read(ttcHeaderSize)
            fileObject.seek(0)
            if len(ttcHeaderData) != ttcHeaderSize:
                wx.LogError("Not a Font Collection (not enough data)")
                return False
            ttcHeader = sstruct.unpack(ttcHeaderFormat, ttcHeaderData)
            numFonts = ttcHeader["numFonts"]
            fontNumber = getFontNumber(numFonts)
        else:
            fontNumber = -1
        self.font = TTFont(self, fileObject, fontNumber=fontNumber)
        self.font.getGlyphOrder()
        self.font.disassembleInstructions = True
        self.UpdateAllViews(self, ["load"])

        dbg("FontToolsDocument.LoadObject() -> done", indent=0)
        return True

    def SaveObject(self, fileObject: BinaryIO) -> bool:
        if isinstance(self.font, TTFont):
            self.font.save(fileObject)
            dbg("FontToolsDocument.SaveObject() -> done")
            return True
        return False
