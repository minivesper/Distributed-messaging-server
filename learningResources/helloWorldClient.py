import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello World!"

#this creates a new socket on this terminal for connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#client attempts to connect to socket at TCP_IP and TCP_PORT
s.connect((TCP_IP, TCP_PORT))

#Wether or not connection is accepted, attempts to send MESSAGE to the server.
s.sendto(MESSAGE.encode(),(TCP_IP, TCP_PORT))

#Server stuff happens here. Then this socket attempts to grab data from the server.
data = s.recv(BUFFER_SIZE)

# closes current socket and connection to server
s.close()

print("received data:", data)
