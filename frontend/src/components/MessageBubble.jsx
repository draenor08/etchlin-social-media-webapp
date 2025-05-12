// src/components/Messages/MessageBubble.jsx
import React from 'react';
import '../styles/pageStyles/messages.css';

function MessageBubble({ message, currentUserId }) {
    const isOwnMessage = message.sender_id === currentUserId;
    return (
        <div className={`message-bubble ${isOwnMessage ? 'own' : 'other'}`}>
            <p>{message.text}</p>
            <span className="message-timestamp">{new Date(message.timestamp).toLocaleString()}</span>
        </div>
    );
}

export default MessageBubble;