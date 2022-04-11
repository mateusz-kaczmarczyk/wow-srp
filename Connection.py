from socket import *

class Connection:
  def __init__(self, host, port):
    self.socket = socket(AF_INET,SOCK_STREAM)
    self.socket.connect((host, port))

  def sendData(self, packet):
    self.socket.send(packet)

  def receiveData(self, packetType):
    data = self.socket.recv(1024)
    return packetType(data)

  def close(self):
    self.socket.close()