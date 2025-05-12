import React, { useEffect, useState } from 'react';
import MessageBubble from '../components/MessageBubble';
import MessageInput from '../components/MessageInput';
import '../styles/pageStyles/messages.css';
import { useParams } from 'react-router-dom';

const MessagesPage = () => {
    const { friendId } = useParams();
    const [messages, setMessages] = useState([]);
    const [friendInfo, setFriendInfo] = useState({});
    const [currentUserId, setCurrentUserId] = useState(null);

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/messages/${friendId}/`, {
                    credentials: 'include',
                });
                const data = await res.json();
                setMessages(data.messages || []);
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };

        const fetchCurrentUser = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/auth/user/', {
                    credentials: 'include',
                });
                const data = await res.json();
                setCurrentUserId(data.user.user_id);
            } catch (error) {
                console.error('Error fetching current user:', error);
            }
        };

        const fetchFriendInfo = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/profile/${friendId}/`, {
                    credentials: 'include',
                });
                const data = await res.json();
                setFriendInfo(data.user || {});
            } catch (error) {
                console.error('Error fetching friend info:', error);
            }
        };

        fetchMessages();
        fetchCurrentUser();
        fetchFriendInfo();
    }, [friendId]);

    const handleSendMessage = async (text) => {
        try {
            const res = await fetch('http://localhost:8000/api/send_message/', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ receiver_id: friendId, text }),
            });
            if (res.ok) {
                // Refresh the message list to include the newly sent message
                const updatedRes = await fetch(`http://localhost:8000/api/messages/${friendId}/`, {
                    credentials: 'include',
                });
                const updatedData = await updatedRes.json();
                setMessages(updatedData.messages || []);
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div className="messages-page">
            <div className="chat-header">
                <img src={`http://localhost:8000/media/${friendInfo.profile_picture}`} alt="Friend" className="chat-header-img" />
                <span className="chat-header-name">{friendInfo.first_name} {friendInfo.last_name}</span>
            </div>
            <div className="messages-container">
                {messages.map((msg) => (
                    <MessageBubble key={msg.message_number} message={msg} currentUserId={currentUserId} />
                ))}
            </div>
            <MessageInput onSend={handleSendMessage} />
        </div>
    );
};

export default MessagesPage;