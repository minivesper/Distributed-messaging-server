class Database:

    def __init__(self):
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

    def write(self,fname, writeText):
        try:
            f = open(fname, 'a')
            try:
                f.write(writeText + "\n")
            except EXPECTED_EXCEPTION_TYPES as e:
                print("could not write to file %s"%(e))
                return(1)
            finally:
                f.close()
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return(2)
        return(0)

    def read(self,fname,username):
        messages = []
        try:
           f = open(fname, 'r')
           try:
               for line in f:
                   lparts = line.split(",")
                   if(lparts[1] == username):
                       messages.append(line[:-1])
           except EXPECTED_EXCEPTION_TYPES as e:
               print("could not read from file %s"%(e))
               return None, 1
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return None, 2
        return messages, 0
