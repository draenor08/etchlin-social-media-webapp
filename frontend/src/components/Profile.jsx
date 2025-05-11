import React, { useState, useEffect, useCallback } from 'react';
import { MoreVert } from '@mui/icons-material';
import '../styles/componentStyles/profile.css';

const Profile = ({ profileData, isCurrentUser, refreshProfile, userPosts }) => {
    const [showOptions, setShowOptions] = useState(false);
    const [isEditingBio, setIsEditingBio] = useState(false);
    const [newBio, setNewBio] = useState(profileData.bio || '');
    const [selectedFile, setSelectedFile] = useState(null);
    const [friendStatus, setFriendStatus] = useState(null);
    const [friendCount, setFriendCount] = useState(0);

    const fetchFriendStatus = useCallback(async () => {
        try {
            const res = await fetch(`http://localhost:8000/api/friends/status/${profileData.user_id}/`, {
                credentials: 'include'
            });
            const data = await res.json();
            setFriendStatus(data.status);
        } catch (error) {
            console.error('Error fetching friend status:', error);
        }
    }, [profileData.user_id]);

    const fetchFriendCount = useCallback(async () => {
        try {
            const res = await fetch(`http://localhost:8000/api/friends/count/${profileData.user_id}/`, {
                credentials: 'include'
            });
            const data = await res.json();
            setFriendCount(data.count || 0);
        } catch (error) {
            console.error('Error fetching friend count:', error);
        }
    }, [profileData.user_id]);

    useEffect(() => {
        if (!isCurrentUser) {
            fetchFriendStatus();
            fetchFriendCount();
        }
    }, [isCurrentUser, fetchFriendStatus, fetchFriendCount]);

    const handleFriendAction = async () => {
        try {
            const endpoint = 
                friendStatus === 'pending' ? 'friend/remove' :
                friendStatus === 'accepted' ? 'friend/remove' :
                `${profileData.user_id}/send_request`;

            const res = await fetch(`http://localhost:8000/api/${endpoint}/`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ receiver_id: profileData.user_id })
            });
            
            if (res.ok) {
                fetchFriendStatus();
                fetchFriendCount();
            }
        } catch (error) {
            console.error('Error handling friend action:', error);
        }
    };

    // Function to handle profile picture upload
    const handleProfilePictureUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('profile_picture', selectedFile);

        try {
            const response = await fetch('http://localhost:8000/api/profile/upload/picture/', {
                method: 'POST',
                credentials: 'include',
                body: formData
            });
            if (response.ok) {
                setSelectedFile(null);
                refreshProfile();
            }
        } catch (error) {
            console.error('Error uploading profile picture:', error);
        }
    };

    // Function to handle bio submission
    const handleBioSubmit = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/profile/update/bio/', {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bio: newBio })
            });
            if (response.ok) {
                setIsEditingBio(false);
                refreshProfile();
            }
        } catch (error) {
            console.error('Error updating bio:', error);
        }
    };

    return (
        <div className="profile-container">
            <div className="profile-header">
                <img 
                    src={`http://localhost:8000/media/${profileData.profile_picture}`} 
                    alt="Profile" 
                    className="profile-picture" 
                />
                <div className="profile-details">
                    <h2>{profileData.first_name} {profileData.last_name}</h2>
                    <p>Email: {profileData.email}</p>
                    <p>Date of Birth: {profileData.date_of_birth}</p>
                    <p>Bio: {profileData.bio || 'No bio available'}</p>
                    <p>Friends: {friendCount}</p>
                </div>
                {isCurrentUser ? (
                    <div className="profile-options" onClick={() => setShowOptions(!showOptions)}>
                        <MoreVert />
                        {showOptions && (
                            <div className="options-menu">
                                <span className="optionText" onClick={() => setIsEditingBio(true)}>Edit Bio</span>
                                <label className="optionText" onClick={(e) => e.stopPropagation()}>
                                    Upload Profile Picture
                                    <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
                                </label>
                                <button className="saveBtn" onClick={() => handleProfilePictureUpload()}>Save Picture</button>
                            </div>
                        )}
                    </div>
                ) : (
                    <button className="friend-button" onClick={handleFriendAction}>
                        {friendStatus === 'accepted' ? 'Remove Friend' : friendStatus === 'pending' ? 'Cancel Request' : 'Add Friend'}
                    </button>
                )}
            </div>

            {isEditingBio && (
                <div className="edit-bio-container">
                    <textarea value={newBio} onChange={(e) => setNewBio(e.target.value)} placeholder="Edit your bio..." />
                    <button onClick={handleBioSubmit}>Save</button>
                    <button onClick={() => setIsEditingBio(false)}>Cancel</button>
                </div>
            )}

            <div className="user-posts">
                <h3>{profileData.first_name}'s Posts</h3>
                {userPosts.length > 0 ? (
                    <div className="posts-grid">
                        {userPosts.map(post => (
                            <div key={post.post_id} className="post-item">
                                <img src={`http://localhost:8000/${post.image_url}`} alt="Post" />
                                <p>{post.caption}</p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>No posts yet</p>
                )}
            </div>
        </div>
    );
};

export default Profile;