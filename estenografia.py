from PIL import Image

# This marker tells me exactly where the secret ends so I don't 
# keep reading random image noise as if it were text.
DELIMITER = "[FIN]"

def get_image_capacity(img):
    """Calculates how many characters this specific image can hold."""
    width, height = img.size
    total_pixels = width * height
    # Since 1 character = 8 bits (1 byte), and I'm only using the Red channel,
    # my capacity is pixels divided by 8, minus the space for the delimiter.
    return (total_pixels // 8) - len(DELIMITER)

def text_to_bits(text):
    """Converts a string of text into a continuous string of 0s and 1s."""
    # ord(char) gets the ASCII/Unicode number (e.g., 'A' -> 65)
    # format(..., '08b') turns that number into an 8-digit binary string (65 -> 01000001)
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits_stream):
    """Turns a stream of bits back into readable characters."""
    text = ""
    # I loop through the bit string in chunks of 8 (one byte at a time)
    for i in range(0, len(bits_stream), 8):
        byte_bits = bits_stream[i:i+8]
        if len(byte_bits) < 8:
            break
        # I convert the binary string to an integer (Base 2)
        # then chr() turns that integer back into a character.
        text += chr(int(byte_bits, 2))
    return text

def hide_message(image_path, message, output_path):
    """Hides a secret message within the Least Significant Bit (LSB) of the Red channel."""
    try:
        # I must ensure it's RGB so I have consistent Red/Green/Blue channels to work with.
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return # I 'return' here to bail out of the function if the file is missing.

    capacity = get_image_capacity(img)
    if len(message) > capacity:
        print(f"Error: Message too long. Max capacity: {capacity} chars.")
        return

    # I append the delimiter so the 'reveal' function knows when to stop.
    bits_to_hide = text_to_bits(message + DELIMITER)
    
    # I 'load' the pixels into a workbench so I can modify them directly in memory.
    pixels = img.load()
    width, height = img.size
    bit_index = 0
    
    # I iterate through every pixel, row by row (y) and column by column (x).
    for y in range(height):
        for x in range(width):
            if bit_index < len(bits_to_hide):
                r, g, b = pixels[x, y]
                
                # I get the current secret bit I want to hide (0 or 1).
                bit_to_hide = int(bits_to_hide[bit_index])
                
                # Bitwise Magic:
                # 1. (r & 0b11111110) forces the last bit of the Red value to 0.
                # 2. | bit_to_hide then places my secret bit into that 0 slot.
                new_r = (r & 0b11111110) | bit_to_hide
                
                # I update the pixel with the modified Red and the original G and B.
                pixels[x, y] = (new_r, g, b)
                bit_index += 1
            else:
                break
        if bit_index >= len(bits_to_hide):
            break

    # I save the final image. Note: it MUST be PNG to avoid compression destroying my bits!
    img.save(output_path)
    print(f"Success! Message hidden in: {output_path}")

def reveal_message(image_path):
    """Extracts the hidden bits from the Red channel and reconstructs the message."""
    try:
        img = Image.open(image_path).convert('RGB')
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    pixels = img.load()
    width, height = img.size
    hidden_bits = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # (r & 1) isolates the last bit. If r is 157 (10011101), r & 1 gives me 1.
            hidden_bits += str(r & 1)
            
            # Every time I have 8 bits, I check if the message has reached the delimiter.
            if len(hidden_bits) % 8 == 0:
                current_text = bits_to_text(hidden_bits)
                if current_text.endswith(DELIMITER):
                    # I return the text without the delimiter.
                    return current_text[:-len(DELIMITER)]

    return "No hidden message found."

def main():
    while True:
        print("\n--- LSB Steganography Tool ---")
        print("1. Hide a message in an image")
        print("2. Reveal a message from an image")
        print("3. Check image capacity")
        print("4. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            in_img = input("Enter path to source image (e.g., original.png): ")
            text_file = input("Enter path to text file containing your poem: ")
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    message = f.read()
                out_img = input("Enter path for output image (must be .png): ")
                hide_message(in_img, message, out_img)
            except FileNotFoundError:
                print("Error: Text file not found.")
                
        elif choice == '2':
            in_img = input("Enter path to the image with the hidden message: ")
            msg = reveal_message(in_img)
            print(f"\n--- Revealed Message ---\n{msg}\n------------------------")

        elif choice == '3':
            in_img = input("Enter image path: ")
            try:
                img = Image.open(in_img)
                cap = get_image_capacity(img)
                print(f"Image {in_img} can hide approx. {cap} characters.")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == '4':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()