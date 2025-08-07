#!/usr/bin/env python3
"""
Secure Chat Application Launcher
================================

This script allows you to easily start either the server or client
for the secure chat application.

Usage:
    python run_chat.py server    # Start the server
    python run_chat.py client    # Start the client GUI
    python run_chat.py both      # Start both server and client (in separate windows)
"""

import sys
import subprocess
import threading
import time
import os

def print_banner():
    """Print a cool banner for the chat application"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔐 SECURE CHAT APP 🔐                    ║
    ║                                                              ║
    ║  Features:                                                   ║
    ║  • AES-256 Encryption                                        ║
    ║  • Real-time messaging                                       ║
    ║  • Beautiful GUI interface                                   ║
    ║  • Multi-client support                                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def start_server():
    """Start the chat server"""
    print("🚀 Starting Secure Chat Server...")
    print("📍 Server will listen on 127.0.0.1:5001")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        # Change to the project directory and run server
        project_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(project_dir, "server", "server.py")
        subprocess.run([sys.executable, server_path], cwd=project_dir, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def start_client():
    """Start the chat client GUI"""
    print("🖥️  Starting Secure Chat Client...")
    print("🔗 Client will connect to 127.0.0.1:5001")
    print("⏹️  Close the GUI window to stop the client\n")
    
    try:
        # Change to the project directory and run client
        project_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(project_dir, "gui", "chat_ui.py")
        subprocess.run([sys.executable, gui_path], cwd=project_dir, check=True)
    except Exception as e:
        print(f"❌ Error starting client: {e}")

def start_both():
    """Start both server and client in separate processes"""
    print("🚀 Starting both server and client...")
    print("⏳ Server will start first, then client...\n")
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Start client
    start_client()

def main():
    """Main launcher function"""
    print_banner()
    
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python run_chat.py server    # Start the server")
        print("  python run_chat.py client    # Start the client GUI")
        print("  python run_chat.py both      # Start both server and client")
        print()
        print("Example:")
        print("  python run_chat.py both")
        return
    
    command = sys.argv[1].lower()
    
    if command == "server":
        start_server()
    elif command == "client":
        start_client()
    elif command == "both":
        start_both()
    else:
        print(f"❌ Unknown command: {command}")
        print("Valid commands: server, client, both")

if __name__ == "__main__":
    main() 