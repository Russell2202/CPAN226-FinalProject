## Features

- **AES-256 Encryption**: All messages are encrypted using Fernet (AES-256 in CBC mode)
- **GUI**: Interface built with Tkinter
- **Real-time Messaging**: Instant message delivery with socket networking
- **Multi-client Support**: Server can handle multiple clients simultaneously
- **User-friendly**: Easy-to-use interface with connection status indicators
- **Background Threading**: Non-blocking message reception
- **Color-coded Messages**: Different colors for sent, received, and system messages


### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Use the Launcher (Recommended)
```bash
# Start both server and client
python run_chat.py both

# Or start them separately
python run_chat.py server    
python run_chat.py client   
```

#### Option 2: Manual Start
```bash
# Terminal 1: Start the server
python server/server.py

# Terminal 2: Start the client GUI
python gui/chat_ui.py
```
### Starting the Server
1. Run the server first using one of the methods above
2. The server will listen on `127.0.0.1:5001`
3. You will see connection status and incoming messages in the terminal

### Using the Client GUI
1. Launch the client GUI
2. Click the **"Connect"** button to connect to the server
3. Once connected, the status will show "Connected"
4. Type your message in the text box and press **Enter** or click **"Send"**
5. Messages are automatically encrypted before sending
6. Received messages are automatically decrypted and displayed

### GUI Features
- **Connection Status**: Shows if you're connected to the server
- **Chat History**: Scrollable area showing all messages with timestamps
- **Color Coding**: 
  - Blue: Messages you sent
  - Green: Messages you received
  - Gray: System messages
- **Real-time Updates**: Messages appear instantly as they're received


### Technical Details

### Encryption
- Uses **Fernet** (AES-256 in CBC mode with PKCS7 padding)
- Keys are automatically generated and stored in `secret.key`
- All messages are encrypted before transmission

### Networking
- **Protocol**: TCP sockets
- **Address**: 127.0.0.1:5001 (localhost)
- **Threading**: Background threads for non-blocking message reception
- **Multi-client**: Server supports multiple simultaneous connections

### GUI Framework
- **Framework**: Tkinter (Python's standard GUI library)
- **Design**: Modern flat design with custom colors
- **Responsive**: Auto-scrolling chat display
- **User Experience**: Intuitive controls and status indicators


### Adding New Features
1. **New Message Types**: Modify the `add_message()` method in `chat_ui.py`
2. **Custom Encryption**: Extend the `aes_utils.py` module
3. **Server Features**: Add methods to the `ChatServer` class in `server.py`

### Testing
1. Start the server: `python run_chat.py server`
2. Start multiple clients: `python run_chat.py client` (in different terminals)
3. Send messages between clients to test encryption and networking

