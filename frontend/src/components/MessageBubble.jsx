import React from 'react';
import '../styles/pageStyles/messages.css';

function MessageBubble({ message, currentUserId }) {
    const isOwnMessage = message.sender_id === currentUserId;
    let formattedTimestamp = "Unknown time";

    try {
        const date = new Date(message.timestamp);
        if (!isNaN(date)) {
            formattedTimestamp = date.toLocaleString();
        }
    } catch (error) {
        console.error("Error formatting timestamp:", error);
    }

    return (
        <div className={`message-bubble ${isOwnMessage ? 'own' : 'other'}`}>
            <p>{message.text}</p>
            <span className="message-timestamp">{formattedTimestamp}</span>
        </div>
    );
}

export default MessageBubble;