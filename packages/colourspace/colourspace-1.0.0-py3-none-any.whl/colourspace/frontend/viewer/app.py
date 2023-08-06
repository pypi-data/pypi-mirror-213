# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import logging
import os
import sys
import wx

from colourspace.av.container import Container
from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.av.filter.correct import CorrectedStream
from colourspace.av.filter.rotate import rotate_filters
from colourspace.frontend.window.video import VideoFrame
from colourspace.util.settings import Settings
from pathlib import Path
from pylru import lrucache

SETTINGS_FILENAME = str(Path.home().joinpath(".clrview.cfg"))
SETTINGS_VERSION = 1
MAX_REMEMBERED_VIDEOS = 1000


class App(wx.App):
    def Open(self, filename=None):
        stream = None

        if filename:
            filename = os.path.abspath(filename)

            # Is this already opened?
            if filename in self._opened:
                frame = self._opened[filename]
                frame.Raise()
                return frame

            # Try opening a new one
            logger = logging.getLogger(__name__)
            try:
                container = Container(filename)
                stream = container.streams[0]  # Multiple tracks in a video not supported in app

                # Read profile from settings
                input_profile = self.GetVideoProfileFromSettings(stream)
                output_profile = self.GetOutputProfileFromSettings()

                # Apply automatic corrections
                stream = CorrectedStream(stream, input_profile, output_profile)
            except Exception as e:
                logger.warning(f"Failed to open '{os.path.basename(filename)}'", exc_info=e)
                wx.MessageDialog(None, f"Failed to open '{os.path.basename(filename)}': {e}",
                                 "Failed to open file", wx.OK | wx.CENTER | wx.ICON_ERROR).ShowModal()
                return None
        else:
            # Make sure all Falsy filenames converge into a single window
            filename = None

        if None in self._opened:
            # Opening a new one, which is not empty.
            # Make sure we've closed the empty window.
            self._opened[None].Close()
            del self._opened[None]

        display_width, _ = wx.DisplaySize()
        min_max_size = display_width // 4, display_width // 2
        frame = VideoFrame(self, stream, initial_min_max_size=min_max_size)
        frame.Center()
        frame.Show()
        self._opened[filename] = frame
        return frame

    def OnInit(self):
        self._opened = {}
        self._settings = Settings(SETTINGS_FILENAME, SETTINGS_VERSION)
        return True

    @property
    def Settings(self):
        return self._settings

    def GetVideoProfileFromSettings(self, video):
        # Read video settings from file
        videos = self._settings.get("videos", lrucache(MAX_REMEMBERED_VIDEOS))

        filename = video.container.filename

        if filename not in videos:
            # Assign a most appropriate profile
            profile, _ = Profile.from_stream(video)

            # Update video settings cache
            videos[filename] = profile

            # Update Settings file
            self._settings.set("videos", videos)
        else:
            # Get profile directly from cache
            profile = videos[filename]

        return profile

    def UpdateVideoProfileInSettings(self, video, profile):
        # Read video settings from file
        videos = self._settings.get("videos", lrucache(MAX_REMEMBERED_VIDEOS))

        # Update video settings cache
        videos[video.container.filename] = profile

        # Update settings file
        self._settings.set("videos", videos)

    def GetOutputProfileFromSettings(self):
        return self._settings.get("profile", PROFILES["bt709"])

    def UpdateOutputProfileInSettings(self, profile):
        self._settings.set("profile", profile)

    def OnCloseWindow(self, filename):
        del self._opened[filename]

    def Quit(self):
        # Cache the opened windows as
        # self._opened is going to be modified
        # by each closed window
        opened = list(self._opened.values())

        for window in opened:
            window.Close()

        # This will close left-over windows (if any)
        self.ExitMainLoop()


def main():
    # WARNING/libav.swscaler           (66753 ): deprecated pixel format used, make sure you did set range correctly
    format = "%(levelname)-7s/%(name)-24s (%(process)-6d): %(message)s"
    logging.basicConfig(format=format)

    app = App()

    if sys.argv[1:]:
        # Open all files passed by command line
        for filename in sys.argv[1:]:
            app.Open(filename)
    else:
        # No args specified, open an empty window
        app.Open()

    app.MainLoop()


if __name__ == "__main__":
    main()
