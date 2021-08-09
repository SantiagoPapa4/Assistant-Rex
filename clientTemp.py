import json
from os import PRIO_PGRP
import socket
import pickle
from uuid import getnode as get_mac

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect(("0.0.0.0", 1404))

def getmac(interface):

  try:
    mac = open('/sys/class/net/'+interface+'/address').readline()
  except:
    mac = "00:00:00:00:00:00"

  return mac[0:17]

Sender = getmac("wlp2s0")

def sendPack(target, Type, data):
    global serverSocket
    global Sender
    packet = {"target": Sender , "sender":Sender, "type": Type ,"data":data}
    serverSocket.sendall(bytes(json.dumps(packet),encoding="utf-8"))

Logged = False
sendPack(Sender, "login" ,"s3rwpw8r9")
reply = json.loads(serverSocket.recv(4096).decode("utf-8"))

if reply["type"] == "ack" and reply["data"] == "s3rwpw8r9":
  Logged = True
  print("Logged into the server!")

def communicate(msg):
  if not Logged:
    return "Sorry, you must first login."
  if msg == "" or msg == None:
    return ""
  global serverSocket
  global Sender
  type = "echo"
  sendPack(Sender, type ,msg)

  acked = False
  while not acked:
    answer = json.loads(serverSocket.recv(4096).decode("utf-8"))
    if answer["type"] == "ack" and answer["data"] == msg:
      print("Server received data without loss.")
      acked = True
    elif answer["type"] == "ack" and answer["data"] != msg:
      sendPack(Sender, type ,msg)
  if acked:
    answer = json.loads(serverSocket.recv(4096).decode("utf-8"))
    if answer["type"] == "echo":
      return (answer["data"])


