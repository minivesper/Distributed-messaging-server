import socket
import getpass
import base64
# import inquirer
#from Crypto.Cipher import AES
from pprint import pprint

cipher = AES.new('5050',AES.MODE_ECB)

class LOGN:
    def __init__(self,username,passwd,permission):
        self.username = username
        self.passwd = passwd
        self.permission = permission
        self.type = "LOGN"

    def getUsername(self):
        return self.username

    def getPermis(self):
        return self.permission

    def getPass(self):
        return self.passwd

    def encode(self):
        sendStr = "LOGN|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|"+ str(len(self.getPass())) + "|" + self.getPass() + "|" + str(self.getPermis())
        return sendStr

    def decode(self, stream):
        s = stream.split("|")
        self.username = s[2]
        self.passwd = s[4]
        self.permission = s[5]


    def __repr__(self):
        return("%s,%s,%s"%(self.getUsername(), self.getPass(), self.getPermis()))


class UPDT:
    def __init__(self, Username, ouser, Tag, Perm):
        self.Username = Username
        self.Tag = Tag
        self.Perm = Perm
        self.ouser = ouser
        self.type = "UPDT"

    def getUsername(self):
        return self.Username

    def getouser(self):
        return self.ouser

    def getTag(self):
        return self.Tag

    def getPerm(self):
        return self.Perm

    def interpretTag(self, Tag):
        if Tag == "LOGN":
            ret = "1"
        elif Tag == "SMSG":
            ret = "2"
        elif Tag =="CMSG":
            ret = "3"
        elif Tag == "RMSG":
            ret = "4"
        elif Tag == "UPDT":
            ret = "5"
        elif Tag == "CACM":
            ret = "6"
        elif Tag == "DMSG":
            ret = "7"
        return (ret)

    def encode(self, Tag):
        tagUp = self.interpretTag(Tag)
        sendStr = "UPDT|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|" + str(len(self.getouser())) + "|" + self.getouser()+ "|" + str(len(tagUp)) + "|" + tagUp + "|" + str(len(self.getPerm())) + "|" + self.getPerm()
        return sendStr

    def decode(self, stream):
        spstr = stream.split("|")
        self.Username = spstr[2]
        self.ouser = spstr[4]
        self.Tag = spstr[6]
        self.Perm = spstr[8]

    def __repr__(self):
        return("%s, %s, %s, %s"%(self.getUsername(), self.getouser(), self.getTag(), self.getPermis()))



class CACM:
    def __init__(self, username, password, permission):
        self.username = username
        self.password = password
        self.permission = permission

    def getUsername(self):
        return self.username

    def getPass(self):
        return self.password

    def getPermis(self):
        return self.permission

    def encode(self):
        sendStr = "CACM|"
        sendStr += str(len(self.getUsername())) + "|" + self.getUsername() + "|" + str(len(self.getPass())) + "|" + self.getPass() + "|" + str(self.getPermis())
        return sendStr

    def decode(self, parseStr):
        parselist = parseStr.split("|")
        print(parselist)
        self.username = parselist[2]
        self.password = parselist[4]
        self.permission = parselist[5]

    #def encrypt(self,string):
    #    encrypted_string = base64.b64encode(cipher.encrypt(string))
    #    return encrypted_string

    #def decrypt(self,string):
    #    decrypted_string = cipher.decrypt(base64.b64decode(string))
    #    return decrypted_string

    def __repr__(self):
        return("%s,%s,%s"%(self.getUsername(),self.getPass(),self.getPermis()))


class SMSG:
    def __init__(self, Username, Recipient, Message):
        self.Username = Username
        self.Recipient = Recipient
        self.Message = Message
        self.type = "SMSG"

    def encode(self):
        sendStr = "SMSG"
        sendStr += "|" + str(len(self.Username)) + "|" + self.getUsername() +"|" + str(len(self.Recipient)) + "|" + self.getRecipient() +"|" + str(len(self.Message)) + "|" + self.getMessage()
        return sendStr

    def decode(self, parseStr):
        parselist = parseStr.split("|")
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
        self.type = "RMSG"
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
        printstr = "\nHere are yo "+ str(len(self.messages)) + " messages:\n"
        for m in self.messages:
            singlestr = "MSG#" + str(self.messages.index(m)+1) +"\n"+ "From: " + m[0] + "\nTo: " + m[1] + "\nmsg: " + m[2] + "\n"
            printstr += singlestr
        return printstr

class DMSG:

    def __init__(self,Username,Recipient,Message):
            self.Username = Recipient
            self.Recipient = Username
            self.Message = Message
            self.type = "DMSG"

    def encode(self):
        return "DMSG|" + str(len(self.Username)) + "|" + self.getUsername() +"|" + str(len(self.Recipient)) + "|" + self.getRecipient() +"|" + str(len(self.Message)) + "|" + self.getMessage()

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
        return("%s,%s,%s"%(self.Recipient,self.Username,self.Message))

class CMSG:

    def __init__(self, Username):
        self.Username = Username
        self.type = "CMSG"

    def getUsername(self):
        return self.Username

    def encode(self):
        return "CMSG|" + str(len(self.getUsername())) + "|" + self.getUsername()
        #return self.encrypt(string)

    def decode(self,stream):
        #stream = self.decrypt(stream)
        spstr = stream.split("|")
        self.Username = spstr[2]

    #def encrypt(self,string):
    #    encrypted_string = base64.b64encode(cipher.encrypt(string))
    #    return encrypted_string

    #def decrypt(self,string):
    #    decrypted_string = cipher.decrypt(base64.b64decode(string))
    #    return decrypted_string

    def __repr__(self):
        return("%s"%(self.getUsername()))
