#!/usr/bin/env python

"""
kr_popup: functions for showing info or erorr message
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk


def show_info_or_error_message(active_widget, primary_msg,
                               secondary_msg, msg_type, title, buttons ):
    """Shows an error or info  message dialog"""
    dialog = Gtk.MessageDialog(title=title, transient_for=active_widget,
                               flags=0, message_type=msg_type,
                               buttons=buttons, text=primary_msg)
    if secondary_msg:
        if isinstance(secondary_msg, list):
            secmsg = '\n'.join([ln for ln in secondary_msg])
        elif isinstance(secondary_msg, str):
            secmsg = secondary_msg
        else:
            print("show_info_or_error_message:"
                  + " secondary message is list nor str",
                  file=sys.stderr)
        #dialog.format_secondary_text(secondary_msg)
        dialog.format_secondary_text(secmsg)
    dialog.run()
    dialog.destroy()


def show_error_message(active_widget, primary_msg, secondary_msg):
    """Shows an error message dialog"""
    show_info_or_error_message(active_widget, primary_msg, secondary_msg,
                               Gtk.MessageType.ERROR, "ERROR",
                               Gtk.ButtonsType.CLOSE)


def show_info_message(active_widget, primary_msg, secondary_msg):
    """ Shows an informational message dialog """
    show_info_or_error_message(active_widget, primary_msg, secondary_msg,
                               Gtk.MessageType.INFO, "Informational",
                               Gtk.ButtonsType.CLOSE)

