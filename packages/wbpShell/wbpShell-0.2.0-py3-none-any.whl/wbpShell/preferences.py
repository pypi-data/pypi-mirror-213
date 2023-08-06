"""
preferences
===============================================================================

Manage persistent configuration of the shell window.
"""
import wx.stc as stc
from wbBase.control.textEditControl import PyTextEditConfig
from wbBase.dialog.preferences import PreferencesPageBase

name = "Shell"


class ShellEditConfig(PyTextEditConfig):
    def __init__(self, parent):
        super().__init__(parent)
        self.ShowLineNumbers = False
        self.WrapMode = stc.STC_WRAP_WORD

    def appendProperties(self, page):
        """Append properties to PreferencesPage"""
        self.registerPropertyEditors(page)
        self.appendProperties_main(page)
        self.appendProperties_caret(page)
        self.appendProperties_selection(page)
        self.appendProperties_line_warp(page)
        self.appendProperties_syntax_colour(page)


class ShellPreferences(PreferencesPageBase):
    def __init__(self, parent):
        PreferencesPageBase.__init__(self, parent)
        self.settings = ShellEditConfig(self)
        self.settings.appendProperties(self)

    def applyValues(self):
        win = self.app.TopWindow.panelManager.getWindowByCaption(name)
        self.settings.getPropertyValues(self)
        self.settings.apply(win)

    def saveValues(self):
        self.applyValues()
        self.settings.save()
