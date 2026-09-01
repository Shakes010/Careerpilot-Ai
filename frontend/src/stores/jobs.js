import { defineStore } from 'pinia'
import jobsApi from '@/services/jobsApi'

export const useJobsStore = defineStore('jobs', {
  state: () => ({
    jobs: [],
    pagination: {
      total: 0,
      page: 1,
      page_size: 20,
      total_pages: 0
    },
    currentJob: null,
    dashboardMetrics: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchJobs(filters = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await jobsApi.listJobs(filters)
        if (response.success && response.data) {
          this.jobs = response.data.jobs
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch jobs.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchJobDetails(id) {
      this.loading = true
      this.error = null
      try {
        const response = await jobsApi.getJobDetails(id)
        if (response.success && response.data) {
          this.currentJob = response.data
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to fetch job details.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async createJob(jobData, publish = false) {
      this.loading = true
      this.error = null
      try {
        const response = await jobsApi.createJob(jobData, publish)
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to create job.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateJob(id, jobData) {
      this.loading = true
      this.error = null
      try {
        const response = await jobsApi.updateJob(id, jobData)
        if (response.success && response.data) {
          this.currentJob = response.data
        }
        return response
      } catch (err) {
        this.error = err.response?.data?.detail || 'Failed to update job.'
        throw err
      } finally {
        this.loading = false
      }
    },

    async publishJob(id) {
      this.loading = true
      try {
        const response = await jobsApi.publishJob(id)
        if (response.success && response.data) {
          this.updateJobInState(response.data)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async pauseJob(id) {
      this.loading = true
      try {
        const response = await jobsApi.pauseJob(id)
        if (response.success && response.data) {
          this.updateJobInState(response.data)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async closeJob(id) {
      this.loading = true
      try {
        const response = await jobsApi.closeJob(id)
        if (response.success && response.data) {
          this.updateJobInState(response.data)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async deleteJob(id) {
      this.loading = true
      try {
        const response = await jobsApi.deleteJob(id)
        if (response.success) {
          this.jobs = this.jobs.filter(j => j.id !== id)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchDashboardMetrics() {
      this.loading = true
      try {
        const response = await jobsApi.getDashboardMetrics()
        if (response.success && response.data) {
          this.dashboardMetrics = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    updateJobInState(updatedJob) {
      const idx = this.jobs.findIndex(j => j.id === updatedJob.id)
      if (idx !== -1) {
        this.jobs[idx] = updatedJob
      }
      if (this.currentJob?.id === updatedJob.id) {
        this.currentJob = updatedJob
      }
    }
  }
})
