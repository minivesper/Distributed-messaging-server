import socket
import sys
import re
import getpass
# import inquirer
from Requests import *
from pprint import pprint

ADDRESS_OF_SERVER = '127.0.0.1'

class Client:
    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.cachedMessages = None

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

    def handleReturn(self, returnreq):
        if(returnreq[0:4] == "RMSG"):
            rm = RMSG(None,None)
            rm.decode(returnreq)
            self.cachedMessages = rm.messages
            print(rm)
        else:
            print(returnreq)

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
        elif(inp_str == "DMSG"):
            message_num = input("delete which message number?: ")
            message_num = int(message_num)
            req = DMSG(self.cachedMessages[message_num-1][0],self.cachedMessages[message_num-1][1],self.cachedMessages[message_num-1][2])
            req = req.encode()
        elif(inp_str == "UPDT"):
            userupdt = input("which user do you want to update? ")
            #Todo need to check if user exists
            permname = input("what permission do you want to change? ")
            while (permname not in("LOGN", "SMSG", "RMSG", "CMSG", "UPDT", "CACM","DMSG")):
                print("Need to input LOGN, RMSG, CMSG, UPDT, CACM, or DMSG")
                permname = input("what permission do you want to change? ")
            permbool = input("Input change: ")
            while (permbool not in("0","1")):
                print("Need to input 0 or 1")
                permbool = input("Input change: ")
            req = UPDT(username, userupdt, permname, permbool)
            req = req.encode(permname)
        elif(inp_str == "QUIT"):
            self.getSocket().close()
            sys.exit(1)
        if(req != ""):
            self.getSocket().sendto(req.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
            data = self.getSocket().recv(self.getBUFFER_SIZE())
            self.handleReturn(data.decode())
        else:
            print("%s is not a valid request type"%(inp_str))

    # def recvall(self, sock):
    #     data=""
    #     data.encode('utf-8')
    #     while True:
    #         part = sock.recv(self.getBUFFER_SIZE())
    #         print("%s"% part)
    #         data += part
    #         if part < self.getBUFFER_SIZE():
    #             break
    #     return data

    def run(self, currentUsername):
        while True:
            inp = input("enter Command: ").upper()
            self.handleCommand(inp, currentUsername)

    def createUser(self):
        user = None
        inp = input("Welcome: enter command ").upper()
        if inp == "LOGN":
            user, pwd, permission = self.inputCredentials()
            return user
        elif inp == "CACM":
            user, pwd, permission = self.getCredentials()
            user = self.checkCredentials(user, pwd, permission)
            return user
        else:
            print("%s is not a valid request type"%(inp))
            return user

    def getCredentials(self):
        print("please enter a username with only letters and numbers")
        user = input("Username: ")
        while (re.search("[a-z|0-9]", user)) is None:
            print("please enter a username with only letters and numbers")
            user = input("Username: ")
            while (len(user))>15:
                print("please enter a username with 15 characters")
                user = input("Username: ")
        print("Please create a password")
        pwd = getpass.getpass("Password for " + user + ":")
        while(len(pwd))<8:
            print("Password needs to be a minimum of 8 characters")
            pwd = getpass.getpass("Password for " + user + ":")
        while(len(pwd))>15:
            print("Password needs to be a max of 15 characters")
            pwd = getpass.getpass("Password for " + user + ":")
        while(re.search("[a-z]", pwd)) is None:
            print("Password needs to contain 1 lowercase value")
            pwd = getpass.getpass("Password for " + user + ":")
        while(re.search("[A-Z]", pwd)) is None:
            print("Password needs to contain 1 uppercase value")
            pwd = getpass.getpass("Password for " + user + ":")
        while(re.search("[0-9]", pwd)) is None:
            print("Password needs to contain 1 number")
            pwd = getpass.getpass("Password for " + user + ":")
        while(re.search("[!@#$%^&*]", pwd)) is None:
            print("Password needs to contain a special character (!@#$%^&*)")
            pwd = getpass.getpass("Password for " + user + ":")
        permission = input("Permission code: ")
        while permission != "1" and permission != "2":
            print("Permission code needs to be 1 for member or 2 for admin access")
            permission = input("Permission code: ")
        return user, pwd, permission

    def checkCredentials(self, user, pwd, permission):
        lreq = CACM(user,pwd,permission)
        lreq= lreq.encode()
        self.getSocket().sendto(lreq.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
        data = self.getSocket().recv(self.getBUFFER_SIZE())
        if(data.decode() == "username already exists, please enter a new username"):
            print(data.decode())
            user = self.createUser()
            return
        if permission == "2":
            print("Your credentials have been sent to admin, checkback later for approval")
            sys.exit(1)
            return user
        else:
            print(data.decode())
            return user

    def inputCredentials(self):
        user = input("Username: ")
        passwd = getpass.getpass("Password for " + user + ":")
        permission = input("Permission code: ")
        lreq = LOGN(user,passwd,permission)
        lreq = lreq.encode()
        self.getSocket().sendto(lreq.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
        data = self.getSocket().recv(self.getBUFFER_SIZE())
        if(data.decode() == "not verified"):
            print(data.decode())
            user = None
            return user, passwd, permission,
        else:
            # s = self.getSocket()
            # data = self.recvall(s)
            #print(data.decode())
            return user, passwd, permission

    #inquirer code we are not using for the time being
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

if __name__ == "__main__":
    c = Client(ADDRESS_OF_SERVER,5005,1024)
    while True:
        user = c.createUser()
        if user:
            c.run(user)
                # c.chooseMessage(user)
