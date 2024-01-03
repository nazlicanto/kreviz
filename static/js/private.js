document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('private-chat-container');
    const chatUsername = document.getElementById('chat-username');
    const messageInput = document.getElementById('message-input');
    const messageForm = document.getElementById('message-form');
    const chatMessages = document.getElementById('chat-messages');
    const closeChatButton = document.getElementById('close-chat');
    // const initialMessagesData = JSON.parse('{{ private_chats_messages_json|safe }}');

    let currentChatUser = null;
    let messagesByUser = initialMessagesData || {}; 
 

    // Sunucudan gelen ilk mesajları yükleme
    function loadInitialMessages() {
        if (initialMessagesData) {
            for (const [username, messages, timestamp] of Object.entries(initialMessagesData)) {
                if (!messagesByUser[username]) {
                    messagesByUser[username] = [];
                }
                messagesByUser[username].push(...messages);
            }
        }
    }

    loadInitialMessages();


    document.querySelectorAll('.user').forEach(userElement => {
        userElement.addEventListener('click', () => {
            const username = userElement.getAttribute('data-username');
            openChat(username);
        });
    });

    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message && currentChatUser) {
            sendMessage(currentChatUser, message);
            messageInput.value = '';
        }
    });

    closeChatButton.addEventListener('click', () => {
        chatContainer.classList.add('hidden');
    });

    function openChat(username) {
        currentChatUser = username;
        chatUsername.textContent = username;
        chatContainer.classList.remove('hidden');
        updateChatMessages();
    }

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/priv/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if(data.type == 'chat_messages') {
            const username = data.username;
            const message = data.message;
            const timestamp = data.timestamp;


            // Mesajı yerel depolamada saklama
            if (!messagesByUser[username]) {
                messagesByUser[username] = [];
            }
            messagesByUser[username].push({ message, timestamp});
            
            // Eğer şu an açık olan sohbet bu kullanıcıysa, sohbet arayüzünü güncelle
            if (currentChatUser === username) {
            updateChatMessages();
        }
    }
    };

    function sendMessage(username, message) {
        const isPrivateChat = true;
        const recipient = currentChatUser;

        // Burada WebSocket üzerinden mesaj gönderme işlemi yapılabilir
        // Örnek: chatSocket.send(JSON.stringify({ ... }));
        chatSocket.send(JSON.stringify({
            message: message,
            username: username,
            is_private: isPrivateChat,
            recipient: recipient
            // diğerlerini de ekle
        }));

        // Yeni mesajı yerel depolamaya ekleme ve sohbet penceresini güncelleme
        if (!messagesByUser[username]) {
            messagesByUser[username] = [];
    }
        messagesByUser[username].push({ message, timestamp: new Date().toISOString() });
        updateChatMessages();
}


    function updateChatMessages() {
        chatMessages.innerHTML = '';
        if (messagesByUser[currentChatUser]) {
            messagesByUser[currentChatUser].forEach(({ message, timestamp }) => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.textContent = `${timestamp}: ${message}`;
                chatMessages.appendChild(messageElement);
            });
        }
    }
});
