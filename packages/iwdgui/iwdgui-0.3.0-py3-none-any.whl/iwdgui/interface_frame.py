#!/usr/bin/python3
"""
iwd_interface_frame: code related to the interface frame
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import socket

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

from . import exitcodes
from .msg_window import show_error_message

try:
    from  netifaces import ifaddresses, AF_LINK, AF_INET, AF_INET6
except Exception as e:
    show_error_message("Please install netifaces", str(e),
                       exitcode=exitcodes.IMPORT_FAILED)


from . import pyiwd

from .common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, VALUE_LEN, RIGHT,\
    BOTTOM, GtkValueLabel, addln2grid

from .common_frame import Frame


# list of tuples to connect modes and radiobutton labels:
_RADIOBUTTON_MODES_AND_LABELS = [
    (pyiwd.OFFLINE_MODE, "Off"),
    (pyiwd.STATION_MODE, "Station"),
    (pyiwd.AD_HOC_MODE, "Ad-hoc"),
    (pyiwd.ACCESS_POINT_MODE, "Access Point")]


def get_netifaces_addr(iface, addr_type):

    try:
        addresses = ifaddresses(iface)[addr_type]
        return addresses
    except Exception as e:
        return None


class InterfaceFrame(Gtk.Frame):
    "Everything related to the interface frame"

    #def __init__(self, dev_name, mode_change_callback):
    def __init__(self, dev_name):
        self._vendor = GtkValueLabel()
        self._model = GtkValueLabel()
        self._ipv4_address = GtkValueLabel()
        self._ipv6_supoort = socket.has_ipv6
        self._dev_name = dev_name
        self._dev_path = pyiwd.dev_path_by_name(dev_name)
        if self._ipv6_supoort:
            self._ipv6_address = GtkValueLabel()
        self._adapter_dic = self._get_adapter_dic()

        print("Adapter:", self._adapter_dic)

        self._dev_dic = pyiwd.dev_dic_by_path(self._dev_path)
        self._mode = pyiwd.dev_mode_by_dic(self._dev_dic)

        # construct frame
        Gtk.Frame.__init__(self, label="Wireless interface",
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)

        self.supported_modes = self._adapter_dic['SupportedModes']
        self.supported_modes.append(pyiwd.OFFLINE_MODE)
        radiobox = Gtk.Box()
        button = None
        self.radiobutton = {}
        for mode, label in _RADIOBUTTON_MODES_AND_LABELS:
            if mode in self.supported_modes:
                button = Gtk.RadioButton.new_with_label_from_widget(button,
                                                                    label)
                if self._mode == mode:
                    button.set_active(True)
                button.connect("toggled", self._mode_toggled, mode)
                radiobox.pack_start(button, False, False, 4)
                self.radiobutton[mode] = button

        ln = addln2grid(grid, None, "Mode", radiobox)
        ln = addln2grid(grid, ln, "Vendor", self._vendor)
        self.set_vendor_name(self._adapter_dic['Vendor'])
        ln = addln2grid(grid, ln, "Model", self._model)
        try:
            self.set_model_name(self._adapter_dic["Model"])
        except Exception as e:
            print("No model information for adapter, error:", e)
        ln = addln2grid(grid, ln, "IPv4 address", self._ipv4_address)
        if self._ipv6_supoort:
            ln = addln2grid(grid, ln, "IPv6 address", self._ipv6_address)
        self.update_ip_addresses()
        self.add(grid)

    def _mode_toggled(self, widget, mode):
        if widget.get_active():
            pyiwd.dev_set_mode(self._dev_path, mode)

    def set_mode(self, mode):
        if mode in self.supported_modes:
            self._mode = mode
            self.radiobutton[mode].set_active(True)
        else:
            print("Device", self._dev_name, "does not support mode", mode)

    def get_mode(self):
        return self._mode

    def get_dev_path(self):
        return self._dev_path

    def _get_adapter_dic(self):
        adapter_dic = pyiwd.adapter_dic_by_devname(self._dev_name)
        return adapter_dic

    def set_vendor_name(self, vendor):
        self._vendor.set_text(vendor[:VALUE_LEN])

    def set_model_name(self, model):
        self._model.set_text(model[:VALUE_LEN])

    def set_ipv4_address(self, ipv4_address):
        self._ipv4_address.set_text(ipv4_address)
        return ipv4_address

    def set_ipv6_address(self, ipv6_address):
        if self._ipv6_supoort:
            self._ipv6_address.set_text(ipv6_address)
        return ipv6_address

    def update_ipvX_address(self, family, update_fn):
        "Updates an IPv4/6 addr, requires a family and an update function"
        ip_addr_lst = get_netifaces_addr(self._dev_name, family)
        update_fn(ip_addr_lst[0]['addr'] if ip_addr_lst else "")

    def update_ipv4_address(self):
        self.update_ipvX_address(AF_INET, self.set_ipv4_address)

    def update_ipv6_address(self):
        if self._ipv6_supoort:
            self.update_ipvX_address(AF_INET6, self.set_ipv6_address)

    def update_ip_addresses(self):
        self.update_ipv4_address()
        if self._ipv6_supoort:
            self.update_ipv6_address()

    def dbus_props_change(self, iface, path, name, value):
        pass




class if_handling():
    "Class controling the interface handling"

    def __init__(self, dev_name, frame):
        self._frame = frame
        self._dev_name = dev_name

    def _mode_toggled(self, widget, mode):
        if widget.get_active():
            pyiwd.dev_set_mode(self._dev_path, mode)

    def set_mode(self, mode):
        if mode in self.supported_modes:
            self._mode = mode
            self.radiobutton[mode].set_active(True)
        else:
            print("Device", self._dev_name, "does not support mode", mode)

    def get_mode(self):
        return self._mode

    def get_dev_path(self):
        return self._dev_path

    def _get_adapter_dic(self):
        adapter_dic = pyiwd.adapter_dic_by_devname(self._dev_name)
        return adapter_dic

    def set_vendor_name(self, vendor):
        self._vendor.set_text(vendor[:VALUE_LEN])

    def set_model_name(self, model):
        self._model.set_text(model[:VALUE_LEN])

    def set_ipv4_address(self, ipv4_address):
        self._ipv4_address.set_text(ipv4_address)
        return ipv4_address

    def set_ipv6_address(self, ipv6_address):
        if self._ipv6_supoort:
            self._ipv6_address.set_text(ipv6_address)
        return ipv6_address

    def update_ipvX_address(self, family, update_fn):
        "Updates an IPv4/6 addr, requires a family and an update function"
        ip_addr_lst = get_netifaces_addr(self._dev_name, family)
        update_fn(ip_addr_lst[0]['addr'] if ip_addr_lst else "")

    def update_ipv4_address(self):
        self.update_ipvX_address(AF_INET, self.set_ipv4_address)

    def update_ipv6_address(self):
        if self._ipv6_supoort:
            self.update_ipvX_address(AF_INET6, self.set_ipv6_address)

    def update_ip_addresses(self):
        self.update_ipv4_address()
        if self._ipv6_supoort:
            self.update_ipv6_address()

    def dbus_props_change(self, iface, path, name, value):
        pass



