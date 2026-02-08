import axios from 'axios';

// Vite proxy handles the connection to port 9000
const api = axios.create({
  baseURL: '/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 1. Request Interceptor: Adds the Token & IDs to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Observability headers
  config.headers['X-Request-Id'] = crypto.randomUUID();
  config.headers['X-Process-Id'] = localStorage.getItem('process_id') || crypto.randomUUID();

  return config;
});

// 2. Response Interceptor: Handles expired sessions (401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Dispatch a custom event instead of hard reloading
      window.dispatchEvent(new Event("auth:unauthorized"));
    }
    return Promise.reject(error);
  }
);

export default api;