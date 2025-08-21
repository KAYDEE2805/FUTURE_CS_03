from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, 'rb') as original_file:
        original_data = original_file.read()
    encrypt_data = f.encrypt(original_data)
    with open(file_path + '.enc', 'wb') as encrypted_file:
        encrypted_file.write(encrypt_data)
    os.remove(file_path)

def decrypt_file(encrypted_file_path, key):
    f = Fernet(key)
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    decrypted_data = f.decrypt(encrypted_data)
    original_file_path = encrypted_file_path.replace ('.enc', '')
    with open(original_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    return original_file_path