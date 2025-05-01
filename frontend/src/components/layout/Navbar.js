import NavbarStyles from "../styles/components/NavbarStyles";  
import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <NavbarStyles>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/profile">Profile</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/signup">Signup</Link></li>
        </ul>
      </nav>
    </NavbarStyles>
  );
}

export default Navbar;
