# Iwdgui

[Iwdgui](https://gitlab.com/hfernh/iwdgui) is a graphical frontend for
[iwd](https://iwd.wiki.kernel.org), Intel's iNet Wireless Daemon.


# Feature overview

- Graphical user interface for iwd, focusing on practical use, making it easy
  to connect a laptop or desktop to a wifi network.
- Supporting multiple wireless adapters, in different tabs.
- Can provide  detailed information: vendor/model of the wireless interface,
  IP address information, radio standard (802.??), channel, signal strength,
  etc.
- Iwdgui supports station mode, access point mode, and ad-hoc mode.
  (The latter two depend on the wireless network interface capabilities)
- Able to manage previously connected networks.


# Technical overview

- Iwdgui consists of a [single window](https://gitlab.com/hfernh/iwdgui/-/raw/master/screenshots/iwdgui-mainwindow.png).
  in which a user can select the wireless interface, the network to connect to,
  and get information on a previously connected network.
- Currently iwdgui supports 'station' mode, i.e. the mode in which a laptop
  or desktop connects to a wireless access point or router.
- Iwdgui and  the iwd daemon communicate over a
  [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/) connection.


# Dependencies

The following software is needed to run iwdgui:
- [Python3](https://www.python.org), as the programming language.
- [GTK3](https://developer.gnome.org/gtk3/stable), as the graphical toolkit
- [PyGObject](https://pygobject.readthedocs.io), which provides the Python
  bindings for GTK3, GLib, etc.
- [Dbus-python](https://pypi.org/project/dbus-python) for interfacing
  with iwd over [D-Bus](https://www.freedesktop.org/wiki/Software/dbus).
- [Netifaces](https://github.com/al45tair/netifaces), to obtain IP address
  information.


# Operating environment prerequisites

- Iwd should be running.
- At least one iwd network interface device should be available, powered on,
  and configured in station mode.
- [Python3](https://www.python.org), as the programming language.
- [GTK3](https://developer.gnome.org/gtk3/stable), as the graphical toolkit.
- [Dbus-python](https://pypi.org/project/dbus-python) as Python D-Bus binding.
- [Netifaces](https://github.com/al45tair/netifaces), to obtain IP address
  information.


# License

Iwdgui is licensed under a
[BSD-3 license](https://gitlab.com/hfernh/iwdgui/-/blob/master/LICENSE).


# Feedback

If you have an enhancement request, or something is not working properly then
please log an [issue](https://gitlab.com/hfernh/iwdgui/-/issues) against
the project.
