import socket
import getpass
import inquirer
from Requests import *
from pprint import pprint

class Client:
    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s
        s.connect((self.TCP_IP, self.TCP_PORT))

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getSocket(self):
        return self.socket

    def handleCommand(self, inp_str):
        self.getSocket().sendto(inp_str.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
        data = self.getSocket().recv(self.getBUFFER_SIZE())
        print(data.decode())

    def run(self):
        while True:
            inp = input("enter Command: ")
            self.handleCommand(inp)

    def inputCredentials(self):
        user = input("Username:")
        passwd = getpass.getpass("Password for " + user + ":")
        self.handleCommand(user)
        self.handleCommand(passwd)
        return user,passwd

    def handleRequest(self):

    def chooseMessage(self, user):
        amswers={}
        while answers != 'Quit':
            questions = [inquirer.List('type',message="What do you want to do?",
                    choices=['Check Messages', 'Send Message', 'Quit'],),]
            answers = inquirer.prompt(questions)
            if answers["type"] == 'Send Message':
                who = input("who do you send to ")
                what = input("what you send ")
                sm = SMSG(user,who,what)
                self.handleCommand(str(sm))
            if answers["type"]=='Check Messages':
                cm =CMSG(user)
                #need to create function that deals with if user is going to request all messages from all recipients at once? & how the server will handle it
            if answers["type"]=='Quit':
                s = getSocket()
                s.close()
            #pprint(response)
            #response = get_answer(answers)
            #self.handleCommand(response)


# TCP_IP = '127.0.0.1'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024
# MESSAGE = "Hello World!"

if __name__ == "__main__":
    c = Client('127.0.0.1',5005,1024)
    user, passwd = c.inputCredentials()
    c.chooseMessage(user)
    c.run()
