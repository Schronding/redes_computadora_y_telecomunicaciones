from PIL import Image

# --- El Delimitador ---
# Se añade al final del mensaje para saber dónde parar de leer.
DELIMITER = "[FIN]"

def get_image_capacity(img):
    """Calcula cuántos caracteres (bytes) se pueden ocultar en la imagen."""
    # Usamos 8 píxeles para ocultar 1 caracter (1 bit por píxel)
    width, height = img.size
    total_pixels = width * height
    # Restamos el delimitador para dar una capacidad "útil"
    capacity = (total_pixels // 8) - len(DELIMITER)
    return capacity

def text_to_bits(text):
    """Convierte un string (ej: "A") a una lista de bits (ej: "01000001")."""
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits_stream):
    """Convierte un stream de bits (ej: "01000001") a un string (ej: "A")."""
    text = ""
    for i in range(0, len(bits_stream), 8):
        byte_bits = bits_stream[i:i+8]
        if len(byte_bits) < 8:
            break
        text += chr(int(byte_bits, 2))
    return text

def hide_message(image_path, message, output_path):
    """Oculta un mensaje en una imagen y la guarda."""
    
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error abriendo la imagen: {e}")
        return

    # 1. Verificar capacidad
    capacity = get_image_capacity(img)
    print(f"Capacidad máxima: {capacity} caracteres.")
    
    if len(message) > capacity:
        print(f"Error: El mensaje es muy largo. Máximo {capacity} caracteres.")
        return

    # 2. Preparar mensaje y bits
    message_with_delimiter = message + DELIMITER
    bits_to_hide = text_to_bits(message_with_delimiter)
    
    pixels = img.load()
    width, height = img.size
    
    bit_index = 0
    
    # 3. Iterar y ocultar (izquierda-derecha, arriba-abajo)
    for y in range(height):
        for x in range(width):
            
            if bit_index < len(bits_to_hide):
                # Obtener el píxel (R, G, B)
                r, g, b = pixels[x, y]
                
                # Obtener el bit que queremos ocultar
                bit_to_hide = int(bits_to_hide[bit_index])
                
                # --- Magia de bits ---
                # (r & 0b11111110) pone el último bit de R en 0
                # | bit_to_hide      añade nuestro bit (0 o 1)
                new_r = (r & 0b11111110) | bit_to_hide
                # ---------------------
                
                # Guardar el nuevo píxel en la imagen
                pixels[x, y] = (new_r, g, b)
                
                bit_index += 1
            else:
                # Mensaje ocultado, parar de iterar
                break
        if bit_index >= len(bits_to_hide):
            break

    # 4. Guardar la nueva imagen
    img.save(output_path)
    print(f"¡Mensaje ocultado! Imagen guardada en: {output_path}")

def reveal_message(image_path):
    """Revela un mensaje oculto en una imagen."""
    
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error abriendo la imagen: {e}")
        return

    pixels = img.load()
    width, height = img.size
    
    hidden_bits = ""
    message = ""

    # 1. Iterar y leer LSB
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # --- Magia de bits ---
            # (r & 1) nos da solo el último bit (0 o 1)
            lsb = str(r & 1)
            # ---------------------
            
            hidden_bits += lsb
            
            # 2. Intentar decodificar cada vez que tenemos un byte
            if len(hidden_bits) % 8 == 0:
                # Convertimos lo que llevamos a texto
                message = bits_to_text(hidden_bits)
                
                # 3. Buscar el delimitador
                if message.endswith(DELIMITER):
                    # Lo encontramos!
                    return message[:-len(DELIMITER)] # Devolver mensaje sin [FIN]

    return "No se encontró un mensaje oculto con el delimitador."

# --- Menú Principal ---
def main():
    while True:
        print("\n--- Esteganografía LSB (Python) ---")
        print("1. Ocultar un mensaje en una imagen")
        print("2. Revelar un mensaje de una imagen")
        print("3. Ver capacidad de una imagen")
        print("4. Salir")
        
        choice = input("Elige una opción: ")
        
        if choice == '1':
            try:
                in_img = input("Ruta de la imagen de entrada (ej. original.png): ")
                message = input("Escribe el mensaje a ocultar: ")
                out_img = input("Ruta de la imagen de salida (ej. oculto.png): ")
                hide_message(in_img, message, out_img)
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                
        elif choice == '2':
            try:
                in_img = input("Ruta de la imagen con mensaje oculto (ej. oculto.png): ")
                msg = reveal_message(in_img)
                print(f"\n--- Mensaje Revelado ---")
                print(msg)
                print("--------------------------")
            except Exception as e:
                print(f"Ocurrió un error: {e}")

        elif choice == '3':
            try:
                in_img = input("Ruta de la imagen (ej. original.png): ")
                img = Image.open(in_img)
                capacity = get_image_capacity(img)
                print(f"La imagen {in_img} ({img.width}x{img.height}) puede ocultar aprox. {capacity} caracteres.")
            except Exception as e:
                print(f"Ocurrió un error al abrir la imagen: {e}")
                
        elif choice == '4':
            print("Adiós.")
            break
            
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()