def binary_to_gray(bin_str):
    binary_int = int(bin_str, 2)
    gray_int = binary_int ^ (binary_int >> 1)
    return bin(gray_int)[2:]

bin_str = input("entrada = ")
print("salida = ", binary_to_gray(bin_str))