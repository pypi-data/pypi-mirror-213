#!/usr/bin/env python3

"""
Iwdgui: A graphical frontend for iwd, Intel's iNet Wireless Daemon
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

import sys
import signal
import bisect

from . import exitcodes

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gio
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

# own application packages
from .msg_window import show_error_message, show_info_message
from . import pyiwd
from . import entry
#from .icon import icon_path
#from . import notify
from .menu import IwdMenu
from .interface_frame import InterfaceFrame
from .station_frame import StationFrame
#from .adhoc_frame import AdHocFrame
from .ap_frame import Ap_And_Adhoc_Frame
from .offline_frame import OffLineFrame
from .known_nws_frame import KnownNetworksFrame

APPLICATION_ID = "com.gitlab.hfernh.iwdgui"
PERIODIC_TICK = 15                     # call every so often in seconds


def sigint_handler(sig, frame):      # frame is stack frame, and is ignored
    """ Signal handler for SIGINT, or Ctrl-C,
    to avoid standard Python stack dump """
    toplevels = Gtk.Window.list_toplevels()
    for toplevel in toplevels:
        toplevel.destroy()


class IwdGuiWin(Gtk.Window):
    """ this is the main window of iwdgui """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(150, 100)
        self.set_transient_for(None)
        self.set_keep_above(True)
        self.connect("destroy", self.close_window)
        self.tab= {}
        self.if_frame = {}
        self.conn_frame = {}
        self.conn_box = {}
        pyiwd.agent.set_passwd_entry_callback(self.passwd_entry_callback)
        pyiwd.agent.set_release_callback(self.agent_released)

        # construct window
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.menu = IwdMenu(self.advanced_callback, self.close_window)
        box.pack_start(self.menu, False, False, 0)
        box.pack_start(Gtk.Label(), False, False, 0)
        self.dev_notebook = Gtk.Notebook()
        self.dev_name_list = []
        for dev_name in pyiwd.dev_name_list():
            self.add_dev_tab(dev_name)
        self.dev_notebook.set_current_page(0)
        self.dev_notebook.connect("switch-page", self.dev_nb_page_switch)
        box.pack_start(self.dev_notebook, False, False, 0)

        mode = self.if_frame[self.dev_name_list[0]].get_mode()
        self.known_nws_frame = KnownNetworksFrame()
        self.known_nws_frame.set_mode(mode)
        box.pack_start(self.known_nws_frame, False, False, 0)

        self.add(box)
        pyiwd.register_props_changed_callback(
            self.handle_dbus_signal_properties_changed)
        GLib.timeout_add_seconds(PERIODIC_TICK, self.periodic_props_update)
        self.show_all()

    def dev_nb_page_switch(self, notebook, box, pagenr):
        "Called when when the device"
        dev_name = self.dev_name_list[pagenr]
        mode = self.if_frame[dev_name].get_mode()
        self.known_nws_frame.set_mode(mode)

    def construct_conn_frame(self, dev_name, mode):
        dic = {
            pyiwd.STATION_MODE: StationFrame,
            pyiwd.AD_HOC_MODE: Ap_And_Adhoc_Frame,
            pyiwd.ACCESS_POINT_MODE: Ap_And_Adhoc_Frame,
            pyiwd.OFFLINE_MODE: OffLineFrame}
        return dic[mode](dev_name, self.get_advanced(), mode)

    def add_dev_tab(self, dev_name):
        "Adds a tab for a device"
        dev_dic = pyiwd.dev_dic_by_name(dev_name)
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.pack_start(Gtk.Label(), False, False, 0)
        self.if_frame[dev_name] = InterfaceFrame(dev_name)
        box.pack_start(self.if_frame[dev_name], False, False, 0)
        box.pack_start(Gtk.Label(), False, False, 0)
        mode = pyiwd.dev_mode_by_dic(dev_dic)
        self.conn_frame[dev_name] = self.construct_conn_frame(dev_name, mode)
        self.conn_box[dev_name] = Gtk.Box()
        self.conn_box[dev_name].add(self.conn_frame[dev_name])
        box.pack_start(self.conn_box[dev_name], False, False, 0)
        box.pack_end(Gtk.Label(), False, False, 0)
        pos = bisect.bisect_right(self.dev_name_list, dev_name)
        self.tab[dev_name] = box
        self.dev_notebook.insert_page(self.tab[dev_name],
                                  Gtk.Label(dev_name), pos)
        self.dev_notebook.show_all()
        self.dev_name_list.insert(pos, dev_name)

    def dev_path(self, dev_name):
        #return pyiwd.dev_path_by_name(self.dev_name())
        return self.if_frame[dev_name].get_dev_path()

    def nw_name(self, dev_name):
        #return self.conn_frame.get_ssid()
        return self.conn_frame[dev_name].get_ssid()

    def nw_path(self, dev_name):
        return pyiwd.nw_path_by_name(self.nw_name(dev_name))

    def connected(self, dev_name):
        "Checks if we are connected to a network"
        nw_dic = pyiwd.nw_dic_connected_to_dev(self.dev_path(dev_name))
        return nw_dic != None

    def advanced_callback(self):
        "Switches between basic and advanced view modes"
        #widget is a menuiten, it's child is a checkbutton
        adv = self.get_advanced()
        for dev_name in self.dev_name_list:
            self.conn_frame[dev_name].set_advanced(adv)

    def get_advanced(self):
        return self.menu.get_advanced_view()

    def dev_tab_admin_check(self, dev_name):
        """Creates tab for unknown devices
        - deletes them for devices
        - that do not exist anymore or have a wrong type
        - creates a new tab if deleted because it was the wrong type
        - returns None if the dev_name is no longer valid,
          otherwise dev_name"""

        if dev_name in self.dev_name_list:              # in our admin
            if not dev_name in pyiwd.dev_name_list():   # bur for real
                #remove device tab
                for widget_dic in [self.if_frame, self.conn_frame, self.tab]:
                    widget_dic[dev_name].destroy()
                    widget_dic.pop(dev_name)
                self.dev_name_list.remove(dev_name)
                return None
        else:
            self.add_dev_tab(dev_name)
        return dev_name


    def dev_check(self, iface, path):
        dev_name = None
        dev_path = {"AdHoc" : path,
                    "Device" : path,
                    "Station" : path,
                    "AccessPoint" : path,
                    "Network" : pyiwd.nw_devpath_by_nwpath(path),
                    "KnownNetwork" : None}[iface]
        if dev_path:
            try:
                dev_name = pyiwd.dev_name_by_path(dev_path)
            except Exception as e:
                print("dev_check, could not get dev_name for:", dev_path,
                      "error: ", e)
        if dev_name:
            dev_name = self.dev_tab_admin_check(dev_name)
            if dev_name:
                """
                frame2mode = {
                    OffLineFrame : pyiwd.OFFLINE_MODE,
                    StationFrame : pyiwd.STATION_MODE,
                    AdHocFrame : pyiwd.AD_HOC_MODE,
                    AccessPointFrame : pyiwd.ACCESS_POINT_MODE}
                tab_mode = frame2mode[type(self.conn_frame[dev_name])]
                """
                tab_mode = self.conn_frame[dev_name].get_mode()
                real_mode = pyiwd.dev_mode(dev_path)
                if tab_mode != real_mode:
                    current_page_nr = self.dev_notebook.get_current_page()
                    current_dev_name = self.dev_name_list[current_page_nr]
                    self.conn_frame[dev_name].destroy()
                    self.conn_frame[dev_name] = self.construct_conn_frame(
                        dev_name, real_mode)
                    self.conn_box[dev_name].add(self.conn_frame[dev_name])
                    self.conn_box[dev_name].show_all()

                    new_current_page_nr = self.dev_name_list.index(
                        current_dev_name)
                    self.dev_notebook.set_current_page(new_current_page_nr)
                    self.known_nws_frame.set_mode(real_mode)
        return dev_name, dev_path 


    def handle_dbus_signal_properties_changed(self, interface,
                                             changed, invalidated, path):
        iface = interface[interface.rfind(".") + 1:]
        dev_name, dev_path = self.dev_check(iface, path)
        if dev_name:
            for name, value in changed.items():
                print("{%s} [%s] %s = %s" % (iface, path, name, value))
                self.if_frame[dev_name].dbus_props_change(
                    iface, path, name, value)
                self.conn_frame[dev_name].dbus_props_change(
                    iface, path, name, value)
                self.known_nws_frame.dbus_props_change(
                    iface, path, name, value)


    def passwd_entry_callback(self, path):
        nw_dic = pyiwd.nw_dic_by_path(path)
        return entry.show_password_entry_window(nw_dic["Name"])

    def agent_released(self):
        print("Iwd stopped, agent released: terminating")
        self.destroy()

    def periodic_props_update(self):
        for dev_name in self.dev_name_list:
            if self.dev_tab_admin_check(dev_name):
                dev_path = self.dev_path(dev_name)
                self.if_frame[dev_name].update_ip_addresses()
                self.conn_frame[dev_name].periodic_call()
        return True

    def close_window(self, widget):
        self.destroy()


class IwdGuiApp(Gtk.Application):
    "Main application class"

    def __init__(self,*args, **kwargs):
        super().__init__(
            *args,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if not self.window:
            self.window = IwdGuiWin(application=self,
                                    title="Iwdgui", modal=True)
        self.window.present()

    def do_command_line(self, command_line):
        self.activate()
        return 0

    def remove_window(self):
        self.remove_window(self.window)

def main():
    " iwdgui main "
    # ignore GTK deprecation warnings gwhen not in development mode
    # for development mode, run program as python3 -X dev iwdgui
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    signal.signal(signal.SIGINT, sigint_handler)
    app = IwdGuiApp()
    app.run(sys.argv)

if __name__ == "__main__":
    main()

