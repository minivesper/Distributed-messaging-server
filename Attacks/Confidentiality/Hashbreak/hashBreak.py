import getpass
import base64
from cryptography.fernet import Fernet
import sys


def crack(bytestr, k, search):
    key = bytearray(32)
    keyreal = "qgIbhaErnQ7jntxVgEVo5ReNKFZEASe-TTAh3Q8-uZU="
    # f = Fernet(base64.urlsafe_b64encode(bytes(key)))
    f = Fernet(keyreal)
    try:
        de = f.decrypt(bytestr)
        if str(de)[2:6] == search:
            return de
        else:
            pass
            print("maybe", str(de))
    except:
        pass
        # print("not ", key)
    return "not found"

def genKey(ind):
    k = bytearray(32)
    ai = 31
    while ind >= 1:
        R = int(ind % 64)
        k[ai] = R
        ind = ind - R
        ind = ind/64
        ai = ai-1
    return k

if __name__ == "__main__":
    enc = sys.argv[1]
    print(enc)
    print(crack(enc,"qgIbhaErnQ7jntxVgEVo5ReNKFZEASe-TTAh3Q8-uZU=","LOGN"))
    # bytestr = sys.argv[1]
    # key = bytearray(32)
    # for i in range(32*32):
    #     key = incbyteRFC(key, len(key)-1)
    # f = Fernet(base64.urlsafe_b64encode(bytes(key)))
    # string = "test"
    # string = string.encode('utf-8')
    # ciphertext = f.encrypt(string)
    # print(f.decrypt(ciphertext))
    # print(crack(ciphertext, "test"))
    # print(crack(bytestr,"LOGN"))
