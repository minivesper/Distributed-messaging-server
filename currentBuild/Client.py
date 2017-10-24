import socket
import sys
import getpass
import sys
# import inquirer
from Requests import *
from pprint import pprint

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

    # def createSocket(self):
    #     try:
    #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         print("Socket created successfully")
    #     except socket.error, msg:
    #         print("Error creating socket: %s" %msg)

    # def connectsock(self):
    #     try:
    #         self.getSocket().connect(self.getTCP_PORT, self.getTCP_PORT)
    #         print("Socket connection valid")
    #         return self.socket
    #     except socket.error as msg:
    #         print("Connection Error %s" %msg)
    #         sys.exit(1)

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getSocket(self):
        return self.socket

    def handleCommand(self, inp_str, username):
        req = ""
        if(inp_str == "SMSG"):
            sendTo = input("who send to: ")
            msgtxt = input("what send: ")
            req = SMSG(username, sendTo, msgtxt)
            req = req.encode()
        elif(inp_str == "CMSG"):
            req = CMSG(username)
            req = req.encode()
        elif(inp_str == "quit"):
            self.getSocket().close()
            sys.exit(1)
        if(req != ""):
            self.getSocket().sendto(req.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
            data = self.getSocket().recv(self.getBUFFER_SIZE())
            print(data.decode())
        else:
            print("%s is not a valid request type"%(inp_str))

    def recvall(self, sock):
        data=""
        data.encode('utf-8')
        while True:
            part = sock.recv(self.getBUFFER_SIZE())
            print("%s"% part)
            data += part
            if part < self.getBUFFER_SIZE():
                break
        return data

    def run(self, currentUsername):
        while True:
            inp = input("enter Command: ").upper()
            self.handleCommand(inp, currentUsername)

    def inputCredentials(self):
        user = input("Username: ")
        passwd = getpass.getpass("Password for " + user + ":")
        lreq = LOGN(user,passwd)
        lreq = lreq.encode()
        self.getSocket().sendto(lreq.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
        data = self.getSocket().recv(self.getBUFFER_SIZE())
        # s = self.getSocket()
        # data = self.recvall(s)
        print(data.decode())
        return user

    # def chooseMessage(self, user):
        # answers={}
        # while answers != 'Quit':
        #     questions = [inquirer.List('type',message="What do you want to do?",
        #             choices=['Check Messages', 'Send Message', 'Quit'],),]
        #     answers = inquirer.prompt(questions)
        #     if answers["type"] == 'Send Message':
        #         who = input("who do you send to ")
        #         what = input("what you send ")
        #         sm = SMSG(user,who,what)
        #         self.handleCommand(str(sm))
        #     if answers["type"]=='Check Messages':
        #         cm =CMSG(user)
        #         #need to create function that deals with if user is going to request all messages from all recipients at once? & how the server will handle it
        #     if answers["type"]=='Quit':
        #         #s = getSocket()
        #         s.close()
        #     #pprint(response)
            #response = get_answer(answers)
            #self.handleCommand(response)


# TCP_IP = '127.0.0.1'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024
# MESSAGE = "Hello World!"

if __name__ == "__main__":
    c = Client('127.0.0.1',5005,20)
    user = c.inputCredentials()
    # c.chooseMessage(user)
    c.run(user)
