# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import av

from colourspace.av.exception import AVException
from colourspace.av.stream import Stream


class Filter:
    @property
    def name(self):
        raise NotImplementedError()

    @property
    def params(self):
        raise NotImplementedError()

    @staticmethod
    def get_options(filter_name):
        # Create a PyAV filter (it is just a description)
        # FilterContext is actually used for filtering
        filter = av.filter.filter.Filter(filter_name)

        # Reshape the options tuple into a dict
        return {o.name: o for o in filter.options}

    @staticmethod
    def get_choices_for_option(filter_name, option):
        options = Filter.get_options(filter_name)

        if option not in options:
            raise AVException(
                f"Unsupported option {option} for filter {filter_name}")

        option = options[option]

        return [o.name for o in option.choices]

    @staticmethod
    def set_opt_param(params, name, value):
        if value:
            params[name] = value


class SimpleFilter(Filter):
    def __init__(self, name, params=None):
        self._name = name
        self._params = params

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params


class FilteredStream(Stream):
    def __init__(self, stream, filters, dimensions=None):
        self._stream = stream
        self._filters = filters
        self._dimensions = dimensions

        # Create the filter graph:
        # input buffer -> filter 1 -> filter 2 -> ... -> output buffersink
        graph = av.filter.Graph()

        # Prepare the input
        buffer = graph.add_buffer(template=stream._stream)

        # Input buffer is treated as the initial filter
        previous_filter = buffer

        for f in filters:
            # Convert to filter params:
            # param1=value1:param2=value2:...
            params = ":".join([f"{k}={v}" for k, v in f.params.items()]) if f.params else None

            # Previous filter -> filter
            filter = graph.add(f.name, params) if params else graph.add(f.name)
            previous_filter.link_to(filter)
            previous_filter = filter

        # Last filter -> output sink
        buffersink = graph.add("buffersink")
        previous_filter.link_to(buffersink)

        # Compile the graph
        graph.configure()
        self._graph = graph

        # Now update the initial frame
        self._frame = self._get_frame()

    def _get_frame(self):
        # read current frame from sub-stream
        frame = self._stream.frame

        # push into graph for processing
        self._graph.push(frame)

        # return processed frame
        return self._graph.pull()

    @property
    def position(self):
        return self._stream.position

    def seek(self, position=0):
        if self._stream.seek(position):
            # Substream's frame has changed: reacquire and reprocess
            self._frame = self._get_frame()
            return True

        return False

    @property
    def frame(self):
        return self._frame

    @property
    def container(self):
        return self._stream.container

    @property
    def width(self):
        return self._dimensions[0] if self._dimensions else self._stream.width

    @property
    def height(self):
        return self._dimensions[1] if self._dimensions else self._stream.height

    @property
    def duration(self):
        return self._stream.duration

    @property
    def key_frames(self):
        return self._stream.key_frames

    @property
    def info(self):
        return self._stream.info

    @property
    def has_errors(self):
        return self._stream.has_errors
