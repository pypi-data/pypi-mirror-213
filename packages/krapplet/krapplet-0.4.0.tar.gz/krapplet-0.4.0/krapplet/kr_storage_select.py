"""
kr_storage_select: part of krapplet, a password manager
This module selects the right stoage provider
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

import sys

STORAGE_PROVIDERS = ["gnome-keyring", "memory", "pass"]


class StorageSelect():
    """ class to hoild the selected provider in a class variable
        the intended use is that after the commenadline parameter
        evaluation a storage provider is chosen, e.g. "pass", or
        "gnome-keyring", and that is stored here using the constructor.
        Next using the get function the set provider can be retrieved. """

    provider = None
    gpg_id = None
    armor = None

    def __init__(self, provider = None, gpg_id = None, armor = None):
        if provider:
            if provider in STORAGE_PROVIDERS:
                StorageSelect.provider = provider
                if gpg_id:
                    StorageSelect.gpg_id = gpg_id
                if armor:
                    StorageSelect.armor = armor
            else:
                print("krapplet: error: unrecognized storage provider",
                      provider, file=sys.stderr)
                sys.exit(1)
