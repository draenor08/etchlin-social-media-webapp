import { useEffect, useState } from "react";
import axios from "axios";
import Topbar from "../components/Topbar";
import Sidebar from "../components/Sidebar";
import Feed from "../components/Feed";
import Rightbar from "./Rightbar";
import "../styles/componentStyles/profile.css";

export default function Profile() {
  const [profileData, setProfileData] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/get_profile/", {
          withCredentials: true,
        });
        setProfileData(res.data);
      } catch (err) {
        console.error("Error fetching profile data:", err);
      }
    };

    fetchProfile();
  }, []);

  return (
    <>
      <Topbar />
      <div className="profile">
        <Sidebar />
        <div className="profileRight">
          <div className="profileRightTop">
            <div className="profileCard">
              {profileData ? (
                <>
                  <img
                    className="profileCardImg"
                    src={profileData.profile_picture}
                    alt="Profile"
                  />
                  <div className="profileCardInfo">
                    <h2>{profileData.first_name} {profileData.last_name}</h2>
                    <p><strong>Bio:</strong> {profileData.bio}</p>
                    <p><strong>Email:</strong> {profileData.email}</p>
                    <p><strong>DOB:</strong> {profileData.dob}</p>
                  </div>
                </>
              ) : (
                <p>Loading profile...</p>
              )}
            </div>
          </div>
          <div className="profileRightBottom">
            <Feed />
            <Rightbar profile />
          </div>
        </div>
      </div>
    </>
  );
}
