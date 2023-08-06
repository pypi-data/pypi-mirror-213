#!/usr/bin/python3
"""
iwd_connection_frame: code related to the connection frame
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

from . import pyiwd
from . import entry
from . import notify
from .msg_window import show_error_message, show_info_message
from .comboboxtext import ComboBoxText
from .wifi import wifi_channel, wifi_band, wifi_generation, \
    wifi_signal_strength
from .common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, RIGHT, BOTTOM, \
    GtkValueLabel, addln2grid


# special strings for the nw select combobox
CONNECT_HIDDEN_NW   = "[ Connect to hidden network ]"
CONNECT_PIN         = "[ Connect with PIN entry] ]"
CONNECT_PUSH_BUTTON = "[ Connect with push button ]"

#shorthand to avoid checking if a key is in a dic each time
dicstr = lambda dic, key: dic[key] if key in dic else ""
dicint = lambda dic, key: dic[key] if key in dic else 0

connection_str = lambda b: "Connected" if b else "Not connected"


class StationFrame(Gtk.Frame):
    "Everything related to the interface frame"

    #def __init__(self, dev_name, advanced, on_line):
    def __init__(self, dev_name, advanced, mode):
        "Requires the device name,·nd if we're in advanced mode"
        self._mode = mode
        self._nw_combo = ComboBoxText()
        self._access_point_label = GtkValueLabel()
        self._radio_label = GtkValueLabel()
        self._signal_label = GtkValueLabel()
        self._sec_label = GtkValueLabel()
        #self._connect_hidden_button = Gtk.Button(label="Connect hidden")
        self._dev_name = dev_name
        self._dev_path = pyiwd.dev_path_by_name(dev_name)
        self._advanced = advanced
        #self._on_line = on_line

        # construct frame
        Gtk.Frame.__init__(self,
                           label="Active connection",
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)
        grid.attach_next_to(self._nw_combo, None,
                            Gtk.PositionType.BOTTOM, 2, 1)
        self._nw_combo.connect("changed", self.nw_combo_changed)
        self.populate_nw_combo()
        self.update_nw_props(new_dev_name = dev_name)
        ln = self._nw_combo
        ln = addln2grid(grid, ln, "Access point", self._access_point_label)
        ln = addln2grid(grid, ln, "Radio", self._radio_label)
        ln = addln2grid(grid, ln, "Signal ", self._signal_label)
        ln = addln2grid(grid, ln, "Security", self._sec_label)
        self.add(grid)

    def get_mode(self):
        "returns the interface mode, in this case always pyiwd.STATION_MODE"
        return self._mode

    def set_advanced(self, flag):
        self._advanced = flag
        self.update_nw_props()

    def get_ssid(self):
        return self._nw_combo.get_active_text()

    def _update_nw_combo(self, nw_name):
        "selects an entry in the nw_combo, adds it if needed"
        if not nw_name in self._nw_combo.entries():
            self._nw_combo.insert_text_sorted(nw_name)
        self._nw_combo.set_active_text(nw_name)

    def populate_nw_combo(self):
        current_nw_name = self.get_ssid()
        station_nw_name_list = pyiwd.station_nw_name_list(self._dev_path)
        station_nw_name_list.append(CONNECT_HIDDEN_NW)
        station_nw_name_list.append(CONNECT_PIN)
        station_nw_name_list.append(CONNECT_PUSH_BUTTON)
        self._nw_combo.update_entries(station_nw_name_list)

    def set_ap_label(self, text):
        self._access_point_label.set_text(text if text else "")

    def set_radio_label(self, text):
        self._radio_label.set_text(text if text else "")

    def set_signal_label(self, text):
        self._signal_label.set_text(text if text else "")

    def set_sec_label(self, text):
        self._sec_label.set_text(text if text else "")

    def _ap_str(self, nw_dic, diags):
        ssid = dicstr(nw_dic,'Name') if nw_dic else ""
        if len(ssid) > 0:
            if diags and self._advanced:
                retstr = "SSID: " + ssid
                retstr += ", BSSID: " + dicstr(diags, "ConnectedBss")
            else:
                retstr = ssid
        else:
            retstr = "-"
        return retstr

    def _radio_str(self, nw_dic, diags):

        standard = band = ""
        generation = frequency = channel = 0
        if diags:
            standard = dicstr(diags, "RxMode")
            frequency = dicint(diags, "Frequency")
            if frequency:
                band = wifi_band(frequency)
                channel = wifi_channel(frequency)
            if len(standard) > 0:
                generation = wifi_generation(standard_802=standard)
            elif len(band) > 0:
                generation = wifi_generation(freq_band=band)
            # continue below...
        elif nw_dic and nw_dic['Connected']:
            return "Connected"
        else:
            return "-"

        retstr = "WiFi-" + str(generation) if generation else ""
        if self._advanced:
            if len(band) > 0:
                retstr += ", " + band
            if len(standard) > 0:
                retstr += ", " + standard
            if channel > 0:
                retstr += ", channel " + str(channel)
        return retstr

    def _signal_str(self, nw_dic, diags):
        sig_strength = None
        retstr = "-"
        if diags:
            sig_strength = dicint(diags,"RSSI")
        elif nw_dic:
            nw_path = dicstr(nw_dic, "KnownNetwork") 
            if len(nw_path) > 0:
                sig_strength = pyiwd.station_rssi(
                    self._dev_path, nw_dic["KnownNetwork"])
                if sig_strength:
                    sig_strength = round(sig_strength/100)

        if sig_strength:
            desc, pos = wifi_signal_strength(sig_strength)
            retstr = desc
            if self._advanced:
                retstr += ", " + str(-sig_strength) + " dBm"
                if diags:
                    rx = round(dicint(diags,"RxBitrate")/10)
                    tx = round(dicint(diags,"TxBitrate")/10)
                    if rx > 0:
                        retstr += ", Rx " + str(rx) + " Mbps"
                    if tx > 0:
                        retstr += ", Tx " + str(tx) + " Mbps"
        return retstr

    def _sec_str(self, nw_dic, diags):
        if diags:
            return dicstr(diags, "Security")
        elif nw_dic:
            return dicstr(nw_dic, 'Type')
        else:
            return "-"

    def update_nw_props(self, new_dev_name = None):
        if new_dev_name:
            self._dev_name = new_dev_name
        nw_dic = diags = None
        # get data
        try:
            nw_dic = pyiwd.nw_dic_connected_to_dev(self._dev_name)
            if nw_dic and nw_dic["Name"] != self.get_ssid():
                self._update_nw_combo(nw_dic["Name"])
        except Exception as e:
            pass
        try:
            diags = pyiwd.station_diagnostics(self._dev_path)
        except Exception as e:
            pass
        self.set_ap_label(self._ap_str(nw_dic, diags))
        self.set_radio_label(self._radio_str(nw_dic, diags))
        self.set_signal_label(self._signal_str(nw_dic, diags))
        self.set_sec_label(self._sec_str(nw_dic, diags))

    def set_ssid(self, ssid):
        "Selects a ssid, inserts it in the combobox if needed"
        if ssid in self._nw_combo.entries():
            self._nw_combo.set_active_text(ssid)
        else:
            self._nw_combo.insert_text(0, None, ssid)
            self._nw_combo.set_active(0)


    def nw_combo_changed(self, widget):
        nw_name = self.get_ssid()
        if nw_name == CONNECT_HIDDEN_NW:
            self.connect_hidden()
        elif nw_name == CONNECT_PIN:
            self.connect_pin()
        elif nw_name == CONNECT_PUSH_BUTTON:
            self.connect_push_button()
        else:
            self.connect_network(self.get_ssid())

    def connect_network(self, nw_name):
        "Connects to the selected network, when on-line"
        nw_path = pyiwd.nw_path_by_name(nw_name)
        #if self._on_line and nw_path:
        if True:
            self.set_ap_label("Connecting")
            pyiwd.nw_connect(nw_path, callback = self.connect_callback)

    def connect_callback(self, error):
        if error:
            print("connect_error_handler", error)

    def connect_pin(self):
        show_info_message("Connect PIN not yet implemement", "")

    def connect_push_button(self):
        show_info_message("Connect push button not yet implemement", "")

    def connect_hidden(self):
        entries = entry.show_hidden_essid_entry_window()
        if not entries:
            return
        nw_name = entries[0]
        nw_passphrase = entries[1]
        self.set_ap_label("Connecting")
        self.set_signal_label("")
        self.set_sec_label("")
        pyiwd.agent.set_passphrase(nw_name, nw_passphrase)
        pyiwd.station_connect_hidden_nw(
            self._dev_path, nw_name, callback=self.connect_hidden_callback)


    def connect_hidden_callback(self, error):
        self.update_nw_props()
        if error:
            dbus_error = error.get_dbus_name()
            try:
                error_msg = {
                    "net.connman.iwd.Failed" : "Connection failed",
                    "net.connman.iwd.NotFound" : "Hidden network not found",
                    "net.connman.iwd.NotHidden" : "Network is not hidden",
                    "net.connman.iwd.NotConnected" : "Not connected",
                    "net.connman.iwd.InvalidFormat" : "Wrong password",
                    "net.connman.iwd.NotConfigured" : "Not configured",
                    "net.connman.iwd.InvalidArguments" : "Wrong password",
                    "net.connman.iwd.ServiceSetOverlap":"Multiple networks found",
                    "net.connman.iwd.AlreadyProvisioned" : "Network already known"
                }[dbus_error]
            except KeyError:
                sys.stderr.write("hidden_connect_error_handler KeyError:"
                                 + dbus_error)
                error_msg = error.get_dbus_message()
            except Exception as e:
                sys.stderr.write("hidden_connect_error_handler error:", e)
                error_msg = error.get_dbus_message()
            show_error_message(
                "Connect to hidden network failed",
                [error_msg, "(IWD/D-Bus error: "+error.get_dbus_message()+")"])

    def periodic_call(self):
        "function to initiate scanning every x seconds, and update nw_props"
        try:
            pyiwd.station_scan(self._dev_path)
        except Exception as e:
            print("start_scanning error:", e)
            pass
        self.update_nw_props()

    def dbus_props_change(self, iface, path, name, value):
        "Handle iwd change notifications for station mode"

        if iface == "Station":
            if name == "State":
                self.set_ap_label(value)
                if value == "disconnected":
                    notify.msg(self._dev_name + " disconnected")
                elif value == "connected":
                    self.update_nw_props()
            elif name == "Connected":
                self.set_ap_label(connection_str(value))
            elif name == "ConnectedNetwork":
                network = pyiwd.nw_dic_by_path(value)
                self.update_nw_props()
                notify.msg(self._dev_name
                           + " connected to network "
                           + network["Name"])
            elif name == "Scanning" and not value:
                self.populate_nw_combo()
        elif iface == "Network" and  name == "Connected":
            self.set_ap_label( connection_str(value))

