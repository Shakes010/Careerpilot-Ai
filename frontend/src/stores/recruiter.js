import { defineStore } from 'pinia'
import companyApi from '@/services/companyApi'

export const useRecruiterStore = defineStore('recruiter', {
  state: () => ({
    company: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchCompanyProfile() {
      this.loading = true
      this.error = null
      try {
        const response = await companyApi.getCompanyProfile()
        if (response.success && response.data) {
          this.company = response.data
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch company profile.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateCompanyProfile(data) {
      this.loading = true
      this.error = null
      try {
        const response = await companyApi.updateCompanyProfile(data)
        if (response.success && response.data) {
          this.company = response.data
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to update company profile.'
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
