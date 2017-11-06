import socket
import getpass
import base64
from cryptography.fernet import Fernet
#from Crypto.Cipher import AES
from pprint import pprint

key = "qgIbhaErnQ7jntxVgEVo5ReNKFZEASe-TTAh3Q8-uZU="
#key = Fernet.generate_key()
#print(key)
cipher_key = Fernet(key)
#salt = '!%F=-?Pst970'
#key32 = "{: <32}".format(salt).encode("utf-8")
#cipherobj = AES.new(key32, AES.MODE_ECB)

class Crypt:
    def __init__(self):
        return

    def encryptit(self,string):
        string = string.encode('utf-8')
        ciphertext = cipher_key.encrypt(string)
        return ciphertext

    def decryptit(self,string):
        plaintext = cipher_key.decrypt(string)
        return plaintext

if __name__ == '__main__':
    #just testing it out
    c = Crypt()
    uhm = "were you expecting to find a needle?"
    uhm = uhm.encode('utf-8')
    haystack = c.encryptit(uhm)
    print(haystack)
    translate = c.decryptit(haystack)
    print(translate)
