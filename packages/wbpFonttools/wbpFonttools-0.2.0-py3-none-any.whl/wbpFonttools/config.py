"""
config
===============================================================================

Configuration for the wbpFonttools components.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from wx import stc
from wbBase.control.textEditControl import PyTextEditConfig, XmlTextEditConfig
from wbBase.dialog.preferences import PreferencesPageBase

from .document import TYPENAME
from .window import FontToolsWindow
from .template import FontToolsTemplate

if TYPE_CHECKING:
    from wbBase.document.template import DocumentTemplate
    # from .template import FontToolsTemplate

class ObjectViewConfig(PyTextEditConfig):
    def __init__(self):
        PyTextEditConfig.__init__(self)
        self.ShowLineNumbers = False
        self.WrapMode = stc.STC_WRAP_WORD

    def appendProperties(self, page):
        """Append properties to PreferencesPage"""
        self.registerPropertyEditors(page)
        self.appendProperties_main(page)
        self.appendProperties_caret(page)
        self.appendProperties_selection(page)
        # self.appendProperties_indentation(page)
        # self.appendProperties_line_ending(page)
        self.appendProperties_line_warp(page)
        # self.appendProperties_line_numbers(page)
        # self.appendProperties_code_folding(page)
        self.appendProperties_syntax_colour(page)


class XmlViewConfig(XmlTextEditConfig):
    def __init__(self):
        XmlTextEditConfig.__init__(self)
        self.ShowLineNumbers = False
        self.WrapMode = stc.STC_WRAP_WORD

    def appendProperties(self, page):
        """Append properties to PreferencesPage"""
        self.registerPropertyEditors(page)
        self.appendProperties_main(page)
        self.appendProperties_caret(page)
        self.appendProperties_selection(page)
        # self.appendProperties_indentation(page)
        # self.appendProperties_line_ending(page)
        self.appendProperties_line_warp(page)
        # self.appendProperties_line_numbers(page)
        # self.appendProperties_code_folding(page)
        self.appendProperties_syntax_colour(page)


class FonttoolsPreferencesBase(PreferencesPageBase):
    @property
    def template(self) -> Optional[DocumentTemplate]:
        return self.documentManager.FindTemplateByDocumentTypeName(TYPENAME)


class FonttoolsPreferences(FonttoolsPreferencesBase):
    name = TYPENAME

    def __init__(self, parent):
        FonttoolsPreferencesBase.__init__(self, parent)


class ObjectViewPreferences(FonttoolsPreferencesBase):
    name = "ObjectView"

    def __init__(self, parent):
        FonttoolsPreferencesBase.__init__(self, parent)
        template = self.template
        if isinstance(template, FontToolsTemplate):
            template.objectViewConfig.appendProperties(self)

    @property
    def config(self) -> Optional[PyTextEditConfig]:
        template = self.template
        if isinstance(template, FontToolsTemplate):
            return template.objectViewConfig

    def applyValues(self):
        cfg = self.config
        if isinstance(cfg, PyTextEditConfig):
            cfg.getPropertyValues(self)
            for doc in self.documentManager.documents:
                if doc.typeName == TYPENAME:
                    for view in doc.views:
                        if isinstance(view.frame, FontToolsWindow):
                            cfg.apply(view.frame.filling.text)

    def saveValues(self):
        cfg = self.config
        if isinstance(cfg, PyTextEditConfig):
            cfg.getPropertyValues(self)
            cfg.save()

    def OnChanged(self, event):
        if event.PropertyName in ("font", "background"):
            for p in self.Properties:
                self.RefreshProperty(p)
        event.Skip()


class XmlViewPreferences(FonttoolsPreferencesBase):
    name = "XmlView"

    def __init__(self, parent):
        FonttoolsPreferencesBase.__init__(self, parent)
        cfg = self.config
        if cfg is not None:
            cfg.appendProperties(self)

    @property
    def config(self):
        template = self.template
        if isinstance(template, FontToolsTemplate):
            return template.xlmEditorConfig

    def applyValues(self):
        cfg = self.config
        if cfg is not None:
            cfg.getPropertyValues(self)
            for doc in self.documentManager.documents:
                if doc.typeName == TYPENAME:
                    for view in doc.views:
                        if isinstance(view.frame, FontToolsWindow):
                            cfg.apply(view.frame.textEditor)

    def saveValues(self):
        cfg = self.config
        if cfg is not None:
            cfg.getPropertyValues(self)
            cfg.save()

    def OnChanged(self, event):
        if event.PropertyName in ("font", "background"):
            for p in self.Properties:
                self.RefreshProperty(p)
        event.Skip()
