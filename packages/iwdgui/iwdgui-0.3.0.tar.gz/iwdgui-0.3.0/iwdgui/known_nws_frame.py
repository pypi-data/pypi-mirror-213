#!/usr/bin/python3
"""
iwd_known_networks_frame: code related to the known networks  frame
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

from datetime import datetime

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)


from . import pyiwd
from .comboboxtext import ComboBoxText
from .common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, RIGHT, BOTTOM, \
    GtkValueLabel, addln2grid
from .profile_store import ap_store, adhoc_store

_framelabel_dic = {
    pyiwd.STATION_MODE: "Known networks",
    pyiwd.AD_HOC_MODE: "Known adhoc networks",
    pyiwd.ACCESS_POINT_MODE: "Known access point names",
    pyiwd.OFFLINE_MODE: "known networks" }


def security_str(sec_str):
    "convert pwd to preshared key"
    result = {
        "psk" : "Pre-shared key",
        "open" : "Open",
        "8021x" : "Enterprise"
    }
    try:
        return result[sec_str]
    except KeyError:
        pass
    except Exception as e:
       sys.stderr.write("security_str, unexpected error:", e)
    return sec_str

def localdatetime(ISO_8601_str):
    "Convert an ISO_8601 time string to a local time string"
    dt_utc = datetime.fromisoformat(ISO_8601_str[:-1]+"+00:00")
    dt_tz = dt_utc.astimezone()
    return dt_tz.strftime("%c")

def try_update_text_label(label_widget, dic, field):
    "Tries to set a label_widget to dic[field], or blank on failure"
    try:
        if type(dic[field]) == str:
            strval = dic[field]
        else:
            strval = "Yes" if dic[field] else "No"
        label_widget.set_text(strval)
    except (TypeError, KeyError):
        label_widget.set_text("")

def try_update_checkbox(checkbox_widget, dic, field):
    try:
        checkbox_widget.set_active(dic[field])
    except (TypeError, KeyError):
        checkbox_widget.set_active(False)


class KnownNetworksFrame(Gtk.Frame):
    " Everythng thing to do with the known networks frame"

    def __init__(self):
        self.mode = pyiwd.STATION_MODE
        self.known_network_combo = ComboBoxText()
        self.last_connected = GtkValueLabel()
        self.auto_connect = Gtk.CheckButton()
        self.known_nw_security = GtkValueLabel()
        self.hidden = GtkValueLabel()
        self.forget_network_button = Gtk.Button(label="Forget")

        Gtk.Frame.__init__(self, label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                                       column_spacing=GRID_COL_SPACING,
                                       margin=GRID_MARGIN)
        grid.attach_next_to(self.known_network_combo,
                                          None,
                                          Gtk.PositionType.BOTTOM, 2, 1)
        self.populate_known_network_combo_box()
        self.known_network_combo.connect(
            "changed", self.known_networks_combo_changed)
        ln = self.known_network_combo
        ln = addln2grid(grid, ln,
                        "Last connected", self.last_connected)
        ln = addln2grid(grid, ln,
                        "Auto connect", self.auto_connect)
        self.auto_connect.connect("toggled", self.auto_connect_toggled)
        ln = addln2grid(grid, ln,
                        "Security", self.known_nw_security)
        ln = addln2grid(grid, ln, "Hidden", self.hidden)
        button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button_box.pack_end(self.forget_network_button, False, True, 0)
        grid.attach_next_to(button_box, self.hidden,
                                           Gtk.PositionType.BOTTOM, 1, 1)
        self.forget_network_button.connect("clicked", self.forget_network)
        self.add(grid)
        ap_store.add_callback(self.ap_profile_dir_changed)

    def ap_profile_dir_changed(self):
        "Callback function when the ap_store profile dir has changed"
        if self.mode == pyiwd.ACCESS_POINT_MODE:
            old_profile = self.known_network_combo.get_active_text()
            self.populate_known_network_combo_box()

    def set_mode(self, mode):
        "Called for mode change"
        self.mode = mode
        self.set_label(_framelabel_dic[mode])
        self.populate_known_network_combo_box()
        return

    def populate_known_network_combo_box(self):
        if self.mode == pyiwd.AD_HOC_MODE:
            entries = adhoc_store.profile_list()
        elif self.mode == pyiwd.ACCESS_POINT_MODE:
            entries = ap_store.profile_list()
        else:
            known_networks = pyiwd.known_nw_list()
            entries = [nw["Name"] for nw in known_networks]
        self.known_network_combo.update_entries(entries)
        self.known_networks_combo_changed(self.known_network_combo)

    def get_known_nw_name(self):
        return self.known_network_combo.get_active_text()

    def known_networks_combo_changed(self, widget):
        self.update_known_nw_info()

    def update_known_nw_info(self):
        "Updates the info on a known network"
        if self.mode == pyiwd.AD_HOC_MODE:
            known_nw_dic = adhoc_store.read_profile(self.get_known_nw_name())
        elif self.mode == pyiwd.ACCESS_POINT_MODE:
            known_nw_dic = ap_store.read_profile(self.get_known_nw_name())
        else:
            known_nw_dic = pyiwd.known_nw_dic_by_name(self.get_known_nw_name())
        try_update_text_label(self.last_connected,
                              known_nw_dic,"LastConnectedTime")
        try_update_checkbox(self.auto_connect, known_nw_dic, "AutoConnect")
        try_update_text_label(self.known_nw_security, known_nw_dic, "Type")
        try_update_text_label(self.hidden, known_nw_dic, "Hidden")
        return

    def auto_connect_toggled(self, widget):
        "gets called when the autoconnect checkbox is toggled"
        autoconnect = widget.get_active()
        known_nw_name = self.known_network_combo.get_active_text()
        if self.mode == pyiwd.AD_HOC_MODE:
            profile = adhoc_store.read_profile(known_nw_name)
            profile["AutoConnect"] = autoconnect
            adhoc_store.store_profile(profile)
        elif self.mode == pyiwd.ACCESS_POINT_MODE:
            profile = ap_store.read_profile(known_nw_name)
            profile["AutoConnect"] = autoconnect
            ap_store.store_profile(profile)
        else:
            if known_nw_name:
                known_nw_path = pyiwd.known_nw_path_by_name(known_nw_name)
                pyiwd.known_nw_autoconnect(known_nw_path, autoconnect)
        self.update_known_nw_info()
        return True

    def forget_network(self, widget):
        known_nw_name = self.known_network_combo.get_active_text()
        if known_nw_name:
            if self.mode == pyiwd.AD_HOC_MODE:
                adhoc_store.rm_profile(known_nw_name)
            elif self.mode == pyiwd.ACCESS_POINT_MODE:
                ap_store.rm_profile(known_nw_name)
            else:
                known_nw_path = pyiwd.known_nw_path_by_name(known_nw_name)
                pyiwd.known_nw_forget(known_nw_path)
            self.populate_known_network_combo_box()

    def dbus_props_change(self, iface, path, name, value):
        if ((iface == "Network" and name == "KnownNetwork")
            or (iface == "KnownNetwork")):
            self.populate_known_network_combo_box()
            self.update_known_nw_info()


