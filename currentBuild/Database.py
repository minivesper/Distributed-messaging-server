class Database:

    def __init__(self):
         return

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
                   if(lparts[4] == username):
                       messages.append(line)
           except EXPECTED_EXCEPTION_TYPES as e:
               print("could not read from file %s"%(e))
               return None, 1
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return None, 2
        return messages,0
