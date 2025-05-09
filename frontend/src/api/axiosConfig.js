import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  withCredentials: true, // important for session cookies
});

api.interceptors.response.use(
  response => {
    // You can check the response content type here if you want
    console.log('Response received:', response);
    return response;
  },
  error => {
    // Handle error gracefully
    if (error.response && error.response.status === 404) {
      console.error('API endpoint not found');
    } else {
      console.error('Error fetching data:', error);
    }
    return Promise.reject(error);
  }
);

export default api;
