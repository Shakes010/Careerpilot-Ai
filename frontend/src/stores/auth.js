import { defineStore } from 'pinia';
import apiClient from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('cp_token') || null,
    user: JSON.parse(localStorage.getItem('cp_user') || 'null'),
    profile: JSON.parse(localStorage.getItem('cp_profile') || 'null'),
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    studentName: (state) => state.user?.full_name || 'Student',
    studentEmail: (state) => state.user?.email || '',
    studentUniversity: (state) => state.profile?.university || 'National Institute of Technology',
    studentMajor: (state) => state.profile?.major || 'Master of Computer Applications (MCA)',
  },

  actions: {
    async register(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post('/auth/register', credentials);
        this.setAuthData(response.data);
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Registration failed. Please check your credentials.';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async login(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post('/auth/login', credentials);
        this.setAuthData(response.data);
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Invalid email or password.';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async fetchCurrentUser() {
      if (!this.token) return false;
      this.loading = true;
      try {
        const response = await apiClient.get('/auth/me');
        this.setAuthData(response.data);
        return true;
      } catch (err) {
        this.logout();
        return false;
      } finally {
        this.loading = false;
      }
    },

    setAuthData(authData) {
      this.token = authData.access_token;
      this.user = authData.user;
      this.profile = authData.profile;

      localStorage.setItem('cp_token', authData.access_token);
      localStorage.setItem('cp_user', JSON.stringify(authData.user));
      localStorage.setItem('cp_profile', JSON.stringify(authData.profile));
    },

    logout() {
      this.token = null;
      this.user = null;
      this.profile = null;
      localStorage.removeItem('cp_token');
      localStorage.removeItem('cp_user');
      localStorage.removeItem('cp_profile');
    }
  }
});
