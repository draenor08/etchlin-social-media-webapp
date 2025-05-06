import React, { useState } from 'react';
import { MoreVert } from '@mui/icons-material';
import '../styles/componentStyles/post.css';

function Post({ post, onLike, onComment }) {
    const [commentText, setCommentText] = useState('');
    const [showComments, setShowComments] = useState(false);

    const handleLikeClick = () => {
        onLike(post.id);
    };

    const handleCommentSubmit = () => {
        if (commentText.trim()) {
            onComment(post.id, commentText);
            setCommentText('');
        }
    };

    return (
        <div className="post">
            <div className="postWrapper">
                <div className="postTop">
                    <div className="postTopLeft">
                        <img src={post.user_profile_pic} alt="" className="postProfileImg" />
                        <span className="postUsername">{post.user_name}</span>
                        <span className="postDate">{post.created_at}</span>
                    </div>
                    <div className="postTopRight">
                        <MoreVert />
                    </div>
                </div>
                <div className="postCenter">
                    {post.caption && <span className="postText">{post.caption}</span>}
                    {post.image_url && <img src={post.image_url} alt="" className="postImg" />}
                </div>
                <div className="postBottom">
                    <div className="postBottomLeft">
                        <button className="likeBtn" onClick={handleLikeClick}>
                            {post.liked ? 'Unlike' : 'Like'}
                        </button>
                        <button className="commentBtn" onClick={() => setShowComments(!showComments)}>
                            Comment
                        </button>
                    </div>
                    <div className="postBottomRight">
                        <span className="postLikeCount">{post.like_count} likes</span>
                    </div>
                </div>

                {showComments && (
                    <div className="postComments">
                        <div className="existingComments">
                            {post.comments?.map((c, index) => (
                                <div key={index} className="comment">
                                    <strong>{c.user_name}:</strong> {c.content}
                                </div>
                            ))}
                        </div>
                        <div className="addComment">
                            <input
                                type="text"
                                placeholder="Write a comment..."
                                value={commentText}
                                onChange={(e) => setCommentText(e.target.value)}
                                className="commentInput"
                            />
                            <button onClick={handleCommentSubmit} className="commentSubmitBtn">
                                Post
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Post;
