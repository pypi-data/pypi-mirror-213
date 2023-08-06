# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import re


def time_format(seconds):
    seconds_r = seconds - int(seconds)
    seconds = int(seconds)

    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = (seconds % 3600) % 60

    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{int(seconds_r * 1000):03d}"


# 00:00:00.000
FORMAT = re.compile("(\d+):(\d+):([\d.]+)")


def time_parse(value):
    try:
        # is it already in seconds?
        return float(value)
    except ValueError:
        pass

    # try the time format
    match = FORMAT.fullmatch(value.strip())
    if not match:
        raise ValueError("Invalid time format: either specify as float in seconds or use the time format HH:MM:SS.SSS")

    hours, minutes, seconds = match.groups()

    # Convert back to seconds
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
