#!/usr/bin/env python

"""
kr_crypt: functions for encrypting and decryting strings
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import sys
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def passwd_in_bytes(passphrase):
    if passphrase:
        if isinstance(passphrase, bytes):
            return passphrase
        if isinstance(passphrase, str):
            return str.encode(passphrase)
        else:
            print("unexpected type for passphrase", type(passphrase))
            return b''
    return None

def fernet(passphrase):
    """ Returns a Fernet object, based on a passwd (as a string) """
    salt = "[zG?+=-$xD\S{*A#1-.l^&]z@BL;Z:i%".encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(passwd_in_bytes(passphrase)))
    return Fernet(key)

def sym_encrypt(unenc_str, passphrase):
    """ returns a password protected encrypted string """
    fern = fernet(passphrase)
    if isinstance(unenc_str, bytes):
        unenc_bytes = unenc_str
    elif isinstance(unenc_str, str):
        unenc_bytes = str.encode(unenc_str)
    else:
        print("sym_encrpt: cannot convert", type(unenc_str), "to bytes")
    return fern.encrypt(unenc_bytes)

def sym_decrypt( enc_str, passphrase):
    """ returns a decrypted string """
    fern = fernet(passphrase)
    #try:
    if True:
        if isinstance(enc_str, str):
            enc_str = enc_str.encode()
        dec_str = fern.decrypt(enc_str)
        return dec_str
    """
    except InvalidToken:
        #print( "decrypt failed: invalid token", file=sys.stderr)
        pass
    except:
        print("Unexpected error:", sys.exc_info()[0], file=sys.stderr)"""
    return None



from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric.utils import \
    decode_dss_signature, encode_dss_signature
from cryptography.exceptions import InvalidSignature

def write_serkey(serkey, fname):
    "Writes a serialized key to a file with name fname"
    with fopen(fname, "wb") as fh:
        fh.write(serkey)

def read_serkey(fname):
    "Reads serialized key from a file"
    serkey = b''
    try: 
        with fopen(fname, "rb") as fh:
            fh.read(serkey)
        return serkey
    except Exception as exc:
        print("Can't read seralized key from file", fname, ":", exc)
    return None

def asym_serialize_privkey(privkey, passphrase, fname=None):
    """Serializes a key for storage.
    Will write the serialized key to file fname if fname is not None"""
    if passphrase:
        algo = serialization.BestAvailableEncryption(
            passwd_in_bytes(passphrase))
    else:
        algo = serialization.NoEncryption()
    serialized_privkey = privkey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format = serialization.PrivateFormat.PKCS8,
        encryption_algorithm = algo)
    if fname:
        write_serkey(serialized_privkey)
    return serialized_privkey

def asym_deserialize_privkey(ser_privkey, passphrase, fname=None):
    """Deserializes private key in PEM format with optional password.
    Will read the serizalized key from file if fname is not None"""
    if fname:
        ser_privkey = read_serkey(fname)
    if ser_privkey:
        try:
            privkey = serialization.load_pem_private_key(
                ser_privkey, password=passwd_in_bytes(passphrase))
            return privkey
        except ValueError:              # bad passwd
            pass
        except Exception as exc:
            print("Failed to deserialize private key:", exc)
    return None

def asym_serialize_pubkey(pubkey, fname = None):
    "Serialized a pubkey to PEM format"
    ser_pubkey = pubkey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    if fname:
        write_serkey(ser_pubkey, fname)
    return ser_pubkey

def asym_deserialize_pubkey(ser_pubkey, fname = None):
    "Deserializes a public key in PEM format"
    if fname:
        ser_pubkey = read_serkey(fname)
    if ser_pubkey:
        pubkey = serialization.load_pem_public_key(ser_pubkey)
    return pubkey

def asym_genkey():
    " Generates a private key for asymetric encryption "
    return ec.generate_private_key(ec.SECP384R1())

def asym_pubkey(privkey):
    " Returns the public counterpart of a private key "
    return privkey.public_key()

def asym_encrypt(key, msg):
    "Encrypts a message with a private or public key"
    pad = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None)
    return key.encrypt(msg, pad)

def asym_decrypt(key, enc_msg):
    "Decrypts a message a public or private key"
    pad = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None)
    try:
        msg = key.decrypt(enc_msg, pad)
    except Exception as exc:
        print("Asym_decrypt failed: ", exc)
        msg = None
    return msg

def asym_sharedkey(privkey, peer_pubkey):
    " Returns the shared key for an exchange "
    return privkey.exchange(ec.ECDH(), peer_pubkey)

def asym_derivedkey(key, salt, handshake_data):
    "Creates a derrived key using the handshake data"
    #derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt,
                       info=b'handshake data').derive(key)
    return derived_key

def asym_derived_sharedkey(privkey, peer_pubkey, salt, handshake_data):
    "Combines the fuctions of asym_sharedkey and asym_derivedkey"
    sharedkey = asym_sharedkey(privkey, peer_pubkey)
    return asym_derivedkey(sharedkey, salt, handshake_data)

def asym_signature(unenc_str, privkey):
    " Signs a message with a private key "
    signature = privkey.sign(unenc_str, ec.ECDSA(hashes.SHA256()))
    dec_dss_sig = decode_dss_signature(signature)
    return dec_dss_sig

def asym_signature_verify(unenc_str, sig, pubkey):
    " Verifies the signature of a message: True when passes "
    enc_dss_sig = encode_dss_signature(sig[0],sig[1])
    try:
        pubkey.verify(enc_dss_sig, unenc_str, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
    except Exception as exc:
        print("Unexpected error verifying signature:", str(exc))
    return False
