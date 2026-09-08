import { defineStore } from 'pinia'
import adminApi from '@/services/adminApi'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    metrics: null,
    analytics: null,
    users: [],
    pendingCompanies: [],
    allCompanies: [],
    moderationJobs: [],
    skills: [],
    flaggedActivities: [],
    pagination: { total: 0, page: 1, page_size: 20 },
    loading: false,
    error: null
  }),

  actions: {
    async loginAdmin(credentials) {
      this.loading = true
      this.error = null
      try {
        const response = await adminApi.adminLogin(credentials)
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Admin login failed.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchDashboardMetrics() {
      this.loading = true
      try {
        const response = await adminApi.getDashboardMetrics()
        if (response.success && response.data) {
          this.metrics = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    // Feature 36: User Management
    async fetchUsers(params = {}) {
      this.loading = true
      try {
        const response = await adminApi.listUsers(params)
        if (response.success && response.data) {
          this.users = response.data.users
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateUserStatus(userId, isActive, notes = null) {
      this.loading = true
      try {
        const response = await adminApi.updateUserStatus(userId, isActive, notes)
        if (response.success && response.data) {
          const idx = this.users.findIndex(u => u.id === userId)
          if (idx !== -1) {
            this.users[idx] = response.data
          }
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateUserRole(userId, role) {
      this.loading = true
      try {
        const response = await adminApi.updateUserRole(userId, role)
        if (response.success && response.data) {
          const idx = this.users.findIndex(u => u.id === userId)
          if (idx !== -1) {
            this.users[idx] = response.data
          }
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    // Feature 37: Recruiter Verification
    async fetchPendingVerifications(params = {}) {
      this.loading = true
      try {
        const response = await adminApi.getPendingVerifications(params)
        if (response.success && response.data) {
          this.pendingCompanies = response.data.companies
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchAllCompanies(params = {}) {
      this.loading = true
      try {
        const response = await adminApi.getAllCompanies(params)
        if (response.success && response.data) {
          this.allCompanies = response.data.companies
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async verifyCompany(companyId, notes = 'Verified by administrator') {
      this.loading = true
      try {
        const response = await adminApi.verifyCompany(companyId, { verification_notes: notes })
        if (response.success) {
          this.pendingCompanies = this.pendingCompanies.filter(c => c.id !== companyId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async rejectCompany(companyId, notes) {
      this.loading = true
      try {
        const response = await adminApi.rejectCompany(companyId, { verification_notes: notes })
        if (response.success) {
          this.pendingCompanies = this.pendingCompanies.filter(c => c.id !== companyId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    // Feature 38: Job Moderation
    async fetchJobsForModeration(params = {}) {
      this.loading = true
      try {
        const response = await adminApi.getJobsForModeration(params)
        if (response.success && response.data) {
          this.moderationJobs = response.data.jobs
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async moderateJob(jobId, moderationStatus, notes = null) {
      this.loading = true
      try {
        const response = await adminApi.moderateJob(jobId, { moderation_status: moderationStatus, moderation_notes: notes })
        if (response.success && response.data) {
          const idx = this.moderationJobs.findIndex(j => j.id === jobId)
          if (idx !== -1) {
            this.moderationJobs[idx] = response.data
          }
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    // Feature 39: Skill Library
    async fetchSkills(params = {}) {
      this.loading = true
      try {
        const response = await adminApi.listSkills(params)
        if (response.success && response.data) {
          this.skills = response.data.skills
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async createSkill(skillData) {
      this.loading = true
      try {
        const response = await adminApi.createSkill(skillData)
        if (response.success && response.data) {
          this.skills.unshift(response.data)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateSkill(skillId, skillData) {
      this.loading = true
      try {
        const response = await adminApi.updateSkill(skillId, skillData)
        if (response.success && response.data) {
          const idx = this.skills.findIndex(s => s.id === skillId)
          if (idx !== -1) {
            this.skills[idx] = response.data
          }
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteSkill(skillId) {
      this.loading = true
      try {
        const response = await adminApi.deleteSkill(skillId)
        if (response.success) {
          this.skills = this.skills.filter(s => s.id !== skillId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    // Feature 40: Analytics
    async fetchAnalyticsOverview() {
      this.loading = true
      try {
        const response = await adminApi.getAnalyticsOverview()
        if (response.success && response.data) {
          this.analytics = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    // Feature 41: Flagged Queue
    async fetchFlaggedActivities(params = {}) {
      this.loading = true
      try {
        const response = await adminApi.getFlaggedActivities(params)
        if (response.success && response.data) {
          this.flaggedActivities = response.data.flagged_activities
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async resolveFlaggedActivity(flagId, status, notes = null) {
      this.loading = true
      try {
        const response = await adminApi.resolveFlaggedActivity(flagId, { status, resolution_notes: notes })
        if (response.success && response.data) {
          const idx = this.flaggedActivities.findIndex(f => f.id === flagId)
          if (idx !== -1) {
            this.flaggedActivities[idx] = response.data
          }
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
