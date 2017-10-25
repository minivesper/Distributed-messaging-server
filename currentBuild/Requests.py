import socket
import getpass
# import inquirer
from pprint import pprint

class LOGN:
    def __init__(self,Username,passwd):
        self.Username = Username
        self.passwd = passwd

    def getUsername(self):
        return self.Username

    def getPass(self):
        return self.passwd

    def encode(self):
        sendStr = "LOGN"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|"+ str(len(self.getPass())) + "|" + self.getPass()
        return sendStr

    def decode(self, stream):
        s = stream.split("|")
        self.Username = s[1]
        self.passwd = s[3]

    def __repr__(self):
        return("%s,%s"%(self.getUsername(), self.getPass()))

    # def decode(self, stream):
    #     userlen = ""
    #     user = ""
    #     passlen = ""
    #     password = ""
    #     for i in range(4, len(stream)):
    #         if(stream[i] != "|" and isinstance(userlen, str)):
    #             userlen += stream[i]
    #         elif(stream[i] == "|" and passlen == ""):
    #             userlen = int(userlen)
    #             print(userlen)
    #         elif(stream[i] != "|" and isinstance(userlen, int)):
    #             passlen += stream[i]
    #         elif(stream[i] == "|" and isinstance(userlen, int)):
    #             passlen = int(passlen)
    #     print(passlen)
    #     print(userlen)


class SMSG:
    def __init__(self, Username, Recipient, Message):
        self.Username = Username
        self.Recipient = Recipient
        self.Message = Message

    def encode(self):
        sendStr = "SMSG"
        sendStr += "|" + str(len(self.Username)) + "|" + self.getUsername() +"|" + str(len(self.Recipient)) + "|" + self.getRecipient() +"|" + str(len(self.Message)) + "|" + self.getMessage()
        return sendStr

    def decode(self, parseStr):
        parselist = parseStr.split("|")
        print(parselist)
        self.Username = parselist[2]
        self.Recipient = parselist[4]
        self.Message = parselist[6]


    def getUsername(self):
        return self.Username

    def getRecipient(self):
        return self.Recipient

    def getMessage(self):
        return self.Message

    def __repr__(self):
        return("%s,%s,%s"%(self.Username,self.Recipient,self.Message))

class RMSG:

    def __init__(self, user_sendto, messages):
        self.user_sendto = user_sendto
        self.messages = messages

    def getuser_sendto(self):
        return self.user_sendto

    def getmessages(self):
        return self.messages

    def encode(self, messages):
        lenall = str(len(messages))
        sendstr = "RSMG,"
        beg = sendstr + lenall
        for m in messages:
            sm = m.split(",")
            print(sm)
            for s in sm:
                beg += "," + str(len(s)) + "," + str(s)
                #sets up the request as:
                # RMSG,#messages for user, length of user who sent message, user, length of the user reciving message(we wanted to keep this so we can have clients send a message to multiple people), userrec, length of message, message
        return beg

    def decode(self, messages):
        messages = messages.split(",")
        lenarr = messages[1]
        Matrix = [[0 for x in range(3)] for y in range(lenarr)]
        for m in messages[3:-1]:
        #need to talk about decoding the string from the server. We have the issue of parsing through and knowing when to stop because the


        messages[]
        for m in messages:
            ms = m.split(",")
            for m in ms


class CMSG:

    def __init__(self, Username):
    	self.Username = Username

    def getUsername(self):
        return self.Username

    def encode(self):
        return "CMSG" + str(len(self.getUsername())) + "|" + self.getUsername()

    def decode(self,stream):
        spstr = stream.split("|")
        self.Username = spstr[1]

    def __repr__(self):
        return("%s"%(self.getUsername()))
