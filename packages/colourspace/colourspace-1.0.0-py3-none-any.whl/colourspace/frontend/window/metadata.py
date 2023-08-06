# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx
import wx.grid


class MetadataFrame(wx.Frame):
    def __init__(self, video, *args, **kw):
        super().__init__(*args, **kw)

        info = video.info
        keys = [k for k in info.keys() if not k.startswith("other_")]

        grid = wx.grid.Grid(self)
        grid.CreateGrid(len(keys), 2)

        for idx, k in enumerate(sorted(keys)):
            v = str(info[k])
            grid.SetCellValue(idx, 0, k)
            grid.SetCellValue(idx, 1, v)
            grid.SetReadOnly(idx, 0)
            grid.SetReadOnly(idx, 1)

        grid.SetColLabelValue(0, "Parameter")
        grid.SetColLabelValue(1, "Value")
        grid.EnableDragRowSize(False)
        grid.AutoSizeColumns()

        self.SetTitle(f"{video.container.filename} (metadata)")
        self.Layout()
        self.Center()
