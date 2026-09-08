import { defineStore } from 'pinia'
import sandboxApi from '@/services/sandboxApi'

export const useSandboxStore = defineStore('sandbox', {
  state: () => ({
    challenges: [],
    currentChallenge: null,
    currentAttempt: null,
    myAttempts: [],
    pagination: { total: 0, page: 1, page_size: 20 },
    loading: false,
    error: null
  }),

  actions: {
    async fetchChallenges(params = {}) {
      this.loading = true
      try {
        const response = await sandboxApi.listChallenges(params)
        if (response.success && response.data) {
          this.challenges = response.data.challenges
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchChallengeDetails(id) {
      this.loading = true
      try {
        const response = await sandboxApi.getChallengeDetails(id)
        if (response.success && response.data) {
          this.currentChallenge = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async startAttempt(challengeId) {
      this.loading = true
      try {
        const response = await sandboxApi.startAttempt(challengeId)
        if (response.success && response.data) {
          this.currentAttempt = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchAttemptDetails(attemptId) {
      this.loading = true
      try {
        const response = await sandboxApi.getAttemptDetails(attemptId)
        if (response.success && response.data) {
          this.currentAttempt = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async submitAttempt(attemptId, submissionText) {
      this.loading = true
      try {
        const response = await sandboxApi.submitAttempt(attemptId, submissionText)
        if (response.success && response.data) {
          this.currentAttempt = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchMyAttempts() {
      this.loading = true
      try {
        const response = await sandboxApi.getMyAttempts()
        if (response.success && response.data) {
          this.myAttempts = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    }
  }
})
