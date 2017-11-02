import socket
import sys
import select
from Session import *
from Requests import *
from Database import *
from errHandle import *

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

    def handleReq(self, data, session):
        data = data.decode()
        ret = "nothing to see here"

        if(data[0:4] == "LOGN"):
            lg = LOGN(None, None)
            lg.decode(data)
            if(session.loginAttempt(lg)):
                ret = ("logged in successfully")
            else:
                ret = ("Not a valid login")
            return(ret)

        elif data[0:4] == "CACM":
            ca = CACM(None, None, None)
            ca.decode(data)
            error = self.db.checkDuplicate("./data/logindata.txt", ca.getUsername())
            if error == 0:
                ret =("Account created successfully")
                error2 = self.db.write("logindata", str(ca))
                if error2 == 0:
                    if ca.getPermis() == "2":
                        admin = self.db.getAdmin("./data/logindata.txt")
                        if admin == 1:
                            ret = "could not read file to get admin"
                        if admin ==2:
                            ret = "could not open file"
                        else:
                            caf = str(ca.getUsername()) + ",1,1,1,1,0,0,1"
                            perror = self.db.write("permissionMatrix", str(caf))
                            if perror == 1:
                                ret = "can't write to permissions"
                            elif perror == 2:
                                ret = "could not open permissions file"
                            elif perror == 3:
                                ret = "permission file full"
                            elif perror == 0:
                                for a in admin:
                                    data = ca.getUsername() + "," + a +"," + "requesting permissions %s"%ca.getPermis()
                                    error = self.db.write(a, data)
                                    if error == 0:
                                        ret = "Message sent to admin"
                                    elif error == 1:
                                        ret = "Error in sending message to admin"
                                    elif error == 2:
                                        ret = "File does not exist"
                                    elif error == 3:
                                        ret = "Admin's userbox is full"
                                return (ret)
                            return(ret)
                    else:
                        ca = str(ca.getUsername()) + ",1,1,1,1,0,0,1"
                        error3 = self.db.write("permissionMatrix", str(ca))
                        if error3 == 0:
                            ret = ("Account created successfully created")
                        elif error3 == 1:
                            ret = "Error in writing permissions message"
                        elif error3 == 2:
                            ret = "File does not exist"
                        elif error3 == 3:
                            ret = ("permission matrix is full")
                        return (ret)
                elif error2 == 1:
                    ret = "Error in sending message to admin"
                elif error2 == 2:
                    ret = "File does not exist"
                elif error2 == 3:
                    ret = "Admin's userbox is full"
                return (ret)
            elif error == 1:
                ret = ("Error in sending message")
            elif error == 2:
                ret = "File does not exist"
            elif error == 3:
                ret = ("username already exists, please enter a new username")
                print("ret",ret)
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
                    ret = "Session Validation error"
                    return ret
            else:
                ret = sobj.getRecipient() + "is not a valid account"

        elif data[0:4]=="UPDT":
            uobj = UPDT(None, None, None, None)
            uobj.decode(data)
            if(self.db.checkexistance("./data/permissionMatrix.txt", uobj.getouser())):
                if(session.check(uobj)):
                    error = self.db.updateUser("./data/permissionMatrix.txt", uobj.getUsername(), uobj.getouser(), uobj.getTag(), uobj.getPerm())
                    ret = self.e.update_err(error)
                    return ret
                else:
                    ret = "Session Validation Error"
                    return ret
            else:
                ret = uobj.getouser() + "is not a valid account"
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
                        data = s.conn.recv(self.getBUFFER_SIZE())
                        if data:
                            ret_data = self.handleReq(data, s)
                            s.conn.send(ret_data.encode())
                        else:
                            print(s.conn.getsockname(), "disconnected")
                            connected_clients.remove(s.conn)

if __name__ == "__main__":
    s = Server(ADDRESS_OF_CLIENT,5005,1024)
    s.run()
