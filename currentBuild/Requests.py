import socket
import getpass
import base64
# import inquirer
#from Crypto.Cipher import AES
from pprint import pprint

# cipher = AES.new('5050',AES.MODE_ECB)
class Request:
    def __init__(self,username,typer):
        self.type = typer
        self.username = username

    def getUsername(self):
        return self.username

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

    def encode(self):
        sendStr = "LOGN|"
        sendStr += self.addchar(self.getUsername()) + "|" + self.addchar(self.getPass()) + "?"
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
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def __repr__(self):
        return("%s,%s"%(self.getUsername(), self.getPass()))

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
        return (ret)

    def encode(self):
        tagUp = self.interpretTag(self.getTag())
        sendStr = "UPDT|"
        sendStr += self.addchar(self.getUsername()) + "|" + self.addchar(self.getouser())+ "|" + self.addchar(tagUp) + "|" + self.addchar(self.getPerm()) + "?"
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
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1

    def __repr__(self):
        return("%s, %s, %s, %s"%(self.getUsername(), self.getouser(), self.getTag(), self.getPermis()))

class CACM(Request):
    def __init__(self, username, password, permission):
        Request.__init__(self,username,"CACM")
        self.password = password
        self.permission = permission

    def getPass(self):
        return self.password

    def getPermis(self):
        return self.permission

    def encode(self):
        sendStr = "CACM|"
        sendStr += self.addchar(self.getUsername()) + "|" + self.addchar(self.getPass()) + "|" + self.addchar(str(self.getPermis())) + "?"
        return sendStr

    def decode(self,parseStr):
        parselist = []
        for i in range(len(parseStr)):
            if parselist:
                if parseStr[i] == "?":
                    if parseStr[i-1] != "\\":
                        parselist.append(parseStr[b+1:])
                else:
                    if parseStr[i] == "|":
                        if parseStr[i-1] != "\\":
                            parselist.append(parseStr[b+1:i])
                            b = i
                        elif parseStr[i-1] == "\\":
                            if parseStr[i-1] == "\\" and parseStr[i-2] == "\\":
                                parselist.append(parseStr[b+1:i])
                                b = i
            else:
                if parseStr[i] == "|":
                    if parseStr[i-1] != "\\":
                        parselist.append(parseStr[0:i])
                        b=i
        i = 0
        print(parselist)
        while i< len(parselist):
            parselist[i] = self.removechar(parselist[i])
            i +=1
        self.username = parselist[1]
        self.password = parselist[2]
        self.permission = parselist[3]

    #def encrypt(self,string):
    #    encrypted_string = base64.b64encode(cipher.encrypt(string))
    #    return encrypted_string

    #def decrypt(self,string):
    #    decrypted_string = cipher.decrypt(base64.b64decode(string))
    #    return decrypted_string

    def __repr__(self):
        return("%s,%s,%s"%(self.getUsername(),self.getPass(),self.getPermis()))


class SMSG(Request):
    def __init__(self, Username, Recipient, Message):
        Request.__init__(self,Username,"SMSG")
        self.Recipient = Recipient
        self.Message = Message

    def encode(self):
        sendStr = "SMSG|"
        sendStr +=  self.addchar(self.getUsername()) +"|" + self.addchar(self.getRecipient()) + "|" + self.addchar(self.getMessage()) + "?"
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
                    self.Recipient = stream_item
                    stream_item = ""
                    writes=writes+1
                elif writes == 2:
                    self.Message = stream_item
                    stream_item = ""
                    writes=writes+1
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1
#    def encrypt(self,string):
#        encrypted_string = base64.b64encode(cipher.encrypt(string))
#        return encrypted_string

#    def decrypt(self,string):
#        decrypted_string = cipher.decrypt(base64.b64decode(string))
#        return decrypted_string

    def getRecipient(self):
        return self.Recipient

    def getMessage(self):
        return self.Message

    def __repr__(self):
        return("%s,%s,%s"%(self.username,self.Recipient,self.Message))

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
        lenall = str(len(messages))
        sendstr = "RMSG|"
        beg = sendstr + lenall
        for m in messages:
            sm = m.split(",")
            for s in sm:
                beg += "|" + self.addchar(str(s))
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

class DMSG(Request):

    def __init__(self,Username,Recipient,Message):
            Request.__init__(self,Recipient,"DMSG")
            self.Recipient = Username
            self.Message = Message

    def encode(self):
        return "DMSG|" + self.addchar(self.getUsername()) + "|" + self.addchar(self.getRecipient()) + "|" + self.addchar(self.getMessage()) + "?"

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
        return "CMSG|" + self.addchar(self.getUsername()) + "?"
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
                if stream[c] == "?":
                    return
            else:
                stream_item += stream[c]
            c=c+1
    #def encrypt(self,string):
    #    encrypted_string = base64.b64encode(cipher.encrypt(string))
    #    return encrypted_string

    #def decrypt(self,string):
    #    decrypted_string = cipher.decrypt(base64.b64decode(string))
    #    return decrypted_string

    def __repr__(self):
        return("%s"%(self.getUsername()))
