const roomName = JSON.parse(document.getElementById('room-name').textContent);
const username = JSON.parse(document.getElementById('username').textContent)

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const username = data.username;
    const date = new Date(data.date);
    document.querySelector('#chat-log').value += (
        username + ' | '
        + date.getDay() + '-'
        + date.getMonth() + '-'
        + date.getFullYear() + ' at '
        + date.getHours() + ':' + date.getMinutes()
        + '\n'
        + data.message + '\n\n'
        );
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    const date = new Date();

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username,
        'date': date
    }));
    messageInputDom.value = '';
};