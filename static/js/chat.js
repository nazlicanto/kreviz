document.addEventListener('DOMContentLoaded', () => {
    // Get the room name from the data attribute on the body tag
    const chatRoomIdentifier = document.body.getAttribute('data-room-name');

    if (chatRoomIdentifier) {
        const chatSocket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + chatRoomIdentifier + '/'
        );

        chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const chatLog = document.getElementById('chat-log');
            const newMessage = document.createElement('div');
            newMessage.innerHTML = `<strong>${data.username || 'Anonymous'}:</strong> ${data.message} <br> <small>${data.timestamp || new Date().toLocaleTimeString()}</small>`;
            chatLog.appendChild(newMessage);
            chatLog.scrollTop = chatLog.scrollHeight; // Auto-scroll to the latest message
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.getElementById('chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.getElementById('chat-message-submit').click();
            }
        };

        document.getElementById('chat-message-submit').onclick = function(e) {
            const messageInputDom = document.getElementById('chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({'message': message}));
            messageInputDom.value = '';
        }; 
    } else {
        console.error('Chat room identifier is not defined.');
    }

    // Event listeners for private chat links
    document.querySelectorAll('.private-chat-link').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const username = this.getAttribute('data-username');
            openChatBubble(username);
        });
    });
});