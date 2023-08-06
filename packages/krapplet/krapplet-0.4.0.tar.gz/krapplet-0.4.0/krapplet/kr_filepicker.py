#!/usr/bin/env python

"""
kr_password_entry: facilittes password entry from screen
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

# Assume gtk availability check done in krapplet.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# shortcuts so that calling code does not need to import Gtk
OPEN = Gtk.FileChooserAction.OPEN
SAVE = Gtk.FileChooserAction.SAVE
SELECT_FOLDER = Gtk.FileChooserAction.SELECT_FOLDER
CREATE_FOLDER = Gtk.FileChooserAction.CREATE_FOLDER

class FilePicker():

    def __init__(self, title, fname, action):
        #dialog = Gtk.FileChooserDialog(title=title,
        #                               parent=self, action=action)
        dialog = Gtk.FileChooserDialog(title=title,action=action)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK,)
        dialog.set_current_name(fname)
        self.filename = None
        #self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
        #elif response == Gtk.ResponseType.CANCEL:
        dialog.destroy()

    def selected_file(self):
        return self.filename

    def add_filters(self, dialog):
        """
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)
:q
        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any) """

