import socket
import getpass
import base64
from datetime import datetime
import time
# import inquirer
#from Crypto.Cipher import AES
from pprint import pprint
from Crypt import *

# cipher = AES.new('5050',AES.MODE_ECB)
class Request:
    def __init__(self,username,typer):
        self.type = typer
        self.username = username
        self.time = datetime.now()

    def getUsername(self):
        return self.username

    def getTime(self):
        return str(self.time)

    def addchar(self, string):
        a =''
        for i in string:
            if i == "|":
                a += ''.join(["\\", i])
                print(i)
            elif i == "\\":
                a += ''.join(["\\", i])
            elif i == "?":
                a += ''.join(["\\", i])
            elif i == ",":
                a += ''.join(["\\", i])
            else:
                a += i
        return a

    def removechar(self,string):
        ret = ""
        i = 0
        while i< len(string):
            if string[i] == "?":
                if string[i-1] != "\\":
                    return ret
            if string[i] == "\\":
                i +=1
            ret += string[i]
            i +=1
        return ret

class LOGN(Request):
    def __init__(self,username,passwd):
        Request.__init__(self,username,"LOGN")
        self.passwd = passwd

    def getPass(self):
        return self.passwd

    def getTime(self):
        return str(self.time)

    def encode(self):
        sendStr = "LOGN|"
        sendStr += self.addchar(self.getUsername()) + "|" + self.addchar(self.getPass()) + "|"+ self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.passwd = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.time = stream_item
                    stream_item = ""
                    writes = writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def __repr__(self):
        return("%s,%s,%s, %s"%(self.getUsername(), self.getPass(), self.getpubkey(),self.getTime()))


class PUBK(Request):
    def __init__(self,username, pubkey):
        Request.__init__(self,username,"PUBK")
        self.pubkey = pubkey
        self.username = username

    def getUsername(self):
        return self.username

    def getpubkey(self):
        return self.pubkey

    def encode(self):
        sendStr = "PUBK|"
        sendStr +=  self.addchar(self.getUsername()) + "|" + self.addchar(self.getpubkey()) + "|" + self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\" and stream[c+1] == ",":
                stream_item += stream[c] + stream[c+1]
                c = c+1
            elif stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.pubkey = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.time = stream_item
                    stream_item = ""
                    writes = writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def __repr__(self):
        return("%s,%s,%s"%(self.getUsername(),self.getpubkey(), self.getTime()))


class UPDT(Request):
    def __init__(self, Username, ouser, Tag, Perm):
        Request.__init__(self,Username,"UPDT")
        self.Perm = Perm
        self.ouser = ouser
        self.tag = Tag
        self.type = "UPDT"

    def getouser(self):
        return self.ouser

    def getTag(self):
        return self.tag

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
        elif Tag == "DUSR":
            ret = "8"
        return (ret)

    def encode(self):
        tagUp = self.interpretTag(self.getTag())
        sendStr = "UPDT|"
        sendStr += self.addchar(self.getUsername()) + "|" + self.addchar(self.getouser())+ "|" + self.addchar(tagUp) + "|" + self.addchar(self.getPerm()) + "|"+ self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.ouser = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.tag = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 3:
                    self.Perm = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 4:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def __repr__(self):
        return("%s, %s, %s, %s"%(self.getUsername(), self.getouser(), self.getTag(), self.getPermis()))

class CACM(Request):
    def __init__(self, username, password, permission, pubk):
        Request.__init__(self,username,"CACM")
        self.password = password
        self.permission = permission
        self.pubk = pubk

    def getpubkey(self):
        return self.pubk

    def getPass(self):
        return self.password

    def getPermis(self):
        return self.permission

    def encode(self):
        sendStr = "CACM|"
        sendStr += self.addchar(self.getUsername()) + "|" + self.addchar(self.getPass()) + "|" + self.addchar(str(self.getPermis())) + "|" + self.addchar(self.getpubkey().decode()) + "|" + self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self,stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\" and stream[c+1] == ",":
                stream_item += stream[c] + stream[c+1]
                c = c+1
            elif stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.password = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.permission = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 3:
                    self.pubk = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 4:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

        def __repr__(self):
            return("%s,%s,%s,%s,%s"%(self.getUsername(),self.getPass(),self.getPermis(), self.getpubk(), self.getTime()))

class SMSG(Request):
    def __init__(self, Username, Recipient, Message):
        Request.__init__(self,Username,"SMSG")
        self.Recipient = Recipient
        self.Message = Message

    def encode(self):
        sendStr = "SMSG|"
        sendStr +=  self.addchar(self.getUsername()) +"|" + self.addchar(self.getRecipient()) + "|" + self.addchar(self.getMessage()) +  "|"+ self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\" and stream[c+1] == ",":
                stream_item += stream[c] + stream[c+1]
                c = c+1
            elif stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.Recipient = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.Message = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 3:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def getRecipient(self):
        return self.Recipient

    def getMessage(self):
        return self.Message

    def __repr__(self):
        return("%s,%s,%s"%(self.username,self.Recipient,self.Message))

class DUSR(Request):
    def __init__(self, Username, deleteuser):
        Request.__init__(self,Username,"DUSR")
        self.deleteuser = deleteuser

    def getDeleteuser(self):
        return self.deleteuser

    def encode(self):
        sendStr = "DUSR|"
        sendStr +=  self.addchar(self.getUsername()) +"|" + self.addchar(self.getDeleteuser()) + "|"+ self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\" and stream[c+1] == ",":
                stream_item += stream[c] + stream[c+1]
                c = c+1
            elif stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.deleteuser = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1


    def __repr__(self):
        return("%s,%s"%(self.username,self.deleteuser))

class RMSG(Request):

    def __init__(self, user_sendto, messages):
        Request.__init__(self,user_sendto,"RMSG")
        self.user_sendto = user_sendto
        self.messages = messages

    def getuser_sendto(self):
        return self.user_sendto

    def getmessages(self):
        return self.messages

    def encode(self, messages):
        smessages=[]
        stringp =""
        lenall = str(len(messages))
        sendstr = "RMSG|"
        beg = sendstr + lenall
        for m in messages:
            i = 0
            smessages= []
            while i < len(m):
                if i == len(m)-1:
                    stringp+=m[i]
                    smessages.append(stringp)
                    stringp = ""
                elif m[i] == "\\" and m[i+1] == ",":
                    stringp += m[i+1]
                    i = i+1
                elif m[i] == ",":
                    smessages.append(stringp)
                    stringp = ""
                else:
                    stringp += m[i]
                i = i+1
            for s in smessages:
                beg += "|" + self.addchar(str(s))
        beg += "?"
        return beg

    def decode(self, stream):
        write_messages = []
        single_message = []
        writes = 0
        stream_item = ""
        c = 7
        while c  < len(stream):
            if stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    single_message.append(stream_item)
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    single_message.append(stream_item)
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    single_message.append(stream_item)
                    write_messages.append(single_message)
                    single_message = []
                    stream_item = ""
                    writes=0
                if stream[c] == "?":
                    self.messages = write_messages
                    return
            else:
                stream_item += stream[c]
            c=c+1


    def __repr__(self):
        nomessages = "You have no messages"
        if self.messages == None:
            return nomessages
        else:
            printstr = "\nHere are yo "+ str(len(self.messages)) + " messages:\n"
            for m in self.messages:
                singlestr = "MSG#" + str(self.messages.index(m)+1) +"\n"+ "From: " + m[0] + "\nTo: " + m[1] + "\nmsg: " + m[2] + "\n"
                printstr += singlestr
            return printstr


class DMSG(Request):

    def __init__(self,Username,Recipient,Message):
            Request.__init__(self,Recipient,"DMSG")
            self.Recipient = Username
            self.Message = Message

    def encode(self):
        return "DMSG|" + self.addchar(self.getUsername()) + "|" + self.addchar(self.getRecipient()) + "|" + self.addchar(self.getMessage()) + "|" + self.addchar(self.getTime()) + "?"

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.Recipient = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.Message = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 3:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def getUsername(self):
        return self.username

    def getRecipient(self):
        return self.Recipient

    def getMessage(self):
        return self.Message

    def __repr__(self):
        return("%s,%s,%s"%(self.Recipient,self.username,self.Message))

class CMSG(Request):

    def __init__(self, Username):
        Request.__init__(self,Username, "CMSG")

    def encode(self):
        return "CMSG|" + self.addchar(self.getUsername()) + "|" + self.addchar(self.getTime()) + "?"
        #return self.encrypt(string)

    def decode(self,stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def __repr__(self):
        return("%s"%(self.getUsername()))

class DUSR(Request):
    def __init__(self, Username, deleteuser):
        Request.__init__(self,Username,"DUSR")
        self.deleteuser = deleteuser

    def getDeleteuser(self):
        return self.deleteuser

    def encode(self):
        sendStr = "DUSR|"
        sendStr +=  self.addchar(self.getUsername()) +"|" + self.addchar(self.getDeleteuser()) + "|"+ self.addchar(self.getTime()) + "?"
        return sendStr

    def decode(self, stream):
        writes = 0
        stream_item = ""
        c = 5
        while c  < len(stream):
            if stream[c] == "\\" and stream[c+1] == ",":
                stream_item += stream[c] + stream[c+1]
                c = c+1
            elif stream[c] == "\\":
                stream_item += stream[c+1]
                c=c+1
            elif stream[c] == "|" or stream[c] == "?":
                if writes == 0:
                    self.username = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 1:
                    self.deleteuser = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.time = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1


    def __repr__(self):
        return("%s,%s"%(self.username,self.deleteuser))
