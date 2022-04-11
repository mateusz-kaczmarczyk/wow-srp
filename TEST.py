from Functions import *

##############################################################################################
I = 'LOGIN'
P = 'HASLO'
k = 3
g = 7
N = hex_to_int('b79b3e2a87823cab8f5ebfbf8eb10108535006298b5badbd5b53e1895e644b89') # Warmane N
s = random_N_bytes(32)
##############################################################################################

x = calculate_x(s, I, P)
v = calculate_v(g, x, N)

a = random_N_bytes(32)
A = calculate_A(g, a, N)

b = random_N_bytes(19)
B = calculate_B(g, b, N, k, v)

u = calculate_u(A, B)

SC = calculate_SC(B, k, g, x, N, a, u)
KC = calculate_K(SC)

SS = calculate_SS(A, v, u, N, b)
KS = calculate_K(SS)

M1c = calculate_M1(g, N, I, s, A, B, KC)
M1s = calculate_M1(g, N, I, s, A, B, KS)
M2 = calculate_M2(A, M1c, KS)


print('Client session key:\t', int_to_hex(KC))
print('Server session key:\t', int_to_hex(KS))