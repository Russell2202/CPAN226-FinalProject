import socket
import threading
import time
import sys
import os
from datetime import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from encryption.aes_utils import load_key_from_file, decrypt_message, encrypt_message

class ChatServer:
    def __init__(self):
        # Load the AES key from file
        self.key = load_key_from_file()
        
        # Server configuration
        self.HOST = '127.0.0.1'  
        self.PORT = 5001
        
        # Client management
        self.clients = []
        self.client_lock = threading.Lock()
        
        # Create a TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the address and port
        self.server_socket.bind((self.HOST, self.PORT))
        
        # Start listening for incoming connections
        self.server_socket.listen(5)
        print(f"Secure Chat Server listening on {self.HOST}:{self.PORT}...")
        print("Waiting for clients to connect...")
        
    def start(self):
        try:
            while True:
                # Wait for a client to connect
                conn, addr = self.server_socket.accept()
                print(f"New client connected from {addr}")
                
                # Add client to list
                with self.client_lock:
                    self.clients.append((conn, addr))
                
                # Start client handler thread
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            self.cleanup()
    
    def handle_client(self, conn, addr):
        """Handle individual client connection"""
        try:
            while True:
                # Wait to receive encrypted data from the client
                data = conn.recv(4096) 
                if not data:
                    break  

                try:
                    # Try to decrypt the received data using AES
                    decrypted = decrypt_message(data, self.key)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}]Message from {addr}: {decrypted}")
                    
                    # Echo the message back to all clients
                    self.broadcast_message(decrypted, conn)
                    
                except Exception as e:
                    # Catch any decryption errors
                    print(f"Error decrypting message from {addr}: {e}")
                    
        except Exception as e:
            print(f"Client {addr} error: {e}")
        finally:
            # Remove client from list
            with self.client_lock:
                self.clients = [(c, a) for c, a in self.clients if c != conn]
            
            conn.close()
            print(f"Client {addr} disconnected")
    
    def broadcast_message(self, message, sender_conn):
        """Send message to all connected clients except sender"""
        encrypted = encrypt_message(message, self.key)
        
        with self.client_lock:
            for conn, addr in self.clients:
                if conn != sender_conn:  
                    try:
                        conn.sendall(encrypted)
                    except Exception as e:
                        print(f"Failed to send to {addr}: {e}")
                        # Remove failed client
                        self.clients = [(c, a) for c, a in self.clients if c != conn]
    
    def cleanup(self):
        print("Cleaning up server resources...")
        
        # Close all client connections
        with self.client_lock:
            for conn, addr in self.clients:
                try:
                    conn.close()
                except:
                    pass
            self.clients.clear()
        
        # Close server socket
        try:
            self.server_socket.close()
        except:
            pass
        
        print("Server cleanup complete")

if __name__ == "__main__":
    server = ChatServer()
    server.start()
