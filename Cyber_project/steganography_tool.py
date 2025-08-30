from PIL import Image
import os

def encode_message(image_path, message, output_path):
    """
    Encode a text message into an image using LSB steganography across RGB channels.
    Supports RGB, RGBA, and converts palette images automatically to RGB.
    """
    img = Image.open(image_path)
    
    # Convert palette images (mode P) or grayscale to RGB
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    encoded = img.copy()
    width, height = img.size
    channels = len(img.getbands())  # 3 for RGB, 4 for RGBA

    # Append null character to signify end of message
    message += chr(0)
    message_bits = ''.join([format(ord(c), '08b') for c in message])
    msg_len = len(message_bits)

    if msg_len > width * height * channels:
        raise ValueError(f"Message too long to encode in this image. "
                         f"Max bits: {width * height * channels}, message bits: {msg_len}")

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for ch in range(channels):
                if data_index < msg_len:
                    pixel[ch] = (pixel[ch] & ~1) | int(message_bits[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= msg_len:
                break
        if data_index >= msg_len:
            break

    encoded.save(output_path)
    print(f"Message successfully encoded into {output_path}")


def decode_message(image_path):
    """
    Decode a hidden text message from an image using LSB steganography across RGB(A) channels.
    Supports images with RGB, RGBA, or converted palette images.
    """
    img = Image.open(image_path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    width, height = img.size
    channels = len(img.getbands())
    bits = []

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for ch in range(channels):
                bits.append(pixel[ch] & 1)

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(''.join(map(str, byte)), 2))
        if char == chr(0):  # Null character signifies end
            break
        chars.append(char)

    return ''.join(chars)


if __name__ == "__main__":
    input_file = input("Enter path to input image: ").strip()
    output_file = input("Enter path to output image: ").strip()
    secret_message = input("Enter the message to hide: ")

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
    else:
        encode_message(input_file, secret_message, output_file)
        decoded_message = decode_message(output_file)
        print("Decoded message:", decoded_message)

"""
Advanced Features:
-----------------
1. Supports RGB, RGBA, and palette-based images (automatically converted).
2. Automatically calculates capacity based on image size and channels.
3. Handles larger messages more efficiently.
4. Outputs immediate verification by decoding the hidden messaTraceback (most recent call last):
  File "steganography_tool.py", line 94, in <module> encoding.
5. Provides clear error messages for unsupported formats or oversized messages.
"""
