import socket
import sys
import select
from Requests import *
from Database import *

class Server:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        HOST = None
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.db = Database()
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

    def handleReq(self, data):
        data = data.decode()
        if(data[0:4] == "LOGN"):
            lg = LOGN(None, None, None)
            lg.decode(data)
            print("lg", lg)
            if(lg.getPermis() == "2"):
                print("I am here")
                ver, err = self.db.verify("./data/adminlogin.txt", lg.getUsername(), lg.getPass(), lg.getPermis())
                if(ver):
                    ret = ("logged in successfully.")
                else:
                    ret = ("not verified")
                return(ret)
            elif(lg.getPermis()=="3"):
                ver, err = self.db.verify("./data/masteradmin.txt", lg.getUsername(), lg.getPass(), lg.getPermis())
                if(ver):
                    ret = (" logged in successfully.")
                else:
                    ret = ("not verified")
                return(ret)
            else:
                ver, err = self.db.verify("./data/logindata.txt", lg.getUsername(), lg.getPass(), lg.getPermis())
                if(ver):
                    ret = (" logged in successfully.")
                else:
                    ret = ("not verified")
                return(ret)

        elif data[0:4] == "CACM":
            ca = CACM(None, None, None, None)
            ca.decode(data)
            print(ca)
            if ca.getPermis() == "2":
                error = self.db.checkDuplicate("./data/adminlogin.txt", ca.getUsername())
                if error == 0:
                    admin = self.db.getAdmin("./data/masteradmin.txt")
                    data = data.replace("CACM", "AAPR")
                    data += "|" + admin
                    aa = AAPR(None,None,None,None,None)
                    aa.decode(data)
                    error3 = self.db.write("./data/approvalreq.txt", str(aa))
                    error2 = self.db.write("./data/adminlogin.txt", str(ca))
                    if error2 == 0:
                        ret = ("Account created, waiting on approval")
                    elif error2 == 1:
                        ret = "Error in sending message"
                    elif error2 == 2:
                        ret = "File does not exist"
                    elif error == 3:
                        ret = ("username already exists, please enter a new username")
                return(ret)
            else:
                error = self.db.checkDuplicate("./data/logindata.txt", ca.getUsername())
                if error == 0:
                    error2 = self.db.write("./data/logindata.txt", str(ca))
                    if error2 == 0:
                        ret = ("Account created successfully")
                    elif error2 == 1:
                        ret = "Error in sending message"
                    elif error2 == 2:
                        ret = "File does not exist"
                elif error == 1:
                    ret = ("could not read messages")
                elif error == 2:
                    ret = ("could not open file")
                elif error == 3:
                    ret = ("username already exists, please enter a new username")
            return(ret)

        elif(data[0:4] == "CAPR"):
            cm = CAPR(None)
            cm.decode(data)
            messages = []
            messages, error = self.db.readappr("./data/approvalreq.txt", str(cm))
            rm = RMSG(None, None)
            a = rm.encode(messages)
            if error == 0:
                ret = a
            return(ret)

        elif(data[0:4] == "CMSG"):
            cm = CMSG(None)
            cm.decode(data)
            messages = []
            messages, error = self.db.read("./data/messages.txt", str(cm))
            rm = RMSG(None, None)
            a = rm.encode(messages)
            print(a)
            if error == 0:
                ret = a

            #sm = RMSG(user) //create a recieve message object to send all the stored recpiants messages from server to client
            #parse through the database txt and return all messages with matching recipiant
            return(ret)

        elif data[0:4]=="SMSG":
            #create an empty SMSG object to use our decode function to fill in fields
            sobj = SMSG(None, None, None)
            sobj.decode(data)
            error = self.db.write("./data/messages.txt", str(sobj))
            if error == 0:
                ret = "Message sent successfully"
            elif error == 1:
                ret = "Error in sending message"
            elif error == 2:
                ret = "File does not exist"
        return(ret)


    def run(self):
        print("listening...")
        connected_clients = []
        while True:
            attempts_to_connect, wlist, xlist = select.select([self.getSocket()],[], [], 0.05)

            for connections in attempts_to_connect:
                conn, addr = self.getSocket().accept()
                connected_clients.append(conn)
                print('Connection address:', addr)

            clients_allowed = []
            try:
                clients_allowed, wlist, xlist = select.select(connected_clients,[], [], 0.05)
            except select.error:
                pass

            else:
                for conn in clients_allowed:
                    data = conn.recv(self.getBUFFER_SIZE())
                    if data:
                        ret_data = self.handleReq(data)
                        conn.send(ret_data.encode())
                    else:
                        print(conn.getsockname(), "disconnected")
                        connected_clients.remove(conn)

if __name__ == "__main__":
    s = Server('127.0.0.1',5005,1024)
    s.run()
