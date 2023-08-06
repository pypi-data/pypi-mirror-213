#!/usr/bin/env python3
"""
kr_storage: part of krapplet, a password manager
This is an intermediary layer to distinghuish the different storage providers
Make sure to import kr_storage_select prior to importing this module.
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

from .kr_storage_select import StorageSelect

st_sel=StorageSelect()
STORAGE_PROVIDER = st_sel.provider

# import storage backends
if STORAGE_PROVIDER == "gnome-keyring":
    # print("using gnome-keyring storage provider")
    from .kr_secretstorage import \
        connection_open, create_keyring, get_all_keyrings, search_keys, \
        NotAvailableException, LockedException, KeyNotFoundException, \
        PromptDismissedException
elif STORAGE_PROVIDER == "pass":
    # print("using pass storage provider")
    from .kr_pass import \
        connection_open, create_keyring, get_all_keyrings, search_keys, \
        NotAvailableException, LockedException, KeyNotFoundException, \
        PromptDismissedException, check_gpg, set_armor
    check_gpg(st_sel.gpg_id)
    set_armor(st_sel.armor)
elif STORAGE_PROVIDER == "memory":
    from .kr_memstorage import \
        connection_open, create_keyring, get_all_keyrings, search_keys, \
        NotAvailableException, LockedException, KeyNotFoundException, \
        PromptDismissedException
