import React, { useState, useEffect } from "react";
import axios from "axios";

function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/api/user/1") // Replace with actual user ID
      .then((response) => setUser(response.data))
      .catch((error) => console.error("Error fetching user", error));
  }, []);

  return (
    <div>
      <h1>Profile Page</h1>
      {user && (
        <div>
          <h2>{user.first_name} {user.last_name}</h2>
          <p>{user.bio}</p>
          <img src={user.profile_picture} alt="Profile" />
          {/* Display user posts */}
        </div>
      )}
    </div>
  );
}

export default Profile;
