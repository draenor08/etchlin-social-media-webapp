import { useEffect, useState } from "react";
import Topbar from "../components/Topbar";
import Sidebar from "../components/Sidebar";
import Feed from "../components/Feed";
import Rightbar from "../components/Rightbar";
import "../styles/pageStyles/home.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [userId, setUserId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
  const fetchUserData = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/auth/user/", { withCredentials: true });
      const user = res.data.user;
      setUserId(user.user_id);
    } catch (err) {
      console.error("Failed to fetch user info", err);
      navigate("/auth");
    }
  };

  fetchUserData();
}, [navigate]);



  const handleNotifClick = () => {
    console.log("Notifications clicked");
  };

  const logout = async () => {
    try {
      await axios.post("http://127.0.0.1:8000/api/logout/", {}, { withCredentials: true });
      navigate("/auth");
    } catch (err) {
      console.error("Logout failed", err);
    }
  };

  return (
    <>
      <Topbar
        userId={userId}
        handleNotifClick={handleNotifClick}
        logout={logout}
      />
      <div className="homeContainer">
        <Sidebar />
        <Feed/>
        <Rightbar />
      </div>
    </>
  );
}
