import socket
from encryption.aes_utils import load_key_from_file, decrypt_message

# Load the AES key from file
key = load_key_from_file()

# Server configuration
HOST = '127.0.0.1'  
PORT = 5001        
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(1)
print(f"Secure Chat Server listening on {HOST}:{PORT}...")

# Wait for a client to connect
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        # Wait to receive encrypted data from the client
        data = conn.recv(4096) 
        if not data:
            break  

        try:
            # Try to decrypt the received data using AES
            decrypted = decrypt_message(data, key)
            print(f"Decrypted Message: {decrypted}")
        except Exception as e:
            # Catch any decryption errors
            print("Error decrypting:", e)

except KeyboardInterrupt:
    #Handle Ctrl+C to stop the server
    print("Server shutting down...")

finally:

    conn.close()
    server_socket.close()
