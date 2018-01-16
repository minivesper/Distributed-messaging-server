from Crypt import *
import sys

fc = FernetCrypt()

if __name__ == "__main__":
  password = fc.hashpwd(sys.argv[1], sys.argv[2])
  f = open("../data/logindata.txt", "a")
  f.write(sys.argv[1] + "," + password + "," + str(3) + "\n")
  f.close()
  f = open("../data/permissionMatrix.txt", "a")
  f.write(sys.argv[1] + ",1,1,1,1,1,1,1\n")
  f.close()

  u_keypair = GenKeys()
  u_keypairs = u_keypair.getkeypair().exportKey('PEM')
  f = open("../data/clientkeys/" + sys.argv[1] + ".txt", "w+b")
  f.write(u_keypairs)
  f.close()
  f = open("../data/serverkeys/" + sys.argv[1] + ".txt", "w+b")
  f.write(u_keypair.getpubkey().exportKey('PEM'))
  f.close()
