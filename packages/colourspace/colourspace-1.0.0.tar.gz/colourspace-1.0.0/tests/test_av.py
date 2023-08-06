# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import pytest

from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter, Profile, PROFILES
from colourspace.av.container import Container
from data import TEST_INFOS
from PIL import Image


def check_frame(stream):
    frame = stream.frame
    assert frame, "No frame available"

    image = stream.frame.to_image()
    assert type(image) == Image.Image, "Returned frame is wrong type"
    assert image.size == (stream.width, stream.height), "Wrong frame size"


@pytest.mark.parametrize("filename, info", TEST_INFOS.items())
def test_video_frame(filename, info):
    with Container(filename) as container:
        for stream in container.streams:
            # Make sure the frame is valid
            check_frame(stream)


@pytest.mark.parametrize("filename, info", TEST_INFOS.items())
def test_video_seek(filename, info):
    with Container(filename) as container:
        for stream in container.streams:
            # Seek to half of video
            stream.seek(stream.duration / 2)

            # Make sure the frame is valid
            check_frame(stream)


@pytest.mark.parametrize("filename, info", TEST_INFOS.items())
def test_video_filter(filename, info):
    with Container(filename) as container:
        for stream in container.streams:
            if any([x % 2 for x in (stream.width, stream.height)]):
                # vf_colorspace does not support videos of odd sizes
                continue

            # Get a Profile for this stream
            stream_profile, _ = Profile.from_stream(stream)

            # Create the filter with default output
            filter = ColourspaceFilter(stream_profile, PROFILES["bt709"])

            # Create a Stream for this filter
            stream = FilteredStream(stream, [filter])

            # Make sure the generated frame is valid
            check_frame(stream)
