import subprocess
import sys
import os
import time
import threading

def open_client(client_number):
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(project_dir, "gui", "chat_ui.py")
        
        # Set environment variable to identify this client
        env = os.environ.copy()
        env['CLIENT_NUMBER'] = str(client_number)
        
        subprocess.Popen([sys.executable, gui_path], 
                        cwd=project_dir, 
                        env=env)
        
        print(f"Opened Client {client_number}")
        
    except Exception as e:
        print(f"Failed to open Client {client_number}: {e}")

def main():
    print("Multiple Client Test Launcher")
    print("=" * 40)
    print()
    
    print("Starting server...")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(project_dir, "server", "server.py")
    
    # Start server in background
    server_process = subprocess.Popen([sys.executable, server_path], 
                                     cwd=project_dir)
    
    print("Server started in background")
    print("Waiting 3 seconds for server to initialize...")
    time.sleep(3)
    
  
    print()
    print("Opening multiple clients...")
    
    clients = []
    for i in range(1, 4):  
        client_thread = threading.Thread(target=open_client, args=(i,))
        client_thread.start()
        clients.append(client_thread)
        time.sleep(1)  
    
    
    for client in clients:
        client.join()
    
    try:
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        server_process.terminate()
        print("Server stopped")

if __name__ == "__main__":
    main() 