let chatSocket = new ReconnectingWebSocket( 'ws://' + window.location.host + '/ws/chat/' + roomName + '/');

chatSocket.onopen = function(e) {
  fetchMessages();
};

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    if (data['command'] === 'fetch_messages') {
      for (let i=0; i<data['messages'].length; i++) {
        createMessage(data['messages'][i]);
      }
    } else if (data['command'] === 'new_message'){
      createMessage(data['message']);
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    let messageInputDom = document.getElementById('chat-message-input');
    let message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'message': message,
        'from': email,
        'group_name': roomName
    }));

    messageInputDom.value = '';
};

function fetchMessages() {
  chatSocket.send(JSON.stringify({
      'command': 'fetch_messages',
      'group_name': roomName
  }));
}

function createMessage(data) {
    let msg_email = data['email'];
    let username = data['username'];
    let msgListTag = document.createElement('li');
    let imgTag = document.createElement('img');
    let pTag = document.createElement('p');
    pTag.textContent = username + ': ' + data['message'];
    imgTag.src = 'http://emilcarlsson.se/assets/mikeross.png';

    // console.log("USER MESSAGE\n", msg_email);
    // console.log("USER MESSAGE\n", data);
    // console.log("USER MESSAGE\n", data['message']);

    if (msg_email === email) {
        msgListTag.className = 'sent';
    } else {
        msgListTag.className = 'replies';
    }
    msgListTag.appendChild(imgTag);
    msgListTag.appendChild(pTag);
    document.querySelector('#chat-log').appendChild(msgListTag);
}