import { defineStore } from 'pinia'
import authApi from '@/services/authApi'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('cp_token') || '',
    user: JSON.parse(localStorage.getItem('cp_user') || 'null'),
    companyId: localStorage.getItem('cp_company_id') || '',
    companyName: localStorage.getItem('cp_company_name') || '',
    companyVerificationStatus: localStorage.getItem('cp_company_status') || 'PENDING',
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'ADMIN',
    isRecruiter: (state) => state.user?.role === 'RECRUITER',
    isStudent: (state) => state.user?.role === 'STUDENT',
    isCompanyVerified: (state) => state.companyVerificationStatus === 'VERIFIED'
  },

  actions: {
    async register(registerData) {
      this.loading = true
      this.error = null
      try {
        const response = await authApi.registerRecruiter(registerData)
        if (response.success && response.data) {
          this.setAuthData(response.data)
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Registration failed.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async login(loginData) {
      this.loading = true
      this.error = null
      try {
        const response = await authApi.login(loginData)
        if (response.success && response.data) {
          this.setAuthData(response.data)
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Invalid login credentials.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async changePassword(passwordData) {
      this.loading = true
      this.error = null
      try {
        const response = await authApi.changePassword(passwordData)
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to change password.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async changeEmail(emailData) {
      this.loading = true
      this.error = null
      try {
        const response = await authApi.changeEmail(emailData)
        if (response.success && response.data) {
          this.user.email = response.data.email
          localStorage.setItem('cp_user', JSON.stringify(this.user))
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to change email address.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchCurrentUser() {
      if (!this.token) return
      try {
        const response = await authApi.getCurrentUser()
        if (response.success && response.data) {
          const { user } = response.data
          this.user = user
          localStorage.setItem('cp_user', JSON.stringify(user))
        }
      } catch (err) {
        this.logout()
      }
    },

    setAuthData(data) {
      this.token = data.access_token
      this.user = {
        id: data.user_id,
        email: data.email,
        full_name: data.full_name,
        role: data.role
      }
      this.companyId = data.company_id || ''
      this.companyName = data.company_name || ''
      this.companyVerificationStatus = data.company_verification_status || 'VERIFIED'

      localStorage.setItem('cp_token', data.access_token)
      localStorage.setItem('cp_user', JSON.stringify(this.user))
      localStorage.setItem('cp_company_id', this.companyId)
      localStorage.setItem('cp_company_name', this.companyName)
      localStorage.setItem('cp_company_status', this.companyVerificationStatus)
    },

    logout() {
      this.token = ''
      this.user = null
      this.companyId = ''
      this.companyName = ''
      this.companyVerificationStatus = 'PENDING'

      localStorage.removeItem('cp_token')
      localStorage.removeItem('cp_user')
      localStorage.removeItem('cp_company_id')
      localStorage.removeItem('cp_company_name')
      localStorage.removeItem('cp_company_status')
    }
  }
})
