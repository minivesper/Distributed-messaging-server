import socket

class Client:
    def __init__(self,TCP_IP,TCP_PORT,BUFFER_SIZE):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = BUFFER_SIZE
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s
        s.connect((self.TCP_IP, self.TCP_PORT))

    def getTCP_IP(self):
        return self.TCP_IP

    def getTCP_PORT(self):
        return self.TCP_PORT

    def getBUFFER_SIZE(self):
        return self.BUFFER_SIZE

    def getSocket(self):
        return self.socket

    def handleCommand(self, inp_str):
        self.getSocket().sendto(inp_str.encode('utf-8'),(self.getTCP_IP(), self.getTCP_PORT()))
        data = self.getSocket().recv(self.getBUFFER_SIZE())
        print(data.decode())

    def run(self):
        while True:
            inp = input("enter Command: ")
            self.handleCommand(inp)

# TCP_IP = '127.0.0.1'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024
# MESSAGE = "Hello World!"

if __name__ == "__main__":
    c = Client('127.0.0.1',5005,1024)
    c.run()
