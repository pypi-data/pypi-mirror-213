"""
template
===============================================================================

Implementation of the template part of the doc/view framework 
used by the wbpFonttools plugin.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import wx
from wbBase.control.textEditControl import PyTextEditConfig, XmlTextEditConfig
from wbBase.document.template import (
    DEFAULT_TEMPLATE_FLAGS,
    TEMPLATE_NO_CREATE,
    DocumentTemplate,
)

from .document import TYPENAME, FontToolsDocument
from .view import FontToolsView

if TYPE_CHECKING:
    from wbBase.document.manager import DocumentManager


class FontToolsTemplate(DocumentTemplate):
    """
    Base template for all font formats.
    """
    def __init__(
        self,
        manager: DocumentManager,
        description: str,
        filter: str,
        dir: str,
        ext: str,
    ):
        docTypeName = TYPENAME
        viewTypeName = "FontTools Editor"
        docType = FontToolsDocument
        viewType = FontToolsView
        flags = DEFAULT_TEMPLATE_FLAGS | TEMPLATE_NO_CREATE
        icon = wx.ArtProvider.GetBitmap("FONTTOOLS", wx.ART_FRAME_ICON)
        DocumentTemplate.__init__(
            self,
            manager,
            description,
            filter,
            dir,
            ext,
            docTypeName,
            viewTypeName,
            docType,
            viewType,
            flags,
            icon,
        )
        self.objectViewConfig = PyTextEditConfig(self)
        self.xlmEditorConfig = XmlTextEditConfig(self)
        self.loadConfig()

    def loadConfig(self):
        self.objectViewConfig.load()
        self.xlmEditorConfig.load()


class OpenType_TTF_Template(FontToolsTemplate):
    "OpenType-TTF Font"
    def __init__(self, manager: DocumentManager):
        description = "OpenType-TTF Font"
        filter = "*.ttf"
        dir = ""
        ext = ".ttf"
        FontToolsTemplate.__init__(self, manager, description, filter, dir, ext)


class OpenType_OTF_Template(FontToolsTemplate):
    "OpenType-OTF Font"
    def __init__(self, manager: DocumentManager):
        description = "OpenType-OTF Font"
        filter = "*.otf"
        dir = ""
        ext = ".otf"
        FontToolsTemplate.__init__(self, manager, description, filter, dir, ext)


class WebFont_WOFF_Template(FontToolsTemplate):
    "OpenType-WOFF WebFont"
    def __init__(self, manager: DocumentManager):
        description = "OpenType-WOFF WebFont"
        filter = "*.woff"
        dir = ""
        ext = ".woff"
        FontToolsTemplate.__init__(self, manager, description, filter, dir, ext)


class WebFont_WOFF_2_Template(FontToolsTemplate):
    "OpenType-WOFF-2 WebFont"
    def __init__(self, manager: DocumentManager):
        description = "OpenType-WOFF-2 WebFont"
        filter = "*.woff2"
        dir = ""
        ext = ".woff2"
        FontToolsTemplate.__init__(self, manager, description, filter, dir, ext)


class OpenType_TTC_Template(FontToolsTemplate):
    "OpenType-TTC Collection"
    def __init__(self, manager: DocumentManager):
        description = "OpenType-TTC Collection"
        filter = "*.ttc"
        dir = ""
        ext = ".ttc"
        FontToolsTemplate.__init__(self, manager, description, filter, dir, ext)
