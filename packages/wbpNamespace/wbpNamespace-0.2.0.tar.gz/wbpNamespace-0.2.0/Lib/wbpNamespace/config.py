"""
config
===============================================================================
"""
from __future__ import annotations
from typing import TYPE_CHECKING

import wx.stc as stc
from wbBase.control.textEditControl import PyTextEditConfig
from wbBase.dialog.preferences import PreferencesPageBase

if TYPE_CHECKING:
    from .control import NameSpace

name = "Namespace"

class NameSpaceConfig(PyTextEditConfig):
    def __init__(self, parent):
        super().__init__(parent)
        self.ShowLineNumbers = False
        self.WrapMode = stc.STC_WRAP_WORD

    def appendProperties(self, page):
        """
        Append properties to PreferencesPage
        """
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


class NameSpacePreferences(PreferencesPageBase):
    """
    Additional page for the preferences dialog of the
    Workbench application.
    """
    def __init__(self, parent):
        PreferencesPageBase.__init__(self, parent)
        self.settings = NameSpaceConfig(self)
        self.settings.appendProperties(self)

        self.name = name

    def applyValues(self):
        """
        Apply configuration to the namespace panel.
        """
        win:NameSpace = self.app.TopWindow.panelManager.getWindowByCaption(self.name)
        if win:
            self.settings.getPropertyValues(self)
            tree = win.tree
            tree.SetBackgroundColour(self.settings.backgroundColour.ChangeLightness(130))
            tree.SetForegroundColour(self.settings.foregroundColour)
            self.settings.apply(win.text)

    def saveValues(self):
        self.applyValues()
        self.settings.save()
