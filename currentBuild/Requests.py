import socket
import getpass
# import inquirer
from pprint import pprint

#class Requests:
    # def __init__():
    #     # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     # self.socket = s
    #     # s.connect((self.TCP_IP, self.TCP_PORT))

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
