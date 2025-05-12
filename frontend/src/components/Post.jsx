import React, { useState } from 'react';
import { MoreVert } from '@mui/icons-material';
import '../styles/componentStyles/post.css';

function Post({ post, onLike, onComment, currentUserId, refreshFeed }) {
    const [commentText, setCommentText] = useState('');
    const [showComments, setShowComments] = useState(false);
    const [showOptions, setShowOptions] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editedCaption, setEditedCaption] = useState(post.caption);

    const handleLikeClick = () => {
        onLike(post.id);
    };

    const handleCommentSubmit = () => {
        if (commentText.trim()) {
            onComment(post.id, commentText)
                .then(() => setCommentText(''))
                .catch(error => console.error('Request failed', error));
        }
    };

    const handleEditSubmit = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/post/edit/', {
                method: 'PATCH',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ post_id: post.id, caption: editedCaption })
            });
            if (response.ok) {
                setIsEditing(false);
                refreshFeed();
            }
        } catch (error) {
            console.error('Error updating post:', error);
        }
    };

    const handleDeletePost = async () => {
        if (window.confirm('Are you sure you want to delete this post?')) {
            try {
                const response = await fetch('http://localhost:8000/api/post/delete/', {
                    method: 'DELETE',
                    credentials: 'include',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ post_id: post.id })
                });
                if (response.ok) {
                    refreshFeed();
                }
            } catch (error) {
                console.error('Error deleting post:', error);
            }
        }
    };
    
    const profilePicUrl = post.profilePicture
    ? `http://localhost:8000${post.profilePicture}`
    : post.profilePicture;

    const postImageUrl = post.image ? `http://localhost:8000${post.image}` : '';

    return (
        <div className="post">
            <div className="postWrapper">
                <div className="postTop">
                    <div className="postTopLeft">
                        <img src={profilePicUrl} alt="Profile" className="postProfileImg" />
                        <span className="postUsername">{post.first_name}</span>
                        <span className="postDate">{new Date(post.date).toLocaleDateString()}</span>
                    </div>
                    {post.user_id === currentUserId && (
                        <div className="postTopRight" onClick={() => setShowOptions(!showOptions)}>
                            <MoreVert />
                            {showOptions && (
                                <div className="postOptions">
                                    <span onClick={() => setIsEditing(true)}>Edit Post</span>
                                    <span onClick={handleDeletePost}>Delete Post</span>
                                </div>
                            )}
                        </div>
                    )}
                </div>
                <div className="postCenter">
                    {isEditing ? (
                        <div className="editContainer">
                            <textarea
                                value={editedCaption}
                                onChange={(e) => setEditedCaption(e.target.value)}
                                className="editTextarea"
                            />
                            <button className="editSubmitBtn" onClick={handleEditSubmit}>Save</button>
                            <button className="editCancelBtn" onClick={() => setIsEditing(false)}>Cancel</button>
                        </div>
                    ) : (
                        <>
                            {post.caption && <span className="postText">{post.caption}</span>}
                            {post.image && <img src={postImageUrl} alt="Post" className="postImg" />}
                        </>
                    )}
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
                            {post.comments?.map(c => (
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
