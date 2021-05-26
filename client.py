import socket
import time

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1234

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
lock = False;
while True:
    time.sleep(1)
    ClientSocket.sendall(str.encode("heartbeat"))
    Response = ClientSocket.recv(1024)
    if(Response and Response.decode('utf-8')!="ack"):
        print(Response.decode('utf-8'))
ClientSocket.close()