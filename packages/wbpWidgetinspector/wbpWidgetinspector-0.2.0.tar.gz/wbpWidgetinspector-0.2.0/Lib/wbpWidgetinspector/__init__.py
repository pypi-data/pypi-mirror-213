"""
wbpWidgetinspector
===============================================================================

"""
from __future__ import annotations
from typing import TYPE_CHECKING

import wx
from wx.lib.inspection import InspectionTool

if TYPE_CHECKING:
    from wbBase.application import App

__version__ = "0.2.0"


class WidgetInspector:
    def __init__(self, alt=True, cmd=True, shift=False, keyCode=ord("I")):
        self._alt = alt
        self._cmd = cmd
        self._shift = shift
        self._keyCode = keyCode

    def initInspection(self, app:App) -> None:
        app.Bind(wx.EVT_KEY_DOWN, self._OnKeyPress)
        InspectionTool().Init(wx.DefaultPosition, wx.Size(850, 700), app=app)
        print("Press Ctrl-Alt-I (Cmd-Opt-I on Mac) to launch the WidgetInspector.")

    def _OnKeyPress(self, event:wx.KeyEvent) -> None:
        """
        Event handler, check for our hot-key. 
        Normally it is Ctrl-Alt-I but that can be changed 
        by what is passed to the Init method.
        """
        if (
            event.AltDown() == self._alt
            and event.CmdDown() == self._cmd
            and event.ShiftDown() == self._shift
            and event.GetKeyCode() == self._keyCode
        ):
            self.ShowInspectionTool()
        else:
            event.Skip()

    def ShowInspectionTool(self) -> None:
        """
        Show the Inspection tool, creating it if neccesary, 
        setting it to display the widget under the cursor.
        """
        # get the current widget under the mouse
        wnd, __ = wx.FindWindowAtPointer()
        InspectionTool().Show(wnd)


widgetInspector = WidgetInspector()
wx.GetApp().AddPostInitAction(widgetInspector.initInspection)

