"""
outputwin
===============================================================================

Implementation of the output panel.
"""
import os
import sys

import wx
from wbBase.control import PanelMixin
from wx import aui

from .preferences import name


class OutputWin(wx.TextCtrl, PanelMixin):
    """
    Text control to display output directed to stdout and stderr.
    """

    def __init__(self, parent) -> None:
        wx.TextCtrl.__init__(
            self,
            parent,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE | wx.NO_BORDER,
        )
        self.outputToFile = False
        self.menu = wx.Menu()
        self._applyConfig()
        self._redirect_stdio()
        self._buildMenu()
        # Bind Events
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_RIGHT_CLICK, self)

    # =========================================================================
    # private methods
    # =========================================================================

    def _applyConfig(self) -> None:
        """
        Load and apply configuration for this window
        """
        cfg = self.config
        if cfg:
            self.SetForegroundColour(
                wx.Colour(
                    cfg.Read(
                        "ForegroundColour",
                        self.ForegroundColour.GetAsString(wx.C2S_HTML_SYNTAX),
                    )
                )
            )
            self.SetBackgroundColour(
                wx.Colour(
                    cfg.Read(
                        "BackgroundColour",
                        self.BackgroundColour.GetAsString(wx.C2S_HTML_SYNTAX),
                    )
                )
            )
            self.SetFont(wx.Font(cfg.Read("Font", self.Font.GetNativeFontInfoDesc())))
            self.outputToFile = cfg.ReadBool("OutputToFile", False)
            self.outputPath = os.path.join(
                cfg.Read("/Application/PrivateData/Dir", self.app.privateDataDir),
                "output.txt",
            )

    def _redirect_stdio(self) -> None:
        """
        Redirect stdout and stderr to this window.
        """
        sys.stdout = self
        sys.stderr = self
        print("Print statements go to this stdout window by default.")

    def _buildMenu(self) -> None:
        """
        Build the context menu for this window.
        """
        clearItem = wx.MenuItem(
            self.menu, wx.ID_ANY, "Clear", "Clear output window", wx.ITEM_NORMAL
        )
        clearItem.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, wx.Size(16, 16))
        )
        self.menu.Append(clearItem)
        self.Bind(wx.EVT_MENU, self.on_Clear, clearItem)

        saveItem = wx.MenuItem(
            self.menu, wx.ID_ANY, "Save ...", "Save output to file", wx.ITEM_NORMAL
        )
        saveItem.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_MENU, wx.Size(16, 16))
        )
        self.menu.Append(saveItem)
        self.Bind(wx.EVT_MENU, self.on_Save, saveItem)

    # =========================================================================
    # public methods
    # =========================================================================

    def write(self, text:str) -> None:
        if self.outputToFile:
            with open(self.outputPath, "a", encoding="utf-8") as outFile:
                outFile.write(text)
        super().write(text)

    def isatty(self):
        return False

    # =========================================================================
    # Event handler
    # =========================================================================

    def on_RIGHT_CLICK(self, event):
        """Show the context menu"""
        self.PopupMenu(self.menu, wx.DefaultPosition)

    def on_Clear(self, event):
        """Clear the content of the Output window"""
        self.Clear()

    def on_Save(self, event):
        """Save the content of the Output window to file"""
        sp = self.app.Traits.GetStandardPaths()
        fileName = wx.FileSelector(
            "Save Output to file",
            sp.AppDocumentsDir,
            "%s_out" % self.app.AppName,
            "txt",
            "Text file (*.txt)|*.txt|Any file (*.*)|*.*",
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            self,
        )
        if fileName:
            self.SaveFile(fileName, wx.TEXT_TYPE_ANY)


outputPaneInfo = aui.AuiPaneInfo()
outputPaneInfo.Name(name)
outputPaneInfo.Caption(name)
outputPaneInfo.Dock()
outputPaneInfo.Bottom()
outputPaneInfo.Resizable()
outputPaneInfo.MaximizeButton(True)
outputPaneInfo.MinimizeButton(True)
outputPaneInfo.CloseButton(False)
outputPaneInfo.FloatingSize(wx.Size(300, 200))
outputPaneInfo.BestSize(wx.Size(800, 400))
outputPaneInfo.MinSize(wx.Size(300, 200))
outputPaneInfo.Icon(wx.ArtProvider.GetBitmap("OUTPUT", wx.ART_FRAME_ICON))

outputPanel = (OutputWin, outputPaneInfo)
