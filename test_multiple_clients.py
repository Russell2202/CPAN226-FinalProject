#!/usr/bin/env python3
"""
Multiple Client Test Script
===========================

This script helps you test the chat application with multiple clients
by opening several client windows automatically.

Usage:
    python3 test_multiple_clients.py
"""

import subprocess
import sys
import os
import time
import threading

def open_client(client_number):
    """Open a client window with a specific number"""
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(project_dir, "gui", "chat_ui.py")
        
        # Set environment variable to identify this client
        env = os.environ.copy()
        env['CLIENT_NUMBER'] = str(client_number)
        
        subprocess.Popen([sys.executable, gui_path], 
                        cwd=project_dir, 
                        env=env)
        
        print(f"✅ Opened Client {client_number}")
        
    except Exception as e:
        print(f"❌ Failed to open Client {client_number}: {e}")

def main():
    print("🚀 Multiple Client Test Launcher")
    print("=" * 40)
    print()
    
    # First, start the server
    print("1️⃣  Starting server...")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(project_dir, "server", "server.py")
    
    # Start server in background
    server_process = subprocess.Popen([sys.executable, server_path], 
                                     cwd=project_dir)
    
    print("✅ Server started in background")
    print("⏳ Waiting 3 seconds for server to initialize...")
    time.sleep(3)
    
    # Open multiple clients
    print()
    print("2️⃣  Opening multiple clients...")
    
    clients = []
    for i in range(1, 4):  # Open 3 clients
        client_thread = threading.Thread(target=open_client, args=(i,))
        client_thread.start()
        clients.append(client_thread)
        time.sleep(1)  # Small delay between clients
    
    # Wait for all clients to open
    for client in clients:
        client.join()
    
    print()
    print("🎉 All clients opened!")
    print()
    print("📋 Instructions:")
    print("1. In each client window, enter a different username")
    print("2. Click 'Connect' in each client")
    print("3. Start chatting between the clients!")
    print("4. Close the GUI windows when done")
    print()
    print("🛑 To stop everything, press Ctrl+C in this terminal")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        server_process.terminate()
        print("✅ Server stopped")

if __name__ == "__main__":
    main() 