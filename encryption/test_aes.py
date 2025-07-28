from aes_utils import generate_key, encrypt_message, decrypt_message

key = generate_key()
print("Generated Key:", key)

encrypted = encrypt_message("Hello Hargobind!", key)
print("Encrypted:", encrypted)

decrypted = decrypt_message(encrypted, key)
print("Decrypted:", decrypted)
