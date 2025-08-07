## Features

- **AES-256 Encryption**: All messages are encrypted using Fernet
- **GUI**: Interface built with Tkinter
- **Real-time Messaging**: Instant message delivery with socket networking
- **Multi-client Support**: Server can handle multiple clients at the same time
- **User-friendly**: Interface with connection status indicators
- **Color-coded Messages**: Different colors for sent, received, and system messages


### Running the Application

#### Option 1: Use the Launcher 
```bash
# Start both server and client
python run_chat.py both

# Or start them separately
python run_chat.py server    
python run_chat.py client   
```

#### Option 2: Manual Start
```bash

python server/server.py

python gui/chat_ui.py
```

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
- Uses **Fernet** 
- Keys are automatically generated and stored in `secret.key`
- All messages are encrypted before transmission

### Networking
- **Protocol**: TCP sockets
- **Address**: 127.0.0.1:5001 (localhost)
- **Threading**: Background threads for non-blocking message reception
- **Multi-client**: Server supports multiple simultaneous connections

### GUI Framework
- **Framework**: Tkinter 
- **Design**: Modern flat design with custom colors
- **Responsive**: Auto scrolling chat display
- **User Experience**: Simple to understand controls and status indicators

