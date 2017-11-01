def updateUser(self, fname, username, ouser, tag, perm):

    usercha = re.compile(ouser)
    try:
        f = open("./data/copyperm.txt", 'w')
        with open(fname) as infile:
            for line in infile:
                lparts = line.split(",")
                for i in range(len(lparts)):
                    found = usercha.search(lparts[i])
                    if found:
                        lparts[i] = perm
                        f.seek(f.tell(), len(lparts[i]))
                    f.write(",".join(lparts))
            dest = shutil.move("./data/copyperm.txt", "./data/permissionMatrix.txt")
    except (IOError, OSError) as e:
        print("could not open file %s"%(e))
        return(2)
    return(0)

if __name__ == "__main__":

    a = updateUser("./data/permissionMatrix.txt", "joe", "abbie", "1", "0")
