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
    isRecruiter: (state) => state.user?.role === 'RECRUITER',
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
        const response = await authApi.loginRecruiter(loginData)
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

    async fetchCurrentUser() {
      if (!this.token) return
      try {
        const response = await authApi.getCurrentUser()
        if (response.success && response.data) {
          const { user, company } = response.data
          this.user = user
          this.companyId = company.id
          this.companyName = company.name
          this.companyVerificationStatus = company.verification_status
          
          localStorage.setItem('cp_user', JSON.stringify(user))
          localStorage.setItem('cp_company_id', company.id)
          localStorage.setItem('cp_company_name', company.name)
          localStorage.setItem('cp_company_status', company.verification_status)
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
      this.companyId = data.company_id
      this.companyName = data.company_name
      this.companyVerificationStatus = data.company_verification_status

      localStorage.setItem('cp_token', data.access_token)
      localStorage.setItem('cp_user', JSON.stringify(this.user))
      localStorage.setItem('cp_company_id', data.company_id)
      localStorage.setItem('cp_company_name', data.company_name)
      localStorage.setItem('cp_company_status', data.company_verification_status)
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
