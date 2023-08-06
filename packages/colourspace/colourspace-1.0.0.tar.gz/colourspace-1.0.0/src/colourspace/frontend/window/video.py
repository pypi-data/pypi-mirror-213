# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import sys
import wx

from colourspace.frontend.control.video import VideoPanel, EVT_VIDEO_SEEK
from colourspace.frontend.util.drop import Drop
from colourspace.frontend.window.colourspace import ColourspaceDialog
from colourspace.frontend.window.file import OpenFiles, SaveFrame
from colourspace.frontend.window.metadata import MetadataFrame
from colourspace.frontend.window.seek import SeekDialog
from colourspace.util.time import time_format
from PIL import Image


class VideoFrame(wx.Frame):
    def __init__(self, app, video=None,
                 resize_quality=Image.LINEAR,
                 initial_min_max_size=(320, 640),
                 *args, **kwargs):

        title = video.container.filename if video else "Untitled"
        super().__init__(None, title=title, *args, **kwargs)

        # Calculate appropriate initial size for the video window
        display_width, display_height = wx.DisplaySize()
        display_ratio = display_height / display_width
        _, initial_width = initial_min_max_size
        initial_height = int(initial_width * display_ratio)
        size = self.FromDIP((initial_width, initial_height))
        self.SetSize(size)

        self._app = app
        self._statusbar = self.CreateStatusBar(2)
        self._metadata = None

        if video:
            self._has_video = True
            self._video = VideoPanel(self, video, resize_quality)
        else:
            self._has_video = False
            self._video = wx.Panel(self)

        # Initialise the menu
        self.SetMenuBar(self._create_menu())

        # Set current video position in the status bar to 00:00:00
        self._update_video_position(0)

        self.Layout()

        self.Bind(wx.EVT_CLOSE, self._on_close)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(EVT_VIDEO_SEEK, self._on_video_seek)
        self.SetDropTarget(Drop(app))

    def _on_close(self, event):
        if self._has_video:
            # close the container w/o waiting for dtr
            filename = self._video.Video.container.filename
            self._video.Video.container.close()
            self._app.OnCloseWindow(filename)

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()

    def _on_size(self, event):
        if self._has_video:
            size = self.GetClientSize()
            size = self._video.GetBestSize(size)
            self.SetClientSize(size)

        # Skip the event so that it is handled correctly by somebody else
        event.Skip()

    def _on_video_seek(self, event):
        self._update_video_position(event.position)

    def _update_video_position(self, position):
        position = time_format(position)
        duration = time_format(
            self._video.Video.duration if self._has_video else 0)
        self._statusbar.SetStatusText(position + "/" + duration)

    def _create_menu(self):
        menu_bar = wx.MenuBar()

        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, "", "Open a video or an image file")
        file_close = file_menu.Append(wx.ID_CLOSE, "Close\tCtrl+W", "Close this file")
        menu_bar.Append(file_menu, "&File")

        edit_menu = wx.Menu()
        seek_time = edit_menu.Append(wx.ID_ANY, "Seek\tCtrl+F", "Seek to a particular time")
        edit_menu.AppendSeparator()
        edit_menu.Append(wx.ID_SAVE, "Save frame\tCtrl+S", "Save the current frame along with video")
        edit_menu.Append(wx.ID_SAVEAS, "Save frame as...", "Save the current frame to a specified location")
        menu_bar.Append(edit_menu, "&Edit")

        colourspace = wx.Menu()
        self._correction_enabled = colourspace.AppendCheckItem(
            wx.ID_ANY, "Colour Correction\tCtrl+B", "Enable accurate colour representation")

        # Correction is on by default
        self._correction_enabled.Check()
        colourspace.AppendSeparator()
        input_colourspace = colourspace.Append(
            wx.ID_ANY, "Input Colourspace\tCtrl+[", "Select input colourspace")
        output_colourspace = colourspace.Append(
            wx.ID_ANY, "Output Colourspace\tCtrl+]", "Select output colourspace")
        menu_bar.Append(colourspace, "&Colourspace")

        view_menu = wx.Menu()
        self._metadata_menu = view_menu.AppendCheckItem(
            wx.ID_ANY, "Metadata Inspector\tCtrl+I", "Show metadata inspector window")
        menu_bar.Append(view_menu, "&View")

        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "", "About this application")
        menu_bar.Append(help_menu, "&Help")

        # Bind the events
        self.Bind(wx.EVT_MENU, self._on_open_file, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self._on_close_file, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self._on_seek_time, seek_time)
        self.Bind(wx.EVT_MENU, self._on_save_frame, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self._on_save_frame_as, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self._on_corretion_toggled, self._correction_enabled)
        self.Bind(wx.EVT_MENU, self._on_input_colourspace, input_colourspace)
        self.Bind(wx.EVT_MENU, self._on_output_colourspace, output_colourspace)
        self.Bind(wx.EVT_MENU, self._on_metadata_inspector, self._metadata_menu)
        self.Bind(wx.EVT_MENU, self._on_about, id=wx.ID_ABOUT)

        # Add Exit to File menu on non-MacOS
        if sys.platform != "darwin":
            file_menu.Append(wx.ID_EXIT)
            self.Bind(wx.EVT_MENU, self._on_quit, id=wx.ID_EXIT)

        # Disable stuff if no video present
        if not self._has_video:
            items = \
                list(edit_menu.MenuItems) + \
                list(colourspace.MenuItems) +\
                list(view_menu.MenuItems)

            for item in items:
                item.Enable(False)

        return menu_bar

    # File
    def _on_open_file(self, event):
        for filename in OpenFiles(self):
            self._app.Open(filename)

    def _on_close_file(self, event):
        self.Close()

    def _on_quit(self, event):
        self._app.Quit()

    # Edit
    def _on_seek_time(self, event):
        with SeekDialog(self._video.Video, self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self._video.Seek(dialog.SeekPosition)
                self._video.RefreshFrame()
                self._video.Refresh()

    def _on_save_frame(self, event):
        # generate filename
        position = time_format(self._video.Video.position).replace(":", "_").replace(".", "_")
        filename, _ = os.path.splitext(self._video.Video.container.filename)
        filename = f"{filename}_{position}.png"
        with wx.ProgressDialog("Saving...", f"Saving frame to {os.path.basename(filename)}") as dialog:
            dialog.Pulse()
            self._save_to_file(filename)

    def _on_save_frame_as(self, event):
        filename = SaveFrame(self)
        if filename:
            with wx.ProgressDialog("Saving...", f"Saving frame to {os.path.basename(filename)}") as dialog:
                dialog.Pulse()
                self._video.Frame.save(filename)

    def _save_to_file(self, filename):
        self._video.Frame.save(filename)

    # Colourspace
    def _on_corretion_toggled(self, event):
        self._video.Video.correction = self._correction_enabled.IsChecked()
        self._video.RefreshFrame()
        self._video.Refresh()

    def _on_input_colourspace(self, event):
        with ColourspaceDialog(self._video.Video, True, self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self._video.Video.input_profile = dialog.Profile
                self._app.UpdateVideoProfileInSettings(self._video.Video, dialog.Profile)
                self._video.RefreshFrame()
                self._video.Refresh()

    def _on_output_colourspace(self, event):
        with ColourspaceDialog(self._video.Video, False, self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self._video.Video.output_profile = dialog.Profile
                self._app.UpdateOutputProfileInSettings(dialog.Profile)
                self._video.RefreshFrame()
                self._video.Refresh()

    # View
    def _on_metadata_inspector(self, event):
        if not self._metadata:
            self._metadata = MetadataFrame(self._video.Video, self)

            def on_metadata_close(event):
                self._metadata_menu.Check(False)
                event.Skip()

            self._metadata.Bind(wx.EVT_CLOSE, on_metadata_close)

        self._metadata.Show(self._metadata_menu.IsChecked())

    # Help
    def _on_about(self, event):
        message = """
Colourspace is a Python library and viewer tool used to render videos and images in the proper colourspace using the colorspace FFmpeg filter.

It uses the av package to access FFmpeg functionality, and pymediainfo to obtain file and stream metadata, that is not yet available through av (even though it is available in FFmpeg).

Note: PyAV uses a (rather) outdated version of FFmpeg: 5.1.2, which may lack bug fixes and support for newer functionality.

Licensed under BSD 3-Clause.

Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova"""
        wx.MessageDialog(None, message, "About", wx.OK | wx.CENTER | wx.ICON_INFORMATION).ShowModal()
