"""
tools
===============================================================================

Tools used by the wbpFonttools plugin.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from xml.parsers.expat import ParserCreate

from fontTools.ttLib import getTableClass
from fontTools.ttLib.tables.DefaultTable import DefaultTable

if TYPE_CHECKING:
    from .document import TTFont


class TtxTableParser(object):
    def __init__(self, font: TTFont):
        self.font = font
        self.table: Optional[DefaultTable] = None
        self.root = None
        self.contentStack = []
        self.stackSize = 0

    def parse(self, tableData, tableTag):
        tableClass = getTableClass(tableTag)
        if tableClass is None:
            tableClass = DefaultTable
        self.table = tableClass(tableTag)
        self.font[tableTag] = self.table
        self.contentStack.append([])
        self.stackSize = 1
        parser = ParserCreate("latin1")
        parser.StartElementHandler = self.startElementHandler
        parser.EndElementHandler = self.endElementHandler
        parser.CharacterDataHandler = self.characterDataHandler
        parser.Parse(tableData, True)

    def startElementHandler(self, name, attrs):
        stackSize = self.stackSize
        self.stackSize = stackSize + 1
        if stackSize == 2:
            self.contentStack.append([])
            self.root = (name, attrs, self.contentStack[-1])
        else:
            list = []
            self.contentStack[-1].append((name, attrs, list))
            self.contentStack.append(list)

    def characterDataHandler(self, data):
        if self.stackSize > 1:
            self.contentStack[-1].append(data)

    def endElementHandler(self, name):
        self.stackSize = self.stackSize - 1
        del self.contentStack[-1]
        if self.stackSize == 1:
            self.root = None
        elif self.stackSize == 2:
            name, attrs, content = self.root
            self.table.fromXML(name, attrs, content, self.font)
            self.root = None
