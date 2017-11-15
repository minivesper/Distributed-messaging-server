import socket
import sys
import fileinput
import os
import select
from Session import *
from Requests import *
from Database import *
from Crypt import *
from errHandle import *
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import MD5
from datetime import datetime, timedelta
import time

ADDRESS_OF_CLIENT = '127.0.0.1'

class Server:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.db = Database()
        self.e = errHandle()
        self.active_users = []

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket = s
        except socket.error as msg:
            s = None
            self.socket = None
            print("could not create socket %s"%(msg))
        try:
            s.bind((self.TCP_IP, self.TCP_PORT))
            self.socket.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            self.socket = None
            print("could not bind or listen %s"%(msg))

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getSocket(self):
        return self.socket

    def sendAll(self,sig,reqstr,connection,buffsize):
        req = reqstr.encode('utf-8')
        if not sig:
            connection.send((1).to_bytes(4,'little'))
            connection.send((len(req)).to_bytes(4,'little'))
            connection.send(req)
        else:
            connection.send((0).to_bytes(4,'little'))
            connection.send((len(req)).to_bytes(4,'little'))
            connection.send(req)
            connection.send((len(sig)).to_bytes(4,'little'))
            connection.send(sig)

    def recieveAll(self,connection,buffsize):
        retdata = ""
        data = bytearray()
        packettype = int.from_bytes(connection.recv(4), 'little')
        if packettype == 1:
            packetsize = int.from_bytes(connection.recv(4),'little')
            while packetsize > 0:
                read_sockets, write_sockets, error_sockets = select.select([connection], [], [], 4)
                if connection in read_sockets:
                    if(packetsize > 1024):
                        singlerec = connection.recv(self.getBUFFER_SIZE())
                    else:
                        singlerec = connection.recv(packetsize)
                        packetsize -= sys.getsizeof(singlerec)
                    data.extend(singlerec)
                else:
                    return "timeout"
            return None,data.decode()

        elif packettype == 0:
            ret = []
            for i in range(2):
                retdata = ""
                data = bytearray()
                packetsize = int.from_bytes(connection.recv(4),'little')
                while packetsize > 0:
                    read_sockets, write_sockets, error_sockets = select.select([connection], [], [], 4)
                    if connection in read_sockets:
                        if(packetsize > 1024):
                            singlerec = connection.recv(self.getBUFFER_SIZE())
                        else:
                            singlerec = connection.recv(packetsize)
                            packetsize -= sys.getsizeof(singlerec)
                        data.extend(singlerec)
                    else:
                        return "timeout"
                ret.append(data)
            print(ret)
            return (ret[1].decode(),''),ret[0].decode()



    def handleReq(self, data, session):
        ret = "nothing to see here"
        if(data[0:4] == "LOGN"):
            lg = LOGN(None, None)
            lg.decode(data)
            if(session.datecheck(lg.getTime())):
                if(session.loginAttempt(lg)):
                    if lg.getUsername() not in self.active_users:
                        self.active_users.append(lg.getUsername())
                        print("Logged in successfully") #print statements to show if middleman succeeds
                        ret = ("logged in successfully")
                    else:
                        ret = ("Already logged in byeeee")
                else:
                    ret = ("Not a valid login?")
                return(ret)
            else:
                print("Timed out") #print statement to show middle man cannot access user's account
                ret = "Timed Out"
                return ret

        elif data[0:4] == "PUBK":
            pk = PUBK(None, None)
            pk.decode(data)
            self.db.write(pk) #saves user's public key
            server_pkey = self.db.readserver() #reads server key
            pks = PUBK(None, None) #create new PUBK request object to send back to the client

            #decode that part of data with its public key
            #send whatever server got back to client to verify the signature
        elif data[0:4] =="VERF":
            vf = VERF(None,None)
            vf.decode(data)
            verobj = vf.getverobj()

        elif data[0:4] == "TMOT":
            ret = "you timed out ya fool"

        elif data[0:4] == "CACM":
            ca = CACM(None, None, None)
            ca.decode(data)
            error = self.db.checkDuplicate("./data/logindata.txt", ca.getUsername())
            ret = self.e.duplicate_err(error)
            if error == 0:
                error2 = self.db.write("logindata", str(ca))
                ret = self.e.send_err(error2) #right now if 0, ret will be "message sent successfully". Not just "wrote user"
                if error2 == 0:
                    if ca.getPermis() == "2":
                        print("the user has permissions #2")
                        error3 = self.db.getAdmin("./data/logindata.txt")
                        ret = self.e.admin_err(error3)
                        print(error3)
                        if error3:
                            wperm = str(ca.getUsername()) + ",1,1,1,1,0,0,1"
                            error4 = self.db.write("permissionMatrix", str(wperm))
                            ret = self.e.send_err(error4) #again might want new function to send different message string about permissions
                            if error4 == 0:
                                for a in error3: #error3 should be a list of all admins
                                    data = ca.getUsername() + "," + a +"," + "requesting permissions %s"%ca.getPermis()
                                    error5 = self.db.write(a, data)
                                    ret = self.e.send_err(error5) #again might want to new function to print differnt string about admin (like sent message to admin instead of successfully sent)
                                return (ret)
                            return(ret)
                    else:
                        ca = str(ca.getUsername()) + ",1,1,1,1,0,0,1"
                        error7 = self.db.write("permissionMatrix", str(ca))
                        ret = self.e.send_err(error7) #again change string print out?
                        return (ret)
                return (ret)
            return(ret)

        elif(data[0:4] == "CMSG"):
            cm = CMSG(None)
            if data[6] == None:
                ret = "No messages"
            cm.decode(data)
            if(session.datecheck(cm.getTime())):
                if(session.check(cm)):
                    messages = []
                    messages, error = self.db.read(str(cm.getUsername()))
                    ret = self.e.read_err(error)
                    if(error == 0):
                        rm = RMSG(None, None)
                        ret = rm.encode(messages)
            else:
                print("Timed out") #print statement to show middle man cannot access user's account
                ret = "Timed Out"
            return(ret)

        elif data[0:4]=="DMSG":
            dobj = DMSG(None, None, None)
            dobj.decode(data)
            if(session.datecheck(dobj.getTime())):
                if(session.check(dobj)):
                    error = self.db.delete(dobj.getUsername(), str(dobj))
                    ret = self.e.delete_err(error)
            else:
                print("Timed out") #print statement to show middle man cannot access user's account
                ret = "Timed Out"
            return(ret)

        elif data[0:4]=="SMSG":
            sobj = SMSG(None, None, None)
            sobj.decode(data)
            if(self.db.checkexistance("./data/permissionMatrix.txt", sobj.getRecipient())):
                if(session.datecheck(sobj.getTime())):
                    if(session.check(sobj)):
                        error = self.db.write(sobj.getRecipient(), str(sobj))
                        ret = self.e.send_err(error)
                        return(ret)
                        print("message sent")
                    else:
                        ret = "Session Validation error?"
                        return ret
                else:
                    ret = "Timed out"
                    return ret
            else:
                ret = sobj.getRecipient() + " is not a valid account?"

        elif data[0:4]=="UPDT":
            uobj = UPDT(None, None, None, None)
            uobj.decode(data)
            if(self.db.checkexistance("./data/permissionMatrix.txt", uobj.getouser())):
                if(session.check(uobj)):
                    error = self.db.updateUser("./data/permissionMatrix.txt", uobj.getUsername(), uobj.getouser(), uobj.getTag(), uobj.getPerm())
                    ret = self.e.update_err(error)
                    return ret
                else:
                    ret = "Session Validation Error?"
                    return ret
            else:
                ret = uobj.getouser() + "is not a valid account?"
        return(ret)

    def saveKey(self, paths):
        #after recieving a public key save it in "data/serverkeys/username.txt"
        return

    def loadKey(self, paths):
        if(os.path.exist(paths) and os.stat(paths).st_size != 0):
            f = open(paths)
            keypair = RSA.importKey(f.read())
            return keypair
        else:
            ncry = GenKeys(1024)
            print("generated new keypair")
            keypair = ncry.my_keypair.exportKey('PEM')
            self.db.writek('serverkeys/server', keypairw)
            pubkey = ccry.my_pubkey.exportKey('PEM')
            self.db.writek('clientkeys/server', pubkeyw)
            return keypair

    def run(self):
        path = "data/serverkeys/server.txt"
        print("listening...")
        connected_clients = []
        sessions = []

        counter = 0
        while True:
            attempts_to_connect, wlist, xlist = select.select([self.getSocket()],[], [], 0.05)

            for connections in attempts_to_connect:
                conn, addr = self.getSocket().accept()
                s = Session(conn)
                sessions.append(s)
                connected_clients.append(s.conn)
                #swap public keys
                print('Connection address:', addr)

            clients_allowed = []
            try:
                clients_allowed, wlist, xlist = select.select(connected_clients,[], [], 0.05)
            except select.error:
                pass

            else:

                for s in sessions:
                    if s.conn in clients_allowed:
                        sig, data = self.recieveAll(s.conn,self.getBUFFER_SIZE())
                        if data:
                            #keypair = loadKey(path)
                            #cry = Crypt(keypair)
                            #data = cry.decryptit(data)
                            cry = FernetCrypt()
                            ret_data = self.handleReq(data, s)
                            self.sendAll(None,ret_data,s.conn,self.getBUFFER_SIZE())
                        else:
                            print(s.conn.getsockname(), "disconnected")
                            if s.getUsername() in self.active_users:
                                self.active_users.remove(s.getUsername())
                            connected_clients.remove(s.conn)
                            sessions.remove(s)


if __name__ == "__main__":
    s = Server(ADDRESS_OF_CLIENT,5005,1024)
    s.run()
