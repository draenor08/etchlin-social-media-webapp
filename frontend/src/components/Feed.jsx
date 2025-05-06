import React, { useEffect, useState } from "react";
import Post from "./Post";
import Share from "./Share";
import "../styles/componentStyles/feed.css";

export default function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch("/api/posts/feed/", {
      method: "GET",
      credentials: "include", // important for session auth
    })
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data.posts)) {
          setPosts(data.posts);
        }
      })
      .catch((err) => {
        console.error("Failed to fetch posts:", err);
      });
  }, []);

  const handleLike = async (postId) => {
    try {
      const res = await fetch(`/api/posts/like/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ post_id: postId }),
      });
      if (res.ok) {
        setPosts((prev) =>
          prev.map((post) =>
            post.id === postId
              ? { ...post, liked: !post.liked, like_count: post.liked ? post.like_count - 1 : post.like_count + 1 }
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
      const res = await fetch(`/api/posts/comment/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ post_id: postId, content: commentText }),
      });
      if (res.ok) {
        const newComment = await res.json();
        setPosts((prev) =>
          prev.map((post) =>
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
        {posts.map((post) => (
          <Post key={post.id} post={post} onLike={handleLike} onComment={handleComment} />
        ))}
      </div>
    </div>
  );
}
