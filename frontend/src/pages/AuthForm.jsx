import React, { useState } from 'react';
import '../styles/pageStyles/authForm.css'; // Your external CSS file
import 'boxicons/css/boxicons.min.css'; // Boxicons CDN via npm or use link in index.html

const AuthForm = () => {
  const [isRegistering, setIsRegistering] = useState(false);

  return (
    <div className={`container ${isRegistering ? 'active' : ''}`}>
      <div className="form-box login">
        <form action="#">
          <h1>Login</h1>
          <div className="input-box">
            <input type="text" placeholder="Email" required />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="password" placeholder="Password" required />
            <i className='bx bxs-lock-alt'></i>
          </div>
          <div className="forgot-link">
            <a href="#">Forgot Password?</a>
          </div>
          <button type="submit" className="btn">Login</button>
        </form>
      </div>

      <div className="form-box register">
        <form action="#">
          <h1>Registration</h1>
          <div className="input-box">
            <input type="text" placeholder="First name" required />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="text" placeholder="Last name" required />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="date" placeholder="Date of Birth" required />
            <i className='bx bxs-user'></i>
          </div>
          <div className="input-box">
            <input type="email" placeholder="Email" required />
            <i className='bx bxs-envelope'></i>
          </div>
          <div className="input-box">
            <input type="password" placeholder="Password" required />
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
