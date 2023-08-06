# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import sys

from av.error import FFmpegError
from colourspace.av.exception import AVException
from colourspace.av.stream import Stream
from logging import getLogger


class VideoStream(Stream):
    def __init__(self, container, stream, info):
        if not stream.codec_context:
            raise AVException(f"Unsupported codec {info.get('codec_id', '')}")

        self._container = container
        self._stream = stream
        self._info = info
        self._frame = None
        self._frame = self._get_frame()
        self._position = 0
        self._key_frames = []
        self._has_errors = False

        if container.seekable:
            try:
                # This may fail on corrupt videos, so let's make it optional
                self._key_frames = [float(p.pts * p.time_base)
                                    for p in stream.container.demux(stream) if p.is_keyframe]
            except FFmpegError:
                getLogger(__name__).warning("Could not obtain keyframes")

            # rewind container
            container.seek(0)

        # calculate and cache duration
        if self._stream.duration:
            # obtain directly from FFmpeg video stream
            self._duration = float(self._stream.duration * self._stream.time_base)
        else:
            # sometimes (e.g. for FLV) the stream duration may be None.
            # fall back to the duration of the container
            self._duration = self._container.duration

    def _get_frame(self, position=0):
        # Crude seek to a key frame
        self._container.seek(position)

        # Now seek to a fine position, not just a keyframe
        # by decoding frames until reaching the correct position

        # Keep a copy of the previously decoded frame as it will be the last frame
        # before overrunning the position being sought, thus the correct frame to return
        previous_video_frame = None

        # Retry until finding a frame or reaching EOF
        while not previous_video_frame:
            try:
                # Demux the container and get the next pack for this video stream
                for packet in self._stream.container.demux(self._stream):
                    # Decode all frames in this packet that we just demuxed
                    for frame in packet.decode():
                        # Convert the decoded frame postion to seconds
                        frame_pos = float(frame.pts * frame.time_base) if frame.pts else 0

                        if frame_pos > position:
                            # This frame is JUST pass the position in time
                            # Return the previously devode frame, or this one if
                            # it was the first one anyway
                            return previous_video_frame if previous_video_frame else frame

                        # Cache this current frame
                        previous_video_frame = frame

                # no more frames (EOF), return whatever was last
                return previous_video_frame if previous_video_frame else self._frame
            except FFmpegError as ex:
                # EOFErrors inherits from FFmpegError, but should not be caught
                if isinstance(ex, EOFError):
                    raise ex

                getLogger(__name__).warning("FFmpeg error while decoding", exc_info=ex)
                self._has_errors = True

        # This may be reached if a frame was successfully decoded,
        # i.e. previous_video_frame is not None, yet there was an
        # exception.
        return previous_video_frame if previous_video_frame else self._frame

    @property
    def position(self):
        return self._position

    def seek(self, position=0):
        # Actually seek only if position has changed or decoding for the first time
        if not self._frame or (self._container.seekable and position != self._position):
            self._position = position
            self._frame = self._get_frame(position)
            return True

        # No need to seek
        return False

    @property
    def frame(self):
        return self._frame

    @property
    def container(self):
        return self._container

    @property
    def width(self):
        return self._stream.width

    @property
    def height(self):
        return self._stream.height

    @property
    def duration(self):
        return self._duration

    @property
    def key_frames(self):
        return list(self._key_frames)

    @property
    def info(self):
        return self._info

    @property
    def has_errors(self):
        return self._has_errors
