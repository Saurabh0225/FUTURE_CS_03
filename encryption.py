from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

KEY_FILE = 'key.key'

# Generate and store key securely (once)
def generate_key():
    key = get_random_bytes(32)
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_data):
    key = load_key()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(file_data, AES.block_size))
    return cipher.iv + ct_bytes  # Prepend IV for decryption

def decrypt_file(encrypted_data):
    key = load_key()
    iv = encrypted_data[:AES.block_size]
    ct = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size)
