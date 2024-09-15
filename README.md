# Chat with WebSocket and PrivatBank API

This project consists of a WebSocket server that handles chat messages and retrieves currency exchange rates via the PrivatBank API. The project also includes a simple web page for interacting with the server through a browser.

## **Contents**

1. **WebSocket Server** - `server.py`
2. **Web Page** - `index.html`, `main.js`, `main.css`
3. **Command Logging** - `exchange_commands.log`

## **Requirements**

Before you begin, ensure you have the following tools installed:
- Python 3.7 or newer
- pip (Python package installer)
- aiohttp
- aiofile
- aiopath
- websockets

## **Installation Instructions**

1. **Clone the Repository**

    ```bash
    git clone <URL-of-your-repository>
    cd <repository-name>
    ```

2. **Create a Virtual Environment (recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Unix/MacOS
    venv\Scripts\activate     # For Windows
    ```

3. **Install Dependencies**

    ```bash
    pip install aiohttp aiofile aiopath websockets
    ```

## **Running the Application**

### **Start the WebSocket Server**

In one terminal, run:

```bash
python server.py
