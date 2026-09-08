import api from './api'

export default {
  adminLogin(data) {
    return api.post('/admin/auth/login', data)
  },
  getDashboardMetrics() {
    return api.get('/admin/dashboard')
  },
  // Feature 36: User Management
  listUsers(params = {}) {
    return api.get('/admin/users', { params })
  },
  updateUserStatus(userId, is_active, notes = null) {
    return api.patch(`/admin/users/${userId}/status`, { is_active, notes })
  },
  updateUserRole(userId, role) {
    return api.patch(`/admin/users/${userId}/role`, { role })
  },
  // Feature 37: Recruiter Verification
  getPendingVerifications(params = {}) {
    return api.get('/admin/companies/pending', { params })
  },
  getAllCompanies(params = {}) {
    return api.get('/admin/companies', { params })
  },
  verifyCompany(companyId, data) {
    return api.patch(`/admin/companies/${companyId}/verify`, data)
  },
  rejectCompany(companyId, data) {
    return api.patch(`/admin/companies/${companyId}/reject`, data)
  },
  // Feature 38: Job Moderation
  getJobsForModeration(params = {}) {
    return api.get('/admin/jobs/moderation', { params })
  },
  moderateJob(jobId, data) {
    return api.patch(`/admin/jobs/${jobId}/moderate`, data)
  },
  // Feature 39: Skill Library
  listSkills(params = {}) {
    return api.get('/admin/skills', { params })
  },
  createSkill(data) {
    return api.post('/admin/skills', data)
  },
  updateSkill(skillId, data) {
    return api.put(`/admin/skills/${skillId}`, data)
  },
  deleteSkill(skillId) {
    return api.delete(`/admin/skills/${skillId}`)
  },
  // Feature 40: Analytics
  getAnalyticsOverview() {
    return api.get('/admin/analytics/overview')
  },
  // Feature 41: Flagged Queue
  getFlaggedActivities(params = {}) {
    return api.get('/admin/flagged-queue', { params })
  },
  resolveFlaggedActivity(flagId, data) {
    return api.patch(`/admin/flagged-queue/${flagId}/resolve`, data)
  }
}
