import React, { useState, useEffect } from 'react';
import { PermMedia } from '@mui/icons-material';
import axios from 'axios';
import '../styles/componentStyles/share.css';

export default function Share({ refreshFeed }) {
    const [postText, setPostText] = useState('');
    const [file, setFile] = useState(null);
    const [filePreview, setFilePreview] = useState(null);
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await axios.get("http://localhost:8000/api/auth/user/", {
                    withCredentials: true,
                });
                setUserData(res.data.user);
            } catch (err) {
                console.error("Error fetching profile data:", err);
            }
        };
        fetchUser();
    }, []);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        setFilePreview(URL.createObjectURL(selectedFile));
    };

    const handleSubmit = async () => {
        if (!postText && !file) return;

        const formData = new FormData();
        formData.append('caption', postText);
        if (file) {
            formData.append('image', file);
        }

        try {
            const response = await fetch('http://localhost:8000/api/post/create/', {
                method: 'POST',
                credentials: 'include',
                body: formData
            });

            if (response.ok) {
                setPostText('');
                setFile(null);
                setFilePreview(null);
                refreshFeed();
                console.log("Post created successfully");
            } else {
                const errorData = await response.json();
                console.error("Post failed:", errorData);
            }
        } catch (error) {
            console.error("Error submitting post:", error);
        }
    };

    const profilePicUrl = userData?.profile_picture
        ? `http://localhost:8000/media/${userData.profile_picture}`
        : '/assets/default_profile.png';

    return (
        <div className="share">
            <div className="shareWrapper">
                <div className="shareTop">
                    {userData && (
                        <img 
                            src={profilePicUrl} 
                            alt="Profile" 
                            className="shareProfileImg" 
                        />
                    )}
                    <input
                        type="text"
                        placeholder="What's on your mind?"
                        value={postText}
                        onChange={(e) => setPostText(e.target.value)}
                        className="shareInput"
                    />
                </div>

                <hr className="shareHr" />

                <div className="shareBottom">
                    <div className="shareOptions">
                        <label className="shareOption">
                            <PermMedia className="shareIcon" />
                            <span className="shareOptionText">Photo</span>
                            <input 
                                type="file" 
                                className="shareFileInput" 
                                onChange={handleFileChange} 
                                style={{ display: 'none' }} 
                            />
                        </label>
                    </div>
                    <button className="shareButton" onClick={handleSubmit}>Post</button>
                </div>

                {filePreview && (
                    <div className="sharePreviewWrapper">
                        <img src={filePreview} alt="Preview" className="shareImg" />
                        <button
                            className="sharePreviewRemove"
                            onClick={() => {
                                setFile(null);
                                setFilePreview(null);
                            }}
                        >
                            ✖
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
