import React from 'react';
import { MoreVert } from '@mui/icons-material';
import '../styles/componentStyles/post.css';

function Post({ post }) {
    return (
        <div className="post">
            <div className="postWrapper">
                <div className="postTop">
                    <div className="postTopLeft">
                        <img src={post.userProfilePic} alt="" className="postProfileImg" />
                        <span className="postUsername">{post.username}</span>
                        <span className="postDate">{post.date}</span>
                    </div>
                    <div className="postTopRight">
                        <MoreVert />
                    </div>
                </div>
                <div className="postCenter">
                    <span className="postText">{post.text}</span>
                    {post.image && <img src={post.image} alt="" className="postImg" />}
                </div>
                <div className="postBottom">
                    <div className="postBottomLeft">
                        <button className="likeBtn">Like</button>
                        <button className="commentBtn">Comment</button>
                    </div>
                    <div className="postBottomRight">
                        <span className="postLikeCount">{post.likes} likes</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Post;
