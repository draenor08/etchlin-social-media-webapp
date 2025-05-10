import "../styles/componentStyles/sidebar.css";
import {
  RssFeed,
  Chat,
  PlayCircleFilledOutlined,
  Group,
  Bookmark,
  HelpOutline,
  Event,
  MessageRounded,
} from "@mui/icons-material";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Sidebar() {
  const [friends, setFriends] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFriends = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/friends/", {
          credentials: "include",
        });
        const data = await res.json();
        setFriends(data.friends || []);
      } catch (error) {
        console.error("Failed to fetch friends:", error);
      }
    };
    fetchFriends();
  }, []);

  return (
    <div className="sidebar">
      <div className="sidebarWrapper">
        <ul className="sidebarList">
          <li className="sidebarListItem">
            <RssFeed className="sidebarIcon" />
            <span className="sidebarListItemText">Feed</span>
          </li>
          <li className="sidebarListItem">
            <Chat className="sidebarIcon" />
            <span className="sidebarListItemText">Chats</span>
          </li>
          <li className="sidebarListItem">
            <PlayCircleFilledOutlined className="sidebarIcon" />
            <span className="sidebarListItemText">Videos</span>
          </li>
          <li className="sidebarListItem">
            <Group className="sidebarIcon" />
            <span className="sidebarListItemText">Groups</span>
          </li>
          <li className="sidebarListItem">
            <Bookmark className="sidebarIcon" />
            <span className="sidebarListItemText">Bookmarks</span>
          </li>
          <li className="sidebarListItem">
            <HelpOutline className="sidebarIcon" />
            <span className="sidebarListItemText">Questions</span>
          </li>
          <li className="sidebarListItem">
            <Event className="sidebarIcon" />
            <span className="sidebarListItemText">Events</span>
          </li>
        </ul>
        <button className="sidebarButton">Show More</button>
        <hr className="sidebarHr" />
        <ul className="sidebarFriendList">
          {friends.map(friend => (
            <li key={friend.user_id} className="sidebarFriendItem">
              <div className="friendDetails" onClick={() => navigate(`/messages/${friend.user_id}`)}>
                <img
                  src={`http://localhost:8000/media/${friend.profile_picture}`}
                  alt={"/assets/default-profile.png"}
                  className="sidebarFriendImg"
                />
                <span className="sidebarFriendName">
                  {friend.first_name} {friend.last_name}
                </span>
              </div>
              <MessageRounded
                className="messageIcon"
                onClick={() => navigate(`/messages/${friend.user_id}`)}
              />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
