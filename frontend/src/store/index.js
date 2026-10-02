import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('cp_token') || null,
    user: JSON.parse(localStorage.getItem('cp_user') || 'null'),
    isEligible: localStorage.getItem('cp_is_eligible') === 'true',
    isPremium: localStorage.getItem('cp_is_premium') === 'true'
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role || 'student',
    userFullName: (state) => state.user?.full_name || 'User',
    isUserPremium: (state) => !!state.isPremium
  },
  actions: {
    setAuth(authData) {
      this.token = authData.access_token
      this.user = {
        id: authData.user_id,
        email: authData.email,
        role: authData.role,
        full_name: authData.full_name
      }
      this.isEligible = authData.is_eligible !== false
      this.isPremium = !!authData.is_premium

      localStorage.setItem('cp_token', this.token)
      localStorage.setItem('cp_user', JSON.stringify(this.user))
      localStorage.setItem('cp_is_eligible', String(this.isEligible))
      localStorage.setItem('cp_is_premium', String(this.isPremium))
    },
    setPremium(val) {
      this.isPremium = !!val
      localStorage.setItem('cp_is_premium', String(this.isPremium))
    },
    async refreshProfile() {
      if (!this.token) return
      try {
        const res = await fetch('http://127.0.0.1:8000/auth/me', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`
          }
        })
        if (res.ok) {
          const data = await res.json()
          if (data.student_profile) {
            this.isPremium = !!data.student_profile.is_premium
            this.isEligible = data.student_profile.is_eligible !== false
            localStorage.setItem('cp_is_premium', String(this.isPremium))
            localStorage.setItem('cp_is_eligible', String(this.isEligible))
          }
          if (data.full_name && this.user) {
            this.user.full_name = data.full_name
            localStorage.setItem('cp_user', JSON.stringify(this.user))
          }
        }
      } catch (err) {
        console.error('refreshProfile error:', err)
      }
    },
    logout() {
      this.token = null
      this.user = null
      this.isEligible = true
      this.isPremium = false
      localStorage.removeItem('cp_token')
      localStorage.removeItem('cp_user')
      localStorage.removeItem('cp_is_eligible')
      localStorage.removeItem('cp_is_premium')
    }
  }
})
