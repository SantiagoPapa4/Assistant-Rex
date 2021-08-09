import json
from os import CLD_TRAPPED
import socket
import threading
import sqlite3

import responseAI

def getmac(interface):

  try:
    mac = open('/sys/class/net/'+interface+'/address').readline()
  except:
    mac = "00:00:00:00:00:00"

  return mac[0:17]

#### Credentials
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = ("0.0.0.0", 1404)
serverSocket.bind(serverAddress)
serverSocket.listen()
Sender = getmac("wlp2s0")
clients = []
#### Credentials

def analyzePacket(pack):
  if pack["type"] == "msg":
    print ("{} sent:  {}".format(pack["sender"], pack["data"]))
  if pack["type"] == "echo":
    return(responseAI.chat(pack["data"]))

def craftPack(target, Type, data):
    global serverSocket
    global Sender
    packet = {"target": Sender , "sender":Sender, "type": Type ,"data":data}
    return bytes(json.dumps(packet),encoding="utf-8")

def manageClient():
    global clients
    index = len(clients)-1
    while True:
        dataa = clients[index][0].recv(4096).decode("utf-8")
        data = json.loads(dataa)
        print(data)
        clients[index][0].sendall(craftPack(data["sender"], "ack", data["data"]))
        clients[index][0].sendall(craftPack(data["sender"], "echo", analyzePacket(data)))
    
def login(pack, sock):
    if pack["type"] == "login" and pack["data"] == "s3rwpw8r9":
        return pack["sender"]

print("Listening on: {}".format(serverAddress)) 
while True:
    clientSock, clientAddress = serverSocket.accept()
    data = clientSock.recv(4096).decode("utf-8")
    print(data)
    data = json.loads(data)
    mac = login(data, clientSock)
    if mac != False:
        clients.append((clientSock, clientAddress, mac))
        clientSock.sendall(craftPack(data["sender"], "ack", data["data"]))
        manageThread = threading.Thread(target=manageClient())
        manageThread.start()
