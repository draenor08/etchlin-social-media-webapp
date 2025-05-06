import React, { useState } from 'react';
import '../styles/pageStyles/authForm.css'; // Your external CSS file
import 'boxicons/css/boxicons.min.css'; // Boxicons CDN via npm or use link in index.html
import api from '../api/axiosConfig'; // or wherever you set up Axios with baseURL
import { useNavigate } from 'react-router-dom';

const AuthForm = () => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [registerData, setRegisterData] = useState({
  first_name: '',
  last_name: '',
  dob: '',
  email: '',
  password: ''
  });

  const navigate = useNavigate();

  const handleLoginChange = (e) => {
    setLoginData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };
  
  const handleRegisterChange = (e) => {
    setRegisterData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('login/', loginData);
      alert("Login successful!");
      console.log(res.data);
      navigate('/');
    } catch (err) {
      alert(err.response?.data?.error || "Login failed");
    }
  };
  
  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('register/', registerData);
      alert("Registration successful!");
      console.log(res.data);
      setIsRegistering(false); // go to login
    } catch (err) {
      alert(err.response?.data?.error || "Registration failed");
    }
  };
  
  return (
    <div className={`container ${isRegistering ? 'active' : ''}`}>
      <div className="form-box login">
        <form onSubmit={handleLoginSubmit}>
          <h1>Login</h1>
          <div className="input-box">
            <input type="text" name="email" placeholder="Email" required value={loginData.email} onChange={handleLoginChange} />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="password" name="password" placeholder="Password" required value={loginData.password} onChange={handleLoginChange} />
            <i className='bx bxs-lock-alt'></i>
          </div>
          <div className="forgot-link"><p>Forgot Password?</p></div>
          <button type="submit" className="btn">Login</button>
        </form>

      </div>

      <div className="form-box register">
        <form onSubmit={handleRegisterSubmit}>
          <h1>Registration</h1>
          <div className="input-box">
            <input type="text" name="first_name" placeholder="First name" required value={registerData.first_name} onChange={handleRegisterChange} />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="text" name="last_name" placeholder="Last name" required value={registerData.last_name} onChange={handleRegisterChange} />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="date" name="dob" required value={registerData.dob} onChange={handleRegisterChange} />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="email" name="email" placeholder="Email" required value={registerData.email} onChange={handleRegisterChange} />
            <i className='bx bxs-envelope'></i>
          </div>
          <div className="input-box">
            <input type="password" name="password" placeholder="Password" required value={registerData.password} onChange={handleRegisterChange} />
            <i className='bx bxs-lock-alt'></i>
          </div>
          <button type="submit" className="btn">Register</button>
        </form>

      </div>

      <div className="toggle-box">
        <div className="toggle-panel toggle-left">
          <h1>Hello, Welcome!</h1>
          <p>Don't have an account?</p>
          <button className="btn register-btn" onClick={() => setIsRegistering(true)}>Register</button>
        </div>

        <div className="toggle-panel toggle-right">
          <h1>Welcome Back!</h1>
          <p>Already have an account?</p>
          <button className="btn login-btn" onClick={() => setIsRegistering(false)}>Login</button>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
