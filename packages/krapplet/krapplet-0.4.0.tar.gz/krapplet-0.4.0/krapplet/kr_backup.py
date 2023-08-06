#!/usr/bin/env python

"""
kr_backup: functions for backing up keyrings and keys
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import os
from datetime import datetime

# Assume gtk availability check done in krapplet.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import kr_crypt
from . import kr_json
from . import kr_password_entry
from . import kr_filepicker
from . import kr_storage
from .kr_popup import show_error_message, show_info_message
from .kr_time import timestamp

FRAME_LABEL_XALIGN = 0.025

def backup(path = None):
    """ backups all keysring and keys to a file indicated by path
    if path is None, a file picker option will be provided """

    kr_dic = kr_json.dic_all_keyring()
    #kr_str = json.dumps(kr_dic)
    kr_str = kr_json.dic2str(kr_dic)
    pw_prompt = "Passphrase for backup file"
    passphrase = kr_password_entry.show_password_entry_window(
        title = pw_prompt)
    kr_enc_str = kr_crypt.sym_encrypt(kr_str, passphrase)
    now = datetime.now()
    timestamp_formatstr = "%Y-%m-%d_%H:%M"
    timestamp = now.strftime(timestamp_formatstr)
    backup_fname = "krapplet_" + timestamp + ".bak"
    if path:
        backup_fname = os.path.join(path, backup_fname)
    else:
        folder_picker = kr_filepicker.FilePicker("Backup", backup_fname,
                                                 kr_filepicker.SAVE)
        #folder_picker.dialog.run()
        backup_fname = folder_picker.selected_file()
    if backup_fname:                 # would be None on escape key
        try:
            with open(backup_fname, "wb") as backup_file:
                backup_file.write(kr_enc_str)
                info_msg = "Backup file: " + backup_fname
                show_info_message(None, "Backup successful", info_msg)
        except PermissionError:
            errormsg = "Cannot open file " + backup_fname + " for writing"
            show_error_message(None, "Permission error", errormsg )
        except Exception as exc:
            show_error_message(None, "Error saving backup", str(exc))



class  RestoreDialog(Gtk.Dialog):
    """ class to show keyrings, keys, and attribs, for restore function """
    def __init__(self, backup_fname, dic):
        Gtk.Dialog.__init__(self, title="Restore " + backup_fname, flags=0 )
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        content_area = self.get_content_area()
        self.grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        content_area.add(self.grid)
        self.keyring_frame = Gtk.Frame(label="Keyrings", 
                                       label_xalign=FRAME_LABEL_XALIGN)
        self.grid.attach_next_to(self.keyring_frame, None,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.keyringbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                                  border_width = 5)
        self.keyring_frame.add(self.keyringbox)
        self.key_frame = self.attr_frame = None
        self.restore_all_keys_button = self.restore_button = None

        keyrings = dic["keyrings"]
        kr_group = None
        for keyring in keyrings:
            kr_button = Gtk.RadioButton.new_with_label_from_widget(
                kr_group, keyring["keyring_label"][:32])
            kr_button.connect("toggled", self.show_keyring, keyring)
            self.keyringbox.pack_start(kr_button, False, False, 0)
            if not kr_group:            # first one
                kr_group = kr_button
                self.show_keyring( kr_button, keyring)
        restore_all_keyrings_button = Gtk.Button("Restore all keyrings",
                                                 border_width = 10)
        restore_all_keyrings_button.connect(
            "clicked", self.restore_all_keyrings, keyrings)
        self.grid.attach_next_to(restore_all_keyrings_button,
                                 self.keyring_frame,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.show_all()

    def clear_keybox(self):
        "clear the keyring box"
        if self.key_frame:
            self.key_frame.destroy()
            self.key_frame = None
        if self.restore_all_keys_button:
            self.restore_all_keys_button.destroy()
            self.restore_all_keys_button = None

    def clear_attrbox(self):
        "clear the keyring box"
        if self.attr_frame:
            self.attr_frame.destroy()
            self.attr_frame = None
        if self.restore_button:
            self.restore_button.destroy()
            self.restore_button = None

    def show_keyring(self, button, keyring):
        """ Shows the keys in a keyring """
        if not button.get_active():       # only when activated
            self.clear_keybox()
            self.clear_attrbox()
            return
        #self.key_frame = Gtk.Frame(label="Keys",
        self.key_frame = Gtk.Frame(
            label=keyring["keyring_label"][:20] + " keys",
            label_xalign=FRAME_LABEL_XALIGN)
        self.grid.attach_next_to(self.key_frame, self.keyring_frame,
                                 Gtk.PositionType.RIGHT, 1, 1)
        self.keybox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,
                              border_width = 5)
        self.key_frame.add(self.keybox)
        key_group = None
        for key in keyring["keys"]:
            keybutton = Gtk.RadioButton.new_with_label_from_widget(
                key_group, key["key_label"][:32])
            keybutton.connect("toggled", self.show_key, keyring, key)
            self.keybox.pack_start(keybutton, False, False, 0)
            if not key_group:
                key_group = keybutton
                self.show_key(keybutton, keyring, key)
        self.restore_all_keys_button = Gtk.Button("Restore all keys",
                                                   border_width = 10)
        self.restore_all_keys_button.connect("clicked",
                                             self.restore_all_keys, keyring)
        self.grid.attach_next_to(self.restore_all_keys_button,
                                 self.key_frame,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        self.show_all()


    def show_key(self, button, keyring, key):
        if not button.get_active():
            self.clear_attrbox()
            return
        #self.attr_frame = Gtk.Frame(label="Attributes",
        self.attr_frame = Gtk.Frame(
            label=key["key_label"][:32] + " attributes",
            label_xalign=FRAME_LABEL_XALIGN)
        self.grid.attach_next_to(self.attr_frame, self.key_frame,
                                 Gtk.PositionType.RIGHT, 1, 1)
        key_grid = Gtk.Grid(row_spacing=2, column_spacing=5,border_width=5)
        self.attr_frame.add(key_grid)
        created_prompt = Gtk.Label(label="Created", xalign=0)
        created_value = Gtk.Label(label=timestamp(int(key["created"])),
                                  xalign=0)
        key_grid.attach_next_to(created_prompt,None,
                                Gtk.PositionType.BOTTOM, 1, 1)
        key_grid.attach_next_to(created_value, created_prompt,
                                Gtk.PositionType.RIGHT, 1, 1)

        modified_prompt = Gtk.Label(label="Modified", xalign=0)
        modified_value = Gtk.Label(label=timestamp(int(key["modified"])),
                                   xalign=0)
        key_grid.attach_next_to(modified_prompt, created_prompt,
                                Gtk.PositionType.BOTTOM, 1, 1)
        key_grid.attach_next_to(modified_value, modified_prompt,
                                Gtk.PositionType.RIGHT, 1, 1)

        last_prompt = modified_prompt
        attribs = key["attributes"]
        for attr in attribs:
            attr_prompt = Gtk.Label(label=attr[:32], xalign=0)
            attr_value = Gtk.Label(label=attribs[attr][:32], xalign=0)
            key_grid.attach_next_to(attr_prompt, last_prompt,
                                    Gtk.PositionType.BOTTOM, 1, 1)
            key_grid.attach_next_to(attr_value, attr_prompt,
                                    Gtk.PositionType.RIGHT, 1, 1)
            last_prompt = attr_prompt

        secret_pronpt = Gtk.Label(label="Secret", xalign=0)
        masked_secret = key["secret"][:2] + " ... " + key["secret"][-2:]
        secret_value = Gtk.Label(label=masked_secret, xalign=0)
        key_grid.attach_next_to(secret_pronpt, last_prompt,
                                Gtk.PositionType.BOTTOM, 1, 1)
        key_grid.attach_next_to(secret_value, secret_pronpt,
                                Gtk.PositionType.RIGHT, 1, 1)
        self.restore_button = Gtk.Button("Restore Key", border_width = 10)
        self.restore_button.connect("clicked", 
                                    self.restore_key, keyring, key)
        self.grid.attach_next_to(self.restore_button, self.attr_frame,
                                 Gtk.PositionType.BOTTOM, 1, 1)

        self.show_all()
        return

    def restore_all_keyrings(self, button, keyrings):
        " Restores all the keyrings from the backup "
        log = []
        for keyring in keyrings:
            for rkey in keyring["keys"]:
                self.restore_one_key(keyring, rkey, log)
        if len(log) > 0:
            show_info_message(None, "Restore log", log)

    def restore_all_keys(self, button, restore_keyring):
        " Restores all keys in a keyring "
        log = []
        for rkey in restore_keyring["keys"]:
            self.restore_one_key(restore_keyring, rkey, log)
        if len(log) > 0:
            show_info_message(None, "Restore log", log)

    def restore_key(self, button, restore_keyring, restore_key):
        log = []
        self.restore_one_key(restore_keyring, restore_key, log)
        if len(log) > 0:
            show_info_message(None, "Restore log", log)

    def restore_one_key(self, restore_keyring, restore_key, log):
        " restores a key to the main storage "
        update_done = False
        conn = kr_storage.connection_open()
        for keyring in kr_storage.get_all_keyrings(conn):
            kr_label = keyring.get_label()
            if kr_label == restore_keyring["keyring_label"]:
                for key in keyring.get_all_keys():
                    k_label = key.get_label()
                    if k_label == restore_key["key_label"]:
                        key.set_attributes(restore_key["attributes"])
                        key.set_secret(restore_key["secret"].encode())
                        update_done = True
                        log.append("Key "
                                   + k_label
                                   + " in keyring "
                                   + kr_label
                                   + ": attributes and secret updated.")
                if not update_done:       # key not found
                    if keyring.is_locked():
                        keyring.unlock()
                    if not keyring.is_locked():
                        key = keyring.create_key(
                            restore_key["key_label"],
                            restore_key["attributes"],
                            restore_key["secret"].encode())
                        log.append("Key "
                                   + restore_key["key_label"]
                                   + " in keyring "
                                   + kr_label
                                   + ": created.")
                    update_done = True
        if not update_done:               # keyring not found
            keyring = kr_storage.create_keyring(
                conn, restore_keyring["keyring_label"])
            log.append("Keyring "
                       + restore_keyring["keyring_label"]
                       + ": created.")
            if keyring.is_locked():
                keyring.unlock()
            if not keyring.is_locked():
                key = keyring.create_key(restore_key["key_label"],
                                         restore_key["attributes"],
                                         restore_key["secret"].encode())
                log.append("Key "
                           + restore_key["key_label"]
                           + " in keyring "
                           + restore_keyring["keyring_label"]
                           + ": created")

            else:
                show_error_message(None, 
                                   "Keyring not restored", "Keyring locked")
        return


def restore():
    """ restores keyrings and keys """
    backup_fname = ""
    folder_picker = kr_filepicker.FilePicker("Restore", backup_fname,
                                              kr_filepicker.OPEN)
    backup_fname = folder_picker.selected_file()
    enc_data = None
    if backup_fname:
        try: 
            with open(backup_fname, "rb") as backup_file:
                enc_data = backup_file.read()
        except PermissionError:
            errormsg = "Cannot open file " + backup_fname + " for reading"
            show_error_message(None, "Permission error", errormsg )
        except Exception as exc:
            show_error_message(None, "Error reading backup", str(exc))
    if enc_data:
        pw_prompt = "Passphrase for backup file"
        done = False
        while not done:
            passphrase = kr_password_entry.show_password_entry_window(
                title = pw_prompt)
            if passphrase:
                decstr = kr_crypt.sym_decrypt(enc_data, passphrase)
                if decstr:
                    dic = kr_json.str2dic(decstr)
                    dia = RestoreDialog(backup_fname, dic)
                    dia.run()
                    dia.destroy()
                    done = True
            else:
                done = True


