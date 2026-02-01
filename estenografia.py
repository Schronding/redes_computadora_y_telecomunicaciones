from PIL import Image
# I didn't know what PIL standed for, but it seems it is for 
# Python Imaging Library, but that it was discontinued in 2011
# and was expanded further with Pillow, which is one fork. 

DELIMITER = "[FIN]"
# This allows me to know where the poem should stop reading, as if 
# not the program might incorrectly interpret that those 
# "meaningless" LSB (Least Significant Bits) are trying to convey
# more words. 

def get_image_capacity(img):
    width, height = img.size
    # This is great. I wonder why we use 'img.' instead of 'Image.'
    # though, as I never used a "synonymous" like numpy as np. 
    total_pixels = width * height
    capacity = (total_pixels // 8) - len(DELIMITER)
    # As each character of the ASCII (I forgot what the ASCII
    # standed for too, but it seems it is the American Standard Code
    # for Information Interchange) requires 8 bits or 1 byte in order
    # to represent all the characters that are required for the west. 
    # As there are more characters in other languages I think that
    # was the reason why UTF-8 came to "replace" ASCII. 
    return capacity

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)
    # This return seems very strange to me. For what I have seen 
    # ''.join() means that you want to start from an empty string 
    # and construct it from the arguments inside join. 
    # I don't know what the format function does, but it seems it 
    # is the part that actually transforms the text to bits. I 
    # imagine 08b is a code for the 8 bits or one bit we're looking 
    # for. I don't know what the ord() function does either. 
    # What is surprising to me is that it seems we can have a list 
    # comprehension inside the join; is it possible to have in other
    # parts of python? Maybe format is like a direct mapping 
    # between the character and its 8 bit representation. 
    # I suppose that we're using ASCII throughout the whole process. 

def bits_to_text(bits_stream):
    text = ""
    for i in range(0, len(bits_stream), 8):
    # This for loop says start in 0, and go in steps of 8 until 
    # you have arrived at the bits_stream value, which I assume it 
    # is the bit string of the whole text. As we always return the 
    # exact quantity of bits that we modified, I think this 
    # function is robust enough to not make use of a the try-except 
    # clauses. 
        byte_bits = bits_stream[i:i+8]
        if len(byte_bits) < 8:
        # I don't understand this part... If I am selecting always
        # 8 positions of the index, how could it be that I will ever
        # have something less than 8? I assume it could be in the 
        # delimiter, as there I have 5 ( [FIN] ) but I have not 
        # find the if statement or the logic to know we have arrived
        # to the delimiter yet. 
            break
        text += chr(int(byte_bits, 2))
        # This I don't understand either, as I have never used int 
        # with an argument, I have just used it directly. I 
        # imagine it could be something similar to .2f but to 
        # integers, like a limit that doesn't allow to have more 
        # than 2 digits (from -20 to 20)... but that range would 
        # allow only 40 combinations, and I don't think that I have 
        # used less than 40 characters in any of my poems.
        #  I didn't know that the chr function existed either! 
        # I thought that the 2 digit limit was for letters that might
        # count as one, such as ll, but this logic breaks when I
        # realize it is not the character that it is being modified,
        # but the integer. 
    return text

def hide_message(image_path, message, output_path):
    
    try:
        img = Image.open(image_path).convert('RGB')
        # It seems I can use convert to transform the image into a 
        # variety of formats. In this case RGB. As that is a 3D 
        # array, I assume PIL depends on pandas. 
    except Exception as e:
        print(f"Error abriendo la imagen: {e}")
        return
        # Why do I have a return statement that doesn't returns 
        # anything and an error isn't poppint out? I thought I was
        # forced to always return something with that statement, 
        # even if I what was returned was nothing (None)

    capacity = get_image_capacity(img)
    print(f"Maximum capacity: {capacity} characters.")
    
    if len(message) > capacity:
        print(f"Error: The message is too long. The Maximum is {capacity} characters.")
        return

    message_with_delimiter = message + DELIMITER
    bits_to_hide = text_to_bits(message_with_delimiter)
    # It indeed seems that indeed it might be the LENGTH of the 
    # delimiter, not what it says, the one that breaks the reading
    # of the text. I think there might be an edge case here. If I
    # put text in all the available characters of the picture, I
    # will saturate the LSB of the image and the program will never
    # arrive to the delimiter. The `capacity` variable therefore, 
    # should have `- DELIMITER` in its declaration. 
    
    pixels = img.load()
    # Here I am using 'img.' too. Could it be that there are native
    # image functions in python? I wonder why the '.load()' method
    # doesn't has a path. Could it be that it just means that the
    # img objects can work from this line onwards? But I used
    # img previously, didn't I? 
    width, height = img.size
    
    bit_index = 0
    
    # Iterar y ocultar (izquierda-derecha, arriba-abajo)
    for y in range(height):
        for x in range(width):
            
            if bit_index < len(bits_to_hide):
                # Obtener el píxel (R, G, B)
                # I don't see where we created a 'pixels' array, 
                # and it is not the attribute of an object either... 
                # I am confused. But wait, we did created it! It 
                # was the variable that store the output of  
                # img.load()... then how does the program know what
                # image I am loading? 
                r, g, b = pixels[x, y]
                
                # Obtener el bit que queremos ocultar
                bit_to_hide = int(bits_to_hide[bit_index])
                
                # (r & 0b11111110) pone el último bit de R en 0
                # | bit_to_hide      añade nuestro bit (0 o 1)
                new_r = (r & 0b11111110) | bit_to_hide
                
                pixels[x, y] = (new_r, g, b)
                
                bit_index += 1
            else:
                break
        if bit_index >= len(bits_to_hide):
            break

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

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # (r & 1) nos da solo el último bit (0 o 1)
            lsb = str(r & 1)
            
            hidden_bits += lsb
            
            if len(hidden_bits) % 8 == 0:
                message = bits_to_text(hidden_bits)
                
                if message.endswith(DELIMITER):
                    return message[:-len(DELIMITER)] 

    return "No se encontró un mensaje oculto con el delimitador."

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
                
                ruta_texto = input("Ruta del archivo de texto con el poema (ej. poema.txt): ")
                with open(ruta_texto, 'r', encoding='utf-8') as f:
                    message = f.read()

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