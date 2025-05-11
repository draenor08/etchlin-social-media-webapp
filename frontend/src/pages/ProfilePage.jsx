import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import Profile from '../components/Profile';

const ProfilePage = () => {
    const { id } = useParams();
    const [profileData, setProfileData] = useState(null);
    const [isCurrentUser, setIsCurrentUser] = useState(false);
    const [userPosts, setUserPosts] = useState([]);

    const fetchProfileData = useCallback(async () => {
        try {
            // Fetch profile data
            const res = await fetch(`http://localhost:8000/api/profile/${id}/`, {
                credentials: 'include',
            });
            const profileData = await res.json();
            setProfileData(profileData.user);

            const authRes = await fetch('http://localhost:8000/api/auth/user/', {
                credentials: 'include',
            });
            if (authRes.ok) {
                const authData = await authRes.json();
                if (authData.user && authData.user.user_id) {
                    setIsCurrentUser(String(authData.user.user_id) === id);
                }
            }

            // Fetch user's posts
            const postsRes = await fetch(`http://localhost:8000/api/posts/user/${id}/`, {
                credentials: 'include',
            });
            const postsData = await postsRes.json();
            setUserPosts(postsData.posts || []);
        } catch (error) {
            console.error('Error fetching profile data:', error);
        }
    }, [id]);

    useEffect(() => {
        fetchProfileData();
    }, [fetchProfileData]);

    return profileData ? (
        <Profile 
            profileData={profileData} 
            isCurrentUser={isCurrentUser} 
            userPosts={userPosts} 
            refreshProfile={fetchProfileData} 
        />
    ) : (
        <p>Loading profile...</p>
    );
};

export default ProfilePage;
