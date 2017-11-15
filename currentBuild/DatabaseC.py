import os
import sys
import fileinput
import re
import shutil
from Crypt import *
import glob


class DatabaseC:

    def __init__(self):
        return

    def writesk(self,keypair):
        try:
            fname = "./data/clientkeys/server.txt"
            f = open(fname, 'w')
            if os.path.getsize(fname) + sys.getsizeof(keypair) < 100000:
                try:
                    f.write(keypair)
                finally:
                    f.close()
            else:
                print("inbox is full error")
                return(3)
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(2)
        return(0)

    def writek(self,username, keypair):
        #keypair_e = keypair.exportKey()
        try:
            fname = "./data/clientkeys/" + username + ".txt"
            f = open(fname, 'w+b')
            if os.path.getsize(fname) + sys.getsizeof(keypair) < 100000:
                try:
                    f.write(keypair)
                except EXPECTED_EXCEPTION_TYPES as e:
                    print("could not write to file %s"%(e))
                    return(1)
                finally:
                    f.close()
            else:
                print("inbox is full error")
                return(3)
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(2)
        return(0)

    def readk(self,username): #reads through all the possible client key files to ensure that username typed in is valid
        path = "./data/clientkeys/*.txt"
        files=glob.glob(path)
        for file in files:
            if file == "./data/clientkeys/" + username + ".txt":
                fname = file
                try:
                    f = open(fmame)
                    keypair = RSA.importKey(f.read())
                    return keypair
                except (IOError, OSError) as e:
                    print("could not open file %s"%(e))
                    return None
                finally:
                   f.close()
            else:
                return(2)


       #if(os.stat("data/clientkeys/" + user + ".txt").st_size != 0):
