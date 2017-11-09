import socket
import sys
import select
from Session import *
from Requests import *
from Database import *
from Crypt import *
from errHandle import *
import time

ADDRESS_OF_CLIENT = '127.0.0.1'

class Server:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.db = Database()
        self.e = errHandle()

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

    def sendAll(self,reqstr,connection,buffsize):
        cry = Crypt()
        req = cry.encryptit(reqstr)
        connection.send((len(req)).to_bytes(4,'little'))
        connection.send(req)

    def recieveAll(self,connection,buffsize):
        retdata = ""
        cry = Crypt()
        data = bytearray()
        packetsize = connection.recv(4)
        if int.from_bytes(packetsize,'little') == 0:
            return None
        while sys.getsizeof(data) < int.from_bytes(packetsize,'little'):
            read_sockets, write_sockets, error_sockets = select.select([connection], [], [], 4)
            if connection in read_sockets:
                data.extend(connection.recv(self.getBUFFER_SIZE()))
            else:
                return "TMOT"
        retdata = cry.decryptit(bytes(data)).decode()
        return retdata

    def handleReq(self, data, session):
        ret = "nothing to see here"

        if(data[0:4] == "LOGN"):
            lg = LOGN(None, None)
            lg.decode(data)
            if(session.loginAttempt(lg)):
                ret = ("logged in successfully?")
            else:
                ret = ("Not a valid login?")
            return(ret)

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
            cm.decode(data)
            if(session.check(cm)):
                messages = []
                messages, error = self.db.read(str(cm.getUsername()))
                ret = self.e.read_err(error)
                if(error == 0):
                    rm = RMSG(None, None)
                    ret = rm.encode(messages)
            return(ret)

        elif data[0:4]=="DMSG":
            dobj = DMSG(None, None, None)
            dobj.decode(data)
            print(dobj)
            if(session.check(dobj)):
                error = self.db.delete(dobj.getUsername(), str(dobj))
                ret = self.e.delete_err(error)
            return(ret)

        elif data[0:4]=="SMSG":
            sobj = SMSG(None, None, None)
            sobj.decode(data)
            if(self.db.checkexistance("./data/permissionMatrix.txt", sobj.getRecipient())):
                if(session.check(sobj)):
                    error = self.db.write(sobj.getRecipient(), str(sobj))
                    ret = self.e.send_err(error)
                    return(ret)
                else:
                    ret = "Session Validation error?"
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

    def run(self):
        print("listening...")
        connected_clients = []
        sessions = []
        while True:

            attempts_to_connect, wlist, xlist = select.select([self.getSocket()],[], [], 0.05)

            for connections in attempts_to_connect:
                conn, addr = self.getSocket().accept()
                s = Session(conn)
                sessions.append(s)
                connected_clients.append(s.conn)

                print('Connection address:', addr)

            clients_allowed = []
            try:
                clients_allowed, wlist, xlist = select.select(connected_clients,[], [], 0.05)
            except select.error:
                pass

            else:

                for s in sessions:
                    if s.conn in clients_allowed:
                        data = self.recieveAll(s.conn,self.getBUFFER_SIZE())
                        if data:
                            cry = Crypt()
                            ret_data = self.handleReq(data, s)
                            self.sendAll(ret_data,s.conn,self.getBUFFER_SIZE())
                        else:
                            print(s.conn.getsockname(), "disconnected")
                            connected_clients.remove(s.conn)

if __name__ == "__main__":
    s = Server(ADDRESS_OF_CLIENT,5005,1024)
    s.run()
