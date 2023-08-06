import wx
from wx import aui

from .dirtreewindow import DirTreeWindow

__version__ = "0.2.1"

name = "FileBrowser"

info = aui.AuiPaneInfo()
info.Name(name)
info.Caption(name)
info.Dock()
info.Bottom()
info.Resizable()
info.MaximizeButton(True)
info.MinimizeButton(True)
info.CloseButton(False)
info.FloatingSize(wx.Size(300, 400))
info.BestSize(wx.Size(300, 400))
info.MinSize(wx.Size(100, 200))
info.Icon(wx.ArtProvider.GetBitmap("FILE_BROWSER", wx.ART_FRAME_ICON))

panels = [(DirTreeWindow, info)]
