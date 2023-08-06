from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional

import wx

from .config import FonttoolsPreferences, ObjectViewPreferences, XmlViewPreferences
from .dialog import SelectFontsDialog
from .document import FontToolsDocument, TTFont
from .template import (
    OpenType_OTF_Template,
    OpenType_TTC_Template,
    OpenType_TTF_Template,
    WebFont_WOFF_2_Template,
    WebFont_WOFF_Template,
)

if TYPE_CHECKING:
    from wbBase.application import App

__version__ = "0.2.0"


def CurrentFont() -> Optional[TTFont]:
    """
    Get the currently active font
    """
    app: App = wx.GetApp()
    doc = app.TopWindow.documentManager.currentDocument
    if isinstance(doc, FontToolsDocument):
        return doc.font


def AllFonts() -> Iterable[TTFont]:
    """
    Get all currently open fonts
    """
    app: App = wx.GetApp()
    for doc in app.TopWindow.documentManager.documents:
        if isinstance(doc, FontToolsDocument) and isinstance(doc.font, TTFont):
            yield doc.font


def SelectFonts(message: str = "Select fonts") -> List[TTFont]:
    """
    Show the :class:`~.dialog.SelectFontsDialog` and return the selected fonts.
    """
    fonts = []
    with SelectFontsDialog(message) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            fonts = dlg.selectedFonts
    return fonts


doctemplates = (
    OpenType_OTF_Template,
    OpenType_TTC_Template,
    OpenType_TTF_Template,
    WebFont_WOFF_2_Template,
    WebFont_WOFF_Template,
)

preferencepages = (FonttoolsPreferences, XmlViewPreferences, ObjectViewPreferences)

globalObjects = ("CurrentFont", "AllFonts", "SelectFonts")
