"""
loglistwin
===============================================================================

Panel to show logging output in a list control
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
import wx
from wx import aui
import wx.lib.mixins.listctrl as listmix

from .preferences import name

if TYPE_CHECKING:
    from wbBase.application import App


class ListLog(wx.Log):
    """
    Log target to show logging info in a list control.
    """

    def __init__(self, listWindow: LogListWindow) -> None:
        """
        :param listWindow: The list control which shows the logging info
        """
        super().__init__()
        self.listWindow = listWindow

    def DoLogRecord(self, level: int, msg: str, info: wx.LogRecordInfo) -> None:
        """
        Called to log a new record.

        :param level: Log level
        :param msg: Logging message
        :param info: Information about a log record
        """
        self.listWindow.addEntry(level, msg, info.timestamp)


class LogListWindow(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """
    Implementation of the list control which shows the logging records
    """

    logLevel = {
        wx.LOG_FatalError: "FatalError",
        wx.LOG_Error: "Error     ",
        wx.LOG_Warning: "Warning   ",
        wx.LOG_Message: "Message   ",
        wx.LOG_Status: "Status    ",
        wx.LOG_Info: "Info      ",
        wx.LOG_Debug: "Debug     ",
    }

    def __init__(
        self,
        parent: wx.Window,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
    ) -> None:
        style = wx.LC_NO_HEADER | wx.LC_REPORT | wx.LC_SINGLE_SEL
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

        # setup ListCtrl
        self.InsertColumn(0, "Message")
        self.setResizeColumn(1)
        self.imageList = wx.ImageList(16, 16)
        for art in (wx.ART_ERROR, wx.ART_WARNING, wx.ART_INFORMATION, wx.ART_TIP):
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER, (16, 16)))
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)

        # build PopupMenu
        self.menu = wx.Menu()
        clearItem = wx.MenuItem(
            self.menu, wx.ID_ANY, "Clear", "Clear Log", wx.ITEM_NORMAL
        )
        clearItem.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
        )
        self.menu.Append(clearItem)
        saveItem = wx.MenuItem(
            self.menu, wx.ID_ANY, "Save ...", "Save Log to file", wx.ITEM_NORMAL
        )
        saveItem.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_MENU, (16, 16))
        )
        self.menu.Append(saveItem)

        # Bind Events
        self.Bind(wx.EVT_MENU, self.on_Clear, clearItem)
        self.Bind(wx.EVT_MENU, self.on_Save, saveItem)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_RIGHT_CLICK, self)
        self.log = ListLog(self)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} of "{self.app.AppName}">'

    @property
    def app(self) -> App:
        return wx.GetApp()

    def addEntry(self, level:int, msg:str, timeStamp:float) -> None:
        """
        Add an entry to the ListCtrl.

        :param level: Log level
        :param msg: Logging message
        :param timeStamp: Logging time
        """
        time = datetime.fromtimestamp(timeStamp).strftime("%Y.%m.%d-%H:%M:%S")
        message = f"{self.logLevel[level]} {time} - {msg}"
        itemCount = self.ItemCount
        if level in (wx.LOG_FatalError, wx.LOG_Error):
            i = self.InsertItem(itemCount, message, 0)
        elif level == wx.LOG_Warning:
            i = self.InsertItem(itemCount, message, 1)
        elif level in (wx.LOG_Message, wx.LOG_Status, wx.LOG_Info):
            i = self.InsertItem(itemCount, message, 2)
            if level == wx.LOG_Status:
                self.app.TopWindow.SetStatusText(msg, 0)
        else:
            i = self.InsertItem(itemCount, message, 3)
        self.EnsureVisible(i)

    def on_RIGHT_CLICK(self, event:wx.MouseEvent) -> None:
        """Show the context menu."""
        self.PopupMenu(self.menu, wx.DefaultPosition)

    def on_Clear(self, event:wx.MenuEvent) -> None:
        """Clear the content of the LogList window."""
        self.DeleteAllItems()

    def on_Save(self, event:wx.MenuEvent) -> None:
        """Save the content of the LogList window to file."""
        sp:wx.StandardPaths = self.app.Traits.GetStandardPaths()
        fileName = wx.FileSelector(
            "Save Log to file",
            sp.AppDocumentsDir,
            "%s_log" % self.app.AppName,
            "txt",
            "Text file (*.txt)|*.txt|Any file (*.*)|*.*",
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            self,
        )
        if fileName:
            self.saveLog(fileName)

    def saveLog(self, fileName:str) -> None:
        with open(fileName, "w") as logFile:
            logFile.write("LEVEL      TIMESTAMP             MESSAGE\n")
            for i in range(self.ItemCount):
                logFile.write(self.GetItem(i, 0).Text.strip() + "\n")


logListInfo = aui.AuiPaneInfo()
logListInfo.Name(name)
logListInfo.Caption(name)
logListInfo.Dock()
logListInfo.Bottom()
logListInfo.Resizable()
logListInfo.Hide()
logListInfo.MaximizeButton(True)
logListInfo.MinimizeButton(True)
logListInfo.CloseButton(False)
logListInfo.MinSize(150, 100)
logListInfo.BestSize(250, 200)
logListInfo.Icon(wx.ArtProvider.GetBitmap("LOG", wx.ART_FRAME_ICON))


logListPanel = (LogListWindow, logListInfo)