import axios from 'axios';
import { useState } from 'react';
import '../styles/componentStyles/searchbar.css';

const SearchBar = ({ onUserSelect }) => {
  const [input, setInput] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const res = await axios.get(`http://localhost:8000/api/search/?q=${input}`, { withCredentials: true });
    setResults(res.data);
  };

  return (
    <div>
      <input value={input} onChange={e => setInput(e.target.value)} placeholder="Search users..." />
      <button onClick={handleSearch}>🔍</button>
      <ul>
        {results.map(user => (
          <li key={user.user_id} onClick={() => onUserSelect(user.user_id)}>
            <img src={`http://localhost:8000/media/${user.profile_picture}`} width="30" />
            {user.first_name} {user.last_name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchBar;
