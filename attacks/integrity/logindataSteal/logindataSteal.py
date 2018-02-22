import socket
import sys
import getpass
from Requests import *

class Client:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully")
            self.socket = s
        except socket.error as msg:
            print("Error creating socket: %s" %msg)
            sys.exit(1)
        try:
            s.connect((self.TCP_IP, self.TCP_PORT))
            print("Socket connection valid")
        except socket.error as msg:
            print("Connection Error %s" %msg)
            sys.exit(1)

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getSocket(self):
        return self.socket

    def inputCredentials(self):
        user = input("Username: ")
        passwd = getpass.getpass("Password for " + user + ":")
        lreq = LOGN(user,passwd)
        lreq = lreq.encode()
        self.getSocket().sendto(lreq.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
        data = self.getSocket().recv(self.getBUFFER_SIZE())
        if(data.decode() == "not verified"):
            print(data.decode())
            user = None
            return user
        else:
            # s = self.getSocket()
            # data = self.recvall(s)
            print(data.decode())
            return user

    def run(self, currentUsername):
            req = "CMSG||||||||"
            print(req)
            self.getSocket().sendto(req.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
            data = self.getSocket().recv(self.getBUFFER_SIZE())
            print(data)

if __name__ == "__main__":
    c = Client('127.0.0.1',5005,1024)
    while True:
        user = c.inputCredentials()
        if user:
            c.run(user)
