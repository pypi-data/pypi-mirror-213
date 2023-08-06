#p_!/usr/bin/python3
"""
ap_frame:: code related to the connection frame
(c) 2021-203  Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import os
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

from . import nw_addr
from . import pyiwd
from . import entry
from .comboboxtext import ComboBoxText
from .common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, RIGHT, BOTTOM, \
    GtkValueLabel, addln2grid
from .profile_store import adhoc_store, ap_store

HOSTNAME = os.uname()[1]
INPUT_LEN = 34
NEW_CREATE_NEW_PROFILE = "[ Create new profile ]"

pstore = {pyiwd.ACCESS_POINT_MODE : ap_store,
          pyiwd.AD_HOC_MODE : adhoc_store}

a_dic_fn = {pyiwd.ACCESS_POINT_MODE : pyiwd.ap_dic_by_path,
            pyiwd.AD_HOC_MODE : pyiwd.adhoc_dic_by_path}

a_start_fn = {pyiwd.ACCESS_POINT_MODE : pyiwd.ap_start,
              pyiwd.AD_HOC_MODE : pyiwd.adhoc_start}

a_stop_fn = {pyiwd.ACCESS_POINT_MODE : pyiwd.ap_stop,
             pyiwd.AD_HOC_MODE : pyiwd.adhoc_stop}

a_frame_label = {pyiwd.ACCESS_POINT_MODE : "Access Point",
             pyiwd.AD_HOC_MODE : "Adhoc Network" }




#class AccessPointFrame(Gtk.Frame):
class Ap_And_Adhoc_Frame(Gtk.Frame):
    "Creates the frame for adhoc and access points.. quite the same really"

    def __init__(self, dev_name, advanced, mode):
        self._dev_name = dev_name
        self._advanced = advanced
        self._mode = mode
        self._passphrase = None
        self._dev_path = pyiwd.dev_path_by_name(dev_name)

        self._ap_combo = ComboBoxText()
        self._passphrase_entry = Gtk.Entry(
            xalign=0, width_chars=INPUT_LEN,
            visibility=False, editable=False)
        self._passphrase_entry.set_icon_from_icon_name(
            Gtk.EntryIconPosition(1), "dialog-password")
        self._passphrase_entry.connect(
            "icon-release", self._toggle_pw_visibility)
        dev_dic = pyiwd.dev_dic_by_name(self._dev_name)

        # construct frame
        Gtk.Frame.__init__(self,
                           label=a_frame_label[mode],
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)

        grid.attach_next_to(self._ap_combo, None,
                            Gtk.PositionType.BOTTOM, 2, 1)
        self._ap_combo.connect("changed", self.ac_combo_changed)
        self.populate_ac_combo()
        ln = self._ap_combo
        ln = addln2grid(grid, ln, "Passphrase", self._passphrase_entry)
        self.populate_frame()
        self.add(grid)
        self.check_nw_status()

        pstore[self._mode].add_callback(self.profile_dir_changed)

    def get_mode(self):
        "Returns the current mode"
        return self._mode

    def profile_dir_changed(self):
        "Callback function when the profile_store profile dir has changed"
        old_profile = self._ap_combo.get_active_text()
        self.populate_ac_combo()
        new_profile = self._ap_combo.get_active_text()
        if new_profile == NEW_CREATE_NEW_PROFILE:
            self.stop_ap()
        elif new_profile != old_profile:
            self.start_ap(new_profile)


    def check_nw_status(self):
        #ap_dic = pyiwd.ap_dic_by_path(self._dev_path)
        ap_dic = a_dic_fn[self._mode](self._dev_path)
        passphrase = None
        if ap_dic["Started"]:
            if self._mode == pyiwd.ACCESS_POINT_MODE:
                name = ap_dic["Name"]
            else:
                # kludge, the adhoc dic does not give the nw name
                name = self._ap_combo.get_active_text()
            if self._ap_combo.set_active_text(name):
                profile = pstore[self._mode].read_profile(name)
                if profile:
                    self._passphrase = profile["Passphrase"]
            else:
                passphrase = entry.show_password_entry_window(ap_dic["Name"])
                if len(passphrase) > 0:
                    self._passphrase = passphrase
                    profile = {
                        "Name" : ap_dic["Name"],
                        "Passphrase": passphrase,
                        "AutoConnect" : True }
                    pstore[self._mode].store_profile(profile)
            self._passphrase_entry.set_text(self._passphrase)
        else:
            entries = self._ap_combo.entries()
            if entries[0] != NEW_CREATE_NEW_PROFILE:
                self.start_ap(entries[0])

    def _toggle_pw_visibility(self, widget, icon_pos, event):
        "Called when the visibility icon is clicked:"
        visib = widget.get_visibility()
        widget.set_visibility(not visib)

    def set_advanced(self, flag):
        self._advanced = flag
        self.populate_frame()

    def populate_ac_combo(self):
        entries = pstore[self._mode].profile_list()
        entries.append(NEW_CREATE_NEW_PROFILE)
        self._ap_combo.update_entries(entries)
        if len(entries) == 1:
            self.create_new_profile()

    def ac_combo_changed(self, widget):
        entry = widget.get_active_text()
        if entry == NEW_CREATE_NEW_PROFILE:
            self.create_new_profile()
        else:
            self.start_ap(entry)

    def start_ap(self, nw_name):
        profile = pstore[self._mode].read_profile(nw_name)
        if profile:
            self.stop_ap()
            self.nw_name = profile["Name"]
            self._passphrase = profile["Passphrase"]
            #pyiwd.ap_start(self._dev_path, self.nw_name, self._passphrase,
            #               callback = self.start_callback)
            a_start_fn[self._mode](self._dev_path, self.nw_name,
                                  self._passphrase,
                                  callback = self.start_callback)
        else:
            print("Could not retrieve profile")

    def start_callback(self, error):
        if error and self._mode == pyiwd.ACCESS_POINT_MODE:
            print("Access point start error: ", error)
        else:
            pstore[self._mode].touch(self.nw_name)
            self.populate_ac_combo()
            self._passphrase_entry.set_visibility(False)
            self._passphrase_entry.set_text(self._passphrase)

    def create_new_profile(self):
        ap_name, passphrase, _ = entry.show_start_ap_window(HOSTNAME)
        ap_dic = {"Name" : ap_name,
                  "Passphrase" : passphrase,
                  "AutoConnect" : True}
        pstore[self._mode].store_profile(ap_dic)
        self.populate_ac_combo()
        self._ap_combo.set_active_text(ap_name)
        self.start_ap(self._ap_combo.get_active_text())

    def populate_frame(self):
        try:
            ap_dic = a_dic_fn[self._mode](self._dev_path)
            if ap_dic['Started']:
                if self._passphrase:
                    self._passphrase_entry.set_text(self._passphrase)
                else:
                    self._passphrase_entry.set_text("(unknown)")

        except Exception as e:
            print("AP populate_frame, coul not get ap_dic:", e)
            #self._access_point_label.set_text("")
            #self._station_count_label.set_text("0")

    def stop_ap(self):
        "Called to stop an access point"
        #pyiwd.ap_stop(self._dev_path)
        a_stop_fn[self._mode](self._dev_path)

    def dbus_props_change(self, iface, path, name, value):
        if path == self._dev_path and iface == "AccessPoint":
            self.populate_frame()


    def periodic_call(self):
        "Called every xx (10) seconds"
        #self.populate_frame()
        pass



