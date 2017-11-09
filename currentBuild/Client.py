import socket
import sys
import re
import getpass
import select
# import inquirer
from Crypt import *
from Requests import *
from pprint import pprint
from inputHandle import *
import time

ADDRESS_OF_SERVER = '127.0.0.1'

class Client:
    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.cachedMessages = None
        self.ih = inputHandle()

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

    def sendAll(self,reqstr,buffsize):
        cry = Crypt()
        req = cry.encryptit(reqstr)
        self.getSocket().sendto((len(req)).to_bytes(4,'little'),(self.getTCP_IP(), self.getTCP_PORT()))
        self.getSocket().sendto(req,(self.getTCP_IP(), self.getTCP_PORT()))

    def recieveAll(self,buffsize):
        retdata = ""
        cry = Crypt()
        data = bytearray()
        packetsize = self.getSocket().recv(4)
        while sys.getsizeof(data) < int.from_bytes(packetsize,'little'):
            read_sockets, write_sockets, error_sockets = select.select([self.getSocket()], [], [], 4)
            if self.getSocket() in read_sockets:
                data.extend(self.getSocket().recv(self.getBUFFER_SIZE()))
            else:
                return "timeout"
        retdata = cry.decryptit(bytes(data)).decode()
        return retdata

    def handleCommand(self, inp_str, username):
        req = ""
        if(inp_str == "SMSG"):
            sendTo,msgtxt = self.ih.sendHandle()
            req = SMSG(username, sendTo, msgtxt)
            req = req.encode()

        elif(inp_str == "CMSG"):
            req = CMSG(username)
            req = req.encode()

        elif(inp_str == "DMSG"):
            if(self.cachedMessages == None):
                self.handleCommand("CMSG",username)
                if(self.cachedMessages == None):
                    return
                self.handleCommand("DMSG",username)
            else:
                if(len(self.cachedMessages) != 0):
                    message_num =self.ih.deleteHandle(self.cachedMessages)
                    req = DMSG(self.cachedMessages[message_num-1][1],self.cachedMessages[message_num-1][0],self.cachedMessages[message_num-1][2])
                    req = req.encode()

        elif(inp_str == "UPDT"):
            updts = self.ih.updateHandle()
            req = UPDT(username, updts[0], updts[1], updts[2])
            req = req.encode()

        elif(inp_str == "QUIT"):
            self.getSocket().close()
            sys.exit(1)

        if(req != ""):
            self.sendAll(req,self.getBUFFER_SIZE())
            data = self.recieveAll(self.getBUFFER_SIZE())
            self.handleReturn(data)
        else:
            print("%s is not a valid request type"%(inp_str))

    def run(self, currentUsername):
        while True:
            inp = input("enter Command: ").upper()
            self.handleCommand(inp, currentUsername)

    def createUser(self):
        user = None
        inp = input("LOGN or CACM? ").upper()
        if inp == "LOGN":
            user = self.inputCredentials()
            return user
        elif inp == "CACM":
            user, pwd, permission = self.ih.getCredentials()
            user = self.checkCredentials(user, pwd, permission)
            return user
        else:
            print("LOGN or CACM dummy! not %s"%(inp))
            return user

    def checkCredentials(self, user, pwd, permission):
        cry = Crypt()
        userb = user.encode('utf-8')
        pwdb = pwd.encode('utf-8')
        pwd = cry.hashpwd(userb,pwdb)
        lreq = CACM(user,str(pwd),permission)
        lreq= lreq.encode()
        self.sendAll(lreq,self.getBUFFER_SIZE())
        data = self.recieveAll(self.getBUFFER_SIZE())
        if(data == "username already exists, please enter a new username"):
            print(data)
            user = self.createUser()
            return None
        if permission == "2":
            print("Your credentials have been sent to admin, checkback later for approval")
            sys.exit(1)
            return user
        else:
            print(data)
            return user

    def inputCredentials(self):
        cry = Crypt()
        user = input("Username: ")
        pwd = getpass.getpass("Password for " + user + ": ")
        userb = user.encode('utf-8')
        pwdb = pwd.encode('utf-8')
        pwd = cry.hashpwd(userb,pwdb)
        lreq = LOGN(user,str(pwd))
        lreq = lreq.encode()
        self.sendAll(lreq,self.getBUFFER_SIZE())
        data = self.recieveAll(self.getBUFFER_SIZE())
        print(data)
        if(data == "Not a valid login?"):
            return None
        else:
            return user

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
    user = None
    while not user:
        user = c.createUser()
    c.run(user)
                # c.chooseMessage(user)
