import React, { useEffect, useState } from "react";
import Post from "./Post";
import Share from "./Share";
import "../styles/componentStyles/feed.css";

export default function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/post/feed/", {
      credentials: "include",
    })
      .then(async res => {
        if (!res.ok) {
          const txt = await res.text();
          throw new Error(`HTTP ${res.status}: ${txt}`);
        }
        return res.json();
      })
      .then(data => {
        if (Array.isArray(data.posts)) {
          // transform each post object
          const shaped = data.posts.map(p => ({
            id:            p.post_id,
            user_id:       p.user_id,
            first_name:    p.first_name,            // or `${p.first_name} ${p.last_name}`
            profilePicture:p.profile_picture,
            caption:       p.caption,
            image:         p.image_url,
            date:          new Date(p.timestamp),
            like_count:    p.like_count,
            comment_count: p.comment_count,
            comments:      p.comments,
            liked:         p.liked || false         // if you return liked state
          }));
          setPosts(shaped);
        }
      })
      .catch(err => {
        console.error("Failed to fetch posts:", err);
      });
  }, []);

  const handleLike = async postId => {
    // note: now comparing p.id, not p.id === postId
    try {
      const res = await fetch("http://localhost:8000/api/like/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ post_id: postId }),
      });
      if (res.ok) {
        setPosts(prev =>
          prev.map(post =>
            post.id === postId
              ? {
                  ...post,
                  liked: !post.liked,
                  like_count:
                    post.liked ? post.like_count - 1 : post.like_count + 1,
                }
              : post
          )
        );
      }
    } catch (error) {
      console.error("Error liking post:", error);
    }
  };

  const handleComment = async (postId, commentText) => {
    try {
      const res = await fetch("http://localhost:8000/api/comment/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ post_id: postId, content: commentText }),
      });
      if (res.ok) {
        const newComment = await res.json();
        setPosts(prev =>
          prev.map(post =>
            post.id === postId
              ? { ...post, comments: [...post.comments, newComment] }
              : post
          )
        );
      }
    } catch (error) {
      console.error("Error posting comment:", error);
    }
  };

  return (
    <div className="feed">
      <div className="feedWrapper">
        <Share />
        {posts.map(post => (
          <Post
            key = {post.post_id}
            post={post}
            onLike={() => handleLike(post.id)}
            onComment={text => handleComment(post.id, text)}
          />
        ))}
      </div>
    </div>
  );
}
