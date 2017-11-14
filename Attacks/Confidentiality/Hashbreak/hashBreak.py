import getpass
import base64
from cryptography.fernet import Fernet
from pprint import pprint
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import os

def crack(bytestr, search):
    key = bytearray(32)
    keyreal = "qgIbhaErnQ7jntxVgEVo5ReNKFZEASe-TTAh3Q8-uZU="
    while key[0] < 32:
        f = Fernet(base64.urlsafe_b64encode(bytes(key)))
        # f = Fernet(keyreal)
        try:
            de = f.decrypt(bytestr)
            if str(de)[2:6] == search:
                print(key)
                return de
            else:
                pass
                # print("maybe", str(de))
        except:
            pass
            # print("not ", key)
        key = incbyteRFC(key, len(key)-1)
    return "not found"

def incbyteRFC(key, ind):
    newnum = key[ind] + 1
    if(newnum > 32):
        key[ind] = 0
        key = incbyteRFC(key,ind-1)
    else:
        key[ind] += 1
    return key

if __name__ == "__main__":
    bytestr = sys.argv[1]
    key = bytearray(32)
    for i in range(32*32):
        key = incbyteRFC(key, len(key)-1)
    f = Fernet(base64.urlsafe_b64encode(bytes(key)))
    string = "test"
    string = string.encode('utf-8')
    ciphertext = f.encrypt(string)
    print(f.decrypt(ciphertext))
    print(crack(ciphertext, "test"))
    # print(crack(bytestr,"LOGN"))
