letras = "abcdefghijklmnopqrstuvwxyz"


def encriptacion_simple(mensaje, sigma, desplazamientos, inversa=False):
    alfabeto = {}
    mensaje_cod = ""
    if inversa == False: 
        for _ in desplazamientos:
            for i in range(len(letras)):
                alfabeto.add(letras[i],letras[i+sigma])
            for letra in mensaje:
                mensaje_cod += alfabeto[letra]
        return encriptacion_simple(mensaje_cod, sigma, desplazamientos - 1)
    else:
        for i in range(len(letras)//2):
            alfabeto.add([i],[-i])
        for letra in mensaje:
            mensaje_cod += alfabeto[letra]
        return mensaje_cod

def encriptacion_lineal(mensaje, a, b):
    mensaje_cod = ""
    alfabeto = {}
    for i in range(len(letras)):
        alfabeto.add(letras[i], i)
    for letra in mensaje:
        mensaje_cod += letras[(a * alfabeto[letra]) + b]
    return mensaje_cod