const ws = new WebSocket('ws://localhost:8080');

document.getElementById('formChat').addEventListener('submit', (e) => {
    e.preventDefault();
    ws.send(document.getElementById('textField').value);
    document.getElementById('textField').value = '';
});

document.getElementById('formCommand').addEventListener('submit', (e) => {
    e.preventDefault();
    ws.send(document.getElementById('commandField').value);
    document.getElementById('commandField').value = '';
});

ws.onopen = (e) => {
    console.log('Connected to WebSocket');
};

ws.onmessage = (e) => {
    console.log(e.data);
    const text = e.data;

    const elMsg = document.createElement('div');
    elMsg.textContent = text;
    document.getElementById('subscribe').appendChild(elMsg);
};
