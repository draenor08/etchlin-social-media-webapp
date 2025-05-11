import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/componentStyles/searchbar.css';

const SearchBar = () => {
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);
  const [showResults, setShowResults] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    const query = e.target.value;
    setInput(query);
    if (query.length > 1) {
      try {
        const res = await axios.get(`http://localhost:8000/api/search/?q=${query}`, {
          withCredentials: true
        });
        setResults(res.data);
        setShowResults(true);
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    } else {
      setResults([]);
      setShowResults(false);
    }
  };

  const handleUserSelect = (userId) => {
    setShowResults(false);
    setInput("");
    navigate(`/profile/${userId}`);
  };

  return (
    <div className="search-bar">
      <input
        value={input}
        onChange={handleSearch}
        placeholder="Search users..."
        onFocus={() => setShowResults(results.length > 0)}
        onBlur={() => setTimeout(() => setShowResults(false), 150)}
      />
      {showResults && (
        <ul className="search-results">
          {results.map(user => (
            <li key={user.user_id} onClick={() => handleUserSelect(user.user_id)}>
              <img src={`http://localhost:8000/media/${user.profile_picture}`} alt="Profile" />
              <span>{user.first_name} {user.last_name}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SearchBar;
