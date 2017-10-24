import socket
import sys
import select
from Requests import *

class Server:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        HOST = None
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        print(data, "request recieved")
        ret = "you requested: "
        ret += data
        return(ret)

    def handleSMSG(self, data):
        data = data.decode()
        if data[0:4]=="SMSG":
            #create an empty SMSG object to use our decode function to fill in fields
            sobj = SMSG(None, None, None)
            sendmesobj = sobj.decode(data)
            error = db.write("filename", str(sendmesobj))
            if error == 0:
                ret = "Message sent successfully"
            elif error == 1:
                ret = "Error in sending message"
            elif error == 2:
                ret = "File does not exist"
        return(ret)


    def run(self):
        print("listening...")
        conn, addr = self.getSocket().accept()

        print('Connection address:', addr)
        while 1:
          #stores the data sent by the connection socket. max size of data is BUFFER_SIZE
          data = conn.recv(self.getBUFFER_SIZE())
          if data:
              ret_data = self.handleReq(data)
          else:
              break
          #Sends identical data back to connected client.
          conn.send(ret_data.encode())

# TCP_IP = '127.0.0.1'
# TCP_PORT = 5005
# BUFFER_SIZE = 20  # Normally 1024, but we want fast response

if __name__ == "__main__":
    s = Server('127.0.0.1',5005,1024)
    s.run()
