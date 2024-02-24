//chatbot.js

document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('btn-send-message');
    const chatBody = document.getElementById('chat-body');
    const newSessionButton = document.querySelector('.btn-new-session');
    const sessionList = document.getElementById('session-list');
    let sessionIdCounter = 0;

    // Function to create a session item with a delete button
    function createSessionItem(sessionId) {
        const sessionItem = document.createElement('li');
        sessionItem.classList.add('session-item');
        sessionItem.dataset.sessionId = sessionId;

        const sessionTitle = document.createElement('span');
        sessionTitle.textContent = `Session ${sessionId}`;
        sessionItem.appendChild(sessionTitle);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.classList.add('btn-delete-session');
        deleteButton.onclick = function() {
            sessionItem.remove(); // Remove the session item from the list
        };
        sessionItem.appendChild(deleteButton);

        sessionList.appendChild(sessionItem);

        // Clicking the session title switches to that session
        sessionTitle.onclick = () => {
            switchSession(sessionId);
        };
    }

    // Function to switch to a specific session
    function switchSession(sessionId) {
        chatBody.innerHTML = ''; // Clear the chat body
        addMessageToChat(`Switched to session ${sessionId}. How can I help you?`, 'bot');
        // Implement further functionality as needed, e.g., loading session chat history
    }

    // Start a new chat session
    newSessionButton.addEventListener('click', () => {
        sessionIdCounter++; // Increment the session counter
        createSessionItem(sessionIdCounter);
        switchSession(sessionIdCounter); // Switch to the new session
    });

    // Function to add a message to the chat body
    function addMessageToChat(text, sender = 'user') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender);
        messageDiv.textContent = text;
        chatBody.appendChild(messageDiv);
        chatBody.scrollTop = chatBody.scrollHeight; // Scroll to the latest message
    }

    // Send message on button click
    sendButton.addEventListener('click', () => {
        const messageText = chatInput.value.trim();
        if (messageText) {
            addMessageToChat(messageText);
            chatInput.value = ''; // Clear the input field
            // Placeholder for sending the message to the server and receiving a response
        }
    });

    // Send message on enter key press
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
});
