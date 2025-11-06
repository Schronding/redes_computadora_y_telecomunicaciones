import math

LETRAS = "abcdefghijklmnopqrstuvwxyz"

def desplazamiento_simple(mensaje, sigma):

    mensaje_cod = ""
    for letra in mensaje.lower():
        if letra in LETRAS:
            i_original = LETRAS.index(letra)
            i_nuevo = (i_original + sigma) % 26
            mensaje_cod += LETRAS[i_nuevo]
        else:
            mensaje_cod += letra
    return mensaje_cod

def sustitucion_multiple(mensaje, desplazamientos):
    mensaje_cod = ""
    i_clave = 0  
    
    for letra in mensaje.lower():
        if letra in LETRAS:
            sigma = desplazamientos[i_clave]
            
            i_original = LETRAS.index(letra)
            i_nuevo = (i_original + sigma) % 26
            mensaje_cod += LETRAS[i_nuevo]
            
            i_clave = (i_clave + 1) % len(desplazamientos)
        else:
            mensaje_cod += letra
    return mensaje_cod

def cifrado_lineal(mensaje, a, b):
    if math.gcd(a, 26) != 1:
        return (f"Error: 'a' ({a}) no es coprimo con 26. "
                "Prueba con: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25")

    mensaje_cod = ""
    for letra in mensaje.lower():
        if letra in LETRAS:
            i_original = LETRAS.index(letra)
            i_nuevo = (a * i_original + b) % 26
            mensaje_cod += LETRAS[i_nuevo]
        else:
            mensaje_cod += letra
    return mensaje_cod


def cifrado_caotico(longitud):

    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0
    
    x, y, z = 0.1, 0.0, 0.0
    
    dt = 0.01
    
    desplazamientos_caoticos = []
    
    for _ in range(100):
        dx = (sigma * (y - x)) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz

    while len(desplazamientos_caoticos) < longitud:
        dx = (sigma * (y - x)) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz
        
        desplazamiento = int(abs(x * 1000)) % 26
        desplazamientos_caoticos.append(desplazamiento)
        
    return desplazamientos_caoticos

def cifrado_caotico(mensaje):

    print("Generando clave caótica desde el atractor de Lorenz...")
    desplazamientos = cifrado_caotico(len(mensaje))
    
    print(f"Clave generada (primeros 10): {desplazamientos[:10]}...")
    return sustitucion_multiple(mensaje, desplazamientos)

def main_menu():
    print("1. Desplazamiento simple")
    print("2. Desplazamiento multiple")
    print("3. Cifrado Lineal")
    print("4. Cifrado Caótico (Atractor de Lorenz)")
    print("5. Salir")
    
    opcion = input("Selecciona una opción (1-5): ")
    return opcion

while True:
    opcion = main_menu()
    
    if opcion == '1':
        try:
            mensaje = input("Introduce el mensaje: ")
            sigma = int(input("Introduce el desplazamiento (ej. 3): "))
            cifrado = desplazamiento_simple(mensaje, sigma)
            print(f"Mensaje cifrado: {cifrado}")
        except ValueError:
            print("Error: El desplazamiento debe ser un número entero.")
            
    elif opcion == '2':
        try:
            mensaje = input("Introduce el mensaje: ")
            clave_str = input("Introduce los desplazamientos separados por coma (ej. 3,5,10): ")
            desplazamientos = [int(s.strip()) for s in clave_str.split(',')]
            
            if not desplazamientos:
                print("Error: Debes introducir al menos un desplazamiento.")
            else:
                cifrado = sustitucion_multiple(mensaje, desplazamientos)
                print(f"Mensaje cifrado: {cifrado}")
        except ValueError:
            print("Error: Todos los desplazamientos deben ser números enteros.")

    elif opcion == '3':
        try:
            mensaje = input("Introduce el mensaje: ")
            a = int(input("Introduce el valor 'a' (coprimo con 26): "))
            b = int(input("Introduce el valor 'b': "))
            cifrado = cifrado_lineal(mensaje, a, b)
            print(f"Mensaje cifrado: {cifrado}")
        except ValueError:
            print("Error: 'a' y 'b' deben ser números enteros.")
            
    elif opcion == '4':
        mensaje = input("Introduce el mensaje: ")
        cifrado = cifrado_caotico(mensaje)
        print(f"Mensaje cifrado: {cifrado}")
        
    elif opcion == '5':
        print("Saliendo del programa...")
        break
        
    else:
        print("Opción no válida. Por favor, introduce un número del 1 al 5.")