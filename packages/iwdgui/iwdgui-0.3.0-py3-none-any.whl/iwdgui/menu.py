#!/usr/bin/python3
"""
iwd_menu: the iwd menu code
(c) 2021-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

BSD_LICENSE = \
"""Copyright 2021 - 2023 Johannes Willem Fernhout
<hfern@fernhout.info>. All rights reserved.

Redistribution and use in source and binary forms, with or
without modification are permitted provided that the following
conditions are met:

1. Redistributions of source code must retain the above
   copyright notice, this list of conditions and the following
   disclaimer.

2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials
   provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products
   derived from this software without specific prior written
   permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT
HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO,PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
OF SUCH DAMAGE."""

__VERSION__ = "0.3.0"

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

#from .icon import icon_path
from . import icon

def _add2menu(mnu, mni):
    "Adds a menuitem to a menu, returns the menuitem to allow chaining"
    mnu.add(mni)
    return mni

class _MenuItem(Gtk.MenuItem):
    "Helper class for menuitems"
    def __init__(self, label, action=None, widget=Gtk.AccelLabel, data=None):
        Gtk.MenuItem.__init__(self)
        widget = widget(label=label, xalign=0)
        if action:
            self.connect("activate", action)
        self.add(widget)


class IwdMenu(Gtk.MenuBar):
    "Everything related to the menu"
    def __init__(self, advanced_callback, close_window_callback):
        Gtk.MenuBar.__init__(self)
        self._advanced_callback = advanced_callback

        # build the menubar
        applications_mni = _add2menu(self, _MenuItem("Application"))
        application_mnu = Gtk.Menu()
        self._adv_checkbox = _add2menu(
            application_mnu,
            _MenuItem("Advanced",
                     widget=Gtk.CheckButton,
                     action=self.toggle_advanced_view)).get_child()
        _add2menu(application_mnu, _MenuItem("About", action=self.about))
        _add2menu(application_mnu, _MenuItem("Exit",
            action=close_window_callback))
        applications_mni.set_submenu(application_mnu)

    def get_advanced_view(self):
        return self._adv_checkbox.get_active()

    def set_advanced_view(self, on_off):
        self._adv_checkbox.set_active(on_off)
        return on_off

    def toggle_advanced_view(self, widget):
        self.set_advanced_view(not self.get_advanced_view())
        self._advanced_callback()

    def about(self, widget):
        "Shows the about dialog"
        icon_pixbuf = icon.get_pixbuf(iconname=icon.IWDGUI_LOGO, res=96)
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_logo(icon_pixbuf)
        about_dialog.set_program_name("Iwdgui")
        about_dialog.set_version("Version " + __VERSION__)
        about_dialog.set_comments(
            "A graphical frontend for iwd, Intel's iNet Wireless Daemon")
        about_dialog.set_authors(["Johannes Willem Fernhout"])
        about_dialog.set_copyright( "(c) 2021 - 2022 Johannes Willem Fernhout")
        about_dialog.set_license(BSD_LICENSE)
        about_dialog.set_website("https://gitlab.com/hfernh/iwdgui")
        about_dialog.set_website_label("iwdgui on GitLab")
        #extra_button = about_dialog.add_button("Version Info", 0)

        about_dialog.show_all()
        about_dialog.run()
        about_dialog.destroy()

