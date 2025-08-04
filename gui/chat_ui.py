import tkinter as tk
from encryption.aes_utils import generate_key, encrypt_message, decrypt_message

# Generate AES key
from encryption.aes_utils import load_key_from_file
key = load_key_from_file()


# Tkinter setup
window = tk.Tk()
window.title("AES Encryption Tester")
window.geometry("500x400")

# Widgets
tk.Label(window, text="Enter message to encrypt:").pack()

message_entry = tk.Entry(window, width=60)
message_entry.pack(pady=5)

encrypt_result = tk.StringVar()
decrypt_result = tk.StringVar()

def handle_encrypt():
    msg = message_entry.get()
    if msg:
        encrypted = encrypt_message(msg, key)
        encrypt_result.set(encrypted.decode())  # for display
        decrypted = decrypt_message(encrypted, key)
        decrypt_result.set(decrypted)

tk.Button(window, text="Encrypt + Decrypt", command=handle_encrypt).pack(pady=10)

tk.Label(window, text="Encrypted Message:").pack()
tk.Label(window, textvariable=encrypt_result, wraplength=450, bg="lightgray").pack(pady=5)

tk.Label(window, text="Decrypted Message:").pack()
tk.Label(window, textvariable=decrypt_result, bg="lightblue").pack(pady=5)

# Start GUI loop
window.mainloop()
