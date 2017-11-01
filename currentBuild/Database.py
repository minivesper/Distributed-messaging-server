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

    def verify(self, fname, username, passwd):
        found = False
        try:
            f = open(fname, 'r')
            try:
                for line in f:
                    lparts = line.split(",")
                    if(lparts[0] == username and lparts[1][:-1] == passwd):
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

    def write(self, recipient, writeText):
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
