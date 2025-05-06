import React, { useState } from 'react';
import { PermMedia } from '@mui/icons-material';
import '../styles/componentStyles/share.css';

function Share() {
    const [postText, setPostText] = useState('');
    const [file, setFile] = useState(null);
    const [filePreview, setFilePreview] = useState(null);

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
            const response = await fetch('/api/posts/create/', {
                method: 'POST',
                credentials: 'include',
                body: formData
            });

            if (response.ok) {
                setPostText('');
                setFile(null);
                setFilePreview(null);
                // Optionally refresh feed
            } else {
                console.error("Post failed");
            }
        } catch (error) {
            console.error("Error submitting post:", error);
        }
    };

    return (
        <div className="share">
            <div className="shareWrapper">
                <div className="shareTop">
                    <img src="path_to_profile_pic" alt="" className="shareProfileImg" />
                    <input 
                        placeholder="What's on your mind?" 
                        className="shareInput" 
                        value={postText}
                        onChange={(e) => setPostText(e.target.value)}
                    />
                </div>
                <hr className="shareHr" />
                <div className="shareBottom">
                    <div className="shareOptions">
                        <label className="shareOption">
                            <PermMedia htmlColor="tomato" className="shareIcon" />
                            <span className="shareOptionText">Photo</span>
                            <input 
                                type="file" 
                                className="shareOptionInput" 
                                onChange={handleFileChange} 
                                style={{ display: 'none' }}
                            />
                        </label>
                    </div>
                    <button className="shareButton" onClick={handleSubmit}>Post</button>
                </div>
                {filePreview && <img src={filePreview} alt="preview" className="shareImg" />}
            </div>
        </div>
    );
}

export default Share;
