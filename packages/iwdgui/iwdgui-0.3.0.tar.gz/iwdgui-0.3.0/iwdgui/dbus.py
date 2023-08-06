#!/usr/bin/python3
"""
dbus: provides a system bus, and a session bus
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

from . import exitcodes
from .msg_window import show_error_message

DBUS_ERROR_NOREPLY = "org.freedesktop.DBus.Error.NoReply"
DBUS_ERROR_NOTFOUND = "org.freedesktop.DBus.Error.NotFound"
DBUS_ERROR_SERVICEUNKNOWN = "org.freedesktop.DBus.Error.ServiceUnknown"

DBUS_ERRORS = [
    DBUS_ERROR_NOREPLY,
    DBUS_ERROR_NOTFOUND,
    DBUS_ERROR_SERVICEUNKNOWN
]

system_bus = None
session_bus = None

try:
    import dbus
    from dbus.mainloop.glib import DBusGMainLoop
except Exception as e:
    show_error_message("Please install dbus-python", str(e),
                       exitcode=exitcodes.IMPORT_FAILED)

loop = DBusGMainLoop(set_as_default=True)

def connect2systembus():
    global system_bus
    try:
        system_bus = dbus.SystemBus()
    except Exception as e:
        show_error_message("Cannot attach to dbus system bus", str(e),
                           exitcode=exitcodes.DBUS_ATTACH_ERROR)

def connect2sessionbus():
    global session_bus
    try:
        session_bus = dbus.SessionBus()
    except Exception as e:
        show_error_message("Cannot attach to dbus session bus", str(e),
                           exitcode=exitcodes.DBUS_ATTACH_ERROR)

def dbus_if(bus, service, path, interface):
    try:
        return dbus.Interface(bus.get_object(service, path), interface)
    except Exception as e:
        show_error_message("DBus interface error (is iwd running?)",
                           ["service: " + service,
                            "path: " + path,
                            "interface: " + interface,
                            str(e)],
                           exitcode=exitcodes.IWD_NOT_RUNNING)


def connect():
    print("dbus connect")
    connect2systembus()
    connect2sessionbus()

connect()
