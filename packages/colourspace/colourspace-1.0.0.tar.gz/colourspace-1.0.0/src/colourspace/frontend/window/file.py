# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import wx

from collections import OrderedDict
from itertools import chain

FILE_TYPES = OrderedDict([
    ("Video files", [
        "264",
        "asf",
        "avi",
        "divx",
        "h263",
        "h264",
        "hevc",
        "m2v",
        "m4v",
        "mkv",
        "mov",
        "mp4",
        "mpg",
        "qt",
        "vob",
        "webm",
        "webp",
        "wmv",
    ]),
    ("Image files", [
        "bmp",
        "gif",
        "jpg",
        "jpeg",
        "png",
        "psd",
        "tga",
        "tif",
        "tiff",
    ]),
])

SAVE_TYPES = OrderedDict([
    ("PNG", [
        "png"
    ]),
    ("JPEG", [
        "jpg",
        "jpeg"
    ]),
])


def get_extensions(types):
    return [f".{e}" for e in chain(*types.values())]


def get_wildcards(types):
    wildcards = []

    for name, extensions in types.items():
        wildcards += [
            name,
            # transform: [jpg, JPEG] -> [jpg, jpeg] -> [*.jpg, *.jpeg] -> "*.jpg;*.jpeg"
            ";".join([f"*.{e.lower()}" for e in extensions])
        ]

    # Convert to FILE type|*.ext|...
    return "|".join(wildcards)


def OpenFiles(parent):
    with wx.FileDialog(parent, "Open video/image file", wildcard=get_wildcards(FILE_TYPES),
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as dialog:

        if dialog.ShowModal() == wx.ID_OK:
            return dialog.GetPaths()

        return []


def SaveFrame(parent):
    with wx.FileDialog(parent,
                       "Safe frame as", wildcard=get_wildcards(SAVE_TYPES),
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
        if dialog.ShowModal() == wx.ID_OK:
            filename, ext = os.path.splitext(dialog.GetPath())
            ext = ext.lower()

            if ext not in get_extensions(SAVE_TYPES):
                # Get current filter
                filter_index = dialog.GetFilterIndex()
                # Get extensions for current filter
                extensions = list(SAVE_TYPES.values())[filter_index]
                # Append first extension for filter
                ext += "." + extensions[0]

            return filename + ext
