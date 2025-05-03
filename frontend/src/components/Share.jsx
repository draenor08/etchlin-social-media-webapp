import React, { useState } from 'react';
import { PermMedia, EmojiEmotions } from '@mui/icons-material';
import '../styles/componentStyles/share.css';

function Share() {
    const [postText, setPostText] = useState('');
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(URL.createObjectURL(e.target.files[0]));
    };

    const handleSubmit = () => {
        // Send post to backend using POST request
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
                        <div className="shareOption">
                            <PermMedia htmlColor="tomato" className="shareIcon" />
                            <span className="shareOptionText">Photo/Video</span>
                            <input type="file" className="shareOptionInput" onChange={handleFileChange} />
                        </div>
                        <div className="shareOption">
                            <EmojiEmotions htmlColor="goldenrod" className="shareIcon" />
                            <span className="shareOptionText">Feelings/Activity</span>
                        </div>
                    </div>
                    <button className="shareButton" onClick={handleSubmit}>Post</button>
                </div>
                {file && <img src={file} alt="" className="shareImg" />}
            </div>
        </div>
    );
}

export default Share;
