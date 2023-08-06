# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import wx


class Drop(wx.FileDropTarget):
    def __init__(self, app):
        super().__init__()
        self._app = app

    def OnDropFiles(self, x, y, filenames):
        # Remove directories from list
        filenames = [f for f in filenames if not os.path.isdir(f)]
        for filename in filenames:
            self._app.Open(filename)

        return True
