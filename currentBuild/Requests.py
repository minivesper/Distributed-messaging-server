import socket
import getpass
# import inquirer
from pprint import pprint

class LOGN:
    def __init__(self,username,passwd,permission):
        self.username = username
        self.passwd = passwd
        self.permission = permission


    def getPermis(self):
        return self.permission

    def getUsername(self):
        return self.username

    def getPass(self):
        return self.passwd

    def encode(self):
        sendStr = "LOGN|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|"+ str(len(self.getPass())) + "|" + self.getPass() + "|" + str(self.getPermis())
        print(sendStr)
        return sendStr

    def decode(self, stream):
        s = stream.split("|")
        self.username = s[2]
        self.passwd = s[4]
        self.permission = s[5]


    def __repr__(self):
        return("%s,%s,%s"%(self.getUsername(), self.getPass(), self.getPermis()))

class CAPR:

    def __init__(self, Username):
    	self.Username = Username

    def getUsername(self):
        return self.Username

    def encode(self):
        return "CAPR|" + str(len(self.getUsername())) + "|" + self.getUsername()

    def decode(self,stream):
        spstr = stream.split("|")
        self.Username = spstr[2]

    def __repr__(self):
        return("%s"%(self.getUsername()))

class RAPR:

    def __init__(self, user_sendto, messages):
        self.user_sendto = user_sendto
        self.messages = messages

    def getuser_sendto(self):
        return self.user_sendto

    def getmessages(self):
        return self.messages

    def encode(self, messages):
        lenall = str(len(messages))
        sendstr = "RAPR|"
        beg = sendstr + lenall
        for m in messages:
            sm = m.split(",")
            for s in sm:
                beg += "|" + str(len(s)) + "|" + str(s)
                #sets up the request as:
                # RMSG,#messages for user, length of user who sent message, user, length of the user reciving message(we wanted to keep this so we can have clients send a message to multiple people), userrec, length of message, message
        print(beg)
        return beg

    def decode(self, messages):
        write_messages = []
        single_message = []
        messages = messages.split("|")
        messages = messages[2:]
        for i in range(len(messages)):
            if i%6 == 3:
                single_message.append(messages[i])
            elif i%6 == 5:
                single_message.append(messages[i])
            elif i%6 == 1:
                single_message.append(messages[i])
            if(len(single_message) == 3):
                write_messages.append(single_message)
                single_message = []
        self.messages = write_messages

    def __repr__(self):
        printstr = "\nHere are yo "+ str(len(self.messages)) + " messages:\n"
        for m in self.messages:
            singlestr = "From: " + m[0] + "\nTo: " + m[1] + "\nmsg: " + m[2] + "\n"
            printstr += singlestr
        return printstr


# class CUSR:
#     def __init__(self, username):
#         self.username = username
#
#     def getUsername(self):
#         return self.username

class CACM:
    def __init__(self, username, password, permission):
        self.username = username
        self.password = password
        self.permission = permission
        self.approval = approval

    def getUsername(self):
        return self.username

    def getAppr(self):
        return self.approval

    def getPass(self):
        return self.password

    def getPermis(self):
        return self.permission

    def encode(self):
        sendStr = "CACM|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|" + str(len(self.getPass())) + "|" + self.getPass() + "|" + str(self.getPermis()) + "|" + str(self.getAppr())
        return sendStr

    def decode(self, parseStr):
        parselist = parseStr.split("|")
        print(parselist)
        self.username = parselist[2]
        self.password = parselist[4]
        self.permission = parselist[5]
        self.approval = parselist[6]

    def __repr__(self):
        return("%s,%s,%s,%s"%(self.getUsername(),self.getPass(),self.getPermis(), self.getAppr()))

class AAPR:
    def __init__(self, username, password, permission,approval, admin):
        self.username = username
        self.password = password
        self.permission = permission
        self.approval = approval
        self.admin = admin

    def getUsername(self):
        return self.username

    def getPass(self):
        return self.password

    def getPermis(self):
        return self.permission

    def getAdmin(self):
        return self.admin

    def getAppr(self):
        return self.approval

    def encode(self):
        sendStr = "AAPP|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|" + str(len(self.getPass())) + "|" + self.getPass() + "|" + str(self.getPermis()) + "|" + str(self.getAppr()) + "|" + self.getAdmin()
        return sendStr

    def decode(self, parseStr):
        parselist = parseStr.split("|")
        print(parselist)
        self.username = parselist[2]
        self.password = parselist[4]
        self.permission = parselist[5]
        self.approval = parselist[6]
        self.admin = parselist[7]

    def __repr__(self):
        return("%s,%s,%s,%s,%s"%(self.getUsername(),self.getPass(),self.getPermis(), self.getAppr(), self.getAdmin()))

    #may be a direction we go when we get rid of bars
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
        sendstr = "RMSG|"
        beg = sendstr + lenall
        for m in messages:
            sm = m.split(",")
            for s in sm:
                beg += "|" + str(len(s)) + "|" + str(s)
                #sets up the request as:
                # RMSG,#messages for user, length of user who sent message, user, length of the user reciving message(we wanted to keep this so we can have clients send a message to multiple people), userrec, length of message, message
        return beg

    def decode(self, messages):
        write_messages = []
        single_message = []
        messages = messages.split("|")
        messages = messages[2:]
        for i in range(len(messages)):
            if i%6 == 3:
                single_message.append(messages[i])
            elif i%6 == 5:
                single_message.append(messages[i])
            elif i%6 == 1:
                single_message.append(messages[i])
            if(len(single_message) == 3):
                write_messages.append(single_message)
                single_message = []
        self.messages = write_messages

    def __repr__(self):
        printstr = "\nHere are yo messages:\n"
        for m in self.messages:
            singlestr = "From: " + m[0] + "\nTo: " + m[1] + "\nmsg: " + m[2] + "\n"
            printstr += singlestr
        return printstr

class CMSG:

    def __init__(self, Username):
    	self.Username = Username

    def getUsername(self):
        return self.Username

    def encode(self):
        return "CMSG|" + str(len(self.getUsername())) + "|" + self.getUsername()

    def decode(self,stream):
        spstr = stream.split("|")
        self.Username = spstr[1]

    def __repr__(self):
        return("%s"%(self.getUsername()))
