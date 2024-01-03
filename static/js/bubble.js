let messagesByUser = {};

document.addEventListener('DOMContentLoaded', () => {
    // HTML Elements
    const chatBubble = document.getElementById('chat-bubble');
    const chatOpenButton = document.getElementById('chat_open');
    const chatCloseButton = document.querySelector('.close-btn');
    const chatForm = document.getElementById('private-chat-form');
    const chatInput = document.getElementById('private-chat-message-input');
    const chatLog = document.getElementById('private-chat-log');

    // Open chat bubble
    chatOpenButton.addEventListener('click', () => {
        chatBubble.style.display = 'block';
    });

    // Initialize WebSocket
    const chatRoomIdentifier = document.body.getAttribute('data-room-name');
    const protocolPrefix = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const chatSocket = new WebSocket(
        protocolPrefix + window.location.host + '/ws/chat/' + chatRoomIdentifier + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const username = data['username'];
        const message = data['message'];

        storeMessage(username, message, new Date().toLocaleTimeString());
        updateChatLog(username);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        // Implement reconnection logic here if needed
    };

    chatForm.addEventListener('submit', (event) => {
        event.preventDefault();
        sendPrivateMessage();
    });

    function storeMessage(username, message, timestamp) {
        if (!messagesByUser[username]) {
            messagesByUser[username] = [];
        }
        messagesByUser[username].push({ message, timestamp });
    }

    document.body.addEventListener('click', (event) => {
        if (event.target.classList.contains('username')) {
            const selectedUsername = event.target.getAttribute('data-username');
            openChatBubble(selectedUsername);
        }
    });

    function openChatBubble(username) {
        const bubbleUsername = document.getElementById('bubble-username');
        bubbleUsername.textContent = username;
        chatBubble.style.display = 'block';
        updateChatLog(username);
    }

    function updateChatLog(username) {
        const messages = messagesByUser[username] || [];
        chatLog.innerHTML = '';
        messages.forEach(messageData => {
            const messageDiv = document.createElement('div');
            messageDiv.textContent = `${messageData.message} ${messageData.timestamp}`;
            chatLog.appendChild(messageDiv);
        });
    }

    function sendPrivateMessage() {
        const message = chatInput.value.trim();
        const recipient = document.getElementById('bubble-username').textContent;
        if (message && recipient) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'private': true,
                'recipient': recipient
            }));

            storeMessage(recipient, message, new Date().toLocaleTimeString());
            updateChatLog(recipient);
            chatInput.value = '';
        }
    }

    // Removed redundant event listener for close button
    chatCloseButton.addEventListener('click', () => {
        chatBubble.style.display = 'none';
    });
});
