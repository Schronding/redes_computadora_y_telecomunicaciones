M_str = "11010"
G_str = "1011"
length_G = len(G_str)

def codigo_rendundancia_ciclica(G, M):
    result_str = ""
    for index in range(length_G):
        if M_str[index] == G_str[index]:
            result_str += "0"
        else:
            result_str += "1"
    return codigo_rendundancia_ciclica(10011, result_str + M_str[length_G:]) 

print(codigo_rendundancia_ciclica(G_str, M_str)[:-(length_G-1)])