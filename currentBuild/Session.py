from Database import *

class Session:

    def __init__(self, socket):
        self.conn = socket
        self.db = Database()
        self.loggedin = False

        self.username = None

        self.LOGNp = True
        self.SMSGp = False
        self.CMSGp = False
        self.RMSGp = False
        self.UPDTp = False
        self.CACMp = True

    def loginAttempt(self, LOGNreq):
        ver, err = self.db.verify("./data/logindata.txt", LOGNreq.getUsername(), LOGNreq.getPass(), LOGNreq.getPermis())
        if ver:
            self.username = LOGNreq.getUsername()
            self.loggedin = True
            self.setper(self.username)
            return True
        else:
            return False

    def setper(self,user):
        f = open("./data/permissionMatrix.txt")
        f.readline()
        for line in f:
            lparts = line.split(",")
            if lparts[0] == user:
                self.LOGNp = lparts[1]
                self.SMSGp = lparts[2]
                self.CMSGp = lparts[3]
                self.RMSGp = lparts[4]
                self.UPDTp = lparts[5]
                self.CACMp = lparts[6]
        #go into permission matrix and set booleans

    def check(self, data):
        print("log", self.loggedin)
        if not self.loggedin:
            return False

        if(self.SMSGp == "1" and data.type == "SMSG" and data.Username == self.username):
            return True
        if(self.CMSGp == "1" and data.type == "CMSG" and data.Username == self.username):
            return True
        print(self.UPDTp)
        print(data.type)
        print(data.Username)
        if(self.UPDTp == "1" and data.type == "UPDT" and data.Username == self.username):
            return True
        else:
            return False
