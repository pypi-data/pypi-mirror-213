"""
preferences
===============================================================================
"""
import wx
import wx.propgrid as pg

from wbBase.dialog.preferences import PreferencesPageBase

name = "LogList"


class LogListPreferences(PreferencesPageBase):
    def __init__(self, parent) -> None:
        PreferencesPageBase.__init__(self, parent)
        logLabels = [
            "FatalError",
            "Error",
            "Warning",
            "Message",
            "Status",
            "Info",
            "Debug",
        ]
        logLevels = [i for i in range(7)]
        loglevel = wx.Log.GetLogLevel()
        if loglevel not in logLevels:
            loglevel = wx.LOG_Info
        self.Append(
            pg.EnumProperty("Logging Level", "loglevel", logLabels, logLevels, loglevel)
        )

    def applyValues(self) -> None:
        """
        Apply configuration to the log list panel.
        """
        values = self.GetPropertyValues()
        wx.Log.SetLogLevel(values["loglevel"])

    def saveValues(self) -> None:
        """
        Save configuration to the config store of the application.
        """
        values = self.GetPropertyValues()
        cfg = self.config
        cfg.WriteInt("loglevel", values["loglevel"])
