"""
wbpLoglist
===============================================================================

List view for the history of wx log messages

"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

import wx

from .loglistwin import logListPanel
from .preferences import LogListPreferences, name

if TYPE_CHECKING:
    from wbBase.application import App
    from wbBase.dialog.preferences import PreferencesPageBase
    from wx import aui

__version__ = "0.2.0"


#: Panels provided by the wbpLoglist plugin.
panels: List[Tuple[type[wx.Window], aui.AuiPaneInfo]] = [logListPanel]

#: Preference pages provided by the wbpLoglist plugin.
preferencepages: List[type[PreferencesPageBase]] = [LogListPreferences]


def AddLogToLogChain(app: App) -> None:
    """
    Post init action which adds a new logging target to the log chain
    of the Workbench application.

    :param app: Workbench application
    """
    wx.Log.GetActiveTarget()
    app.logChain = wx.LogChain(app.TopWindow.panelManager.getWindowByCaption(name).log)


def restoreLogLevel(app: App) -> None:
    plugin = None
    for name, module in app.pluginManager.items():
        if hasattr(module, "panels") and module.panels == panels:
            plugin = name
            break
    if plugin:
        cfg = app.config
        with wx.ConfigPathChanger(cfg, f"/Plugin/{plugin}/"):
            wx.Log.SetLogLevel(cfg.ReadInt("loglevel", wx.Log.GetLogLevel()))


wx.GetApp().AddPostInitAction(AddLogToLogChain)
wx.GetApp().AddPostInitAction(restoreLogLevel)
