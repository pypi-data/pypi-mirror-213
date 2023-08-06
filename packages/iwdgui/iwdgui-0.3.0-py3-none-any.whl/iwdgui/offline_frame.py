#!/usr/bin/python3
"""
iwd_offlineOffLineFrame_frame: code related to the connection frame
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import sys
from . import exitcodes

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

from .common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN

class OffLineFrame(Gtk.Frame):
    "Dummy frame, just a screen filler"

    def __init__(self, dev_name, advanced, mode):
        """Requires the device name,·
        and callbacks for nw_combo and hidden buttons"""
        print("OffLineFrame init")
        # construct frame
        Gtk.Frame.__init__(self,
                           label="Off line",
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        self._mode = mode
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.add(Gtk.Label())
        box.add(Gtk.Label())
        box.add(Gtk.Label())
        box.add(Gtk.Label())
        self.add(box)

    def get_mode(self):
        "returns the mode, in this case always pyiwd.OFFLINE_MODE"
        return self._mode

    def dbus_props_change(self, iface, path, name, value):
        pass

    def periodic_call(self):
        pass

    def set_advanced(self, flag):
        pass
