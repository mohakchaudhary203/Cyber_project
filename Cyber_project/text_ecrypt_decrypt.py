from cryptography.fernet import Fernet

def generate_key():
    """Generate a key for encryption and decryption."""
    return Fernet.generate_key() 
def encrypt_text(plain_text, key):
    """Encrypt the plain text using the provided key."""
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(plain_text.encode())
    return encrypted_text 
def decrypt_text(encrypted_text, key):
    """Decrypt the encrypted text using the provided key."""
    fernet = Fernet(key)
    decrypted_text = fernet.decrypt(encrypted_text).decode()
    return decrypted_text 
if __name__ == "__main__":
    # Example usage
    key = generate_key()
    print(f"Generated Key: {key.decode()}")
    
    original_text = "Hello, World!"
    print(f"Original Text: {original_text}")
    
    encrypted = encrypt_text(original_text, key)
    print(f"Encrypted Text: {encrypted.decode()}")
    
    decrypted = decrypt_text(encrypted, key)
    print(f"Decrypted Text: {decrypted}")   
# Ensure the decrypted text matches the original
    assert original_text == decrypted, "Decryption did not return the original text!" 
#File: text_ecrypt_decrypt.py
# Description: A simple module to encrypt and decrypt text using symmetric encryption (Fernet). 
# Usage: Run the script to see an example of generating a key, encrypting text, and decrypting it back. 
# Note: This implementation is for educational purposes and may not cover all security aspects needed for production use. 
# Always use well-established libraries and follow best practices for production systems.   
# Ensure to handle exceptions and edge cases in real-world applications. 
# The key must be securely stored and managed in real-world applications. 
# The encrypted text is in bytes; convert to string for display or storage if needed. 
# The original text must be encoded to bytes before encryption and decoded back to string after decryption. 
# The key must be the same for both encryption and decryption.
# The Fernet key is URL-safe base64-encoded 32-byte key.
# The cryptography library must be installed: pip install cryptography 
# Ensure to install the cryptography library: pip install cryptography 
# This code requires Python 3.6 or higher due to f-strings and type hints.