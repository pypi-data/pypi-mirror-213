#!/usr/bin/env python3

"""
kr_test: the krapplet test suite
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.

Usage: python -m unittest krapplet.kr_test

"""



import unittest
import secrets

#import krapplet.kr_pass
from .kr_storage_select import StorageSelect
st_sel=StorageSelect("pass")

from . import kr_json
from . import kr_pass
from . import kr_crypt
from . import kr_memstorage
from .krapplet import gen_pw


#class TestStringMethods(unittest.TestCase):
class test_kr_passs(unittest.TestCase):
    """ kr_pass tests: for the pass compatible storage provider """

    def setUp(self):
        """ test the creation/deletion of keyrings and keys """
        self.test_passwd = "__test_keyring_pw"
        self.keyring_name = "__test_keyring"
        self.keyname = "__test_key"
        self.attrs = { "URL": "http://www.xyz.com" }
        self.secret = bytes("secret", 'utf-8')
        self.conn = kr_pass.connection_open()
        self.conn.set_passphrase(self.test_passwd)
        self.keyring = kr_pass.create_keyring(self.conn,
                                                       self.keyring_name)
        if self.keyring.is_locked():
            self.keyring.unlock()
        self.key = self.keyring.create_key(self.keyname,
                                           self.attrs,
                                           self.secret)

    def tearDown(self):
        """ deletes the test key and test keyring """
        self.key.delete()
        self.keyring.delete()
        self.conn.close()

    def test_pass_key(self):
        """ Finds the key and sees if it has the right value """
        conn = kr_pass.connection_open()
        conn.set_passphrase(self.test_passwd)
        test_success = False
        for keyring in kr_pass.get_all_keyrings(conn):
            if keyring.get_label() == self.keyring_name:
                for key in keyring.get_all_keys():
                    if key.get_label() == self.keyname:
                        self.assertEqual(key.get_attributes(), self.attrs)
                        self.assertEqual(key.get_secret(), self.secret)
                        test_success = True
        conn.close()
        self.assertTrue(test_success)

    def test_update_key(self):
        """ tests updating a key's attrs, and secret """
        conn = kr_pass.connection_open()
        conn.set_passphrase(self.test_passwd)
        attrs = self.attrs
        for key in kr_pass.search_keys(conn, attrs):
            self.assertEqual(key.get_attributes(), self.attrs)
            new_attrs = { "Num": "001" }
            key.set_attributes(attrs)
            self.assertEqual(key.get_attributes(), attrs)
            new_label = "NewLabel"
            key.set_label(new_label)
            self.assertEqual(key.get_label(), new_label)
            new_secret = bytes("NewSecret", 'utf-8')
            key.set_secret(new_secret)
            self.assertEqual(key.get_secret(), new_secret)
        conn.close()


"""
class test_kr_memstorage(unittest.TestCase):
    def setUp(self):
        self.con = kr_memstorage.connection_open()

    def test_1(self):
        self.assertTrue(self.con.is_locked())
        krlabel = "kr_label"
        k_label = "k_label"
        k_attr = {}
        k_attr["type"] = "loper"
        k_attr["color"] = "grey"
        k_secret = "5ecr3T"
        kr = kr_memstorage.create_keyring(self.con, krlabel)
        self.assertEqual(kr.get_label(), krlabel)
        k =  kr.create_key(k_label, k_attr, k_secret)
        self.assertEqual(k.get_label(), k_label)
        self.assertEqual(k.get_attributes(), k_attr)
        self.assertEqual(k.get_secret(), k_secret)
        k_newlabel = "k_newlabel"
        k_newattr = {}
        k_newattr["newtype"] = "newloper"
        k_newattr["newtype"] = "newloper"
        k_newsecret = "new5ecr3T"
        k.set_label(k_newlabel)
        self.assertEqual(k.get_label(), k_newlabel)
        k.set_attributes(k_newattr)
        self.assertEqual(k.get_attributes(), k_newattr)
        k.set_secret(k_newsecret)
        self.assertEqual(k.get_secret(), k_newsecret)
        # something with created and modified times..? 
        krnewlabel = "kr2_label"
        kr2 = kr_memstorage.create_keyring(self.con, krnewlabel)
        k.move(krnewlabel)
        print( "key delete" )
        k.delete()
        print( "keyring delete" )
        kr.delete()
        print( "keyring2 delete" )
        kr2.delete()

"""

class test_kr_json(unittest.TestCase):

    def test_json(self):
        """ Test of the json module """
        kr_dic = kr_json.dic_all_keyring()
        kr_str = kr_json.dic2str(kr_dic)
        kr_dic2 = kr_json.str2dic(kr_str)
        self.assertEqual(kr_dic, kr_dic2)
        kr_str2 = kr_json.dic2str(kr_dic2)
        self.assertEqual(kr_str, kr_str2)



class test_kr_crypt(unittest.TestCase):
    "Test symetric  encryption"
    def setUp(self):
        self.secret_msg = "!terces siht wonk ot si eno oN"
        self.passphrase = "S3creT---!"

    def test_crypt(self):
        " test encryption "
        encrypted_secret_msg = kr_crypt.sym_encrypt(
            self.secret_msg, self.passphrase)
        decrypted_secret_msg = kr_crypt.sym_decrypt(
            encrypted_secret_msg, self.passphrase).decode("utf-8")
        self.assertEqual(self.secret_msg, decrypted_secret_msg)
        """
        wrong_passphrase = "S3creT---?"
        failed_decrypted_secret_msg = kr_crypt.sym_decrypt(
            encrypted_secret_msg, wrong_passphrase)
        self.assertIsNone(failed_decrypted_secret_msg)
        """


class test_kr_asymcrypt(unittest.TestCase):
    "Test for asymetric encryption"
    def setUp(self):
        self.secret_msg = "!terces siht wonk ot si eno oN"
        self.passphrase = b"S3creT---!"
        self.alice_privkey = kr_crypt.asym_genkey()
        self.alice_pubkey = kr_crypt.asym_pubkey(self.alice_privkey)
        self.bob_privkey = kr_crypt.asym_genkey()
        self.bob_pubkey = kr_crypt.asym_pubkey(self.bob_privkey)
        self.salt = secrets.token_bytes()

    def test_asym_shared_keys(self):
        "Test diffie-hellman key exchange"
        alice_sh_key = kr_crypt.asym_derived_sharedkey(
            self.alice_privkey, self.bob_pubkey, self.salt, "test")
        bob_sh_key = kr_crypt.asym_derived_sharedkey(
            self.bob_privkey, self.alice_pubkey, self.salt, "test")

        # Alice and Bob's shared keys should be the same:
        self.assertEqual(alice_sh_key, bob_sh_key)

        # wrong shared key uses the wrong salt:
        wrong_sh_key = kr_crypt.asym_derived_sharedkey(
            self.bob_privkey, self.alice_pubkey, self.salt + b'ss', "tEst")
        self.assertNotEqual(alice_sh_key, wrong_sh_key)

    def test_privkey_serialization_no_passwd(self):
        "Test for serializing a private key with no passwd"
        ser_privkey = kr_crypt.asym_serialize_privkey(
            self.alice_privkey, None)
        privkey = kr_crypt.asym_deserialize_privkey(ser_privkey, None)
        self.assertIsNotNone(privkey)
        if privkey:
            ser2_privkey = kr_crypt.asym_serialize_privkey( privkey, None)
            self.assertEqual(ser_privkey, ser2_privkey)

    def test_privkey_serialization_with_passwd(self):
        "Test for serializing a private key with a passwd"
        ser_privkey = kr_crypt.asym_serialize_privkey(
            self.alice_privkey, self.passphrase)
        privkey = kr_crypt.asym_deserialize_privkey(ser_privkey,
                                                    self.passphrase)
        self.assertIsNotNone(privkey)
        """ 
        if privkey:
            ser2_privkey = kr_crypt.asym_serialize_privkey(privkey,
                                                           self.passphrase)
            self.assertEqual(ser_privkey, ser2_privkey) """


    def test_privkey_serialization_with_passwd_fail(self):
        "Test for serializing a private key with a passwd"
        ser_privkey = kr_crypt.asym_serialize_privkey(
            self.alice_privkey, self.passphrase)
        privkey = kr_crypt.asym_deserialize_privkey(ser_privkey, "a_guess")
        self.assertIsNone(privkey)

    def test_asym_signing(self):
        "Test signing verification"
        msg2sign = b'This is a very important message'
        alice_sign = kr_crypt.asym_signature(
            msg2sign, self.alice_privkey)
        self.assertTrue(kr_crypt.asym_signature_verify(
            msg2sign, alice_sign, self.alice_pubkey))

    def test_asym_signing_fail(self):
        "Test signing verification"
        msg2sign = b'This is a very important message'
        alice_sign = kr_crypt.asym_signature(
            msg2sign, self.alice_privkey)
        bad_sign = (10,10)
        self.assertFalse(kr_crypt.asym_signature_verify(
            msg2sign, bad_sign, self.alice_pubkey))





if __name__ == '__main__':
    unittest.main()


