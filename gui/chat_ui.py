import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import time
import sys
import os
from datetime import datetime

# Add the parent directory to the path so we can import encryption module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from encryption.aes_utils import load_key_from_file, encrypt_message, decrypt_message

class ChatClient:
    def __init__(self):
        # Load encryption key
        self.key = load_key_from_file()
        
        # Network settings
        self.HOST = '127.0.0.1'
        self.PORT = 5001
        self.client_socket = None
        self.connected = False
        self.receive_thread = None
        
        # Create GUI
        self.setup_gui()
        
    def create_styled_button(self, parent, text, command, bg_color='white', fg_color='black'):
        """Create a clean button with white background and black text"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=5,
            activebackground='#f0f0f0',
            activeforeground='black',
            cursor='hand2'  # Hand cursor on hover
        )
        return button
        
    def setup_gui(self):
        # Main window
        self.root = tk.Tk()
        self.root.title("🔐 Secure Chat Client")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background='#2c3e50')
        style.configure('Custom.TButton', 
                       background='#3498db', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, 
                              text="🔐 Secure Chat Client", 
                              font=('Arial', 18, 'bold'),
                              bg='#2c3e50', 
                              fg='#ecf0f1')
        title_label.pack(pady=(0, 20))
        
        # Username input area
        username_frame = tk.Frame(main_frame, bg='#2c3e50')
        username_frame.pack(fill=tk.X, pady=(0, 10))
        
        username_label = tk.Label(username_frame,
                                 text="Your Name:",
                                 font=('Arial', 10, 'bold'),
                                 bg='#2c3e50',
                                 fg='#ecf0f1')
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.username_entry = tk.Entry(username_frame,
                                      font=('Arial', 10),
                                      bg='white',
                                      fg='black',
                                      relief=tk.FLAT,
                                      bd=0,
                                      width=20,
                                      insertbackground='black')  # Cursor color
        self.username_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.username_entry.insert(0, "User" + str(int(time.time()) % 1000))  # Default username
        
        # Connection status
        self.status_frame = tk.Frame(main_frame, bg='#2c3e50')
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(self.status_frame, 
                                    text="🔴 Disconnected", 
                                    font=('Arial', 12),
                                    bg='#2c3e50', 
                                    fg='#e74c3c')
        self.status_label.pack(side=tk.LEFT)
        
        # Connect button
        self.connect_btn = self.create_styled_button(
            self.status_frame, 
            "Connect", 
            self.toggle_connection,
            bg_color='white',
            fg_color='black'
        )
        self.connect_btn.pack(side=tk.RIGHT)
        
        # Chat area
        chat_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat history
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message input area
        input_frame = tk.Frame(main_frame, bg='#2c3e50')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Message entry
        self.message_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='white',
            fg='black',
            relief=tk.FLAT,
            bd=0,
            insertbackground='black'  # Cursor color
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind('<Return>', self.send_message)
        
        # Send button
        self.send_btn = self.create_styled_button(
            input_frame,
            "Send",
            self.send_message,
            bg_color='white',
            fg_color='black'
        )
        self.send_btn.pack(side=tk.RIGHT)
        
        # Info panel
        info_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.SUNKEN, bd=1)
        info_frame.pack(fill=tk.X)
        
        self.info_label = tk.Label(
            info_frame,
            text="Ready to connect to server...",
            font=('Arial', 9),
            bg='#34495e',
            fg='#bdc3c7'
        )
        self.info_label.pack(pady=5)
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def toggle_connection(self):
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()
    
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.HOST, self.PORT))
            self.connected = True
            
            # Update UI
            self.status_label.config(text="🟢 Connected", fg='#27ae60')
            self.connect_btn.config(text="Disconnect", bg='#e74c3c')
            self.info_label.config(text=f"Connected to {self.HOST}:{self.PORT}")
            
            # Start receiving thread
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            
            self.add_system_message("Connected to server successfully!")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.info_label.config(text="Connection failed")
    
    def disconnect_from_server(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False
        
        # Update UI
        self.status_label.config(text="🔴 Disconnected", fg='#e74c3c')
        self.connect_btn.config(text="Connect", bg='#27ae60')
        self.info_label.config(text="Disconnected from server")
        
        self.add_system_message("Disconnected from server")
    
    def send_message(self, event=None):
        if not self.connected:
            messagebox.showwarning("Not Connected", "Please connect to the server first!")
            return
        
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Get username
        username = self.username_entry.get().strip()
        if not username:
            username = "Anonymous"
        
        try:
            # Create message with username
            full_message = f"{username}: {message}"
            
            # Encrypt and send message
            encrypted = encrypt_message(full_message, self.key)
            self.client_socket.sendall(encrypted)
            
            # Display sent message
            self.add_message(username, message, "sent")
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send message: {str(e)}")
            self.disconnect_from_server()
    
    def receive_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                # Decrypt and display message
                decrypted = decrypt_message(data, self.key)
                
                # Parse username and message
                if ": " in decrypted:
                    username, message = decrypted.split(": ", 1)
                else:
                    username = "Unknown"
                    message = decrypted
                
                # Don't show your own messages as received
                current_username = self.username_entry.get().strip()
                if username != current_username:
                    self.add_message(username, message, "received")
                
            except Exception as e:
                if self.connected:  
                    self.root.after(0, lambda: messagebox.showerror("Receive Error", f"Connection lost: {str(e)}"))
                    self.root.after(0, self.disconnect_from_server)
                break
    
    def add_message(self, sender, message, msg_type):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on message type
        if msg_type == "sent":
            color = "#2980b9"  
            prefix = "➤"
        elif msg_type == "received":
            color = "#27ae60"  
            prefix = "◀"
        else:
            color = "#7f8c8d"  
            prefix = "ℹ"
        
        formatted_message = f"[{timestamp}] {prefix} {sender}: {message}\n"
        
        self.root.after(0, lambda: self._update_chat_display(formatted_message, color))
    
    def add_system_message(self, message):
        self.add_message("System", message, "system")
    
    def _update_chat_display(self, message, color):
        self.chat_display.config(state=tk.NORMAL)
        
        # Insert message with color
        self.chat_display.insert(tk.END, message)
        
        # Apply color to the last line
        last_line_start = self.chat_display.index("end-2c linestart")
        last_line_end = self.chat_display.index("end-1c")
        
        # Create tag for color
        tag_name = f"color_{int(time.time() * 1000)}"
        self.chat_display.tag_add(tag_name, last_line_start, last_line_end)
        self.chat_display.tag_config(tag_name, foreground=color)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def on_closing(self):
        if self.connected:
            self.disconnect_from_server()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.run()
