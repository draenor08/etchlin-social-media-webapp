import { createGlobalStyle } from "styled-components";

// Define the global styles
const GlobalStyles = createGlobalStyle`
  /* Reset default margin and padding for all elements */
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  /* Set the background and font for the body */
  body {
    font-family: 'Arial', sans-serif; /* You can use any font you prefer */
    background-color: #f4f4f4;  /* Light background color */
    color: #333; /* Dark text color for readability */
    line-height: 1.6;
  }

  /* Set basic styles for links */
  a {
    text-decoration: none;
    color: inherit; /* Inherit the text color */
  }

  /* Add some basic spacing and styling to the page */
  h1, h2, h3, h4, h5, h6 {
    font-family: 'Arial', sans-serif;
    margin-bottom: 0.5em;
  }

  p {
    margin-bottom: 1em;
  }

  /* Style buttons */
  button {
    cursor: pointer;
    background-color: #007bff; /* Blue background for buttons */
    color: white;
    border: none;
    padding: 10px 15px;
    font-size: 16px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #0056b3; /* Darker blue when hovered */
  }
  
  /* Set a container for main content to center and add padding */
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  /* Responsive design (for smaller screens) */
  @media (max-width: 768px) {
    body {
      font-size: 14px; /* Smaller font for mobile devices */
    }

    .container {
      padding: 10px;
    }
  }
`;

export default GlobalStyles;
