import React, { useState } from 'react';
import { MoreVert } from '@mui/icons-material';
import '../styles/componentStyles/post.css';

function Post({ post, onLike, onComment }) {
    const [commentText, setCommentText] = useState('');
    const [showComments, setShowComments] = useState(false);

    const handleLikeClick = () => {
        onLike(post.post_id);
    };

    const handleCommentSubmit = () => {
        if (commentText.trim()) {
            onComment(post, commentText);
            setCommentText('');
        }
    };

    const profilePicUrl = post.profile_picture ? `http://localhost:8000${post.profile_picture}` : '/assets/default_profile.png';
    const postImageUrl = post.image_url ? `http://localhost:8000${post.image_url}` : '';

    return (
        <div className="post">
            <div className="postWrapper">
                <div className="postTop">
                    <div className="postTopLeft">
                        <img src={profilePicUrl} alt="Profile" className="postProfileImg" />
                        <span className="postUsername">{post.first_name}</span>
                        <span className="postDate">{new Date(post.timestamp).toLocaleDateString()}</span>
                    </div>
                    <div className="postTopRight">
                        <MoreVert />
                    </div>
                </div>
                <div className="postCenter">
                    {post.caption && <span className="postText">{post.caption}</span>}
                    {post.image_url && <img src={postImageUrl} alt="Post" className="postImg" />}
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
                            {post.comments?.map((c) => (
                                <div key={c.comment_id} className="comment">
                                    <strong>{c.first_name}:</strong> {c.content}
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
