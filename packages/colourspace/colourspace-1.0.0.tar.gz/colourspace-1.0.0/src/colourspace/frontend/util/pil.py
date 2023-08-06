# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import wx

PIL_TO_WX = {
    "RGB": wx.Bitmap.FromBuffer,
    "RGBA": wx.Bitmap.FromBufferRGBA,
}


def image_to_bitmap(image):
    if image.mode not in PIL_TO_WX:
        raise ValueError(f"Unsupported PIL image mode: {image.mode}")

    return PIL_TO_WX[image.mode](*image.size, image.tobytes())
