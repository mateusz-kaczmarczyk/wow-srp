from socket import *
from Functions import *
from Connection import *
from Packets import *
import time

# WARMANE AUTH SERVER HOST: 188.138.40.87  
# WARMANE AUTH SERVER PORT: 3724

class Client:
  def __init__(self, login, password, authServerHost, authServerPort):
    self.k = 3
    self.I = login
    self.P = password
    self.a = random_N_bytes(32)
    self.authServerConnection = Connection(authServerHost, authServerPort)

  def authChallengeHandler(self):
    packet = authLogonChallengePacket()
    self.authServerConnection.sendData(packet)
    logonChallenge = self.authServerConnection.receiveData(AuthLogonChallenge)
    self.B = logonChallenge.B
    self.g = logonChallenge.g
    self.N = logonChallenge.N
    self.s = logonChallenge.s

  def authLogonProofHandler(self):
    self.A = calculate_A(self.g, self.a, self.N)
    self.x = calculate_x(self.s, self.I, self.P)
    self.u = calculate_u(self.A, self.B)
    self.S = calculate_SC(self.B, self.k, self.g, self.x, self.N, self.a, self.u)
    self.K = calculate_K(self.S)
    self.M1 = calculate_M1(self.g, self.N, self.I, self.s, self.A, self.B, self.K)
    self.CRC = H(random_N_bytes(32))
    packet = authLogonProofPacket(self.A, self.M1, self.CRC)
    self.authServerConnection.sendData(packet)
    authLogonProof = self.authServerConnection.receiveData(AuthLogonProof)
    return authLogonProof.e

  def realmListHandler(self):
    packet = realmListPacket()
    self.authServerConnection.sendData(packet)
    self.realmList = self.authServerConnection.receiveData(RealmList)
    self.authServerConnection.close()

  def connectToGameServer(self):
    self.gameServerConnection = Connection(self.realmList.icecrownHost, self.realmList.icecrownPort)
    self.gameServerConnection.receiveData(Default)
    self.gameServerConnection.close()
