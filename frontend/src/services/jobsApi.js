import api from './api'

export default {
  listJobs(params = {}) {
    return api.get('/recruiter/jobs', { params })
  },
  createJob(data, publish = false) {
    return api.post('/recruiter/jobs', data, { params: { publish } })
  },
  getJobDetails(id) {
    return api.get(`/recruiter/jobs/${id}`)
  },
  updateJob(id, data) {
    return api.put(`/recruiter/jobs/${id}`, data)
  },
  publishJob(id) {
    return api.patch(`/recruiter/jobs/${id}/publish`)
  },
  pauseJob(id) {
    return api.patch(`/recruiter/jobs/${id}/pause`)
  },
  closeJob(id) {
    return api.patch(`/recruiter/jobs/${id}/close`)
  },
  deleteJob(id) {
    return api.delete(`/recruiter/jobs/${id}`)
  },
  getDashboardMetrics() {
    return api.get('/recruiter/dashboard')
  }
}
