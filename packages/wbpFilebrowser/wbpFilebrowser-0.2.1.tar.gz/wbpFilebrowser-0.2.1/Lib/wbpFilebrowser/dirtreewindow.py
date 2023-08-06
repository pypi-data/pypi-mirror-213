"""
dirtreewindow
===============================================================================

"""
from __future__ import annotations

from typing import Dict, List
import os
import wx

from wbBase.document import DOC_SILENT
from wbBase.control import PanelMixin

fileFilter: List[str] = [
    "All files (*.*)|*.*",
    "Fonts|*.otf;*.ttf;*.woff;*.woff2;",
    "Python files (*.py)|*.py",
]

filterString: str = "|".join(fileFilter)


class DirTreeWindow(wx.Panel, PanelMixin):
    def __init__(
        self,
        parent: wx.Window,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.TAB_TRAVERSAL | wx.NO_BORDER,
        name: str = "Filebrowser",
    ):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        s = wx.DIRCTRL_SHOW_FILTERS | wx.NO_BORDER
        f = "All files (*.*)|*.*|Python files (*.py)|*.py"
        d = 0
        sizerMain = wx.BoxSizer(wx.VERTICAL)

        # Bookmark choice
        sizerBookmark = wx.BoxSizer(wx.HORIZONTAL)
        self.label_Bookmark = wx.StaticText(
            self, wx.ID_ANY, "Bookmark", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.label_Bookmark.Wrap(-1)
        sizerBookmark.Add(self.label_Bookmark, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.BookmarkChoices: Dict[str, str] = self.loadBookmarks()
        self.choice_Bookmark = wx.Choice(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            sorted(self.BookmarkChoices.keys()),
            0,
        )
        self.choice_Bookmark.SetSelection(wx.NOT_FOUND)
        sizerBookmark.Add(
            self.choice_Bookmark, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5
        )
        sizerMain.Add(sizerBookmark, 0, wx.EXPAND, 0)

        # DirCtrl
        self.DirCtrl = wx.GenericDirCtrl(
            self, -1, style=s, filter=filterString, defaultFilter=d
        )
        self.DirCtrl.TreeCtrl.SetWindowStyle(
            wx.TR_FULL_ROW_HIGHLIGHT
            | wx.TR_HAS_BUTTONS
            | wx.TR_LINES_AT_ROOT
            | wx.TR_NO_LINES
            | wx.TR_SINGLE
            | wx.TR_TWIST_BUTTONS
            | wx.NO_BORDER
        )
        self.DirCtrl.ShowHidden(False)
        sizerMain.Add(self.DirCtrl, 1, wx.EXPAND, 0)

        self.SetSizer(sizerMain)
        self.Layout()

        # build PopupMenu
        self.menu = wx.Menu()
        addBookmark = wx.MenuItem(
            self.menu,
            wx.ID_ANY,
            "Bookmark folder ...",
            "Add current folder as bookmark",
            wx.ITEM_NORMAL,
        )
        addBookmark.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_MENU, wx.Size(16, 16))
        )
        self.menu.Append(addBookmark)
        delBookmark = wx.MenuItem(
            self.menu,
            wx.ID_ANY,
            "Delete Bookmarks ...",
            "Remove bookmarks",
            wx.ITEM_NORMAL,
        )
        delBookmark.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK, wx.ART_MENU, wx.Size(16, 16))
        )
        self.menu.Append(delBookmark)

        # Connect Events
        self.choice_Bookmark.Bind(wx.EVT_CHOICE, self.on_BOOKMARK_CHOICE)
        self.DirCtrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_TREE_ITEM_ACTIVATED)
        self.DirCtrl.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_TREE_ITEM_RIGHT_CLICK)
        self.Bind(wx.EVT_MENU, self.on_ADD_BOOKMARK, addBookmark)
        self.Bind(wx.EVT_MENU, self.on_DELETE_BOOKMARK, delBookmark)

    def loadBookmarks(self) -> Dict[str, str]:
        """
        Load saved bookmarks from application config.

        :return: key: Bookmark name, value: path to bookmarked item
        """
        result = {}
        cfg = self.config
        if isinstance(cfg, wx.ConfigBase) and cfg.HasGroup("bookmarks"):
            cfg.SetPath("bookmarks")
            more, name, index = cfg.FirstEntry
            while more:
                result[name] = cfg.Read(name)
                more, name, index = cfg.GetNextEntry(index)
        return result

    def saveBookmarks(self) -> None:
        """
        Save bookmarks to application config.
        """
        cfg = self.config
        if isinstance(cfg, wx.ConfigBase):
            if cfg.HasGroup("bookmarks"):
                cfg.DeleteGroup("bookmarks")
            for name in sorted(self.BookmarkChoices.keys()):
                cfg.Write(f"bookmarks/{name}", self.BookmarkChoices[name])
            cfg.Flush()

    def on_BOOKMARK_CHOICE(self, event: wx.CommandEvent) -> None:
        path = self.BookmarkChoices[event.String]
        self.DirCtrl.SetPath(path)

    def on_TREE_ITEM_ACTIVATED(self, event: wx.TreeEvent) -> None:
        path = self.DirCtrl.GetFilePath()
        if os.path.isfile(path):
            self.app.documentManager.CreateDocument(path, DOC_SILENT)
        event.Skip()

    def on_TREE_ITEM_RIGHT_CLICK(self, event: wx.TreeEvent) -> None:
        """Show the context menu"""
        self.PopupMenu(self.menu, wx.DefaultPosition)

    def on_ADD_BOOKMARK(self, event: wx.MenuEvent) -> None:
        path = self.DirCtrl.GetPath()
        if os.path.isfile(path):
            path = os.path.dirname(path)
        print(path)
        if path not in self.BookmarkChoices.values():
            message = f'Enter name for bookmark to path\n"{path}"'
            caption = "New Bookmark"
            default_value = os.path.basename(path)
            name = wx.GetTextFromUser(message, caption, default_value, self)
            if name:
                self.BookmarkChoices[name] = path
            self.choice_Bookmark.Set(sorted(self.BookmarkChoices.keys()))
            self.choice_Bookmark.Selection = self.choice_Bookmark.FindString(name)
            self.saveBookmarks()
        else:
            wx.LogMessage("This path is already bookmarked")

    def on_DELETE_BOOKMARK(self, event: wx.MenuEvent) -> None:
        message = "Select bookmarks to delete"
        caption = "Delete Bookmarks"
        choices = sorted(self.BookmarkChoices.keys())
        dialog = wx.MultiChoiceDialog(self, message, caption, choices)
        if dialog.ShowModal() == wx.ID_OK:
            for i in dialog.Selections:
                del self.BookmarkChoices[choices[i]]
            self.choice_Bookmark.Set(sorted(self.BookmarkChoices.keys()))
            self.choice_Bookmark.Selection = wx.NOT_FOUND
            self.saveBookmarks()
        dialog.Destroy()
        event.Skip()
