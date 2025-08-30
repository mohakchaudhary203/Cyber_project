import os
import hashlib
import base64
import hmac

MAGIC_BYTES = b"$31$"
ITERATIONS = 310000
SALT_LEN = 16
KEY_LEN = 32

def encode_base64(data):
    """Encode bytes to URL-safe base64 without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=')

def decode_base64(data):
    """Decode URL-safe base64, adding any missing padding."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    data = data.rstrip(b'=')
    padding_len = (4 - len(data) % 4) % 4
    data += b'=' * padding_len
    return base64.urlsafe_b64decode(data)

def hash_password(password):
    """Hash password using PBKDF2-HMAC-SHA256 with salt."""
    salt = os.urandom(SALT_LEN)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS, dklen=KEY_LEN)
    return MAGIC_BYTES + encode_base64(salt) + b"$" + encode_base64(dk)

def verify_password(stored_hash, password):
    """Verify password against stored hash using constant-time comparison."""
    if not stored_hash.startswith(MAGIC_BYTES):
        raise ValueError("Invalid hash format")
    rest = stored_hash[len(MAGIC_BYTES):]
    b64_salt, b64_dk = rest.split(b"$")
    salt = decode_base64(b64_salt)
    dk = decode_base64(b64_dk)
    new_dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS, dklen=KEY_LEN)
    return hmac.compare_digest(dk, new_dk)

if __name__ == "__main__":
    test_password = input("Enter a password to hash: ")
    hashed = hash_password(test_password)
    print(f"Hashed password: {hashed}")
    verify = input("Re-enter password to verify: ")
    print(f"Password verified: {verify_password(hashed, verify)}")
# File: crypto_auth.py
# Description: A module for hashing and verifying passwords using PBKDF2-HMAC-SHA256 with salt and constant-time comparison.
# It also includes functions for URL-safe base64 encoding and decoding.
# Usage: Run the script and follow prompts to hash and verify a password.
# Note: This implementation is for educational purposes and may not cover all security aspects needed for production use. 
# Always use well-established libraries for production systems.
# Ensure to handle exceptions and edge cases in real-world applications.
