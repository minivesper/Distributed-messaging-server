import socket
import sys
import select
from Session import *
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

    def handleReq(self, data, session):
        data = data.decode()
        ret = "no data"
        if(data[0:4] == "LOGN"):
            lg = LOGN(None, None)
            lg.decode(data)
            ver = session.loginAttempt(lg)
            #ver, err = self.db.verify("./data/logindata.txt", lg.getUsername(), lg.getPass())
            if(ver):
                ret = (" logged in successfully.")
            else:
                ret = ("not verified")
            return(ret)
        elif(data[0:4] == "CMSG"):
            cm = CMSG(None)
            cm.decode(data)
            if(session.check(cm)):
                messages = []
                messages, error = self.db.read(str(cm))
                rm = RMSG(None, None)
                a = rm.encode(messages)
                if error == 0:
                    ret = a
                elif error == 1:
                    ret = "could not read messages"
                elif error == 2:
                    ret = "could not open file"
            #sm = RMSG(user) //create a recieve message object to send all the stored recpiants messages from server to client
            #parse through the database txt and return all messages with matching recipiant
            return(ret)
        elif data[0:4]=="SMSG":
            #create an empty SMSG object to use our decode function to fill in fields
            sobj = SMSG(None, None, None)
            sobj.decode(data)
            if(session.check(sobj)):
                error = self.db.write(sobj.getRecipient(), str(sobj))
                if error == 0:
                    ret = "Message sent successfully"
                elif error == 1:
                    ret = "Error in sending message"
                elif error == 2:
                    ret = "File does not exist"
                elif error == 3:
                    ret = "This users inbox is full"
            return(ret)
        elif data[0:4]=="DMSG":
            #create an empty SMSG object to use our decode function to fill in fields
            dobj = DMSG(None, None, None)
            dobj.decode(data)
            if(session.check(dobj)):
                error = self.db.delete(dobj.getUsername(), str(dobj))
                if error == 0:
                    ret = "Message sent successfully"
                elif error == 1:
                    ret = "Error in deleting message"
                elif error == 2:
                    ret = "File does not exist"
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
                connected_clients.append(conn)

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
    s = Server('127.0.0.1',5005,1024)
    s.run()
