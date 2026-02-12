import axios from 'axios';

const api = axios.create({
  baseURL: '/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Flag to prevent multiple refresh calls simultaneously
let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// 1. Request Interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.headers['X-Request-Id'] = crypto.randomUUID();
  config.headers['X-Process-Id'] = localStorage.getItem('process_id') || crypto.randomUUID();
  return config;
});

// 2. Response Interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if error is 401 and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // If already refreshing, queue this request
        return new Promise(function(resolve, reject) {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token;
            return api(originalRequest);
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const refreshToken = localStorage.getItem('refresh_token');

      // If no refresh token, logout immediately
      if (!refreshToken) {
        window.dispatchEvent(new Event("auth:unauthorized"));
        return Promise.reject(error);
      }

      try {
        // Call the new refresh endpoint
        // Note: Using axios directly here to avoid interceptor loops
        const response = await axios.post('/refresh', { refresh_token: refreshToken });

        const { access_token, refresh_token } = response.data;

        // Update storage
        localStorage.setItem('token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        // Update the header for the failed request
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;

        processQueue(null, access_token);
        isRefreshing = false;

        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        isRefreshing = false;
        // If refresh fails, redirect to login
        window.dispatchEvent(new Event("auth:unauthorized"));
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;