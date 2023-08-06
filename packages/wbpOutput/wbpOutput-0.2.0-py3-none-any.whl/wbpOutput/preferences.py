"""
preferences
===============================================================================

Manage persistent configuration of the output window.
"""
import wx
import wx.propgrid as pg

from wbBase.dialog.preferences import PreferencesPageBase

name = "Output"

class OutputWinPreferences(PreferencesPageBase):
    """
    Page for the preferences dialog to configure the output window.
    """
    def __init__(self, parent):
        PreferencesPageBase.__init__(self, parent)
        self.Append(pg.PropertyCategory("Main"))
        cfg = self.config
        if cfg:
            self.Append(
                pg.ColourProperty(
                    "Foreground Colour",
                    "ForegroundColour",
                    wx.Colour(cfg.Read("ForegroundColour", "Black")),
                )
            )
            self.Append(
                pg.ColourProperty(
                    "Background Colour",
                    "BackgroundColour",
                    wx.Colour(cfg.Read("BackgroundColour", "White")),
                )
            )
            self.Append(
                pg.FontProperty(
                    "Font",
                    "Font",
                    wx.Font(
                        cfg.Read("Font", self.app.TopWindow.Font.GetNativeFontInfoDesc())
                    ),
                )
            )
            self.Append(
                pg.BoolProperty(
                    "Copy Output to File",
                    "OutputToFile",
                    cfg.ReadBool("OutputToFile", False)
                )
            )
        self.SetPropertyAttributeAll("UseCheckbox", True)

    def applyValues(self):
        pane = self.app.TopWindow.panelManager.getPaneByCaption(name)
        if pane:
            propValues = self.GetPropertyValues()
            win = pane.window
            win.SetForegroundColour(propValues["ForegroundColour"])
            win.SetBackgroundColour(propValues["BackgroundColour"])
            win.SetFont(propValues["Font"])
            win.outputToFile = propValues["OutputToFile"]
            win.Refresh()

    def saveValues(self):
        self.applyValues()
        propValues = self.GetPropertyValues()
        cfg = self.config
        if cfg:
            for colourType in ("ForegroundColour", "BackgroundColour"):
                cfg.Write(colourType, propValues[colourType].GetAsString(wx.C2S_HTML_SYNTAX))
            cfg.Write("Font", propValues["Font"].GetNativeFontInfoDesc())
            cfg.WriteBool("OutputToFile", propValues["OutputToFile"])
