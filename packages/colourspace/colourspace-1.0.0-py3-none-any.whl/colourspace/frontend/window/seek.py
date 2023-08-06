# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import wx

from colourspace.util.time import time_format, time_parse


class SeekDialog(wx.Dialog):
    def __init__(self, video, *args, **kw):
        super().__init__(*args, **kw)

        self._video = video
        self._position = video.position

        self.SetTitle(f"Seek ({os.path.basename(video.container.filename)})")

        sizer = wx.BoxSizer(wx.VERTICAL)

        self._position_control = wx.TextCtrl(self, value=time_format(self._position))
        sizer.Add(self._position_control, 0, wx.ALL | wx.EXPAND, 5)

        # buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        button_ok = wx.Button(self, wx.ID_OK)
        button_ok.SetDefault()
        button_ok.SetFocus()
        button_sizer.Add(button_ok, 0, wx.ALL, 5)

        button_cancel = wx.Button(self, wx.ID_CANCEL)
        button_sizer.Add(button_cancel, 0, wx.ALL, 5)

        button_reset = wx.Button(self, wx.ID_DEFAULT, "Current")
        button_reset.Bind(wx.EVT_BUTTON, self._on_reset)
        button_sizer.Add(button_reset, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.EXPAND, 5)

        # fix up the frame
        self.SetSizeHints(wx.Size(200, 100), wx.DefaultSize)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.Centre(wx.BOTH)

    def Validate(self):
        try:
            position = time_parse(self._position_control.Value)
            if position > self._video.duration:
                raise ValueError("Position is outside video duration")
        except ValueError as e:
            wx.MessageDialog(None, str(e), "Invalid time", wx.OK | wx.CENTER | wx.ICON_ERROR).ShowModal()
            return False

        self._position = position
        return True

    @property
    def SeekPosition(self):
        return self._position

    def _on_reset(self, event):
        self._position = self._video.position
        self._position_control.Value = time_format(self._position)
