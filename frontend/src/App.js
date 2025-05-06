import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AuthForm from './pages/AuthForm';
import HomePage from './pages/Home';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/auth" element={<AuthForm />} />
        <Route path="/" element={<PrivateRoute><HomePage /></PrivateRoute>} />
        {/* Add other protected routes similarly */}
      </Routes>
    </Router>
  );
}

export default App;