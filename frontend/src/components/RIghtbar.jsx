// src/components/Rightbar.js
import React, { useEffect, useState } from 'react';
import "../styles/componentStyles/rightbar.css";
import { Link } from "react-router-dom";

export default function Rightbar({ profile }) {
    const [requests, setRequests] = useState([]);
    const [friends, setFriends] = useState([]);

    // Fetch friend requests
    useEffect(() => {
        const fetchRequests = async () => {
            try {
                const res = await fetch("http://localhost:8000/api/friends/requests/", {
                    credentials: "include",
                });
                const data = await res.json();
                setRequests(data.requests || []);
            } catch (error) {
                console.error("Failed to fetch friend requests:", error);
            }
        };

        // Fetch accepted friends
        const fetchFriends = async () => {
            try {
                const res = await fetch("http://localhost:8000/api/friends/", {
                    credentials: "include",
                });
                const data = await res.json();
                setFriends(data.friends || []);
            } catch (error) {
                console.error("Failed to fetch friends:", error);
            }
        };

        fetchRequests();
        fetchFriends();
    }, []);

    const handleRequestResponse = async (requesterId, action) => {
        try {
            const res = await fetch(`http://localhost:8000/api/${requesterId}/respond/`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ requester_id: requesterId, action }),
            });
            if (res.ok) {
                // Remove the processed request from the list
                setRequests(requests.filter(req => req.user_id !== requesterId));
            }
        } catch (error) {
            console.error("Error responding to friend request:", error);
        }
    };

    return (
        <div className="rightbar">
            <div className="rightbarWrapper">
                <h2 className="rightbarMainTitle">Notifications</h2>

                {/* Friend Requests */}
                <h4 className="rightbarSectionTitle">Friend Requests</h4>
                <ul className="rightbarFriendList">
                    {requests.length > 0 ? (
                        requests.map((req) => (
                            <li key={req.user_id} className="requestItem">
                                <img
                                    src={`http://localhost:8000/media/${req.profile_picture}`}
                                    alt="Profile"
                                    className="requestImg"
                                />
                                <span className="requestName">
                                    {req.first_name} {req.last_name}
                                </span>
                                <div className="requestActions">
                                    <button onClick={() => handleRequestResponse(req.user_id, 'accept')} className="acceptBtn">Accept</button>
                                    <button onClick={() => handleRequestResponse(req.user_id, 'reject')} className="rejectBtn">Reject</button>
                                </div>
                            </li>
                        ))
                    ) : (
                        <p className="noRequests">No pending requests</p>
                    )}
                </ul>

                {/* Friends List */}
                <h4 className="rightbarSectionTitle">Your Friends</h4>
                <ul className="rightbarFriendList">
                    {friends.map(friend => (
                        <li key={friend.user_id} className="rightbarFriendItem">
                            <img
                                src={`http://localhost:8000/media/${friend.profile_picture}`}
                                alt="Profile"
                                className="rightbarFriendImg"
                            />
                            <Link to={`/profile/${friend.user_id}`} className="rightbarFriendName">
                                {friend.first_name} {friend.last_name}
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
