import socket
import sys
import os

# Add the parent directory to the path so we can import encryption module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from encryption.aes_utils import load_key_from_file, encrypt_message

# Load the AES key from file
key = load_key_from_file()

# Server address 
HOST = '127.0.0.1'  
PORT = 5001        

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    while True:
        # Ask the user for a message to send
        message = input("Enter message (or type 'exit' to quit): ")

        if message.lower() == 'exit':
            break  

        # Encrypt the message using AES
        encrypted = encrypt_message(message, key)

        # Send the encrypted message to the server
        client_socket.sendall(encrypted)
        print("Encrypted message sent.")

except ConnectionRefusedError:
    print("Could not connect to the server. Make sure the server is running.")
except KeyboardInterrupt:
    print("\nClient interrupted.")

finally:
  
    client_socket.close()
