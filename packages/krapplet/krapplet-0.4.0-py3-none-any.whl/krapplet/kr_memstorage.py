#!/usr/bin/env python3

"""
kr_memstorage: an in--memory storage provider, used for testing 
purposes and intermediairy layer for backup/restore import/export etc
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

from datetime import datetime
from typing import Dict, Iterator
import locale
from datetime import datetime
#import xml.etree.ElementTree as ET
import json

DEFAULT_COLLECTION = "????"

#from kr_pass import \
from .kr_secretstorage import \
    connection_open, create_keyring, \
    get_all_keyrings, search_keys, NotAvailableException, \
    LockedException, KeyNotFoundException, PromptDismissedException

# FIXME: needs to move to util.py ...!!
def timestamp(since_epoch):
    """returns a string according to local locale
    based on seconds since epoch 1-JAN-1970"""
    if since_epoch:
        from_timestamp = datetime.fromtimestamp(since_epoch)
        date_string = from_timestamp.strftime(
            locale.nl_langinfo(locale.D_T_FMT))
        return date_string
    return""


#def dic_key( dic, key):
def dic_key(key):
    """ materialized key """
    k_label = key.get_label()
    """
    dic[k_label] = {}
    dic[k_label]["created"] = str(int(key.get_created()))
    dic[k_label]["modified"] = str(int(key.get_modified()))
    dic[k_label]["secret"] = key.get_secret().decode("utf-8")
    dic[k_label]["attributes"] = key.get_attributes()
    """
    dic = {}
    dic["key_label"] = k_label
    dic["created"] = str(int(key.get_created()))
    dic["modified"] = str(int(key.get_modified()))
    dic["secret"] = key.get_secret().decode("utf-8")
    dic["attributes"] = key.get_attributes()
    return dic


#def dic_keyring( dic, keyring):
def dic_keyring( keyring):
    """ materialized keyring """
    kr_label = keyring.get_label()
    #dic[kr_label] = {}
    dic = {}
    dic["keyring_label"] = kr_label
    dic["keys" ] = []
    for key in keyring.get_all_keys():
        #dic_key(dic[kr_label], key)
        dic["keys" ].append(dic_key(key))
    return dic

def dic_all_keyring():
    """ returns the dictionary representation of all keyrings """

    dic = {}
    dic["keyrings"] = []
    conn = connection_open()
    for keyring in get_all_keyrings(conn):
        if keyring.is_locked():
            keyring.unlock()
        if not keyring.is_locked() and len(keyring.get_label()) > 0:
            #dic_keyring( kr_dic, keyring )
            dic["keyrings"].append(dic_keyring(keyring))
    return dic


from .kr_password_entry import show_password_entry_window


# Exception classes:
class PassException(Exception):
    """All exceptions derive from this class."""
    pass

class NotAvailableException(PassException):
    pass

class LockedException(PassException):
    pass

class KeyNotFoundException(PassException):
    pass

class PromptDismissedException(PassException):
    pass



class Path():
    """ hold the keyringlabel and the keylabel """

    def __init__(self, keyringlabel = None, keylabel=None):
        self.keyringlabel = keyringlabel
        self.keylabel = keylabel

    def set_keyringlabel(self, keyringlabel):
        self.keyringlabel = keyringlabel

    def set_keylabel(self, keylabel):
        self.keylabel = keylabel


class Connection():
    """ This class maintains the passhrase for gpg """

    passphrase = "" 
    locked = True
    keyrings = {}
    keyrings["keyrings"] = []

    def add_keyring(self, keyringlabel):
        keyring = {}
        keyring["label"] = keyringlabel
        keyring["key_list"] = []
        Connection.keyrings["keyrings"].append(keyring)

    def get_keyring(self, keyringlabel):
        for keyring in Connection.keyrings["keyrings"]:
            if keyring["label"] == keyringlabel:
                return keyring
        print("get_keyting: -- not found" )
        return None


    def get_key(self, keyringlabel, keylabel):
        keyring = self.get_keyring(keyringlabel)
        if keyring:
            for key in keyring["key_list"]:
                if key["label"] == keylabel:
                    return key
                else:
                    print("get_key - key not found")
        else:
            print("get_key = keyring not found")
        return None

    def add_key(self, path):

        keyringlabel = path.keyringlabel
        keylabel = path.keylabel
        """ path actually contains the keyring label """
        keyring = self.get_keyring(keyringlabel)
        if keyring:
            key = {}
            key["label"] = keylabel
            key["created"] = key["modified"] = datetime.now()
            key["secret"] = ""
            key["attributes"] = {}
            keyring["key_list"].append(key)
            return
        print( "Cannot add key", keylabel,
                "to keyring", keyringlabel,
               ": keyring not found" )

    def delete_key(self, keyringlabel, keylabel):
        keyring = self.get_keyring(keyringlabel)
        if keyring:
            key = self.get_key(keyringlabel, keylabel)
            if key:
                keyring["key_list"].remove(key)
            else:
                print("key not found")
        else:
            print("keyring not found")

    def delete_keyring(self, keyringlabel):
        keyring = self.get_keyring(keyringlabel)
        self.keyrings["keyrings"].remove(keyring)


    def get_passphrase(self) -> str:
        """ performs validity check and returns the password str,
            or "" when it was cleared """
        return Connection.passphrase

    def set_passphrase(self, passphrase: str) -> None:
        """ set the passphrase for the connection,
        in fact unlocking the connection """
        Connection.passphrase = passphrase
        Connection.locked = False

    def lock(self) -> None:
        """ Locks a connection by clearing the passphrase """
        Connection.passphrase = ""
        Connection.locked = True

    def is_locked(self) -> bool:
        """ Returns the current lock state of a connection """
        return Connection.locked

    def close(self) -> None:
        """ closes the connection, no action needed actually """


def connection_open() -> Connection:
    """ Opens the connection to the pass store, verifies it existence """
    conn = Connection()
    return conn


class Key():
    """Represents a secret item."""
    def __init__(self, connection, path: str, session = None) -> None:
        self.connection = connection
        self.path = path
        connection.add_key(self.path)

    def __eq__(self, other) -> bool:
        return (self.path == other.path)

    def is_locked(self) -> bool:
        """Returns: True if item is locked, otherwise False."""
        return self.connection.is_locked()

    def ensure_not_locked(self) -> None:
        """If kehyring is locked, raises: LockedException"""
        if self.connection.is_locked():
            raise LockedException("Item is locked!")

    def lock(self) -> None:
        """ Lock the connection """
        self.connection.lock()

    def unlock(self) -> bool:
        """ to simulate unlocking, a password prompt is showm,
            the password is captured, and with the password we try to decrypt
            the key. Return True if successful, False otherwise """

        while self.is_locked():
            passwd = show_password_entry_window()
            #if len( passwd ) > 0:
            if passwd != None:
                self.connection.set_passphrase(passwd)
                self.connection.unlock()
                return True
            else:
                return False           # no entry or escape pressed

    def get_key(self):
        key = self.connection.get_key(self.path.keyringlabel,
                                      self.path.keylabel)
        if key:
            return key
        else:
            raise KeyNotFoundException("Key " + self.keylabel + " not found" )

    def get_attributes(self) -> Dict[str, str]:
        """Returns item attributes (dictionary)."""
        key = self.get_key()
        return key["attributes"]

    def set_attributes(self, attributes: Dict[str, str]) -> None:
        """ Sets item attributes to attributes """
        key = self.get_key()
        key["attributes"] = attributes

    def get_label(self) -> str:
        """ retrieves the label for a key """
        return self.path.keylabel

    def set_label(self, label: str) -> None:
        """ the label is the last part of the itempath,
        changing the label means renamiing the file """
        key = self.get_key()
        key["label"] = label
        self.path.set_keylabel(label)

    def delete(self) -> None:
        """ just delete the file? """
        self.connection.delete_key(self.path.keyringlabel,
                                   self.path.keylabel)

    def get_secret(self) -> bytes:
        """Returns item secret (bytestring)."""
        key = self.get_key()
        return key["secret"]

    def get_secret_content_type(self) -> str:
        """ Not supported as such, therefore always return text/plain """
        return "text/plain"

    def set_secret(self, secret: bytes,
                   content_type: str = 'text/plain') -> None:
        """Sets secret to `secret`,
           content_type is there for compat reasons, but is ignored """
        key = self.get_key()
        key["secret"] = secret

    def get_created(self) -> int:
        """Returns UNIX timestamp (integer), when the item was created. """
        key = self.get_key()
        return key["created"]

    def get_modified(self) -> int:
        """Returns UNIX timestamp, when the item was last modified."""
        key = self.get_key()
        return key["modified"]

    def move(self, new_keyring_label):
        key = self.get_key()
        self.connection.delete_key(self.path.keyringlabel,
                                   self.path.keylabel)
        newkeyring = self.connection.get_keyring(new_keyring_label)
        self.path.set_keyringlabel(new_keyring_label)
        newkeyring["key_list"].append(key)


class Keyring():
    """Represents a kehyring."""

    def __init__(self,
                 connection: Connection,
                 path: str = DEFAULT_COLLECTION,
                 session = None) -> None:
        """ the path is the keyring label """
        self.path = Path(keyringlabel = path)
        self.connection = connection
        #connection.add_keyring(self.path.keyringlabel)

    def is_locked(self) -> bool:
        """Returns :const:`True` if item is locked,
           otherwise :const:`False`."""
        return self.connection.is_locked()

    def ensure_not_locked(self) -> None:
        """If keyring is locked, raises LockedException"""
        if self.is_locked():
            raise LockedException('Keyring is locked!')

    def unlock(self) -> bool:
        """ Attempts to unlock a Keyring, 
            currently not using the gpg-agent """
        is_locked = self.is_locked()
        while is_locked:
            passwd = show_password_entry_window()
            #if len( passwd ) > 0:
            if passwd != None:
                self.connection.set_passphrase(passwd)
                is_locked = False
            else:
                break
        return self.is_locked()

    def lock(self) -> None:
        """Locks the keyring."""
        self.connection.lock()

    def delete(self) -> None:
        """Deletes the keyringi and all keys attached to it."""
        self.connection.delete_keyring(self.path.keyringlabel)
        self.keyringlabel = None

    def get_all_keys(self) -> Iterator[Key]:
        """Returns a generator of all keys on the keyring."""
        keyring = self.connection.get_keyring(self.path.keyringlabel)
        if keyring:
            keygen = (Key(self.connection, 
                          Path(self.path.keyringlabel, key["label"])) 
                          for key in keyring["key_list"])
            return keygen
        return

    def search_items(self, attributes: Dict[str, str]) -> Iterator[Key]:
        """Returns a generator of keys with the given attributes."""
        keyring = self.connection.get_keyring(self.path.keyringlabel)
        if keyring:
            for key in keyring["key_list"]:
                key_attributes = key.get_attributes()
                for attrib in key_attributes:
                    if attrib == attributes:
                        yield key
        return


    def get_label(self) -> str:
        """Returns the keyring label."""
        return self.path.keyringlabel

    def set_label(self, label: str) -> None:
        """ the label is the last part of the keyring path,
            changing the label means renamiing the dir """
        self.ensure_not_locked()
        keyring = self.connection.get_keyring(self.path.keyringlabel)
        if keyring:
            self.keyringlabel = keyring["keyring_label"] = label
            self.path.set_keyringlabel(label)


    def create_key(self, label: str, attributes: Dict[str, str],
                   secret: bytes, replace: bool = False,
                   content_type: str = 'text/plain') -> Key:

        """ Creates a key and returns it """
        keypath = Path(keyringlabel = self.path.keyringlabel,
                       keylabel = label)
        key = Key(self.connection, keypath)
        if key:
            key.set_secret(secret)
            key.set_attributes(attributes)
            return key
        return None                     # FIXME: raise an exception ?



def create_keyring(connection: Connection, label: str,
                   alias: str = '', session = None) -> Keyring:
    """Creates a new keyring and returns it. Alias and session are ignored
    for this implementation it only requires a directory to be created """

    keyring = Keyring(connection, label)
    connection.add_keyring(label)
    return keyring


def get_all_keyrings(connection) -> Iterator[Keyring]:
    """Returns a generator of all available keyrings."""

    """
    for con_keyring in connection.keyrings["keyrings"]:
        keyringlabel = con_keyring["label"]
        keyring = Keyring(connection, keyringlabel)
        yield keyring
    """
    keyring_gen = (Keyring(connection, con_keyring["label"])
                   for con_keyring in connection.keyrings["keyrings"])
    return keyring_gen


def get_default_keyring(connection,session = None) -> Keyring:
    """Returns the default keyring. If it doesn't exist, creates it."""
    for keyring in self.get_all_keyrings( connection ):
        if keyring.get_label() == "default":
            return keyring
    return Keyring(connection, "default")


def get_any_keyring(connection) -> Keyring:
    """Returns any keyring, in the following order of preference:
    - The default keyring;
    - The "session" keyring (usually temporary);
    - The first keyring in the keyring list."""

    return get_default_keyring()


def get_keyring_by_alias(connection, alias: str) -> Keyring:
    """Returns the keyring with the given `alias`. If there is no
    such keyring, raises KeyNotFoundException"""

    for keyring in get_all_keyrings(connection):
        if keyring.get_label() == alias:
            return keyring
    raise KeyNotFoundException('No keyring found.')


def search_keys(connection, attributes: Dict[str, str]) -> Iterator[Key]:
    """Returns a generator of keys in all keyrings with the given
    attributes. `attributes` should be a dictionary."""
    for keyring in get_all_keyrings(connection):
        return keyring.search_items(attributes)
    return
