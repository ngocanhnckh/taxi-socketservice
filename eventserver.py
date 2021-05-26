import socket
import os
from _thread import *
import threading

#Server configuration
ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1234
ThreadCount = 0

#Try to start the socket
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

lock = threading.Lock()
gMsg = ""


class clientThread(threading.Thread):
    def __init__(self, connection, killed=False):
        threading.Thread(self)
        

    def run(self):
        self.connection.send(str.encode('You are connected'))
        global gMsg
        msg = gMsg
        try:
            while True:
                if(self.killed):
                    return
                lock.acquire()
                
                if (msg!=gMsg): 
                    msg=gMsg
                    self.connection.sendall(str.encode(msg))
                    print(msg)
                else:
                    self.connection.sendall(str.encode("ack"))
                
                lock.release()
                
                data = self.connection.recv(2048)
                reply = data.decode('utf-8')
            
                if (data and (reply!="heartbeat")):
                    print(reply)
                    lock.acquire()
                    gMsg = reply
                    lock.release()
        except:
            print("One connection died of error")
            self.raise_exception()
            try:
                global ThreadCount
                ThreadCount -= 1
                self.connection.close()
            except:
                print("I hope Mr.Son won't see this error")


    def raise_exception(self):
        self.killed = True




def threaded_client(connection):
    connection.send(str.encode('You are connected'))
    global gMsg
    msg = gMsg
    try:
        while True:
            
            lock.acquire()
            
            if (msg!=gMsg): 
                msg=gMsg
                connection.sendall(str.encode(msg))
                print(msg)
            else:
                connection.sendall(str.encode("ack"))
            
            lock.release()
            
            data = connection.recv(2048)
            reply = data.decode('utf-8')
        
            if (data and (reply!="heartbeat")):
                print(reply)
                lock.acquire()
                gMsg = reply
                lock.release()
    except:
        print("One connection died of error")
        try:
            global ThreadCount
            ThreadCount -= 1
            connection.close()
            return
        except:
            print("I hope Mr.Son won't see this error")
        
    

while True:
    try:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        #t = clientThread((Client,))
        start_new_thread(threaded_client, (Client, ))
        #t.start()
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    except:
        print("error")
ServerSocket.close()