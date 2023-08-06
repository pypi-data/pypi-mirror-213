#!/usr/bin/env python3

"""
Iwdgui: A graphical frontend for iwd, Intel's iNet Wireless Daemon
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

BSD_LICENSE = """
Copyright 2021 Johannes Willem Fernhout <hfern@fernhout.info>.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

# Standard Python modules
import sys
import signal
from os.path import dirname

try:
    from  netifaces import ifaddresses, AF_LINK, AF_INET, AF_INET6
except:
    sys.stderr.write("Please install netifaces", file=sys.stderr)
    sys.exit(1)


# iwdgui application  modules
import pyiwd
import passwd_entry



# Non-Python dependencies. Not sure if they are installed
# import GTK3
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gdk, Gio
except:
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent",
                     file=sys.stderr)
    sys.exit(1)


#__VERSION__ = "0.1.0"
__VERSION__ = "0.0.1.a2"                  # alpha 1 release
FRAME_LABEL_XALIGN = 0.025
VALUE_LEN = 36
PROMPT_LEN = 12
COMBOBOX_LEN = 64
PERIODIC_TICK = 1500                     # call every so often in ms
ICONNAME = "iwdgui"

# Gtk shortcuts:
BOTTOM = Gtk.PositionType.BOTTOM
RIGHT = Gtk.PositionType.RIGHT


def sigint_handler(sig, frame):      # frame is stack frame, and is ignored
    """ Signal handler for SIGINT, or Ctrl-C,
    to avoid standard Python stack dump """
    #print("Signal", sig, "received, terminating", file=sys.stderr)
    toplevels = Gtk.Window.list_toplevels()
    for toplevel in toplevels:
        toplevel.destroy()
    Gtk.main_quit()

def add_item2menu(mnu=None, label=None, action=None, data=None):
    """ adds a menuitem to a menu (mnu), optionally with an
    activate action and data to be passed to the action """
    if  mnu is None or label is None:
        print("add_item2menu: mnu nor label can be None", file=sys.stderr)
        raise AssertionError
    mni =  Gtk.MenuItem(label=label)
    if action:
        if data:
            mni.connect("activate", action, data)
        else:
            mni.connect("activate", action)
    mnu.append( mni )
    return mni

def addln2grid(grid, ln, label, widget):
    """ adds a line to a grid. ln is the last leftside widget to add
    below to label is the text of the prompt, widget is the value.
    Returns the labelwidget of the created prompt"""
    prompt = Gtk.Label(label=label.ljust(PROMPT_LEN),
                       xalign=0,
                       selectable=True,
                       width_chars=PROMPT_LEN,
                       max_width_chars=PROMPT_LEN)
    grid.attach_next_to(prompt, ln, BOTTOM, 1, 1)
    grid.attach_next_to(widget, prompt, RIGHT, 1, 1)
    return prompt

def get_netifaces_addr(iface, addr_type):

    try:
        #print("get_netifaces_addr, iface", iface, "addr_type", addr_type)
        addresses = ifaddresses(iface)[addr_type]
        return addresses
    except Exception as e:
        print("Failed to get id address for", iface, " error:", e)
        return None

def icon_path(iconname, res):
    """ finds the path to an icon, based on std Gtk functions,
    so looking in standard locations like $HOME/.icons,
    $XDG_DATA_DIRS/icons, and /usr/share/pixmaps """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.lookup_icon(iconname, res, 0)
    if icon:
        path = icon.get_filename()
        return path
    #print("Iwdgui icon "
    #      + iconname
    #      + " with resolution "
    #      + str(res)
    #      + " not found", file=sys.stderr)
    return ""


class GtkValueLabel(Gtk.Label):
    def __init__(self):
        super().__init__()
        self.set_xalign(0)
        self.set_width_chars(VALUE_LEN)
        self.set_max_width_chars(VALUE_LEN)
        self.set_selectable(True)

class IwdGuiWin(Gtk.Window):
    """ this is the main window if iwdgui """

    def __init__(self):
        Gtk.Window.__init__(self, title="Iwdgui", modal=True)
        self.set_default_size(150, 100)
        self.set_transient_for(None)
        self.set_keep_above(True)
        self.connect("destroy", Gtk.main_quit)
        self.box = None
        self.active_device = None
        self.active_network = None

        # define all class Gtk widgets here
        # Available networks frame

        # Device frame
        self.interface_combo = Gtk.ComboBoxText()
        #self.scanning_checkbox = Gtk.CheckButton()
        self.ipv4_address = GtkValueLabel()
        self.ipv6_address = GtkValueLabel()

        # Connection status frame
        self.network_combo = Gtk.ComboBoxText()
        self.essid_label = GtkValueLabel()
        self.network_connected_label_yn = GtkValueLabel()
        self.signal_strength_label = GtkValueLabel()
        self.sec_label = GtkValueLabel()

        # Known networks frame
        self.known_network_combo = Gtk.ComboBoxText()
        self.last_connected = GtkValueLabel()
        self.auto_connect = GtkValueLabel()
        self.known_nw_security = GtkValueLabel()
        self.hidden = GtkValueLabel()
        self.forget_network_button = Gtk.Button(label="Forget")
        self.forget_network_button.connect("clicked", self.forget_network)
        self.add_network_button = Gtk.Button(label=" Add ")
        self.add_network_button.connect("clicked", self.add_network)

        #self.iwdobj = pyiwd.IwdObj(self.passwd_entry_callback)
        self.bus = pyiwd.bus()
        agent = pyiwd.Agent(self.bus, self.passwd_entry_callback))
        agent_mgr = pyiwd.AgentManager(self.bus)
        agent_mgr.RegisterAgent(agent.path)

        self.construct()
        #self.iwdobj.register_properties_callback(
        #    self.handle_dbus_signal_properties_changed)
        pyiwd.register_properties_callback(
            self.handle_dbus_signal_properties_changed)
        GLib.timeout_add(PERIODIC_TICK, self.periodic_props_update)

    def construct(self):
        "Constructs the window contents"

        #device_list = self.iwdobj.device_list()
        iwd_object_if = pyiwd.ObjectIf(self.bus)
        device_list = iwd_object_if.device_list()
        self.active_device = device_list[0]        #FIXME: handle commandline

        if self.box:
            self.box.destroy()
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        # build menu
        menubar = Gtk.MenuBar()
        applications_mni = add_item2menu(
            mnu=menubar, label="Application", action=None, data=None)
        # applications menu
        application_mnu = Gtk.Menu()
        about_mni = add_item2menu(
            mnu=application_mnu, label="About", action=self.about)
        quit_mnu = add_item2menu(
            mnu=application_mnu, label="Exit", action=self.app_exit)
        applications_mni.set_submenu(application_mnu)
        self.box.add(menubar)

        # interface frame
        device_frame = Gtk.Frame(label="Interface",
                                 label_xalign=FRAME_LABEL_XALIGN)
        device_grid = Gtk.Grid(row_spacing=2, column_spacing=20)
        device_frame.add(device_grid)

        device_grid.attach_next_to(self.interface_combo, None,
                                   Gtk.PositionType.BOTTOM, 2, 1)
        self.populate_interface_combo_box()
        self.interface_combo.connect("changed", self.interface_combo_changed)
        ln = self.interface_combo
        #ln = addln2grid(device_grid, ln, "Scanning", self.scanning_checkbox)
        #self.scanning_checkbox.connect("toggled", 
        #                               self.scanning_checkbox_toggled)
        ln = addln2grid(device_grid, ln, "IPv4 address", self.ipv4_address)
        ln = addln2grid(device_grid, ln, "IPv6 address", self.ipv6_address)


        # Active connection frame
        status_frame = Gtk.Frame(label="Active connection",
                                  label_xalign=FRAME_LABEL_XALIGN)
        status_grid = Gtk.Grid(row_spacing=2, column_spacing=20)
        status_frame.add(status_grid)

        status_grid.attach_next_to(self.network_combo, None,
                                   Gtk.PositionType.BOTTOM, 2, 1)
        self.install_network_combo_signal_handler()
        self.populate_network_combo_box()
        ln = self.network_combo
        ln = addln2grid(status_grid, ln, "Network name", self.essid_label)
        ln = addln2grid(status_grid, ln, "State", self.network_connected_label_yn)
        ln = addln2grid(status_grid, ln, "Singal Strength", self.signal_strength_label)
        ln = addln2grid(status_grid, ln, "Security", self.sec_label)

        # known networks frame
        known_networks_frame = Gtk.Frame(label="Known networks",
                                         label_xalign=FRAME_LABEL_XALIGN)
        known_networks_grid = Gtk.Grid(row_spacing=2, column_spacing=20)
        known_networks_frame.add(known_networks_grid)
        known_networks_grid.attach_next_to(self.known_network_combo,
                                          None,
                                          Gtk.PositionType.BOTTOM, 2, 1)
        self.populate_known_network_combo_box()
        self.known_network_combo.connect("changed", 
                                          self.known_networks_combo_changed)
        ln = self.known_network_combo
        ln = addln2grid(known_networks_grid, ln,
                        "Last connected", self.last_connected)
        ln = addln2grid(known_networks_grid, ln,
                        "Auto connect", self.auto_connect)
        ln = addln2grid(known_networks_grid, ln,
                        "Security", self.known_nw_security)
        ln = addln2grid(known_networks_grid, ln, "Hidden", self.hidden)

        """
        button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        #button_box.pack_end(self.forget_network_button, False, True, 0)
        #button_box.pack_end(self.add_network_button, False, True, 0)
        known_networks_grid.attach_next_to(button_box, self.hidden,
                                           Gtk.PositionType.BOTTOM, 1, 1)
        """

        # build the window contents:
        self.box.add(Gtk.Label())
        self.box.add(device_frame)
        self.box.add(Gtk.Label())
        self.box.add(status_frame)
        self.box.add(Gtk.Label())
        self.box.add(known_networks_frame)
        self.box.add(Gtk.Label())

        self.unblock_network_combo_signal_handler()

        self.add(self.box)
        self.show_all()

    def populate_interface_combo_box(self):
        "Populates the interface combo with connected devices"
        self.interface_combo.remove_all()
        device_list = self.iwdobj.device_list()
        station_list = self.iwdobj.station_list()
        idx = selected = 0
        found = False
        for device in device_list:
            if device["Mode"] == 'station':
                self.interface_combo.append_text(device['Name'])
                device_key = self.iwdobj.get_device_key_by_name(device['Name'])
                for station in station_list:
                    if station['State'] == 'connected':
                        station_dev = dirname(station['ConnectedNetwork'])
                        if station_dev == device_key:
                            found = True
                if found:
                    selected = idx
                    self.active_device = device
                    self.active_device_key = self.iwdobj.get_device_key_by_name(
                        device["Name"])
                    found = False
                idx += 1
        self.interface_combo.set_active(selected)
        self.iwdobj.start_scan(self.active_device_key)
        self.update_interface_status()

    def interface_combo_changed(self, combobox):
        print("interface_combo_changed")
        active_device_name = combobox.get_active_text()
        if not active_device_name:
            return
        self.active_device_key = self.iwdobj.get_device_key_by_name(
            active_device_name)
        self.active_device = self.iwdobj.get_device_by_key(
            self.active_device_key)
        self.iwdobj.start_scan(self.active_device_key)
        self.update_interface_status()
        self.populate_network_combo_box()

    def update_interface_status(self):
        device = self.iwdobj.get_device_by_key(self.active_device_key)
        #station = self.iwdobj.get_station_by_key(self.active_device_key)
        #self.scanning_checkbox.set_active(station['Scanning'])

        ipv4_addr = get_netifaces_addr(device["Name"], AF_INET)
        if ipv4_addr:
            v4_addr = ipv4_addr[0]['addr']
        else:
            v4_addr = ""
        self.ipv4_address.set_text(v4_addr)
        ipv6_addr = get_netifaces_addr(device["Name"],AF_INET6)
        if ipv6_addr:
            v6_addr = ipv6_addr[0]['addr']
        else:
            v6_addr = ""
        self.ipv6_address.set_text(v6_addr)

    def scanning_checkbox_toggled(self, widget):
        print("scanning_checkbox_toggled", widget.get_active())
        #if widget.get_active():
        #    self.iwdobj.start_scan(self.active_device_key)


    def install_network_combo_signal_handler(self):
        self.network_combohandler = self.network_combo.connect(
            "changed", self.network_combo_change)

    def block_network_combo_signal_handler(self):
        self.network_combo.handler_disconnect(self.network_combohandler)
        self.network_combohandler = None

    def unblock_network_combo_signal_handler(self):
        self.install_network_combo_signal_handler()

    def populate_network_combo_box(self):
        self.block_network_combo_signal_handler()
        #network_list = self.iwdobj.network_list()
        network_list = self.iwdobj.device_network_list(self.active_device_key)
        self.network_combo.remove_all()
        count = connected_network_idx = 0
        self.selected_network_key = None
        for network in network_list:
           # print("network:", network)
            if network['Device'] == self.active_device_key:
                self.network_combo.append_text(network["Name"])
                if network["Connected"]:
                    connected_network_idx = count
                    self.active_network = network
                count += 1
        self.unblock_network_combo_signal_handler()
        self.network_combo.set_active(connected_network_idx) 
        self.network_combo_exists = True
        self.update_network_props()



    def network_combo_change(self, combobox):
        if not self.network_combohandler:
            return
        active_network_name = combobox.get_active_text()
        if (self.active_network and 
            active_network_name == self.active_network["Name"]):
            return
        network_list = self.iwdobj.network_list()
        for network in network_list:
            print("network", network)
            if network["Name"] == active_network_name:
                self.active_network = network
        #self.update_network_props()
        self.connect_network()

    def update_network_props(self):
        if not self.active_device or not self.active_network:
            return
        self.station_props = self.iwdobj.get_station_props(self.active_device,
                                                           self.active_network)

        if self.station_props:
            sig_strength = str(self.station_props["Signalstrength"] / 100) + " dBm"
            if self.station_props["Connected"]:
                connected = "connected"
            else:
                connected = "no"
            security = self.station_props["Type"]
        else:
            print("no props")
            sig_strength = "-"
            connected = "no"
            security = "-"
        #self.interface_label.set_text(self.active_device["Name"])
        self.essid_label.set_text(self.active_network["Name"])
        self.network_connected_label_yn.set_text(connected)
        self.signal_strength_label.set_text(sig_strength)
        self.sec_label.set_text(security)

    def handle_dbus_signal_properties_changed(self, interface,
                                             changed, invalidated, path):

        def update_connected():
            self.network_connected_label_yn.set_text("Connected")
            #ip_addr = get_netifaces_addr(self.active_device["Name"], AF_INET)
            self.update_interface_status()
            #print("ip address:", ip_addr)

        def update_not_connected():
            self.network_connected_label_yn.set_text("Disconnected")
            self.essid_label.set_text("")

        def handle_dbus_station_state_change():
            if value == "connected":
                update_connected()
            else:
                update_not_connected()

        def handle_station_connectednetwork_change():
            network = self.iwdobj.get_network_by_key(value)
            self.active_network = network
            self.essid_label.set_text(self.active_network["Name"])
            self.update_network_props()


        def handle_station_scanning_change():
            #should_be_scanning = self.scanning_checkbox.get_active()
            #if should_be_scanning and not value:        # scan again
            if not value:        # scan again
                self.iwdobj.start_scan(signal_devkey)
            self.iwdobj.refresh_objects()
            self.populate_interface_combo_box()

        def handle_dbus_signal_station_change():

            #device_key = self.iwdobj.get_device_key_by_name(self.active_device)
            #print("device_key:", device_key, "path", path)
            #if path == self.device_key:
            if True:
                station_dispatch = {
                    "State" : handle_dbus_station_state_change,
                    "ConnectedNetwork": handle_station_connectednetwork_change,
                    "Scanning" : handle_station_scanning_change}

                station_dispatch[name]()

        def handle_dbus_signal_network_change():
                if name == "Connected":
                    if value:
                        update_connected()
                    else:
                        update_not_connected()
                else:
                    print(iface, "properties_changed, name not caught:", name)


        def handle_dbus_connected_network_station_change():
            if value:
                update_connected()
            else:
                update_not_connected()

        iface_dispatch = {
            "Station" : handle_dbus_signal_station_change,
            "Network" : handle_dbus_signal_network_change }

        iface = interface[interface.rfind(".") + 1:]
        #print("Active device name:", self.active_device["Name"])
        #active_devkey = self.iwdobj.get_device_key_by_name(
        #    self.active_device["Name"])
        for name, value in changed.items():
            print("{%s} [%s] %s = %s" % (iface, path, name, value))
            signal_devkey = path
            if iface == "Network":
                signal_devkey = dirname(path)
            if signal_devkey == self.active_device_key:
                print("signal_devkey:", signal_devkey)
                iface_dispatch[iface]()
            else:
                print("update ignored:", signal_devkey,
                      "!=", self.active_device_key)

    def passwd_entry_callback(self, path):
        #print("passwd_entry_callback for", path)
        return passwd_entry.show_password_entry_window(
            title=self.active_network["Name"])
        return "singapore"

    def connect_network(self):
        if self.active_network:
            self.iwdobj.connect_network(self.active_network)

    def disconnect_network(self):
        self.iwdobj.disconnect_network(self.active_network)

    def periodic_props_update(self):
        #print("*", end = '', sep = "", flush=True)
        oldobj = self.iwdobj.objects
        self.iwdobj.refresh_objects()
        if oldobj != self.iwdobj.objects:
            self.update_interface_status()
            self.update_network_props()
        #return False
        return True

    def populate_known_network_combo_box(self):
        known_networks = self.iwdobj.knownnetwork_list()
        self.known_network_combo.remove_all()
        for known_network in known_networks[::-1]:
            label = known_network["Name"]
            self.known_network_combo.append_text(known_network["Name"])
        self.known_network_combo.set_active(0)
        self.known_networks_combo_changed(self.known_network_combo)

    def known_networks_combo_changed(self, widget):
        known_network_name = widget.get_active_text()
        known_networks = self.iwdobj.knownnetwork_list()
        for known_network in known_networks:
            if known_network_name == known_network["Name"]:
                self.last_connected.set_text(known_network["LastConnectedTime"])
                self.auto_connect.set_text(
                    "yes" if known_network["AutoConnect"] else "no")
                self.known_nw_security.set_text(known_network["Type"])
                self.hidden.set_text(
                    "yes" if known_network["Hidden"] else "no")


    def forget_network(self, widget):
        known_network_name = self.known_network_combo.get_active_text()
        self.iwdobj.forget_network(known_network_name)
        self.populate_known_network_combo_box()


    def add_network(self, widget):
        #print("add_network")
        pass

    def about(self, widget):
        #print("About...")
        """Shows the about dialog"""
        image = Gtk.Image()
        image.set_from_file(icon_path( ICONNAME, 96))
        icon_pixbuf = image.get_pixbuf()
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_logo(icon_pixbuf)
        about_dialog.set_program_name("Iwdgui")
        about_dialog.set_version("Version " + __VERSION__)
        about_dialog.set_comments("A graphical frontend for iwd, Intel's iNet Wireless Daemon")
        about_dialog.set_authors(["Johannes Willem Fernhout"])
        about_dialog.set_copyright( "(c) 2021 Johannes Willem Fernhout")
        about_dialog.set_license(BSD_LICENSE)
        about_dialog.set_website("https://gitlab.com/hfernh/iwdgui")
        about_dialog.set_website_label("iwdgui on GitLab")
        about_dialog.show_all()
        about_dialog.run()
        about_dialog.destroy()

    def app_exit(self, widget):
        #print("app_exit")
        Gtk.main_quit()


class IwdGuiApp(Gtk.Application):
    """" This is the main application class of iwdgui.
         It handles the standard signals for startup, activate
    """
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.example",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.activated = False

    """ leave default handler in place for now
    def do_startup(self):
        print("do_startup") """

    def do_activate(self):
        """  print("do_activate")  """
        if self.activated:                  # already running
            self.window.present()           # just set focus to our window
        else:
            self.window = IwdGuiWin()
            self.window.show()
            self.activated = True




def main():
    """ iwdgui main """
    # ignore GTK deprecation warnings gwhen not in development mode
    # for development mode, run program as python3 -X dev iwdgui
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    signal.signal(signal.SIGINT, sigint_handler)
    app = IwdGuiApp()
    app.run(sys.argv)
    Gtk.main()
    print("All done..!")

if __name__ == "__main__":
    main()
