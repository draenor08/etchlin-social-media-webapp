import React from 'react';
import { Search, Person, Chat, Notifications } from '@mui/icons-material';
import '../styles/componentStyles/topbar.css';

function Topbar() {
    return (
        <div className="topbar">
            <div className="topbarWrapper">
                <div className="topbarLeft">
                    <span className="logo">Etchlin</span>
                </div>
                <div className="topbarCenter">
                    <div className="searchbar">
                        <Search className="searchIcon" />
                        <input placeholder="Search for friends, posts..." className="searchInput" />
                    </div>
                </div>
                <div className="topbarRight">
                    <div className="topbarIcons">
                        <div className="topbarIconItem">
                            <Notifications />
                            <span className="topbarIconBadge">1</span>
                        </div>
                        <div className="topbarIconItem">
                            <Chat />
                        </div>
                        <div className="topbarIconItem">
                            <Person />
                        </div>
                    </div>
                    <img src="path_to_your_profile_pic" alt="" className="topbarImg" />
                </div>
            </div>
        </div>
    );
}

export default Topbar;
