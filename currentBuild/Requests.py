import socket
import getpass
# import inquirer
from pprint import pprint

# class Requests:
#     def __init__():
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket = s
#         s.connect((self.TCP_IP, self.TCP_PORT))

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
        return("LOGN: %s %s"%(self.getUsername(), self.getPass()))

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
        self.Username = parselist[2]
        self.Recipient = parselist[4]
        self.Message = parselist[6]

    def __repr__(self):
        return("SMSG: %s %s %s"%(self.getUsername(),self.getRecipient(),self.getMessage()))

    def getUsername(self):
        return self.Username

    def getRecipient(self):
        return self.Recipient

    def getMessage(self):
        return self.Message

    def __repr__(self):
        return("%s %s %s"%(self.Username,self.Recipient,self.Message))

class CMSG:

    def __init__(self, Username):
    	self.Username = Username
