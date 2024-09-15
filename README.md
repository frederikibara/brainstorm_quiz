# Chat with WebSocket and PrivatBank API
![png-transparent-green-grass-privatbank-kiev-brovary-logo-text-ukraine-line-thumbnail](https://github.com/user-attachments/assets/e4cac6c2-34e3-4fad-bc09-c19db927b5b1)


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
