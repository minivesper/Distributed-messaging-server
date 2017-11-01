import socket
import getpass
import base64
# import inquirer
#from Crypto.Cipher import AES
from pprint import pprint

cipher = AES.new('5050',AES.MODE_ECB)

class LOGN:
    def __init__(self,Username,passwd):
        self.Username = Username
        self.passwd = passwd

    def getUsername(self):
        return self.Username

    def getPass(self):
        return self.passwd

    def encode(self):
        sendStr = "LOGN|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|"+ str(len(self.getPass())) + "|" + self.getPass()
        return sendStr

    def decode(self, stream):
        s = stream.split("|")
        self.Username = s[1]
        self.passwd = s[3]

    #def encrypt(self,string):
    #    encrypted_string = base64.b64encode(cipher.encrypt(string))
    #    return encrypted_string

    #def decrypt(self,string):
    #    decrypted_string = cipher.decrypt(base64.b64decode(string))
    #    return decrypted_string

    def __repr__(self):
        return("%s,%s"%(self.getUsername(), self.getPass()))

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
        print(parselist)
        self.Username = parselist[2]
        self.Recipient = parselist[4]
        self.Message = parselist[6]

#    def encrypt(self,string):
#        encrypted_string = base64.b64encode(cipher.encrypt(string))
#        return encrypted_string

#    def decrypt(self,string):
#        decrypted_string = cipher.decrypt(base64.b64decode(string))
#        return decrypted_string

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

#    def encrypt(self,string):
#        encrypted_string = base64.b64encode(cipher.encrypt(string))
#        return encrypted_string

#    def decrypt(self,string):
#        decrypted_string = cipher.decrypt(base64.b64decode(string))
#        return decrypted_string

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
        #return self.encrypt(string)

    def decode(self,stream):
        #stream = self.decrypt(stream)
        spstr = stream.split("|")
        self.Username = spstr[1]

    #def encrypt(self,string):
    #    encrypted_string = base64.b64encode(cipher.encrypt(string))
    #    return encrypted_string

    #def decrypt(self,string):
    #    decrypted_string = cipher.decrypt(base64.b64decode(string))
    #    return decrypted_string

    def __repr__(self):
        return("%s"%(self.getUsername()))
