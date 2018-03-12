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

ADDRESS_OF_SERVER = '127.0.0.1'

class Client:
    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.cachedMessages = None
        self.ih = inputHandle()

    def createSock(self,port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully")
            self.socket = s
        except socket.error as msg:
            print("Error creating socket: %s" %msg)
            sys.exit(1)
        try:
            s.connect((self.TCP_IP, port))
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
    port = 5005
    c.createSock(port)
    c.getSocket().sendto((1000).to_bytes(4,'little'),(c.getTCP_IP(), c.getTCP_PORT()))
    print("sent 1000 byte request\nwaiting for response...")
    print("response recieved: ", c.recieveAll(c.getSocket().recv(c.getBUFFER_SIZE())))
