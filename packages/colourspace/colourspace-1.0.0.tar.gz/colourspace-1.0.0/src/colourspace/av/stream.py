# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

class Stream():
    @property
    def position(self):
        """Returns the current position"""
        raise NotImplementedError()

    def seek(self, position=0):
        """Seek to a precise position. Defaults to start of file."""
        raise NotImplementedError()

    @property
    def frame(self):
        """Returns the current frame"""
        raise NotImplementedError()

    @property
    def container(self):
        """Returns the file container"""
        raise NotImplementedError()

    @property
    def width(self):
        """Returns the width of the video frames"""
        raise NotImplementedError()

    @property
    def height(self):
        """Returns the width of the height frames"""
        raise NotImplementedError()

    @property
    def duration(self):
        """Returns the duration of the stream in seconds"""
        raise NotImplementedError()

    @property
    def key_frames(self):
        """Returns a list of the positions of the keyframes"""
        raise NotImplementedError()

    @property
    def info(self):
        """Returns a dict of metadata for this stream"""
        raise NotImplementedError()

    @property
    def has_errors(self):
        """Returns true if there were any errors during decoding"""
        raise NotImplementedError()
