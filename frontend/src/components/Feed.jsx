import React, { useEffect, useState, useCallback } from "react";
import Post from "./Post";
import Share from "./Share";
import "../styles/componentStyles/feed.css";
import axios from 'axios';

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);

  useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await axios.get("http://localhost:8000/api/auth/user/", {
                    withCredentials: true,
                });
                setCurrentUserId(res.data.user.user_id);
            } catch (err) {
                console.error("Error fetching profile data:", err);
            }
        };
        fetchUser();
    }, []);

  const fetchPosts = useCallback(() => {
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
          const shaped = data.posts.map(p => ({
            id: p.post_id,
            user_id: p.user_id,
            first_name: p.first_name,
            profilePicture: p.profile_picture,
            caption: p.caption,
            image: p.image_url,
            date: new Date(p.timestamp),
            like_count: p.like_count,
            comment_count: p.comment_count,
            comments: p.comments,
            liked: p.liked || false,
          }));
          setPosts(shaped);
        }
      })
      .catch(err => {
        console.error("Failed to fetch posts:", err);
      });
  }, []);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const handleLike = async postId => {
    try {
      const res = await fetch("http://localhost:8000/api/like/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ post_id: postId }),
      });

      if (res.ok) {
        setPosts(prevPosts =>
          prevPosts.map(post =>
            post.id === postId
              ? {
                  ...post,
                  liked: !post.liked,
                  like_count: post.liked ? post.like_count - 1 : post.like_count + 1,
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
      const res = await fetch("http://localhost:8000/api/comment/create/", {
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
        <Share refreshFeed={fetchPosts} />
        {posts.map(post => (
          <Post 
          key={post.id} 
          post={post} 
          onLike={handleLike} 
          currentUserId={currentUserId} 
          onComment={handleComment}  
          refreshFeed={fetchPosts}
          />
        ))}
      </div>
    </div>
  );
}
