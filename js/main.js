console.log('Hello world!');

// WebSocketClient class
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.ws = new WebSocket(this.url);
    }

    onOpen(callback) {
        this.ws.onopen = callback;
    }

    onMessage(callback) {
        this.ws.onmessage = callback;
    }

    send(message) {
        this.ws.send(message);
    }
}

// UIHandler class
class UIHandler {
    constructor(wsClient) {
        this.wsClient = wsClient;
        this.formChat = document.getElementById('formChat');
        this.textField = document.getElementById('textField');
        this.subscribe = document.getElementById('subscribe');
    }

    init() {
        this.formChat.addEventListener('submit', (e) => this.handleSubmit(e));
        this.wsClient.onOpen(() => console.log('Connected to WebSocket server!'));
        this.wsClient.onMessage((e) => this.handleMessage(e));
    }

    handleSubmit(e) {
        e.preventDefault();
        const message = this.textField.value.trim();
        if (message) {
            this.wsClient.send(message);
            this.textField.value = '';
        }
    }

    handleMessage(e) {
        const text = e.data;
        const elMsg = document.createElement('div');
        elMsg.textContent = text;
        this.subscribe.appendChild(elMsg);
    }
}

// Initialize WebSocket and UI
const wsClient = new WebSocketClient('ws://localhost:8080');
const uiHandler = new UIHandler(wsClient);

uiHandler.init();
