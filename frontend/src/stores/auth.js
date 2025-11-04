import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authApi } from '@/api/api';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null);
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'));
  const isAuthenticated = computed(() => !!token.value);

  const setToken = (newToken) => {
    token.value = newToken;
    if (newToken) {
      localStorage.setItem('token', newToken);
    } else {
      localStorage.removeItem('token');
    }
  };

  const setUser = (userData) => {
    user.value = userData;
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData));
    } else {
      localStorage.removeItem('user');
    }
  };

  const login = async (credentials) => {
    try {
      const response = await authApi.login(credentials);
      setToken(response.data.token);
      setUser(response.data.user);
      return response;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const response = await authApi.register(userData);
      return response;
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  };

  const verifyCode = async (email, code) => {
    try {
      const response = await authApi.verifyCode(email, code);
      setToken(response.data.token);
      setUser(response.data.user);
      return response;
    } catch (error) {
      console.error('Verification failed:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setToken(null);
      setUser(null);
    }
  };

  const init = () => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken) {
      token.value = storedToken;
    }
    
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser);
      } catch (e) {
        console.error('Failed to parse user data from localStorage', e);
        localStorage.removeItem('user');
      }
    }
  };

  init();

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    verifyCode,
    logout,
    setToken,
    setUser,
  };
});
