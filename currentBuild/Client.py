import socket
import sys
import re
import getpass
import select
# import inquirer
from DatabaseC import *
from errHandle import *
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
        self.fc = FernetCrypt()
        self.dbc = DatabaseC()
        self.e = errHandle()
        self.username =""
        self.keyLoaded = False
        #self.asym = asymetricSuite(keypair)

        keyExist = self.ih.YorN("Do you have a keypair acessible from this location? ")
        if keyExist:
            self.c_keys = self.ih.getkey()
            self.keyLoaded = True
            if not self.c_keys:
                self.c_keys = GenKeys()
        else:
            self.c_keys = GenKeys()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully")
            self.socket = s
        except socket.error as msg:
            print("Error creating socket: %s" %msg)
            sys.exit(1)
        try:
            print(self.TCP_IP, self.TCP_PORT)
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

    def sendAll(self,sig,reqstr,buffsize):
        req = reqstr
        if not sig:
            self.getSocket().sendto((1).to_bytes(4,'little'),(self.getTCP_IP(),self.getTCP_PORT()))
            self.getSocket().sendto((len(req)).to_bytes(4,'little'),(self.getTCP_IP(), self.getTCP_PORT()))
            self.getSocket().sendto(req,(self.getTCP_IP(), self.getTCP_PORT()))
        else:
            self.getSocket().sendto((0).to_bytes(4,'little'),(self.getTCP_IP(),self.getTCP_PORT()))
            self.getSocket().sendto((len(req)).to_bytes(4,'little'),(self.getTCP_IP(), self.getTCP_PORT()))
            self.getSocket().sendto(req,(self.getTCP_IP(), self.getTCP_PORT()))
            self.getSocket().sendto((len(sig)).to_bytes(4,'little'),(self.getTCP_IP(), self.getTCP_PORT()))
            self.getSocket().sendto(sig,(self.getTCP_IP(), self.getTCP_PORT()))


    def recieveAll(self,buffsize):
        retdata = ""
        data = bytearray()
        packettype = int.from_bytes(self.getSocket().recv(4), 'little')
        if packettype == 1:
            packetsize = int.from_bytes(self.getSocket().recv(4),'little')
            while packetsize > 0:
                read_sockets, write_sockets, error_sockets = select.select([self.getSocket()], [], [], 4)
                if self.getSocket() in read_sockets:
                    if(packetsize > 1024):
                        singlerec = self.getSocket().recv(self.getBUFFER_SIZE())
                    else:
                        singlerec = self.getSocket().recv(packetsize)
                        packetsize -= sys.getsizeof(singlerec)
                    data.extend(singlerec)
                else:
                    return "timeout"
            return None,bytes(data)

        elif packettype == 0:
            ret = []
            for i in range(2):
                retdata = ""
                data = bytearray()
                packetsize = int.from_bytes(self.getSocket().recv(4),'little')
                while packetsize > 0:
                    read_sockets, write_sockets, error_sockets = select.select([self.getSocket()], [], [], 4)
                    if self.getSocket() in read_sockets:
                        if(packetsize > 1024):
                            singlerec = self.getSocket().recv(self.getBUFFER_SIZE())
                        else:
                            singlerec = self.getSocket().recv(packetsize)
                            packetsize -= sys.getsizeof(singlerec)
                        data.extend(singlerec)
                    else:
                        return "timeout"
                ret.append(bytes(data))
            return (int(ret[1].decode()),),(ret[0],)

    def handleReturn(self, returnreq):
        if returnreq[0:4] == "PUBK" :
            pk = PUBK(None,None)
            pk.decode(returnreq)
            self.dbc.writesk(pk.getpubkey())
            return
        elif returnreq[0:4] == "RMSG":
            rm = RMSG(None,None)
            rm.decode(returnreq)
            print(rm)
            self.cachedMessages = rm.messages
        else:
            print(returnreq)

    def handleCommand(self, inp_str, username):
        req = "Not a valid Server-- attacker present"
        if(inp_str == "SMSG"):
            sendTo,msgtxt = self.ih.sendHandle()
            req = SMSG(username, sendTo, msgtxt)
            req = req.encode()

        elif(inp_str == "CMSG"):
            req = CMSG(username)
            req = req.encode()

        elif(inp_str == "DUSR"):
            updts = self.ih.deleteUserHandle()
            req = DUSR(username, updts)
            req = req.encode()

        elif(inp_str == "DMSG"):
            if(self.cachedMessages == None):
                self.handleCommand("CMSG",username)
                if(self.cachedMessages == None):
                    return
                self.handleCommand("DMSG",username)
            else:
                if(len(self.cachedMessages) != 0):
                    print(self.cachedMessages)
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
            #change to server's public key duh idiot
            keypair = self.dbc.readk(username)
            asym = asymetricSuite(keypair)
            sig,enc_req = asym.encryptit(req,self.dbc.readsk())
            self.sendAll(str(sig[0]).encode(),enc_req[0],self.getBUFFER_SIZE())
            sig, data = self.recieveAll(self.getBUFFER_SIZE())
            msg,ver = asym.decryptit(data,sig,self.dbc.readsk())
            if(ver):
                self.handleReturn(msg.decode())
            else:
                return req
        else:
            print("%s is not a valid request type"%(inp_str))


    def run(self, currentUsername):
        while True:
            inp = input("enter Command: ").upper()
            self.handleCommand(inp, currentUsername)

    def login(self):
        user = None
        user = self.inputCredentials()
        return user

    def createUser(self):
        #generate keypairs for encryption and swap public keys
        if self.keyLoaded:
            user = self.inputCredentials()
        else:
            user = None
            user, pwd, permission = self.ih.getCredentials()
            user = self.checkCredentials(user, pwd, permission)
        return user

    def checkCredentials(self, user, pwd, permission):
        userb = user.encode('utf-8')
        pwdb = pwd.encode('utf-8')
        pwd = self.fc.hashpwd(userb, pwdb)

        u_keypair = self.c_keys
        u_keypairs = u_keypair.getkeypair().exportKey('PEM')
        self.c_keys = self.c_keys.getkeypair()
        error = self.dbc.writek(user, u_keypairs)
        ret = self.e.send_err(error) #need to come back to this ??
        #u_keypairs = u_keypair.getpubkey().exportKey('PEM')

        if error == 0:
            lreq = CACM(user,pwd.decode(),permission, u_keypair.getpubkey().exportKey('PEM'))
            lreq= lreq.encode()
            lreq = self.fc.encryptit(lreq)
            self.sendAll(None,lreq,self.getBUFFER_SIZE())
            sig, data = self.recieveAll(self.getBUFFER_SIZE())
            msg = self.fc.decryptit(data)
            self.handleReturn(msg.decode())
            if(data == "username already exists, please enter a new username"):
                user = self.inputCredentials()
                return None
            if permission == "2":
                print("Your credentials have been sent to admin, checkback later for approval")
                user = self.login()
                return user
            else:
                print("account created, please login")
                user = self.login()
                return user

    def inputCredentials(self):
        user, pwd, userb, pwdb = self.ih.credHandle()
        self.username = user
        keypair = self.c_keys
        print(keypair)
        if not keypair:
            print("username does not exist")
            return None
        else:
            asym = asymetricSuite(keypair) #inits the asymmetric suite so we can use encryption
            u_pubkey = keypair.publickey().exportKey('PEM')
            pwd = self.fc.hashpwd(userb,pwdb) #creates the hash of the password
            lreq = LOGN(user,pwd.decode())
            lreq = lreq.encode() #changes string to bytes
            sig, enc_lreq = asym.encryptit(lreq, self.dbc.readsk())
            self.sendAll(str(sig[0]).encode(),enc_lreq[0],self.getBUFFER_SIZE())
            sig, data = self.recieveAll(self.getBUFFER_SIZE())
            msg,ver = asym.decryptit(data,sig,self.dbc.readsk())
            if(ver):
                self.handleReturn(msg.decode())
            else:
                return req
            strmsg  = msg.decode()
            if(strmsg == "Not a valid login?"):
                print(data)
                return None
            elif (strmsg == "Already logged in byeeee"):
                print(data)
                self.getSocket().close()
                sys.exit(1)
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
