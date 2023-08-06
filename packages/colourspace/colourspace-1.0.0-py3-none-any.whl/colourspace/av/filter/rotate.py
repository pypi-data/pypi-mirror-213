# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.av.filter import SimpleFilter
from math import pi


def rotate_filters(angle, dimensions):
    # Make sure the angle is in 0..360
    # See get_rotation() in fftools/cmdutils.c
    angle -= 360 * int(angle/360 + 0.9/360)

    # Handle different rotations.
    # See `if (autorotate) {` in fftools/ffplay.c
    if abs(angle - 90) < 1:
        # Rotated by 90. Simple transpose is enough
        return [
            SimpleFilter("transpose", {
                "dir": "clock",
            }),
        ], (dimensions[1], dimensions[0])
    elif abs(angle - 180) < 1:
        # Rotated by 180. Use horizontal and vertical flip
        return [
            SimpleFilter("hflip"),
            SimpleFilter("vflip"),
        ], None
    elif abs(angle - 270) < 1:
        # Rotated by 270. Simple transpose is enough
        return [
            SimpleFilter("transpose", {
                "dir": "cclock",
            }),
        ], (dimensions[1], dimensions[0])
    elif abs(angle) > 1:
        # Generic rotation by an odd angle
        return [
            SimpleFilter("rotate", {
                "angle": angle * (pi / 180),
            }),
        ], None
    else:
        # No rotation necessary (0 <= angle < 1)
        return [], None
