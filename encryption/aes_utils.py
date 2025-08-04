from cryptography.fernet import Fernet
import os

# --- KEY MANAGEMENT ---

def generate_key():
    """Generates a new AES key using Fernet."""
    return Fernet.generate_key()

def save_key_to_file(key: bytes, filename="secret.key"):
    """Saves the AES key to a file."""
    with open(filename, "wb") as f:
        f.write(key)

def load_key_from_file(filename="secret.key") -> bytes:
    """Loads the AES key from a file, or creates one if it doesn't exist."""
    if not os.path.exists(filename):
        key = generate_key()
        save_key_to_file(key, filename)
        return key
    with open(filename, "rb") as f:
        return f.read()

# --- ENCRYPTION / DECRYPTION ---

def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts a string message using the given AES key."""
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted: bytes, key: bytes) -> str:
    """Decrypts a message using the given AES key."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted).decode()
