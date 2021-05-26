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
    Input = input('Say Something: ')
    if (Input == 'stop'):
        ClientSocket.close()
        break
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    if(Response and (Response.decode('utf-8')!="ack" or Response.decode('utf-8')!="ackack")):
        print(Response.decode('utf-8'))

ClientSocket.close()