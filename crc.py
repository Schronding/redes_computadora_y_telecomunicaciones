M_str = "1101011011"
G_str = "10011"

def calcular_crc(msg_str, gen_str):

    msg = [int(bit) for bit in msg_str]
    gen = [int(bit) for bit in gen_str]
    
    k = len(gen)
    padding_len = k - 1
    
    dividend = msg + [0] * padding_len
    
    for i in range(len(msg)):
        
        if dividend[i] == 1:
            for j in range(k):
                dividend[i+j] = (dividend[i+j] + gen[j]) % 2
        
        remainder = dividend[-(padding_len):]
    
    remainder_str = "".join(map(str, remainder))
    
    return remainder_str


crc_remainder = calcular_crc(M_str, G_str)
trama_transmitida = M_str + crc_remainder

print(f"Mensaje Original (M):     {M_str}")
print(f"Polinomio Generador (G):  {G_str}")
print(f"Residuo CRC (R):          {crc_remainder}")
print(f"Trama Transmitida (M + R):  {trama_transmitida}")