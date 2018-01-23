from Database import *
from datetime import datetime, timedelta
import time
from Crypt import *
from errHandle import *
import os

class Session:

    def __init__(self, socket):
        self.conn = socket
        self.db = Database()
        self.fc = FernetCrypt()
        self.e = errHandle()
        self.loggedin = False
        self.username = None
        self.LOGNp = True
        self.SMSGp = False
        self.CMSGp = False
        self.RMSGp = False
        self.UPDTp = False
        self.CACMp = True
        self.DMSGp = False

        keypair = self.loadSKey("./data/serverkeys/server.txt")
        self.ac = asymetricSuite(keypair)

    def getLoggedin(self):
        return self.loggedin

    def getUsername(self):
        return self.username

    def loadSKey(self, paths):
        if(os.path.exists(paths) and os.stat(paths).st_size != 0):
            f = open(paths)
            keypair = RSA.importKey(f.read())
            return keypair
        else:
            print("Something went terribly terribly wrong")
            return None

    def checkpubkey(self, dec, sig, username):
        path = "./data/serverkeys/" + username + ".txt"
        try:
            f = open(path)
            keypair = RSA.importKey(f.read())
            pub_key = keypair.publickey()
            ver = self.ac.valSignature(dec, sig, pub_key)
            if ver:
                return True
            else:
                return False
        except (IOError, OSError) as e:
            print("could not open file %s" % (e))
            return None
        finally:
           f.close()

    def loginAttempt(self, LOGNreq):
        ver, err = self.db.verify("./data/logindata.txt", LOGNreq.getUsername(), LOGNreq.getPass())
        if ver:
            self.username = LOGNreq.getUsername()
            self.loggedin = True
            self.setper(self.username)
            return True
        else:
            return False

    def assignUser(self, CACMreq):
        error19, username = self.db.returnUser(CACMreq.getUsername())
        ret = self.e.send_err(error19)
        if error19 ==0:
            print("got here session bitch")
            self.username = username

    def datecheck(self,reqtime):
            dt = datetime.strptime(reqtime, "%Y-%m-%d %H:%M:%S.%f")
            time = dt + timedelta(seconds=5)
            dtt = datetime.now()
            if dtt <= time:
                return True
            return False

    def setper(self,user):
        f = open("./data/permissionMatrix.txt")
        f.readline()
        for line in f:
            lparts = line[:-1].split(",")
            if lparts[0] == user:
                self.LOGNp = lparts[1]
                self.SMSGp = lparts[2]
                self.CMSGp = lparts[3]
                self.RMSGp = lparts[4]
                self.UPDTp = lparts[5]
                self.CACMp = lparts[6]
                self.DMSGp = lparts[7]
        #go into permission matrix and set booleans

    def sEncrypt(self,data):
        print("dude22")
        print(self.loggedin)
        if self.loggedin:
            print("dude")
            path = "./data/serverkeys/" + self.username + ".txt"
            pubk = self.loadSKey(path)
            sig,msg = self.ac.encryptit(data,pubk)
            return sig,msg
        elif self.username: #this is only for the CACM part so that the server can send back his public key--unclear if this safe??
            path = "./data/serverkeys/" + self.username + ".txt"
            pubk = self.loadSKey(path)
            sig,msg = self.ac.encryptit(data,pubk)
            return sig,msg
        else:
            data = self.fc.encryptit(data)
            return None,data

    def sDecrypt(self,sig,data):
        if not sig:
            data = self.fc.decryptit(data)
            return data

        elif not self.username: #specifically for the LOGN request! Since self.username is not assigned yet
            req = self.ac.decPri(data)
            lg = req.decode().split("|")
            if self.checkpubkey(req,sig,lg[1]):
                return req
            else:
                return None

        else: #for everyother request (SMSG, CMSG, ...)
            path = "./data/serverkeys/" + self.username + ".txt"
            pubk = self.loadSKey(path)
            msg,ver = self.ac.decryptit(data,sig,pubk)
            if(ver):
                return msg
            else:
                return None

    def check(self, data):
        if not self.loggedin:
            return False
        if(self.SMSGp == "1" and data.type == "SMSG" and data.username == self.username):
            return True
        if(self.CMSGp == "1" and data.type == "CMSG" and data.username == self.username):
            return True
        if(self.DMSGp == "1" and data.type == "DMSG" and data.username == self.username):
            return True
        if(self.UPDTp == "1" and data.type == "UPDT" and data.username == self.username):
            return True
        else:
            return False
