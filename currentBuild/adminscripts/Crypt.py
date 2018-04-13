import socket
import getpass
import base64
from cryptography.fernet import Fernet
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
from pprint import pprint
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


#generate public/private key pairs
#note: keypair is the private key

key = "qgIbhaErnQ7jntxVgEVo5ReNKFZEASe-TTAh3Q8-uZU="

cipher_key = Fernet(key)

class GenKeys:#Randomly Generateing Asymetric Keys

    def __init__(self):
        self.my_keypair = self.keygen()
        self.my_pubkey = self.my_keypair.publickey()


    def keygen(self):
        random_gen = Random.new().read
        this_keypair = RSA.generate(1024, random_gen)
        return this_keypair

    def getkeypair(self):
        return self.my_keypair

    def getpubkey(self):
        return self.my_pubkey


class asymetricSuite:

    def __init__(self, keypair):
        self.my_keypair = keypair
        self.my_pubkey = self.my_keypair.publickey()

    def getSignature(self, msg):
        hash_of_my_msg = MD5.new(msg).digest()
        my_signature = self.my_keypair.sign(hash_of_my_msg, '')
        return my_signature

    def getpubkey(self):
        return self.my_pubkey

    def encPub(self, msg, thier_pubkey):
        encrypted_for_them = thier_pubkey.encrypt(msg, 32)
        return encrypted_for_them

    def decPri(self, encrypted_msg):
        # Decrypt messages using own private keys...
        decrypted_msg = self.my_keypair.decrypt(encrypted_msg)
        return decrypted_msg

    def valSignature(self, decrypted_msg, sender_sig, sender_pubkey):
        # Signature validation and console output...
        ret = False
        hash_msg_decrypted = MD5.new(decrypted_msg).digest()
        if sender_pubkey.verify(hash_msg_decrypted, sender_sig):
            ret = True
            return ret
        else:
            ret = False
            return ret

    def encryptit(self, msg, thier_pubkey):
        sig = self.getSignature(msg.encode('utf-8'))
        enc = self.encPub(msg.encode('utf-8'), thier_pubkey)
        return sig,enc

    def decryptit(self, enc, sender_sig, sender_pubkey):
        dec = self.decPri(enc)
        val = self.valSignature(dec, sender_sig, sender_pubkey)
        return dec,val

class FernetCrypt:#Fernet Key Encryption As Well As Hashing
    def __init__(self):
        return

    def hashpwd(self, salt, password):
        kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32, salt = salt, iterations = 100000, backend = default_backend())
        hashp = base64.urlsafe_b64encode(kdf.derive(password))
        return hashp

    def encryptit(self,string):
        string = string.encode('utf-8')
        ciphertext = cipher_key.encrypt(string)
        return ciphertext

    def decryptit(self,string):
        plaintext = cipher_key.decrypt(string)
        return plaintext
