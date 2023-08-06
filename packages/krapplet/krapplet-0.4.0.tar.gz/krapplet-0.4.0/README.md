# Krapplet

Krapplet is a graphical password manager for Linux.
Its name derives from 'keyring applet'.


# Feature overview

- Graphical password manager.
- Passwords are considered secrets, contained in keys, organized per keyring.
- Keys also can also contain associated information like username, email
  addresses, and/or a website URL.
- Contains a password generator.


# Technical overview

- Written in Python3, using the GTK3 toolkit.
- Keys are stored using:
  [gnome-keyring](https://wiki.gnome.org/Projects/GnomeKeyring), or
  [GPG](https://gnupg.org/)-encrypted in a format compatibe with the
  [pass](https://www.passwordstore.org) command line password manager.


# Documentation

The documentation of krapplet Can be found on
[readthedocs.io](https://krapplet.readthedocs.io/en/latest/index.html).


# License

Krapplet is licensed under a
[BSD-3 license](https://gitlab.com/hfernh/krapplet/-/blob/master/LICENSE).


# Feedback

If something is not working properly then please log an
[issue](https://gitlab.com/hfernh/krapplet/-/issues) against the project.
