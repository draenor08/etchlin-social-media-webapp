import React, { useState, useEffect } from "react";
import axios from "axios";

function Home() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/posts") // Replace with your backend API
      .then((response) => setPosts(response.data))
      .catch((error) => console.error("Error fetching posts", error));
  }, []);

  return (
    <div>
      <h1>Home Page</h1>
      <div>
        {posts.map((post) => (
          <div key={post.post_id}>
            <h2>{post.caption}</h2>
            <img src={post.image_url} alt="Post" />
            {/* Display other post details */}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
