const token = localStorage.getItem('token');
const socket = new WebSocket(`ws://${window.location.host}/ws/chatroom`);

document.getElementById('sendButton').addEventListener('click', () => {
    const messageInput = document.getElementById('messageInput');
    socket.send(JSON.stringify({ message: messageInput.value, token }));
    messageInput.value = '';
});

socket.onmessage = (event) => {
    const messages = document.getElementById('messages');
    const message = JSON.parse(event.data);
    const messageElement = document.createElement('div');
    messageElement.innerText = message.message;
    messages.appendChild(messageElement);
};
