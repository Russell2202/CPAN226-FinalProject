from cryptography.fernet import Fernet  # Import Fernet for AES encryption/decryption
import os 
# ================================
# ===        KEY HANDLING      ===
# ================================

def generate_key():
    """
    Generates a new AES key using Fernet.
    Fernet uses 128-bit AES in CBC mode with PKCS7 padding and HMAC.
    """
    return Fernet.generate_key()


def save_key_to_file(key: bytes, filename="secret.key"):
    """
    Saves the given key to a local file (default: 'secret.key').
    This allows the same key to be reused across sessions.
    """
    with open(filename, "wb") as f:
        f.write(key)


def load_key_from_file(filename="secret.key") -> bytes:
    """
    Loads the encryption key from a file. If the file does not exist,
    it will generate a new key, save it, and then return it.
    """
    if not os.path.exists(filename):
        # If the key file doesn't exist, create one
        key = generate_key()
        save_key_to_file(key, filename)
        return key
    
    # If the key file exists, load and return the key
    with open(filename, "rb") as f:
        return f.read()

# ================================
# === ENCRYPTION / DECRYPTION  ===
# ================================

def encrypt_message(message: str, key: bytes) -> bytes:
    """
    Encrypts a message string using the provided AES key.
    Returns encrypted data in bytes.
    """
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())  # Convert string to bytes before encrypting


def decrypt_message(encrypted: bytes, key: bytes) -> str:
    """
    Decrypts an encrypted message using the provided AES key.
    Returns the original plaintext message as a string.
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted).decode()  # Convert bytes back to string
