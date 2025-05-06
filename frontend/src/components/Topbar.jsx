import SearchBar from './SearchBar';
import '../styles/componentStyles/topbar.css';

const TopBar = ({ onUserSelect }) => (
  <div className="top-bar">
    <h1>Etchlin</h1>
    <SearchBar onUserSelect={onUserSelect} />
    <i className="bx bx-bell"></i> {/* Notification placeholder */}
  </div>
);

export default TopBar;