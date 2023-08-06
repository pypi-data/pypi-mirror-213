#!/usr/bin/python3
"""
iwd_menu: common code for iwd_frame modules
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

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

#constants
FRAME_MARGIN = 2
FRAME_LABEL_XALIGN = 0.025
GRID_MARGIN = 2
GRID_ROW_SPACING = 2
GRID_COL_SPACING = 20
VALUE_LEN = 36
PROMPT_LEN = 12
COMBOBOX_LEN = 64
RIGHT = Gtk.PositionType.RIGHT
BOTTOM = Gtk.PositionType.BOTTOM


#types of widgets
VALUE_STR = 0
VALUE_HIDDEN_STR = 1
VALUE_COMBO = 2
VALUE_RADIO = 3
VALUE_TOGGLE = 4


# list of tuples to connect modes and radiobutton labels:
_RADIOBUTTON_MODES_AND_LABELS = [
    (pyiwd.OFFLINE_MODE, "Off"),
    (pyiwd.STATION_MODE, "Station"),
    (pyiwd.AD_HOC_MODE, "Ad-hoc"),
    (pyiwd.ACCESS_POINT_MODE, "Access Point")]


class RadioBox(Gtk.Box):
    "Creates a box with radio buttons"

    def __init__(self, labels, callback):
        super().__init__()
        self._callback = callback
        self._radiobutton = {}
        button = None
        for label in labels:
            button = Gtk.RadioButton.new_with_label_from_widget(button, label)
            button.connect("toggled", callback)
            radiobox.pack_start(button, False, False, 4)
            self.radiobutton[label] = button

    def set_active(self, label):
        self._radiobutton[label].set_active(True)

    def get_active(self):
        for label in labels:
            if self._radiobutton[label].get_active():
                return label


class GtkValueLabel(Gtk.Label):
    "Customized Gtk.Label class for width, alingment and selectable"
    def __init__(self):
        super().__init__()
        self.set_xalign(0)
        self.set_width_chars(VALUE_LEN)
        self.set_max_width_chars(VALUE_LEN)
        self.set_selectable(True)

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


WIDGETTYPE = {
    VALUE_STR : GtkValueLabel,
    VALUE_HIDDEN_STR : GtkValueLabel,
    VALUE_COMBO : ComboBoxText,
    VALUE_TOGGLE : Gtk.CheckButton,
    VALUE_RADIO : RadioBox }


class Frame(Gtk.Frame):
    "Contains the different frames we see in the main window"

    def __init__(self):
        Gtk.Frame.__init__(self,
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)

    def destroy_child(self):
        "Destroys the main child widget, if it exists"
        child_widget = self.get_child()
        if child_widget:
            child_widget.destroy()

    # Code related to the interface frame"
    def if_frame_construct(self, supported_modes,
                           mode_callback, ipv6_suppport):
        "contructs an interface frame"
        # class vars:
        self._vendor = GtkValueLabel()
        self._model = GtkValueLabel()
        self._ipv4_address = GtkValueLabel()
        self._ipv6_address = GtkValueLabel()

        #Draw an interface frame
        self.destroy_child()
        self.set_label("Wireless interface")
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)
        labels = [label for mode, label in _RADIOBUTTON_MODES_AND_LABELS \
                  if mode in supported_modes]
        self._radiobox = RadioBox(labels, mode_callback)
        ln = addln2grid(grid, None, "Mode", self._radiobox)
        ln = addln2grid(grid, ln, "Vendor", self._vendor)
        ln = addln2grid(grid, ln, "Model", self._model)
        ln = addln2grid(grid, ln, "IPv4 address", self._ipv4_address)
        if ipv6_suppport:
            ln = addln2grid(grid, ln, "IPv6 address", self._ipv6_address)
        self.add(grid)

    def if_get_mode(self):
        return self._radiobox.get_active()

    def if_set_mode(self, label):
        self._radiobox.set_active(label)

    def if_set_vendor(self, vendor):
        self._vendor.set_text(vendor)

    def if_set_model(self, model):
        self._model.set_text(model)

    def if_set_ipv4_address(self, ipv4_address):
        self._ipv4_address.set_text(ipv4_address)

    def if_set_ipv6_address(self, ipv6_address):
        self._ipv6_address.set_text(ipv6_address)

    # Code related to the connection frame
    def conn_frame_construct(self, nw_combo_callback):
        "Constructs a connection mode frame, used for station, ap and adhoc mode"
        self._nw_combo = ComboBoxText()
        self._access_point_label = GtkValueLabel()
        self._radio_label = GtkValueLabel()
        self._signal_label = GtkValueLabel()
        self._sec_label = GtkValueLabel()

        # Draw a station mode frame
        self.destroy_child()
        self.set_label("Connection")
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)
        grid.attach_next_to(self._nw_combo, None,
                            Gtk.PositionType.BOTTOM, 2, 1)
        self._nw_combo.connect("changed", nw_combo_callback)
        ln = self._nw_combo
        ln = addln2grid(grid, ln, "Access point", self._access_point_label)
        ln = addln2grid(grid, ln, "Radio", self._radio_label)
        ln = addln2grid(grid, ln, "Signal ", self._signal_label)
        ln = addln2grid(grid, ln, "Security", self._sec_label)
        self.add(grid)

    def conn_update_nw_combo(self, nw_list):
        self._nw_combo.update_entries(nw_list)

    def conn_set_access_point(self, ap_label):
        self._access_point_label.set_text(ap_label)

    def conn_set_radio_text(self, radio_text):
        self._radio_label.set_text(radio_text)

    def conn_set_signal_text(self, signal_text):
        self._signal_label.set_text(signal_text)

    def conn_set_security_text(self, security_text):
        self._sec_label.set_text(security_text)

    # Code related to the known networks frame
    def known_nw_frame_construct(self):

        self._known_network_combo = ComboBoxText()
        self._last_connected = GtkValueLabel()
        self._auto_connect = Gtk.CheckButton()
        self._known_nw_security = GtkValueLabel()
        self._hidden = GtkValueLabel()
        self._forget_network_button = Gtk.Button(label="Forget")

        self.destroy_child()
        self.set_label("Known networks")
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)
        grid.attach_next_to(self._known_network_combo, None,
                            Gtk.PositionType.BOTTOM, 2, 1)
        self._known_network_combo.connect(
            "changed", self.known_networks_combo_changed)
        ln = self._known_network_combo
        ln = addln2grid(grid, ln,
                        "Last connected", self._last_connected)
        ln = addln2grid(grid, ln,
                        "Auto connect", self._auto_connect)
        self.auto_connect.connect("toggled", self._auto_connect_toggled)
        ln = addln2grid(grid, ln,
                        "Security", self._known_nw_security)
        ln = addln2grid(grid, ln, "Hidden", self._hidden)
        button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button_box.pack_end(self._forget_network_button, False, True, 0)
        grid.attach_next_to(button_box, self.hidden,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self._forget_network_button.connect("clicked", self.forget_network)
        self.add(grid)

    def known_nw_set_last_connected(self, timestr):
        self._last_connected.set_text(timestr)

    def known_nw_set_autoconnect(self, autoconnect_bool):
        self._auto_connect.set_active(autoconnect_bool)

    def known_nw_set_hidden(self, hidden_bool):
        self._hidden.set_text( "Yes" if known_nw_dic["Hidden"] else "No")



