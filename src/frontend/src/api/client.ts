import axios from 'axios';

// --- IN-MEMORY TOKEN STORAGE ---
// This variable holds the token. It is wiped when the page refreshes.
let memoryToken: string | null = null;

// Helper to set the token from other files (like AuthContext)
export const setMemoryToken = (token: string | null) => {
  memoryToken = token;
};
// -------------------------------

const api = axios.create({
  baseURL: '/',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // IMPORTANT: Allows sending Cookies to backend
});

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

// 1. Request Interceptor: Use Memory Token
api.interceptors.request.use((config) => {
  if (memoryToken) {
    config.headers.Authorization = `Bearer ${memoryToken}`;
  }

  // Observability
  config.headers['X-Request-Id'] = crypto.randomUUID();
  // Process ID is still safe in localStorage as it's not a security key
  config.headers['X-Process-Id'] = localStorage.getItem('process_id') || crypto.randomUUID();

  return config;
});

// 2. Response Interceptor: Cookie-based Refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
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

      try {
        // Call /refresh. Browser automatically sends the HttpOnly cookie.
        // We don't send any data in the body.
        const response = await axios.post('/refresh', {}, { withCredentials: true });

        const { access_token } = response.data;

        // Update In-Memory Store
        setMemoryToken(access_token);

        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;

        processQueue(null, access_token);
        isRefreshing = false;

        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        isRefreshing = false;
        // If refresh fails, it means the Cookie is invalid/expired. Logout.
        window.dispatchEvent(new Event("auth:unauthorized"));
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;