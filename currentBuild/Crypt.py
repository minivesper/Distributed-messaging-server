import socket
import getpass
import base64
from cryptography.fernet import Fernet
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
from pprint import pprint
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


#generate public/private key pairs
#note: keypair is the private key
class GenKeys:
    def __init__(self):
        self.keypair = self.genpair()

    def genpair(self):
        random_gen = Random.new().read
        keypair = RSA.generate(1024, random_gen)
        return keypair

class asymetricSuite:
    def __init__(self, keypair, message):
        self.keypair = keypair
        self.pubkey = self.keypair.publickey()
        self.message = message

    #use these two functions to encrypt and decrypt the message being sent to one another
    def encrypt(self, pubkey_o):
        # Encrypt messages using the other party's public key...
        enc_data = self.pubkey.encrypt(self.verobj, 32)
        return enc_data

    def decrypt(self, message):
        # Decrypt messages using own private keys...
        decry_msg = self.keypair.decrypt(message)
        return decry_message

#the point of the signature is to verify that the message has not been modified once sent.
    def genSig(self):
        # Generate digital signatures using private keys...
        hash_request = MD5.new(self.message).digest()
        signature = self.keypair.sign(hash_request, '')
        return signature #this signature needs to be added to any request / message being sent

    def valSignature(self, decry_msg, sender_sig, sender_pubkey):
        # Signature validation...
        ret = False
        hash_decryp_msg = MD5.new(decrypted_msg).digest()
        if sender_pubkey.verify(hash_decry_msg, sender_sig):
            ret = True
            return ret
        else:
            ret = False
            return ret

    def run(self):
        self.exchangeKeys()
        #reciev their pulbic before this
        sig = self.getSignature()
        enc = self.encPub(rec_pub_key)
        #send sig and enc to the reciever somewhere
        #recieve new msg with a signature and publickey
        dec = self.decPri(sender_msg)
        if(self.valSignature(dec, sender_sig, sender_pubkey)):
            print ("Signature valid")
            print ("The message is:")
            print (dec)
            return
        else:
            print ("Signature missmatch")
            return
        return

class Crypt:

    def __init__(self, keypair):
        #self.my_msg = my_msg.encode('utf-8')
        self.my_keypair = keypair
        self.my_pubkey = self.my_keypair.publickey()
        return

    def exchangeKeys(self):
        #In practice public keys are sent accross the wire
        return

    def getSignature(self):
        # Generate digital signatures using private keys...
        hash_of_my_msg = MD5.new(self.my_msg).digest()
        my_signature = self.my_keypair.sign(hash_of_my_msg, '')
        return my_signature

    def encPub(self, rec_key):
        # Encrypt messages using the other party's public key...
        encrypted_for_rec = self.rec_key.encrypt(self.my_msg, 32)
        return encrypted_for_rec

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

class OldCrypt:
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
