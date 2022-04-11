import os
import hashlib

def hex_to_bytes(value):
	return bytes.fromhex(value)

def bytes_to_hex(value):
  return value.hex()

def bytes_to_int(value, order = 'little'):
  return int.from_bytes(value, byteorder = order)

def hex_to_int(value, order = 'little'):
  b = hex_to_bytes(value)
  return bytes_to_int(b, order)

def int_to_bytes(value, order = 'little'):
	return value.to_bytes((value.bit_length() + 7) // 8, byteorder=order)
  
def int_to_hex(value):
  b = int_to_bytes(value)
  return bytes_to_hex(b)

def obj_to_bytes(obj, order = 'little'):
  if type(obj) == bytes:
    return obj
  elif type(obj) == bytearray:
    return bytes(obj)
  elif type(obj) == int:
    return int_to_bytes(obj, order)
  elif type(obj) == str:
    return bytes(obj, 'utf-8')
  else:
    raise TypeError

def H(*args):
	hashFunction = hashlib.sha1()
	for i in args:
		hashFunction.update(i if type(i) == bytes else obj_to_bytes(i))
	return hashFunction.digest()

def random_N_bytes(n):
	return bytes_to_int(os.urandom(n))

def calculate_A(g, a, N):
  return pow(g, a, N)

def calculate_x(s, I, P):
  return bytes_to_int(H(s, H(I, ':', P)))

def calculate_v(g, x, N):
  return pow(g, x, N)

def calculate_u(A, B):
  return bytes_to_int(H(A, B))

def calculate_B(g, b, N, k, v):
  return (k * v + pow(g, b, N)) % N

def calculate_SC(B, k, g, x, N, a, u):
  return pow(B - k * pow(g, x, N), a + u * x, N)

def calculate_SS(A, v, u, N, b):
  return pow(A * pow(v, u, N), b, N)

def calculate_K(S):
  return interleave(S)

def calculate_M1(g, N, I, s, A, B, K):
  xor = bytes(a ^ b for (a, b) in zip(H(N), H(g)))
  M1 = H(xor, H(I), s, A, B, K)
  return M1

def calculate_M2(A, M1, KS):
  return H(A, M1, KS)

def interleave(S):
  S_bytes = int_to_bytes(S)
  while S_bytes[0] == 0:
    S_bytes = S_bytes[1:]
  if len(S_bytes) % 2 == 1:
    S_bytes = bytes(S_bytes[1:])
  E = bytearray()
  F = bytearray()
  K = bytearray()
  length = len(S_bytes)
  for i in range(length):
    if i % 2 == 0:
      E += int_to_bytes(S_bytes[i])
    else:
      F += int_to_bytes(S_bytes[i])
  HE = H(E)
  HF = H(F)
  for i in range(20):
    K += int_to_bytes(HE[i])
    K += int_to_bytes(HF[i])
  return bytes_to_int(bytes(K))