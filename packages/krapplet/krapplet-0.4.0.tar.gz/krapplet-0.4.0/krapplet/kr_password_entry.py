#!/usr/bin/env python

"""
kr_password_entry: facilittes password entry from screen
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

# Assume gtk availability check done in krapplet.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class PasswordEntryDialog(Gtk.Dialog):
    """ PasswordEntryDialog: pops up a window to ask for a password """
    def __init__(self, title: str, prompt: str) -> None:
        Gtk.Dialog.__init__(self, title=title, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        box = self.get_content_area()
        password_prompt = Gtk.Label(label=prompt, xalign=0)
        self.passord_entry = Gtk.Entry(xalign = 0, visibility=False)
        self.passord_entry.set_activates_default(True)
        self.set_default_response(Gtk.ResponseType.OK)
        grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        box.add(grid)
        grid.attach_next_to(password_prompt, None,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.passord_entry, password_prompt,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.show_all()

    def get_pw( self ) -> str:
        """ returns the entered passwd from screen """
        return self.passord_entry.get_text()


def show_password_entry_window(title = "Unlock", prompt = "Passphrase"):
    """ shows the password entry window, return an entered passwd, or
        None when escape was pressed"""

    passwd = ""
    dialog = PasswordEntryDialog(title = title, prompt = "Passphrase")
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        passwd = dialog.get_pw()
    elif response == Gtk.ResponseType.CANCEL:
        passwd = None
    dialog.destroy()
    return passwd
