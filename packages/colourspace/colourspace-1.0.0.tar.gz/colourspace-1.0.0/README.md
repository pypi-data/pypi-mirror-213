# Colourspace
_Colourspace_ is a Python library and viewer tool used to render videos and
images in the proper colourspace using the _colorspace_ _FFmpeg_ filter.

It uses the _av_ package to access _FFmpeg_ functionality, and _pymediainfo_
to obtain file and stream metadata, that is not yet available through _av_
(even though it _is_ available in _FFmpeg_).

Note: _PyAV_ uses a (rather) outdated version of FFmpeg: 5.1.2, which may lack bug fixes
and support for newer functionality. Check the [FFmpeg build script][1] for PyAV.

## License
Licensed under BSD 3-Clause.

## Copyright
Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

  [1]: https://github.com/PyAV-Org/pyav-ffmpeg/blob/61a5e7dcaa0df41c1b6b20fd290dcc8fbc1a9ded/scripts/build-ffmpeg.py#L323
