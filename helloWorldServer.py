import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

#this creates a new socket on this terminal for connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#sets the new socket to be associated with the ip and port. essentially gives the socket an identity?
s.bind((TCP_IP, TCP_PORT))

#sets the socket to listen for connection requests. the parameter sets how many requests can line up to connect to this socket.
s.listen(1)

#automatically accepts a connection and stores
#conn: a new socket object that indicates a session between the server and the client. This socket is where communication between the two will pass through
#addr: the ip of the connected client
conn, addr = s.accept()
print('Connection address:', addr)
while 1:
  #stores the data sent by the connection socket. max size of data is BUFFER_SIZE
  data = conn.recv(BUFFER_SIZE)
  if not data: break
  print("received data:", data)

  #Sends identical data back to connected client.
  conn.send(data)
#conn socket gets closed and deleted
conn.close()
