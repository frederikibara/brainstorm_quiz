# Chat with WebSocket and PrivatBank API and console request

![images](https://github.com/user-attachments/assets/01a187fe-96f9-4bfa-9fb5-a2567a333c90)


This project consists of a WebSocket server that handles chat messages and retrieves currency exchange rates via the PrivatBank API. The project also includes a simple web page for interacting with the server through a browser.

## **Running the Application**

### 1) Console app run in terminal:
python main.py 2

### 2) WebSocket Server:
**In first terminal, run:**
python server.py

**In second terminal, run:**
python -m http.server <you port>

for example : python -m http.server 8900

## **Contents**

1. **WebSocket Server** - `server.py`
2. **Web Page** - `index.html`, `main.js`, `main.css`
3. **Command Logging** - `exchange_commands.log`

## **Requirements**

Before you begin, ensure you have the following tools installed:
- Python 3.9 or newer
- pip (Python package installer)
- aiohttp
- aiofile
- aiopath
- websockets
