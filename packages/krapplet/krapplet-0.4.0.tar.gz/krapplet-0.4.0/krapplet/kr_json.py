#!/usr/bin/env python3

"""
kr_json: functions for translating keyrings and keys to xml and vice versa
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import locale
from datetime import datetime
#import xml.etree.ElementTree as ET
import json

from .kr_storage import \
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
    dic = {}
    dic["keyring_label"] = kr_label
    dic["keys" ] = []
    for key in keyring.get_all_keys():
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
            dic["keyrings"].append(dic_keyring(keyring))
    return dic

def dic2str(kr_dic):
    return json.dumps(kr_dic)

def str2dic(kr_str):
    return json.loads( kr_str )




"""
JSON format:

json_str = '{ "keyring" : [ {  "keyring label" : "<keyring label>", "key" : [ { "key label" : "<key label>" }, {  "key label" : "<key2 label>" } ] } , { "keyring label" : "<keyring label>" } ] }'
"""
