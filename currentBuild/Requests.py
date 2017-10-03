import socket
import getpass
import inquirer
from pprint import pprint

class Requests:
    def __init__():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s
        s.connect((self.TCP_IP, self.TCP_PORT))

class SMSG:
    def __init__(self, Username, Recipient, Message):
        self.Username = Username
        self.Recipient = Recipient
        self.Message = Message

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

    
