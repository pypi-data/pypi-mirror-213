# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.av.filter import FilteredStream
from colourspace.av.filter.colourspace import ColourspaceFilter
from colourspace.av.filter.rotate import rotate_filters
from colourspace.av.stream import Stream


class CorrectedStream(Stream):
    def __init__(self, stream, input_profile, output_profile):
        self._stream = stream
        self._corrected = stream
        self._correction = True
        self._input_profile = input_profile
        self._output_profile = output_profile

        # Get rotation from stream side data
        rotation = float(stream.info.get("rotation", 0))

        # Inject extra filters to handle autorotation.
        # Dimensions may need to change if rotated at 90/270
        self._filters, self._dimensions = rotate_filters(rotation, (stream.width, stream.height))

        self._update_filter()

    def _update_filter(self):
        filters = []

        # Copy the rotation filters (if any)
        filters += self._filters

        # Add the Colourspace filter (if any)
        if self._correction and self._input_profile and self._output_profile:
            filters += [ColourspaceFilter(self._input_profile, self._output_profile)]

        # Spoof the original video with a filtered one if there are rotation
        # filters and/or colourspace correction
        self._corrected = FilteredStream(self._stream, filters, self._dimensions) if filters else self._stream

    @property
    def input_profile(self):
        return self._input_profile

    @input_profile.setter
    def input_profile(self, p):
        self._input_profile = p
        self._update_filter()

    @property
    def output_profile(self):
        return self._output_profile

    @output_profile.setter
    def output_profile(self, p):
        self._output_profile = p
        self._update_filter()

    @property
    def correction(self):
        return self._correction

    @correction.setter
    def correction(self, value):
        self._correction = value
        self._update_filter()

    @property
    def position(self):
        return self._corrected.position

    def seek(self, position=0):
        return self._corrected.seek(position)

    @property
    def frame(self):
        return self._corrected.frame

    @property
    def container(self):
        return self._corrected.container

    @property
    def width(self):
        return self._corrected.width

    @property
    def height(self):
        return self._corrected.height

    @property
    def duration(self):
        return self._corrected.duration

    @property
    def key_frames(self):
        return self._corrected.key_frames

    @property
    def info(self):
        return self._corrected.info

    @property
    def has_errors(self):
        return self._corrected.has_errors
