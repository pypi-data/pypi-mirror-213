# Copyright (C) 2023, Svetlin Ankov, Simona Dimitrova

import os
import wx

from colourspace.av.filter.colourspace import PROFILES, COLOURSPACES, PRIMARIES, TRANSFERS, RANGES, Profile


class ColourspaceDialog(wx.Dialog):
    def __init__(self, video, input, *args, **kw):
        super().__init__(*args, **kw)

        if input:
            self._profile = video.input_profile
            self._default_profile, self._profile_errors = Profile.from_stream(video)
            self.SetTitle(f"Input profile ({os.path.basename(video.container.filename)})")
        else:
            self._profile = video.output_profile
            self._default_profile = PROFILES["bt709"]
            self._profile_errors = {}
            self.SetTitle("Output profile")

        sizer = wx.BoxSizer(wx.VERTICAL)

        def add_choice(name, choices, handler, parent, sizer, error_key=None):
            # label
            label = wx.StaticText(parent, label=name)
            sizer.Add(label, 0, wx.ALL, 5)

            # choices
            sizer_ = wx.BoxSizer(wx.HORIZONTAL)

            choices = wx.Choice(parent, choices=choices)
            choices.SetSelection(0)
            choices.Bind(wx.EVT_CHOICE, handler)
            sizer_.Add(choices, 1, wx.ALL | wx.EXPAND, 5)

            if error_key and (error_key in self._profile_errors):
                profile_warning = wx.StaticText(parent, label="\u26A0")
                profile_warning.SetBackgroundColour((255, 255, 0))
                profile_warning.SetForegroundColour((0, 0, 0))
                profile_warning.SetToolTip(self._profile_errors[error_key])
                sizer_.Add(profile_warning, 0, wx.ALL, 5)

            sizer.Add(sizer_, 0, wx.EXPAND, 5)

            return choices

        self._profiles = add_choice("Profile", ["Custom"] + list(PROFILES.keys()),
                                    self._on_profile, self, sizer, "profile")

        advanced = wx.CollapsiblePane(self, wx.ID_ANY, "Advanced", wx.DefaultPosition,
                                      wx.DefaultSize, wx.CP_DEFAULT_STYLE)
        advanced.Collapse(self._profile.name != "Custom")
        sizer_advanced = wx.BoxSizer(wx.VERTICAL)

        self._colourspaces = add_choice("Colour Space", COLOURSPACES,
                                        self._on_colourspace, advanced.GetPane(), sizer_advanced, "colourspace")
        self._primaries = add_choice("Primaries", PRIMARIES, self._on_primaries,
                                     advanced.GetPane(), sizer_advanced, "primaries")
        self._transfers = add_choice("Transfer", TRANSFERS, self._on_transfer,
                                     advanced.GetPane(), sizer_advanced, "transfer")
        self._ranges = add_choice("Range", ["Ignore"] + RANGES, self._on_range,
                                  advanced.GetPane(), sizer_advanced, "range")

        advanced.GetPane().SetSizer(sizer_advanced)
        advanced.GetPane().Layout()
        sizer_advanced.Fit(advanced.GetPane())
        sizer.Add(advanced, 1, wx.EXPAND | wx.ALL, 5)

        # buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        button_ok = wx.Button(self, wx.ID_OK)
        button_ok.SetDefault()
        button_ok.SetFocus()
        button_sizer.Add(button_ok, 0, wx.ALL, 5)

        button_cancel = wx.Button(self, wx.ID_CANCEL)
        button_sizer.Add(button_cancel, 0, wx.ALL, 5)

        button_reset = wx.Button(self, wx.ID_DEFAULT, "Default")
        button_reset.Bind(wx.EVT_BUTTON, self._on_reset)
        button_sizer.Add(button_reset, 0, wx.ALL, 5)

        sizer.Add(button_sizer, 0, wx.EXPAND, 5)

        self._update_from_profile()

        # fix up the frame
        self.SetSizeHints(wx.Size(200, 100), wx.DefaultSize)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

        self.Centre(wx.BOTH)

    def _update_from_profile(self):
        # Profile name
        idx = self._profiles.FindString(self._profile.name)
        self._profiles.SetSelection(idx)

        # Colourspace
        idx = self._colourspaces.FindString(self._profile.colourspace)
        self._colourspaces.SetSelection(idx)

        # Primaries
        idx = self._primaries.FindString(self._profile.primaries)
        self._primaries.SetSelection(idx)

        # Transfer characteristic
        idx = self._transfers.FindString(self._profile.transfer)
        self._transfers.SetSelection(idx)

        # Range
        idx = self._ranges.FindString(self._profile.range) if self._profile.range else 0
        self._ranges.SetSelection(idx)

    def _on_profile(self, event):
        profile = self._profiles.GetString(self._profiles.GetSelection())

        if profile != "Custom":
            self._profile = PROFILES[profile]

        self._update_from_profile()

    def _on_colourspace(self, event):
        colourspace = self._colourspaces.GetString(self._colourspaces.GetSelection())
        self._profile = Profile(colourspace, self._profile.primaries, self._profile.transfer, self._profile.range)
        self._update_from_profile()

    def _on_primaries(self, event):
        primaries = self._primaries.GetString(self._primaries.GetSelection())
        self._profile = Profile(self._profile.colourspace, primaries, self._profile.transfer, self._profile.range)
        self._update_from_profile()

    def _on_transfer(self, event):
        transfer = self._transfers.GetString(self._transfers.GetSelection())
        self._profile = Profile(self._profile.colourspace, self._profile.primaries, transfer, self._profile.range)
        self._update_from_profile()

    def _on_range(self, event):
        range = self._ranges.GetString(self._ranges.GetSelection())
        if range == "Ignore":
            range = None

        self._profile = Profile(self._profile.colourspace, self._profile.primaries, self._profile.transfer, range)
        self._update_from_profile()

    def _on_reset(self, event):
        self._profile = self._default_profile
        self._update_from_profile()

    @property
    def Profile(self):
        return self._profile
