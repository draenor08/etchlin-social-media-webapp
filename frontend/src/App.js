import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AuthForm from './pages/AuthForm';
import HomePage from './pages/Home';
import PrivateRoute from './components/PrivateRoute';
import ProfilePage from './pages/ProfilePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/auth" element={<AuthForm />} />
        <Route path="/" element={<PrivateRoute><HomePage /></PrivateRoute>} />
        <Route path="/profile/:id" element={<PrivateRoute><ProfilePage/></PrivateRoute>} />
      </Routes>
    </Router>
  );
}

export default App;