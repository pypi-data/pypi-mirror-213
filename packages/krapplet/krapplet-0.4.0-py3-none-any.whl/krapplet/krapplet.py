#!/usr/bin/env python3
"""
krapplet: A password manager written as a gnome-keyring applet
krapplet.py is the main program
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

# standard Python modules
import sys
import os
import signal
import string
import secrets
import random
import locale
import webbrowser
import subprocess
import math
import argparse
from datetime import datetime, timedelta


# Non-Python dependencies. Not sure if they are installed
# import GTK3
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gdk
except:
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent",
                     file=sys.stderr)
    sys.exit(1)


# command line parsing to determine the storage provider
parser = argparse.ArgumentParser( prog = "krapplet",
                                  description = "A password manager")

# currently only gnome-keyring, and pass are supported,
# later on sqlite, and keepass might be added
parser.add_argument( "--storage", nargs='?',
                     default="gnome-keyring",
                     help="gnome-keyring, pass, or memory")
parser.add_argument( "--gpg-id", nargs='?',
                     help="required for pass storage provider")
parser.add_argument( "--armor", action='store_true',
                     help="ASCII encode secrets")
cmd_line = parser.parse_args()
from .kr_storage_select import StorageSelect
st_sel=StorageSelect(cmd_line.storage, cmd_line.gpg_id, cmd_line.armor)
from .kr_storage import \
    connection_open, create_keyring, get_all_keyrings, search_keys, \
    NotAvailableException, LockedException, KeyNotFoundException, \
    PromptDismissedException

from .kr_popup import show_error_message, show_info_message
from . import kr_backup

# application constants:
BSD_LICENSE = """
Copyright 2020-2021 Johannes Willem Fernhout <hfern@fernhout.info>.
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
APP_RESPONSE_DELETE = 1
FRAME_LABEL_XALIGN = 0.025
APP_EMBED_TIMEOUT = 5000                       # 5 seconds
PW_SPECIAL_CHARS = "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
ICONNAME = "krapplet"
DEFAULT_PW_LEN = 16
__VERSION__ = "0.4.0"


# utility functions:
def add_item2menu(mnu=None, label=None, action=None, data=None):
    """ adds a menuitem to a menu (mnu), optionally with an activate action
        and data to be passed to the action """
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


def add_separator2menu(mnu):
    """ add_separator2menu: adds a separator to a menu """
    mni =  Gtk.SeparatorMenuItem()
    mnu.append( mni )

"""
def show_info_or_error_message(active_widget, primary_msg,
                               secondary_msg, msg_type, title, buttons ):
    dialog = Gtk.MessageDialog(title=title, transient_for=active_widget,
                               flags=0, message_type=msg_type,
                               buttons=buttons, text=primary_msg)
    if secondary_msg:
        dialog.format_secondary_text(secondary_msg)
    dialog.run()
    dialog.destroy()


def show_error_message(active_widget, primary_msg, secondary_msg):
    show_info_or_error_message(active_widget, primary_msg, secondary_msg,
                               Gtk.MessageType.ERROR, "ERROR",
                               Gtk.ButtonsType.CLOSE)


def show_info_message(active_widget, primary_msg, secondary_msg):
    show_info_or_error_message(active_widget, primary_msg, secondary_msg,
                               Gtk.MessageType.INFO, "Informational",
                               Gtk.ButtonsType.CLOSE)
"""

def abs_path(rel_path):
    """ returns the absolute path for a file,
    given the relative path to this ,py file """
    packagedir = os.path.dirname(__file__)
    joinedpath = os.path.join(packagedir, rel_path)
    path = os.path.abspath(joinedpath)
    return path


def icon_path(iconname, res):
    """ finds the path to an icon, based on std Gtk functions,
    so looking in standard locations like $HOME/.icons,
    $XDG_DATA_DIRS/icons, and /usr/share/pixmaps """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.lookup_icon(iconname, res, 0)
    if icon:
        path = icon.get_filename()
        return path
    print("Krapplet icon "
          + iconname
          + " with resolution "
          + str(res)
          + " not found", file=sys.stderr)
    return ""


def copy_text2clipboard(txt):
    """ copy_text2clipboard copies the txt parameter to the cliboard """
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(txt, -1)


def timestamp(since_epoch):
    """returns a string according to local locale
    based on seconds since epoch 1-JAN-1970"""
    if since_epoch:
        from_timestamp = datetime.fromtimestamp(since_epoch)
        date_string = from_timestamp.strftime(
            locale.nl_langinfo(locale.D_T_FMT))
        return date_string
    return ""


def int2(a_string):
    """ converts string to in, return 0 on failure """
    try:
        return int(a_string)
    except ValueError:
        return 0


def sigint_handler(sig, frame):      # frame is stack frame, and is ignored
    """ Signal handler for SIGINT, or Ctrl-C,
    to avoid standard Python stack dump """
    print("Signal", sig, "received, terminating", file=sys.stderr)
    toplevels = Gtk.Window.list_toplevels()
    for toplevel in toplevels:
        toplevel.destroy()
    Gtk.main_quit()


def setup_ccs():
    """ Sets up neccessary cascading style sheets"""
    # FIXME: should come from file, not from memory
    css = """
        levelbar block.weak   { background-color: #FF0000; border: #FF0000; }
        levelbar block.ok     { background-color: #FFA500; border: #FF0000; }
        levelbar block.strong { background-color: #00FF00; border: #FF0000; }
        button:active         { background-color: #0274d9; }
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(bytes(css.encode()))
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def password_complexity( passwd):
    """ Calculates password complexity based on the logic found at this
    website: http://passwordstrengthcalculator.com/interpret.php.
    Complexity is the base 2 log of the cardinalty times the password length"""
    if len(passwd) == 0:
        return 0
    upperc_present = lowerc_present = num_present = special_present = False
    cardinality = 0
    for char in passwd:
        if not upperc_present and char in string.ascii_uppercase:
            cardinality += len(string.ascii_uppercase)
            upperc_present = True
        elif not lowerc_present and char in string.ascii_lowercase:
            cardinality += len(string.ascii_lowercase)
            lowerc_present = True
        elif not num_present and char in string.digits:
            cardinality += len(string.digits)
            num_present = True
        elif not special_present and char in PW_SPECIAL_CHARS:
            cardinality += len(PW_SPECIAL_CHARS)
            special_present = True
    complexity = math.log2(cardinality) * len(passwd)
    return int(complexity)


def gen_pw( tot_len, upperc_len, lowerc_len, numeric_len, special_len):
    """ Returns a generated password based on total lenght, and
    the number of capital, lowercase, numeric and special characters"""

    def part_passwd(length, chars):
        """passwd create string of random chars from a set of chars"""
        passw = ""
        #for i in range(length):
        for _ in range(length):
            passw += secrets.choice(chars)
        return passw

    def shuffle_word(word):
        """shuffle_word shuffles the letters of a word"""
        word = list(word)
        random.shuffle(word)
        return ''.join(word)

    extra_len = tot_len - upperc_len - lowerc_len - numeric_len - special_len
    upperc_str = part_passwd(upperc_len, string.ascii_uppercase)
    lowerc_str = part_passwd(lowerc_len, string.ascii_lowercase)
    numeric_str = part_passwd(numeric_len, string.digits)
    special_str = part_passwd(special_len, PW_SPECIAL_CHARS)
    extra_str = ""
    if extra_len > 0:
        if upperc_len:
            extra_str += string.ascii_uppercase
        if lowerc_len:
            extra_str += string.ascii_lowercase
        if numeric_len:
            extra_str += string.digits
        if special_len:
            extra_str += PW_SPECIAL_CHARS
        extra_str = part_passwd(extra_len, extra_str)
    passw = shuffle_word(upperc_str
                      + lowerc_str
                      + numeric_str
                      + special_str
                      + extra_str)
    return passw


class PasswordGeneratorDialog(Gtk.Dialog):
    """ NewPasswordDialog: dialog window to generate a new password """
    def __init__(self, parent ):
        Gtk.Dialog.__init__(self, title="Generate password", flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.tot_len = DEFAULT_PW_LEN
        self.upperc_len = 2
        self.lowerc_len = 2
        self.numeric_len = 2
        self.special_len = 2
        self.show_window()
        self.set_transient_for(parent)

    def show_window( self ):
        """ show_window builds up a window based on the values i
            of self.new_keyname/new_attribs/new_secret """

        self.set_default_size(100, 100)
        box = self.get_content_area()
        frame = Gtk.Frame(label="Parameters", label_xalign=FRAME_LABEL_XALIGN)
        box.add(frame)
        self.grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        frame.add(self.grid)

        prompt_length = Gtk.Label(label="Total length", xalign=0)
        self.entry_lenght = Gtk.Entry( text=str(self.tot_len), \
                                       input_purpose=Gtk.InputPurpose.DIGITS,
                                       xalign=0, width_request=3 )
        self.entry_lenght.connect("insert_text", self.validate, 2)
        prompt_upperc = Gtk.Label(label="Uppercase", xalign=0)
        self.entry_upperc = Gtk.Entry(text=str(self.upperc_len),
                                  input_purpose=Gtk.InputPurpose.DIGITS,
                                  xalign=0)
        self.entry_upperc.connect("insert_text", self.validate, 2)
        prompt_lowerc = Gtk.Label(label="Lowercase", xalign=0)
        self.entry_lowerc = Gtk.Entry(text=str(self.lowerc_len),
                                  input_purpose=Gtk.InputPurpose.DIGITS,
                                  xalign=0 )
        self.entry_lowerc.connect("insert_text", self.validate, 2)
        prompt_numeric = Gtk.Label(label="Numeric", xalign=0)
        self.entry_numeric = Gtk.Entry(text=str(self.numeric_len),
                                  input_purpose=Gtk.InputPurpose.DIGITS,
                                  xalign=0 )
        self.entry_numeric.connect("insert_text", self.validate, 2)
        prompt_special = Gtk.Label(label="special", xalign=0)
        self.entry_special = Gtk.Entry(text=str(self.special_len),
                                  input_purpose=Gtk.InputPurpose.DIGITS,
                                  xalign=0 )
        self.entry_special.connect("insert_text", self.validate, 2)
        empty_line = Gtk.Label()

        self.grid.attach_next_to(prompt_length, None,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_lenght, prompt_length,
                                 Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(prompt_upperc, prompt_length,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_upperc, prompt_upperc,
                                 Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(prompt_lowerc, prompt_upperc,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_lowerc, prompt_lowerc,
                                 Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(prompt_numeric, prompt_lowerc,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_numeric, prompt_numeric,
                                 Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(prompt_special, prompt_numeric,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_special, prompt_special,
                                 Gtk.PositionType.RIGHT, 1, 1)
        box.add( empty_line )
        self.show_all()

    def update_from_window( self ):
        """ updates instance vars from window """
        self.tot_len = int2(self.entry_lenght.get_text())
        self.upperc_len = int2(self.entry_upperc.get_text())
        self.lowerc_len = int2(self.entry_lowerc.get_text())
        self.numeric_len = int2(self.entry_numeric.get_text())
        self.special_len = int2(self.entry_special.get_text())

    def validate(self, widget, new_text, new_text_length, position, maxlen ):
        """ validates keyboard input for numberic, and nrof digits, and
            enables/disables the OK button based on the input given"""
        field_contents = widget.get_text()
        newpos = widget.get_position()
        if (new_text.isnumeric()
            and (new_text_length + len(field_contents)) <= maxlen):
            field_contents = (field_contents[:newpos]
                              + new_text
                              + field_contents[newpos:])
        widget.handler_block_by_func(self.validate)
        widget.set_text(field_contents)
        widget.handler_unblock_by_func(self.validate)
        GLib.idle_add(widget.set_position, newpos+1)
        widget.stop_emission_by_name("insert_text")
        self.update_from_window()
        enabled = ((self.tot_len >= (self.upperc_len + self.lowerc_len
                                     + self.numeric_len + self.special_len))
                   and (self.upperc_len or self.lowerc_len
                        or self.numeric_len or self.special_len ))
        self.set_response_sensitive( Gtk.ResponseType.OK, enabled )

    def generate_new_password(self):
        """ Returns a newly generated passwd """
        self.update_from_window()
        passwd = gen_pw(self.tot_len, self.upperc_len,
                        self.lowerc_len, self.numeric_len, self.special_len)
        return passwd


class KeyDialog(Gtk.Dialog):
    """ KeyDialog: shows a dialog window for keys """
    def __init__(self, parent, key=None, keyring=None):
        Gtk.Dialog.__init__(self, title="Edit key", flags=0 )
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_DELETE, APP_RESPONSE_DELETE,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.key = key
        self.keyring = keyring
        self.extra_attribs = 0
        self.out_of_focus_handler = None
        if self.key:
            self.old_keyring_label = self.new_keyring_label = key.keyring_label
            self.old_keyname = self.new_keyname = key.get_label()
            self.old_attribs = self.new_attribs = key.get_attributes()
            self.old_secret = self.new_secret = key.get_secret().decode("utf-8")
            self.old_created = key.get_created()
            self.old_modified= key.get_modified()
            self.connection = self.key.connection
        else:
            self.old_keyring_label = self.new_keyring_label = keyring.get_label()
            self.old_keyname = self.new_keyname = "New key"
            self.old_attribs = self.new_attribs = {}
            self.new_attribs["URL"] = "https://"
            self.new_attribs["username"] = ""
            self.new_attribs["validity"] = "90"
            self.old_secret = self.new_secret = gen_pw(DEFAULT_PW_LEN,
                                                       2, 2, 2, 2)
            self.old_created = self.old_modified = 0
            self.connection = keyring.connection
        self.secret_visibilty = False
        self.box = None
        self.show_window()

    def show_window( self ):
        """ KeyDialog.show_window builds up a window based on the values i
            of self.new_keyname/new_attribs/new_secret """
        self.set_default_size(150, 100)
        content_area = self.get_content_area()
        if self.box:
            self.box.destroy()
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        content_area.add(self.box)

        keyring_frame = Gtk.Frame(label="Keyring",
                                  label_xalign=FRAME_LABEL_XALIGN)
        keyring_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.box.add(keyring_frame)
        keyring_frame.add(keyring_box)
        self.newkeyring_combo = Gtk.ComboBoxText()
        idx = active_idx = 0
        keyrings = get_all_keyrings(self.connection)
        for keyring in keyrings:
            keyring_label = keyring.get_label()
            if len(keyring_label) > 0:
                self.newkeyring_combo.append_text(keyring_label)
                if keyring_label == self.new_keyring_label:
                    self.keyring = keyring
                    active_idx = idx
                idx += 1
        self.newkeyring_combo.set_active(active_idx)
        keyring_box.pack_start(self.newkeyring_combo, True, True, 0)

        key_frame = Gtk.Frame(label="Key", label_xalign=FRAME_LABEL_XALIGN)
        key_grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        self.box.add(key_frame)
        key_frame.add(key_grid)

        self.newkey_entry = Gtk.Entry(text=self.new_keyname,xalign=0)
        self.newkey_entry.set_max_width_chars(64)
        key_grid.attach_next_to(self.newkey_entry, None,
                                Gtk.PositionType.RIGHT, 2, 1)
        last_prompt = self.newkey_entry

        if self.old_created:
            if self.old_created != self.old_modified:
                created_prompt = Gtk.Label(label="Created", xalign=0)
                created_value  = Gtk.Label(label=timestamp( self.old_created),
                                                            xalign=0)
                key_grid.attach_next_to(created_prompt, last_prompt,
                                        Gtk.PositionType.BOTTOM, 1, 1)
                key_grid.attach_next_to(created_value, created_prompt,
                                        Gtk.PositionType.RIGHT, 1, 1)
                last_prompt = created_prompt
            modified_prompt = Gtk.Label(label=" Modified", xalign=0)
            modified_value  = Gtk.Label(label=timestamp( self.old_modified ),
                                                         xalign=0)
            key_grid.attach_next_to(modified_prompt, last_prompt,
                                    Gtk.PositionType.BOTTOM, 1, 1)
            key_grid.attach_next_to(modified_value, modified_prompt,
                                    Gtk.PositionType.RIGHT, 1, 1)
            last_prompt = modified_prompt

        self.box.add( Gtk.Label())
        attr_frame = Gtk.Frame(label="Attributes",
                               label_xalign=FRAME_LABEL_XALIGN)
        attr_grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        self.box.add(attr_frame)
        attr_frame.add(attr_grid)
        self.attr_prompt = {}
        self.attr_value  = {}
        last_prompt = None
        launch_button_active = False
        expiry_check = False
        for attr in self.new_attribs:
            if  attr != "xdg:schema":
                self.attr_prompt[attr] = Gtk.Entry(text=attr, xalign=0,
                                                   max_width_chars=20)
                self.attr_prompt[attr].set_max_width_chars(20)
                self.attr_value[attr]  = Gtk.Entry(text=self.new_attribs[attr],
                                                   xalign = 0)
                self.attr_value[attr].set_max_width_chars( 42 )
                attr_grid.attach_next_to(self.attr_prompt[attr], last_prompt,
                                         Gtk.PositionType.BOTTOM, 1, 1 )
                attr_grid.attach_next_to(self.attr_value[attr],
                                         self.attr_prompt[attr],
                                         Gtk.PositionType.RIGHT, 1, 1)
                if attr == "URL":
                    launch_button_active = True
                if attr == "validity":
                    expiry_check = self.old_created
                last_prompt = self.attr_prompt[attr]
                last_entry  = self.attr_value[attr]
        if self.extra_attribs:
            self.extra_attr_prompt = Gtk.Entry(xalign = 0)
            self.extra_attr_prompt.set_max_width_chars(20)
            self.extra_attr_entry  = Gtk.Entry(xalign = 0)
            self.extra_attr_entry.set_max_width_chars(42)
            attr_grid.attach_next_to(self.extra_attr_prompt, last_prompt,
                                     Gtk.PositionType.BOTTOM, 1, 1 )
            attr_grid.attach_next_to(self.extra_attr_entry,
                                     self.extra_attr_prompt,
                                     Gtk.PositionType.RIGHT, 1, 1 )
            last_prompt = self.extra_attr_prompt
            last_entry  = self.extra_attr_entry
        attr_button_box = Gtk.Box()
        if launch_button_active:
            launch_button = Gtk.Button(label="Launch")
            launch_button.connect("clicked", self.launch)
            attr_button_box.pack_end(launch_button, False, False, 0)
        add_button = Gtk.Button(label="Add")
        add_button.connect("clicked", self.add_attr)
        attr_button_box.pack_end(add_button, False, False, 2 )
        attr_grid.attach_next_to(attr_button_box, last_prompt,
                                 Gtk.PositionType.BOTTOM, 2, 1)
        self.box.add( Gtk.Label())
        label=secr_frame_label = "Secret"
        expiring = expired = False
        if expiry_check:
            validity = int(self.new_attribs["validity"])
            now = datetime.now()
            modified = datetime.fromtimestamp(self.old_modified)
            expired_date  = modified + timedelta(days=validity)
            expiring_date = modified + timedelta(days=validity - 7)
            if expired_date  < now:
                expired = True
                label = '<span foreground="red" weight="bold">Expired secret</span>'
                secr_frame_label = label
            elif expiring_date < now:
                expiring = True
                label = '<span foreground="orange" weight="bold">Expiring secret</span>'
                secr_frame_label = label
        secr_frame = Gtk.Frame(label=secr_frame_label,
                               label_xalign=FRAME_LABEL_XALIGN)
        if expiring or expired:
            secr_frame.get_label_widget().set_use_markup(True)
        secr_grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        self.box.add(secr_frame)
        secr_frame.add(secr_grid)
        self.secret_value = Gtk.Entry(text=self.new_secret, xalign=0,
                                      visibility=self.secret_visibilty)
        self.secret_value.connect("changed", self.update_complexity_levelbar)
        self.secret_value.set_max_width_chars(64)
        self.complexity_levelbar = Gtk.LevelBar()
        self.complexity_levelbar.set_min_value(password_complexity("abcdefgh"))
        self.complexity_levelbar.set_max_value(100)
        self.complexity_levelbar.add_offset_value("weak", password_complexity("Aa!456789"))
        self.complexity_levelbar.add_offset_value("ok", password_complexity("Aa!45678901"))
        self.complexity_levelbar.add_offset_value("strong", 100)
        self.complexity_levelbar.set_value( min(100, password_complexity( self.new_secret )))
        secret_copy_button = Gtk.Button(label="Copy")
        secret_copy_button.connect("clicked", self.copy_secret2clipboard)
        visi_text = "Hide" if self.secret_visibilty else "Show"
        visi_button = Gtk.Button(label=visi_text)
        visi_button.connect("clicked", self.toggle_secret_visibility)
        gen_button = Gtk.Button(label="Generate")
        gen_button.connect("clicked", self.generate_password)
        secret_promptbox = Gtk.Box(spacing=2)
        secret_promptbox.pack_end(visi_button, False, False, 0)
        secret_promptbox.pack_end(secret_copy_button, False, False, 0)
        secret_promptbox.pack_end(gen_button, False, False, 0)
        secr_grid.attach_next_to(self.secret_value, None,
                                 Gtk.PositionType.RIGHT, 1, 1)
        secr_grid.attach_next_to(self.complexity_levelbar, self.secret_value,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        secr_grid.attach_next_to(secret_promptbox, self.complexity_levelbar,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        last_prompt = secret_promptbox
        emptyline = Gtk.Label()
        self.box.add( emptyline )
        self.show_all()

    def update_complexity_levelbar(self, widget):
        """updates the complexity indicator when entry
        is done in the secret field"""
        pw = widget.get_text()
        complexity = password_complexity(pw)
        self.complexity_levelbar.set_value(min(100, complexity))

    def generate_password(self, button):
        """ action function for generate password """
        self.update_key_from_window()
        self.active_widget = dialog = PasswordGeneratorDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.new_secret = dialog.generate_new_password()
        dialog.destroy()
        self.active_widget = self
        self.secret_visibilty = False
        self.show_window()

    def launch(self, button):
        """ tries to find an attrib["URL"] and lauches it in a webbrowser """
        self.update_key_from_window()
        url = self.new_attribs["URL"]
        webbrowser.open(url, new=0, autoraise=True)
        self.out_of_focus_handler = self.connect("focus-out-event",
                                                 self.refocus)

    def refocus(self, widget, event):
        """ Tries to grab focus back after we lost it due to lauching an URL """
        self.present()
        if self.out_of_focus_handler:
            self.disconnect(self.out_of_focus_handler)
            self.out_of_focus_handler = None

    def update_key_from_window(self):
        """ copies the values from screen to internal structures """
        self.new_keyring_label = self.newkeyring_combo.get_active_text()
        self.new_keyname = self.newkey_entry.get_text()
        screen_attribs = {}
        for attr in self.new_attribs:
            if  attr != "xdg:schema":
                prompt = self.attr_prompt[attr].get_text()
                if prompt != "":
                    value  = self.attr_value[attr].get_text()
                    screen_attribs[prompt] = value
        if self.extra_attribs:
            prompt = self.extra_attr_prompt.get_text()
            if prompt != "":
                value  = self.extra_attr_entry.get_text()
                screen_attribs[prompt] = value
            self.extra_attribs = False
        self.new_secret = self.secret_value.get_text()
        self.new_attribs = screen_attribs

    def toggle_secret_visibility(self, button):
        """ toggles the visibiity of the password """
        self.update_key_from_window()
        self.secret_visibilty = not self.secret_visibilty
        self.show_window()

    def add_attr(self, button):
        """ adds an attribute line to the window """
        self.update_key_from_window()
        self.extra_attribs = True
        self.show_window()

    def copy_secret2clipboard(self, widget):
        " copies the secret from screen to the clipboard """
        self.update_key_from_window()
        copy_text2clipboard(self.new_secret)

    def deletekey(self):
        """ Deletes a key """
        dialog = Gtk.Dialog(title="Delete key", flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dialog.set_default_size(150, 100)
        content_area = dialog.get_content_area()
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.pack_start(Gtk.Label(), True, True, 0)
        box.pack_start(Gtk.Label(label="  Are you sure to delete key '"
                                + self.old_keyname
                                + "' ?  "), True, True, 0)
        content_area.add(box)
        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.key.delete()
        dialog.destroy()

    def savekey(self):
        """ Saves a key """
        self.update_key_from_window()
        if self.old_keyname != self.new_keyname:
            self.key.set_label(self.new_keyname)
        if self.old_attribs != self.new_attribs:
            self.key.set_attributes(self.new_attribs)
        if self.old_secret != self.new_secret:
            self.key.set_secret(self.new_secret.encode("utf-8"))
        if self.keyring and self.old_keyring_label != self.new_keyring_label:
            self.key.move(self.new_keyring_label)

    def create_newkey( self, keyring):
        """ Creates a new key """
        self.update_key_from_window()
        self.key = keyring.create_key( label=self.new_keyname,
                                       attributes=self.new_attribs,
                                       secret=self.new_secret.encode("utf-8"))


class AddKeyRingDialog(Gtk.Dialog):
    """ AddKeyRingDialog: window class to add a keyring,
        prompts for keyring name """
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="New keyring", flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        box = self.get_content_area()
        keyringname_prompt = Gtk.Label(label="Keyring name", xalign=0)
        self.keyringname_input = Gtk.Entry(text="New keyring", xalign = 0)
        grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        box.add(grid)
        grid.attach_next_to(keyringname_prompt, None,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.keyringname_input, keyringname_prompt,
                            Gtk.PositionType.RIGHT, 1, 1)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.show_all()

    def get_newkeyringname(self):
        """ get_newkeyringname: returns the entered name for a new keyring"""
        return self.keyringname_input.get_text()


class StatusIcon:
    """Main entry point, creates a tray icon, and handles rightclicks"""
    def __init__(self):
        self.dbus_open = False
        self.statusicon = Gtk.StatusIcon()
        self.statusicon.set_from_file( icon_path(ICONNAME, 48))
        self.statusicon.connect("popup-menu", self.right_click_event)
        self.statusicon.set_title("Password manager")
        self.statusicon.set_tooltip_text("krapplet: a password manager")
        self.statusicon.set_visible(True)
        self.embedded = False
        GLib.idle_add(self.embed_check)
        GLib.timeout_add(APP_EMBED_TIMEOUT, self.embed_timeout)
        self.active_widget = None

    def embed_check(self):
        """ keep calling until we are embedded """
        if self.statusicon.is_embedded():
            self.embedded = True
            return False                    # don't call again
        return True

    def embed_timeout(self):
        """ if still not emebedded then exit program """
        if self.embedded:
            return False                    # don't call again
        print("Error: could not embed in systray", file=sys.stderr)
        Gtk.main_quit()
        return True

    def right_click_event(self, icon, button, time):
        """ shows the popop menu """
        if self.active_widget:
            self.active_widget.present()
            return
        if self.dbus_open:
            self.connection.close()
        self.connection = connection_open()
        self.dbus_open = True
        self.menu = Gtk.Menu()
        self.keyrings = get_all_keyrings(self.connection)
        self.keyring_labels = []
        for keyring in self.keyrings:
            keyring_label = keyring.get_label()
            if len(keyring_label):
                item = Gtk.MenuItem(label=keyring_label)
                submenu = Gtk.Menu()
                if keyring.is_locked():             # try auto unlock
                    unlock_searchkey = {"keyring" : "LOCAL:/keyrings/"
                                        + keyring_label.replace(" ", "_")
                                        + ".keyring"}
                    unlock_keys = search_keys(self.connection,
                                              unlock_searchkey)
                    for unlock_key in unlock_keys:
                        if not unlock_key.is_locked():
                            keyring.unlock()
                if keyring.is_locked():
                    add_item2menu(mnu=submenu, label="Unlock",
                                  action=self.unlock_keyring, data=keyring)
                else:
                    nrof_keys = 0
                    self.keyring_labels.append(keyring_label)
                    try:
                        for key in keyring.get_all_keys():
                            if key.is_locked():
                                lock_return = key.unlock()
                            key.keyring_label = keyring_label
                            key.keyring_labels = self.keyring_labels
                            add_item2menu(mnu=submenu, label=key.get_label(),
                                          action=self.key_dialog, data=key)
                            nrof_keys += 1
                    except KeyNotFoundException:
                        show_error_message(
                            self.active_widget,
                            "Key not found exception",
                            "Restarting gnome-keyring; this will lock all keyrings" )
                        msg = subprocess.check_output(
                            ["gnome-keyring-daemon", "-r", "-d"],
                            stderr=subprocess.STDOUT )
                        show_info_message(
                             self.active_widget,
                             "Output of gnome-restart command",
                             msg.decode("utf-8"))
                    except:
                        print( "class sys.exc_info()[0]:" , sys.exc_info()[0].__class__)
                        """show_error_message(
                             self.active_widget,
                             "Unexpected error occured, please report this error",
                             sys.exc_info()[0]) """
                    if nrof_keys:
                        add_separator2menu(submenu)
                    add_item2menu(mnu=submenu, label="Add key",
                                  action=self.add_key, data=keyring)
                    if  not nrof_keys:
                        add_item2menu(mnu=submenu, label="Remove keyring",
                                      action=self.remove_keyring, data=keyring)
                    add_item2menu(mnu=submenu, label="Lock keyring",
                                  action=self.lock_keyring, data=keyring )
                item.set_submenu(submenu)
                self.menu.append(item)
        add_separator2menu( self.menu )
        add_item2menu(mnu=self.menu, label="Add keyring",
                      action=self.add_keyring, data=None)
        add_item2menu(mnu=self.menu, label="Backup",
                      action=self.backup, data=None)
        add_item2menu(mnu=self.menu, label="Restore",
                      action=self.restore, data=None)
        add_item2menu(mnu=self.menu, label="About",
                      action=self.show_about_dialog, data=None)
        add_item2menu(mnu=self.menu, label="Quit",
                      action=Gtk.main_quit, data=None)
        self.menu.show_all()
        self.menu.popup(None, None, None, self.statusicon, button, time)

    def unlock_keyring(self, widget, keyring):
        """Unocks a keyring"""
        keyring.unlock()

    def lock_keyring(self, widget, keyring):
        """Locks a keyring"""
        keyring.lock()

    def remove_keyring(self, widget, keyring):
        """Removes a keyring, when it is empty.
        If not it shows an error message"""
        keycount = 0
        for key in keyring.get_all_keys():
            keycount += 1
        if keycount:
            show_error_message(self.active_widget,
                               "Error deleting  keyring",
                               "Keys are still attached to keyring" )
        else:
            keyring.delete()

    def key_dialog(self, widget, key):
        """Pops up a window showing a key, with all the attribs"""
        if not key.is_locked():               # check check double check
            self.active_widget = dialog = KeyDialog(self, key=key)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.savekey()
            elif response == APP_RESPONSE_DELETE:
                dialog.deletekey()
            copy_text2clipboard("")
            dialog.destroy()
            self.active_widget = None
        else:
            show_error_message(self.active_widget,
                               "Key locked", key.get_label() )

    def add_key(self, widget, keyring):
        """Add_key adds a key to a keyrng"""
        self.active_widget = dialog = KeyDialog(self, keyring=keyring)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.create_newkey(keyring)
        dialog.destroy()
        self.active_widget = None

    def add_keyring(self, widget):
        """Pops up a window asking for a new keyring name"""
        self.active_widget = dialog = AddKeyRingDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            keyringname = dialog.get_newkeyringname()
            try:
                create_keyring(self.connection, keyringname)
            except Exception as e:
                show_error_message(self.active_widget,
                                   "Error saving new keyring", str( e ))
        dialog.destroy()
        self.active_widget = None

    def backup(self, widget):
        kr_backup.backup()

    def restore(self, widget):
        kr_backup.restore()

    def show_about_dialog(self, widget):
        """Shows the about dialog"""
        image = Gtk.Image()
        image.set_from_file(icon_path( ICONNAME, 96))
        icon_pixbuf = image.get_pixbuf()
        self.active_widget = about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_logo(icon_pixbuf)
        about_dialog.set_program_name("krapplet")
        about_dialog.set_version("Version " + __VERSION__)
        about_dialog.set_comments("A password manager using gnome-keyring or pass")
        about_dialog.set_authors(["Johannes Willem Fernhout"])
        about_dialog.set_copyright( "(c) 2020-2022 Johannes Willem Fernhout")
        about_dialog.set_license(BSD_LICENSE)
        about_dialog.set_website("https://gitlab.com/hfernh/krapplet")
        about_dialog.set_website_label("krapplet on GitLab")
        about_dialog.show_all()
        about_dialog.run()
        about_dialog.destroy()
        self.active_widget = None

    def __del__(self):
        """ exit code, just some housekeeping """
        if self.dbus_open:
            self.connection.close()


def main():
    """ krapplet main """
    # ignore GTK deprecation warnings gwhen not in development mode
    # for development mode, run program as python3 -X dev krapplet
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    setup_ccs()
    ico = StatusIcon()
    signal.signal(signal.SIGINT, sigint_handler)
    Gtk.main()

if __name__ == "__main__":
    main()
