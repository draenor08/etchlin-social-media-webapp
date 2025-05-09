import React from 'react';
import { Link } from 'react-router-dom';
import { BellIcon, User } from 'lucide-react';
import '../styles/componentStyles/topbar.css';

const Topbar = ({ userId, userProfilePic, handleNotifClick, logout }) => {
  return (
    <header className="topbar">
      <div className="topbar-left">
        <Link to="/" className="logo">Etchlin</Link>
      </div>
      <div className="topbar-center">
        <input type="text" placeholder="Search..." className="search-input" />
      </div>
      <div className="topbar-right">
        <button className="icon-button" onClick={handleNotifClick}>
          <BellIcon size={20} />
        </button>
        <Link to={`api/profile/${userId}`} className="profile-link">
          <User className="profile-pic" />
        </Link>
        <button className="logout-button" onClick={logout}>Logout</button>
      </div>
    </header>
  );
};

export default Topbar;
