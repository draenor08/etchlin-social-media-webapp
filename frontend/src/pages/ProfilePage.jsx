import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

const ProfilePage = () => {
  const { id } = useParams();
  const [user, setUser] = useState({});
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/profile/${id}/`, { withCredentials: true }).then(res => {
      setUser(res.data.user);
      setPosts(res.data.posts);
    });
  }, [id]);

  return (
    <div>
      <ProfileComponent user={user} />
      <div className="post-list">
        {posts.map(post => (
          <div key={post.post_id}>
            <img src={`http://localhost:8000/media/${post.image}`} />
            <p>{post.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProfilePage;
