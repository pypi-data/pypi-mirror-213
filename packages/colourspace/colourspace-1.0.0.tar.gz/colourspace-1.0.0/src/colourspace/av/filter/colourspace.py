# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

from colourspace.av.filter import Filter

NAME = "colorspace"

# Reference: libavfilter/vf_colorspace.c: colorspace_options
# Reference: libavutil/pixfmt.h: AVColorSpace, AVColorPrimaries, AVColorTransferCharacteristic

# Note: gbr is actually AVCOL_SPC_RGB
# Unsupported colourspaces:
# AVCOL_SPC_BT2020_CL           ITU-R BT2020 constant luminance system
# AVCOL_SPC_SMPTE2085           SMPTE 2085, Y'D'zD'x
# AVCOL_SPC_CHROMA_DERIVED_NCL  Chromaticity-derived non-constant luminance system
# AVCOL_SPC_CHROMA_DERIVED_CL   Chromaticity-derived constant luminance system
# AVCOL_SPC_ICTCP               ITU-R BT.2100-0, ICtCp
COLOURSPACES = Filter.get_choices_for_option(NAME, "space")

# bt2020nc  = AVCOL_SPC_BT2020_NCL
# bt2020ncl = AVCOL_SPC_BT2020_NCL
COLOURSPACE_SYNONYMS = {
    "bt2020ncl": "bt2020nc",
}

INFO_TO_COLOURSPACE = {
    "Identity": "gbr",
    "BT.709": "bt709",
    "FCC 73.682": "fcc",
    "BT.470 System B/G": "bt470bg",
    "BT.601": "smpte170m",
    "SMPTE 240M": "smpte240m",
    "YCgCo": "ycgco",
    "BT.2020 non-constant": "bt2020nc",  # same as bt2020ncl
    # "BT.2020 constant": not supported by vf_colorspace
    # "Y'D'zD'x": not supported by vf_colorspace
    # "Chromaticity-derived non-constant": not supported by vf_colorspace
    # "Chromaticity-derived constant": not supported by vf_colorspace
    # "ICtCp": not supported by vf_colorspace
}

PRIMARIES = Filter.get_choices_for_option(NAME, "primaries")

# AVCOL_PRI_JEDEC_P22 = AVCOL_PRI_EBU3213,
PRIMARY_SYNONYMS = {
    "jedec-p22": "ebu3213",
}

INFO_TO_PRIMARIES = {
    "BT.709": "bt709",
    "BT.470 System M": "bt470m",
    "BT.601 PAL": "bt470bg",
    "BT.601 NTSC": "smpte170m",
    "SMPTE 240M": "smpte240m",
    "Generic film": "film",
    "BT.2020": "bt2020",
    "XYZ": "smpte428",
    "DCI P3": "smpte431",
    "Display P3": "smpte432",
    "EBU Tech 3213": "ebu3213",  # same as jedec-p22
}

# Unsupported transfer characteristics:
# AVCOL_TRC_LOG             Logarithmic transfer characteristic (100:1 range)
# AVCOL_TRC_LOG_SQRT        Logarithmic transfer characteristic (100 * Sqrt(10) : 1 range)
# AVCOL_TRC_BT1361_ECG      ITU-R BT1361 Extended Colour Gamut
# AVCOL_TRC_SMPTE2084       SMPTE ST 2084 for 10-, 12-, 14- and 16-bit systems
# AVCOL_TRC_SMPTE428        SMPTE ST 428-1
# AVCOL_TRC_ARIB_STD_B67    ARIB STD-B67, known as "Hybrid log-gamma"
TRANSFERS = Filter.get_choices_for_option(NAME, "trc")


# bt470m        = AVCOL_TRC_GAMMA22
# gamma22       = AVCOL_TRC_GAMMA22
# bt470bg       = AVCOL_TRC_GAMMA28
# gamma28       = AVCOL_TRC_GAMMA28
# srgb          = AVCOL_TRC_IEC61966_2_1
# iec61966-2-1  = AVCOL_TRC_IEC61966_2_1
# xvycc         = AVCOL_TRC_IEC61966_2_4
# iec61966-2-4  = AVCOL_TRC_IEC61966_2_4
TRANSFER_SYNONYMS = {
    "gamma22": "bt470m",
    "gamma28": "bt470bg",
    "iec61966-2-1": "srgb",
    "iec61966-2-4": "xvycc",
}

INFO_TO_TRANSFER = {
    "BT.709": "bt709",
    "BT.470 System M": "bt470m",  # same as gamma22
    "BT.470 System B/G": "bt470bg",  # same as gamma28
    "BT.601": "smpte170m",
    "SMPTE 240M": "smpte240m",
    "Linear": "linear",
    # "Logarithmic (100:1)": not supported by vf_colorspace
    # "Logarithmic (316.22777:1)": not supported by vf_colorspace
    "xvYCC": "xvycc",
    # "BT.1361": not supported by vf_colorspace
    "sRGB/sYCC": "srgb",
    "BT.2020 (10-bit)": "bt2020-10",
    "BT.2020 (12-bit)": "bt2020-12",
    # "PQ": not supported by vf_colorspace
    # "SMPTE 428M": not supported by vf_colorspace
    # "HLG": not supported by vf_colorspace
}

RANGES = [
    "tv",  # tv/mpeg = limited
    "pc",  # pc/jpeg = full
]

INFO_TO_RANGES = {
    "Limited": "tv",
    "Full": "pc",
}

PROFILE_NAMES = Filter.get_choices_for_option(NAME, "all")


class Profile:
    def __init__(self, colourspace, primaries, transfer, range=None):
        # make sure we remove any synonyms
        self._colourspace = COLOURSPACE_SYNONYMS.get(colourspace, colourspace)
        self._primaries = PRIMARY_SYNONYMS.get(primaries, primaries)
        self._transfer = TRANSFER_SYNONYMS.get(transfer, transfer)
        self._range = range

    @property
    def colourspace(self):
        return self._colourspace

    @property
    def primaries(self):
        return self._primaries

    @property
    def transfer(self):
        return self._transfer

    @property
    def range(self):
        return self._range

    def __eq__(self, other):
        # not comparing the colour range as it is not really
        # part of the profile
        return (self.colourspace == other.colourspace) \
            and (self.primaries == other.primaries) \
            and (self.transfer == other.transfer)

    def __hash__(self):
        return hash(self.colourspace) \
            ^ hash(self.primaries) \
            ^ hash(self.transfer)

    def compute_similarity(self, other):
        # priorities: csp > pri > trc
        return \
            4 * int(self.colourspace == other.colourspace) + \
            2 * int(self.primaries == other.primaries) + \
            1 * int(self.transfer == other.transfer)

    @property
    def name(self):
        for name, profile in PROFILES.items():
            if profile == self:
                return name

        return "Custom"

    def __repr__(self):
        return f"{self.name}: {{ csp={self.colourspace}, prm={self.primaries}, trc={self.transfer}, rng={self.range} }}"

    @staticmethod
    def from_stream(stream):
        # get colour profile parameters and do not raise
        # if they are not available in the metadata
        colourspace = stream.info.get("matrix_coefficients")
        primaries = stream.info.get("color_primaries")
        transfer = stream.info.get("transfer_characteristics")
        range = stream.info.get("color_range")

        # Now try matching
        problems = {}

        def validate_param_(param_name, param_type, valid_names):
            nonlocal problems

            if not param_name:
                problems[param_type] = "N/A"
            elif param_name not in valid_names:
                problems[param_type] = f"{param_name} is not supported"
            else:
                return valid_names[param_name]

        colourspace = validate_param_(colourspace, "colourspace", INFO_TO_COLOURSPACE)
        primaries = validate_param_(primaries, "primaries", INFO_TO_PRIMARIES)
        transfer = validate_param_(transfer, "transfer", INFO_TO_TRANSFER)
        range = validate_param_(range, "range", INFO_TO_RANGES)

        profile = Profile(colourspace, primaries, transfer, range)

        if colourspace and primaries and transfer:
            # Everything is valid for the profile
            return profile, problems

        # try to find the closest predefined profile to
        # fill in the unsupported parameters
        # create a dict of score -> predefined profile
        scored_profiles = {profile.compute_similarity(
            p): p for p in PROFILES.values()}
        max_score = max(scored_profiles.keys())

        # If nothing matched, return BT.709 as it is the most common.
        # Otherwise return the highest ranking profile.
        profile = PROFILES["bt709"] if not max_score else scored_profiles[max_score]
        if not max_score:
            problems["profile"] = "Falling back to BT.709"
            return profile, problems

        # Fill in the range
        profile = Profile(profile.colourspace, profile.primaries, profile.transfer, range)

        problems["profile"] = "Using closest match"
        return profile, problems


PROFILES = {
    "bt470m":       Profile("smpte170m", "bt470m", "bt470m"),
    "bt470bg":      Profile("bt470bg", "bt470bg", "bt470bg"),
    "bt601-6-525":  Profile("smpte170m", "smpte170m", "smpte170m"),
    "bt601-6-625":  Profile("bt470bg", "bt470bg", "smpte170m"),
    "bt709":        Profile("bt709", "bt709", "bt709"),
    "smpte170m":    Profile("smpte170m", "smpte170m", "smpte170m"),
    "smpte240m":    Profile("smpte240m", "smpte240m", "smpte240m"),
    "bt2020":       Profile("bt2020ncl", "bt2020", "bt2020-10"),
}

DITHER = Filter.get_choices_for_option(NAME, "dither")

WHITE_POINT_ADAPTATION = Filter.get_choices_for_option(NAME, "wpadapt")


class ColourspaceFilter(Filter):
    def __init__(self, input, output, dither=None, white_point=None):
        self.input = input
        self.output = output
        self.dither = dither
        self.white_point = white_point

    @property
    def name(self):
        return NAME

    @property
    def params(self):
        params = {
            # input
            "ispace": self.input.colourspace,
            "iprimaries": self.input.primaries,
            "itrc": self.input.transfer,

            # output
            "space": self.output.colourspace,
            "primaries": self.output.primaries,
            "trc": self.output.transfer,

            # *fast* is always set to 0 (false), as it is output is useless,
            # as it is inaccurate.
            "fast": "0",
        }

        # not setting iall/all, as we specify space/primaries/trc directly

        # set optional params
        Filter.set_opt_param(params, "irange", self.input.range)
        Filter.set_opt_param(params, "range", self.output.range)
        Filter.set_opt_param(params, "dither", self.dither)
        Filter.set_opt_param(params, "wpadapt", self.white_point)

        # *format* is not supported as we are not interested in changing the frame format,
        # e.g. to yuv420p, yuv422p10, yuv444p12, etc. (all values are in YUV)

        return params
