import os
import sys
import fileinput
import re
import shutil

class DatabaseC:

    def __init__(self):
        return

    def writek(self,recipient, writeText):
        try:
            fname = "./data/" + recipient + ".txt"
            f = open(fname, 'a+b')
            if os.path.getsize(fname) + sys.getsizeof(writeText) < 100000:
                try:
                    print("writeText", writeText)
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
        return(0)

    def readk(self,username):
        fname = "./data/" + username + ".txt"
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   f = infile.readline()
                   return f
           except IOError as e:
               print("could not read from file %s"%(e))
               return None
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return None
