// src/components/Messages/MessageInput.jsx
import React, { useState } from 'react';
import '../styles/pageStyles/messages.css';

function MessageInput({ onSend }) {
    const [text, setText] = useState('');

    const handleSend = () => {
        if (text.trim()) {
            onSend(text);
            setText('');
        }
    };

    return (
        <div className="message-input-container">
            <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type a message..."
                className="message-input"
            />
            <button onClick={handleSend} className="send-button">
                Send
            </button>
        </div>
    );
}

export default MessageInput;
