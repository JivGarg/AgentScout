import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

// Attach auth token to every request
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 → auto-logout
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ── Auth API ────────────────────────────────────────────────
export const authApi = {
  signup: (email, password) =>
    api.post('/auth/signup', { email, password }),

  login: (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },

  getMe: () => api.get('/auth/me'),
};

// ── Research API ────────────────────────────────────────────
export const researchApi = {
  analyze: (url, signal) => api.post('/research/analyze', { url }, { signal }),

  getHistory: (skip = 0, limit = 20) =>
    api.get('/research/history', { params: { skip, limit } }),

  getById: (id) => api.get(`/research/history/${id}`),

  deleteById: (id) => api.delete(`/research/history/${id}`),
};

// ── Resume API ─────────────────────────────────────────────
export const resumeApi = {
  analyze: (resumeText) =>
    api.post('/resume/analyze', { resume_text: resumeText }),
};

export default api;
