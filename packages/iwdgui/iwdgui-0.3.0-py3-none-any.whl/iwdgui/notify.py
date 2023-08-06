#!/usr/bin/python3
"""
notify: deskop notifications using D-BUS
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

from .dbus import session_bus as bus
import dbus

try:
    from .icon import icon_path
except:
    from icon import icon_path

NOTIFY_PATH = "/org/freedesktop/Notifications"
NOTIFY_IF = "org.freedesktop.Notifications"
ICON_RESOLUTION = 96
SUMMARY = "IWDGUI"


_msg_id = 0 
_notify_if = dbus.Interface(bus.get_object(NOTIFY_IF, NOTIFY_PATH), NOTIFY_IF)


def msg(body, summary=SUMMARY, app_name="Iwdgui", replaces_id=0,
        app_icon="iwdgui", actions=[], hints = {"urgency": 1},
        expire_timeout=5000):
    "Internal notification message function"
    global _msg_id
    app_icon_path = icon_path(iconname=app_icon, res=ICON_RESOLUTION)
    try:
        _msg_id = _notify_if.Notify(app_name, _msg_id, app_icon_path, summary,
                                    body, actions, hints, expire_timeout)
    except Exception as e:
        print("Error, cannot do a notification, error:", e)


