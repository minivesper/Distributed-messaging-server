import os
import sys
import fileinput
import re
import shutil
import glob
from Crypt import *


class Database:

    def __init__(self):
        self.counter = 0
        self.counterread = 0
        f = open("./data/logindata.txt","r")
        for line in f:

            #inits message files
            lp = line.split(",")
            fname = "./data/" + lp[0] + ".txt"
            nf = open(fname, "a+")
        return

    def getCounter(self):
        return self.counter

    def verify(self, fname, username, passwd):
        found = False
        try:
            f = open(fname, 'r')
            try:
                for line in f:
                    lparts = line.split(",")
                    if(lparts[0] == username and lparts[1] == passwd):
                        found = True
            except EXPECTED_EXCEPTION_TYPES as e:
                print("could not read from file %s"%(e))
                return(False, 1)
            finally:
                f.close()
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(False, 2)
        return(found,0)

    def getAdmin(self, fname):
        adminusers = []
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       if lparts[2][:-1] == "3":
                           adminusers.append(lparts[0])
                       #later on we could extend this to send a message to all admin people that one person wants approval. Right now, only send to one.
           except IOError as e:
               print("could not read from file %s"%(e))
               return 1
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return 2
        return adminusers

    def checkDuplicate(self, fname, username):
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       if(lparts[0] == username):
                           print("username already exists")
                           return 3
           except IOError as e:
               print("could not read from file %s"%(e))
               return 1
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return 2
        return 0

    def returnUser(self, username):
        try:
           f = open("./data/logindata.txt", 'r')
           f.close()
           try:
               with open("./data/logindata.txt") as infile:
                   for line in infile:
                       lparts = line.split(",")
                       if(lparts[0] == username):
                           return (0, username)
           except IOError as e:
               print("could not read from file %s"%(e))
               return (1, None)
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return (2, None)
        return (3, None)


    def checkexistance(self, fname, ouser):
        with open(fname) as infile:
            for line in infile:
                lparts = line.split(",")
                for i in range(len(lparts)):
                    if lparts[i] == ouser:
                        return True
            print("username does not exist")
            return False


    def updateUser(self, fname, username, ouser, tag, perm):
        usercha = re.compile(ouser)
        try:
            f = open("./data/copyperm.txt", 'w')
            with open(fname) as infile:
                for line in infile:
                    lparts = line.split(",")
                    for i in range(len(lparts)):
                        found = usercha.match(lparts[i])
                        if found:
                            lparts[int(tag)] = perm
                    f.write(",".join(lparts))
                dest = shutil.move("./data/copyperm.txt", "./data/permissionMatrix.txt")
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(2)
        return(0)

    def writek(self,recipient, writeText):
        try:
            fname = "./data/serverkeys/" + recipient + ".txt"
            f = open(fname, 'w+')
            if os.path.getsize(fname) + sys.getsizeof(writeText) < 100000:
                try:
                    f.write(writeText)
                finally:
                    f.close()
            else:
                print("inbox is full error")
                return(3)
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(2)
        return(0)

    def write(self,recipient, writeText):
        try:
            fname = "./data/" + recipient + ".txt"
            f = open(fname, 'a')
            if os.path.getsize(fname) + sys.getsizeof(writeText) < 100000:
                try:
                    f.write(writeText + "\n")
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

    def writeMalicious(self, writeText):
        try:
            fname= "./datamalicious/userinfo" + str(self.counter) + ".dat"
            f = open(fname,'w+b')
            if os.path.getsize(fname) + sys.getsizeof(writeText) < 100000:
                try:
                    f.write(writeText)
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
        self.counter = self.counter + 1
        return(0)

    def readMalicious(self, fname):
        commands = bytearray()
        try:
            with open(fname, "r+b") as infile:
                commands = infile.read()
        except IOError as e:
            print("could not read from file %s"%(e))
            return None, 1
        return commands

    def delete(self, recipient, deleteText):
        try:
            fname = "./data/" + recipient + ".txt"
            f = open(fname, 'r+')
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if line[:-1] != deleteText:
                    f.write(line)
            f.truncate()
            f.close()
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(2)
        return(0)

    def read(self,username):
        messages = []
        fname = "./data/" + username + ".txt"
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       messages.append(line[:-1])
           except IOError as e:
               print("could not read from file %s"%(e))
               return None, 1
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return None, 2
        return messages, 0

    def deleteUser(self, fname, fname2, username):
            fnamemessage = "./data/" + username + ".txt"
            os.remove(fnamemessage)
            fnameserver = "./data/serverkeys/" + username + ".txt"
            os.remove(fnameserver)
            fnameclient = "./data/clientkeys/" + username + ".txt"
            os.remove(fnameclient)
            try:
                f = open("./data/copyperm.txt", 'w')
                with open(fname) as infile:
                    for line in infile:
                        lparts = line.split(",")
                        if username not in lparts:
                            f.write(line)
                    dest = shutil.move("./data/copyperm.txt", "./data/permissionMatrix.txt")
            except (IOError, OSError) as e:
                print("could not open file %s"%(e))

            try:
                f = open("./data/copylogin.txt", 'w')
                with open(fname2) as infile:
                    for line in infile:
                        lparts = line.split(",")
                        if username not in lparts:
                            f.write(line)
                    dest = shutil.move("./data/copylogin.txt", "./data/logindata.txt")
            except (IOError, OSError) as e:
                print("could not open file %s"%(e))
                return(2)
            return(0)

    def readk(self):
        user = "server"
        fname = "./data/serverkeys/server.txt"
        try:
           f = open(fname)
           keypair = RSA.importKey(f.read())
           s_pub = keypair.publickey().exportKey('PEM').decode()
           return s_pub, 0
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return None
        finally:
            f.close()
