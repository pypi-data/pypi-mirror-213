"""
control
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import wx
from wx import aui
from wbBase.control import PanelMixin
from wbBase.control.filling import Filling

from .config import NameSpaceConfig, name

if TYPE_CHECKING:
    pass


class NameSpace(Filling, PanelMixin):
    def __init__(
        self,
        parent: wx.Window,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SP_LIVE_UPDATE
        | wx.SP_NOBORDER
        | wx.SP_NO_XP_THEME
        | wx.NO_BORDER,
    ):
        super().__init__(
            parent,
            id,
            pos,
            size,
            style,
            name="NameSpace",
            rootObject=None,
            rootLabel="NameSpace",
            rootIsNamespace=True,
            static=False,
        )
        self.settings = NameSpaceConfig(self)
        self.settings.load()
        tree = self.tree
        tree.SetBackgroundColour(self.settings.backgroundColour.ChangeLightness(130))
        tree.SetForegroundColour(self.settings.foregroundColour)
        self.settings.apply(self.text)

nameSpaceInfo = aui.AuiPaneInfo()
nameSpaceInfo.Name(name)
nameSpaceInfo.Caption(name)
nameSpaceInfo.MaximizeButton(True)
nameSpaceInfo.MinimizeButton(True)
nameSpaceInfo.CloseButton(False)
nameSpaceInfo.Right()
nameSpaceInfo.Dock()
nameSpaceInfo.Hide()
nameSpaceInfo.Resizable()
nameSpaceInfo.MinSize(150, 100)
nameSpaceInfo.BestSize(250, 200)
nameSpaceInfo.Icon(wx.ArtProvider.GetBitmap("NAMESPACE", wx.ART_FRAME_ICON))

nameSpacePanel = (NameSpace, nameSpaceInfo)