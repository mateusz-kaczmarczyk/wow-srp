# WIRESHARK FILTER: wow || ip.addr == 188.138.40.87 || ip.addr == 54.36.105.148

from Functions import *

def authLogonChallengePacket():
  packet = hex_to_bytes("00082a00576f57000303053430363878006e69570053556e653c000000c0a819730c574f4f44434855434b474731")
  return packet

def authLogonProofPacket(A, M1, CRC):
  packet = bytes(b'\01')
  packet += int_to_bytes(A)
  packet += M1
  packet += CRC
  packet += bytes(b'\00')
  packet += bytes(b'\00')
  return packet

def realmListPacket():
  packet = hex_to_bytes('1000000000')
  return packet

class AuthLogonChallenge:
  def __init__(self, data):
    B_bytes = data[3:35]
    g_bytes = data[36:37]
    N_bytes = data[38:70]
    s_bytes = data[70:102]
    self.B = bytes_to_int(B_bytes)
    self.g = bytes_to_int(g_bytes)
    self.N = bytes_to_int(N_bytes)
    self.s = bytes_to_int(s_bytes)

class AuthLogonProof:
  def __init__(self, data):
    self.e = data[1]

class RealmList:
  def __init__(self, data):
    blackrock_bytes = data[33:51]
    icecrown_bytes = data[71:89]
    lordaeron_bytes = data[110:128]
    blackrock = blackrock_bytes.decode('utf-8')
    icecrown = icecrown_bytes.decode('utf-8')
    lordaeron = lordaeron_bytes.decode('utf-8')
    self.blackrockHost = blackrock.split(':')[0]
    self.blackrockPort = int(blackrock.split(':')[1])
    self.icecrownHost = icecrown.split(':')[0]
    self.icecrownPort = int(icecrown.split(':')[1])
    self.lordaeronkHost = lordaeron.split(':')[0]
    self.lordaeronPort = int(lordaeron.split(':')[1])

class Default:
  def __init__(self, data):
    print(bytes_to_hex(data))