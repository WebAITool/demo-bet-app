import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authApi, userApi } from '@/api/api';

export const useAuthStore = defineStore('auth', () => {
  const isAuth = ref(false);
  const loading = ref(false);
  const error = ref(null);
  const profile = ref(null);

  const isAuthenticated = computed(() => isAuth.value === true);

  const init = async () => {
    loading.value = true;
    error.value = null;
    try {
      await userApi.getBalance();
      isAuth.value = true;
    } catch (e) {
      isAuth.value = false;
    } finally {
      loading.value = false;
    }
  };

  const login = async ({ login, password }) => {
    loading.value = true;
    error.value = null;
    try {
      await authApi.login({ login, password });
      isAuth.value = true;
      return true;
    } catch (e) {
      const status = e?.response?.status;
      if (status === 400) error.value = 'Неверный пароль';
      else if (status === 404) error.value = 'Пользователь не найден';
      else error.value = 'Ошибка входа';
      isAuth.value = false;
      return false;
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } finally {
      isAuth.value = false;
      profile.value = null;
      error.value = null;
    }
  };

  const loadProfile = async () => {
    try {
      const { data } = await userApi.getInfo();
      profile.value = data;
      return data;
    } catch {
      return null;
    }
  };

  return {
    isAuth,
    loading,
    error,
    profile,
    isAuthenticated,
    init,
    login,
    logout,
    loadProfile,
  };
});
