import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
  withCredentials: true, 
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      try {
        const { useAuthStore } = require('@/stores/auth');
        const authStore = useAuthStore();
        authStore.logout?.();
      } catch (_) {}
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  register: (data) => api.post('/auth/register', data),
  verifyCode: (email, code) => api.post('/auth/check_code', { email, code }),
  login: (data) => api.post('/auth/login', data),
  logout: () => Promise.resolve({ data: { message: 'ok' } }),
};

export const eventsApi = {
  getAll: () => api.get('/events/all'),
  getById: (id) => api.get(`/events/${id}`),
  getMy: () => api.get('/events/my/all'),
  createMy: (data) => api.post('/events/my', data),
  updateEvent: (id, payload) => api.patch(`/events/my/${id}`, payload),
};

export const betsApi = {
  placeBet: (data) => api.post('/bets/my', data),
  getMyBets: () => api.get('/bets/my'),
  getByOutcome: (eventId, outcomeId) => api.get(`/bets/${eventId}/${outcomeId}`),
};

export const userApi = {
  getBalance: () => api.get('/user/balance'),
  getInfo: () => api.get('/user/info'),
  updateInfo: (data) => api.post('/user/info', data),
};

export const fetchEvents = async () => {
  const response = await eventsApi.getAll();
  return response.data;
};

export const createEvent = async (event) => {
  const response = await eventsApi.createMy(event);
  return response.data;
};

export const updateEvent = async (id, payload) => {
  const response = await eventsApi.updateEvent(id, payload);
  return response.data;
};

export default api;