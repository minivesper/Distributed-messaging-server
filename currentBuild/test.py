from Crypt import *

def readk(fname):
    user = "server"
    fname = "./data/" + fname + ".txt"
    try:
       f = open(fname)
       keypair = RSA.importKey(f.read())
       return keypair
    except (IOError, OSError) as e:
       print("could not open file %s"%(e))
       return None
    finally:
        f.close()

u_keypair = readk("clientkeys/ele")
u_pubkey = u_keypair.publickey()
u_assym = asymetricSuite(u_keypair)

s_keypair = readk("serverkeys/server")
s_pubkey = s_keypair.publickey()
s_assym = asymetricSuite(s_keypair)

msg = "hello"
sig, enc = u_assym.encryptit(msg, s_pubkey)
val, dec = s_assym.decryptit(enc, sig, u_pubkey)
if dec:
    print(val)
else:
    print("time")
