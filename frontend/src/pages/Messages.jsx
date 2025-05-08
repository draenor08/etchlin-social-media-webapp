import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/pageStyles/messages.css';

export default function MessagesPage() {
    const { otherUserId } = useParams();
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState("");
    const [friend, setFriend] = useState({ name: "", profilePicture: "" });
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Fetch conversation history
        fetch(`/api/${otherUserId}/messages/`)
            .then(res => res.json())
            .then(data => {
                if (data.messages) {
                    setMessages(data.messages);
                    if (data.messages.length > 0) {
                        const firstMsg = data.messages[0];
                        setFriend({
                            name: firstMsg.sender_user_id === otherUserId ? firstMsg.sender_user_id : "Friend",
                            profilePicture: firstMsg.profile_picture || "/default-profile.jpg"
                        });
                    }
                }
            });
    }, [otherUserId]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSendMessage = () => {
        if (message.trim()) {
            fetch('/api/send_message/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ receiver_id: otherUserId, text: message })
            }).then(() => {
                setMessages([...messages, { sender_id: 0, content: message, timestamp: new Date().toISOString() }]);
                setMessage("");
            });
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <img src={friend.profilePicture} alt="Friend" className="chat-header-img" />
                <span className="chat-header-name">{friend.name}</span>
            </div>
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-message ${msg.sender_id === 0 ? 'self' : 'friend'}`}>
                        {msg.content}
                        <span className="chat-timestamp">{new Date(msg.timestamp).toLocaleTimeString()}</span>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            <div className="chat-input">
                <input 
                    type="text" 
                    value={message} 
                    onChange={(e) => setMessage(e.target.value)} 
                    placeholder="Type a message..." 
                />
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    );
}