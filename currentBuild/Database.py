import os
import sys

class Database:

    def __init__(self):
        f = open("./data/logindata.txt","r")
        for line in f:

            #inits message files
            lp = line.split(",")
            fname = "./data/" + lp[0] + ".txt"
            nf = open(fname, "a+")

        return

    def verify(self, fname, username, passwd, permission):
        found = False
        try:
            f = open(fname, 'r')
            try:
                for line in f:
                    lparts = line.split(",")
                    if(lparts[0] == username and lparts[1] == passwd and lparts[2][:-1] == permission):
                        found = True
            except EXPECTED_EXCEPTION_TYPES as e:
                print("could not write to file %s"%(e))
                return(False, 1)
            finally:
                f.close()
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(False, 2)
        return(found,0)

    def getAdmin(self, fname):
        adminuser = ""
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       adminuser = lparts[0]
                       #later on we could extend this to send a message to all admin people that one person wants approval. Right now, only send to one.
           except IOError as e:
               print("could not read from file %s"%(e))
               return adminuser
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return adminuser
        return adminuser

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


    def write(self,fname, writeText):
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

    def readappr(self,fname,username):
        messages = []
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       if(lparts[4] == username):
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

    def read(self,fname,username):
        messages = []
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       if(lparts[4] == username):
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

    def read(self,fname,username):
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
