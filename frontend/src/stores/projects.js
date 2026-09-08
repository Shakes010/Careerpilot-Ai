import { defineStore } from 'pinia'
import projectApi from '@/services/projectApi'

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    projects: [],
    currentProject: null,
    joinRequests: [],
    pagination: { total: 0, page: 1, page_size: 20 },
    loading: false,
    error: null
  }),

  actions: {
    async fetchProjects(params = {}) {
      this.loading = true
      try {
        const response = await projectApi.listProjects(params)
        if (response.success && response.data) {
          this.projects = response.data.projects
          this.pagination = response.data.pagination
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchProjectDetails(id) {
      this.loading = true
      try {
        const response = await projectApi.getProjectDetails(id)
        if (response.success && response.data) {
          this.currentProject = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async createProject(projectData) {
      this.loading = true
      try {
        const response = await projectApi.createProject(projectData)
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async requestToJoin(projectId) {
      this.loading = true
      try {
        const response = await projectApi.requestToJoin(projectId)
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchJoinRequests(projectId) {
      this.loading = true
      try {
        const response = await projectApi.getJoinRequests(projectId)
        if (response.success && response.data) {
          this.joinRequests = response.data
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async acceptJoinRequest(projectId, requestId) {
      this.loading = true
      try {
        const response = await projectApi.acceptJoinRequest(projectId, requestId)
        if (response.success) {
          this.joinRequests = this.joinRequests.filter(r => r.id !== requestId)
          await this.fetchProjectDetails(projectId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async rejectJoinRequest(projectId, requestId) {
      this.loading = true
      try {
        const response = await projectApi.rejectJoinRequest(projectId, requestId)
        if (response.success) {
          this.joinRequests = this.joinRequests.filter(r => r.id !== requestId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateMemberRole(projectId, studentId, role) {
      this.loading = true
      try {
        const response = await projectApi.updateMemberRole(projectId, studentId, role)
        if (response.success) {
          await this.fetchProjectDetails(projectId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async removeMember(projectId, studentId) {
      this.loading = true
      try {
        const response = await projectApi.removeMember(projectId, studentId)
        if (response.success) {
          await this.fetchProjectDetails(projectId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async createTask(projectId, taskData) {
      this.loading = true
      try {
        const response = await projectApi.createTask(projectId, taskData)
        if (response.success) {
          await this.fetchProjectDetails(projectId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async updateTaskStatus(projectId, taskId, status) {
      this.loading = true
      try {
        const response = await projectApi.updateTaskStatus(projectId, taskId, status)
        if (response.success) {
          await this.fetchProjectDetails(projectId)
        }
        return response
      } catch (err) {
        throw err
      } finally {
        this.loading = false
      }
    },

    async submitForVerification(projectId, notes) {
      this.loading = true
      try {
        const response = await projectApi.submitForVerification(projectId, { verification_notes: notes })
        if (response.success) {
          await this.fetchProjectDetails(projectId)
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
