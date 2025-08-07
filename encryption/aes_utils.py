from cryptography.fernet import Fernet  
import os 

def generate_key():
    #Generates a new AES key using Fernet.
    return Fernet.generate_key()


def save_key_to_file(key: bytes, filename="secret.key"):
    #Save key to a local file (secret.key)
    with open(filename, "wb") as f:
        f.write(key)


def load_key_from_file(filename="secret.key") -> bytes:
    if not os.path.exists(filename):
        # If the key file doesn't exist, create one
        key = generate_key()
        save_key_to_file(key, filename)
        return key
    
    # If the key file exists, load and return the key
    with open(filename, "rb") as f:
        return f.read()

def encrypt_message(message: str, key: bytes) -> bytes:
    #Encrypt message using provided AES Key
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())  


def decrypt_message(encrypted: bytes, key: bytes) -> str:

    #Decrypt message using AES key
    fernet = Fernet(key)
    return fernet.decrypt(encrypted).decode()  
