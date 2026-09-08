import api from './api'

export default {
  listProjects(params = {}) {
    return api.get('/projects', { params })
  },
  createProject(data) {
    return api.post('/projects', data)
  },
  getProjectDetails(id) {
    return api.get(`/projects/${id}`)
  },
  updateProject(id, data) {
    return api.put(`/projects/${id}`, data)
  },
  deleteProject(id) {
    return api.delete(`/projects/${id}`)
  },
  requestToJoin(id) {
    return api.post(`/projects/${id}/join`)
  },
  getJoinRequests(id) {
    return api.get(`/projects/${id}/join-requests`)
  },
  acceptJoinRequest(projectId, requestId) {
    return api.post(`/projects/${projectId}/join-requests/${requestId}/accept`)
  },
  rejectJoinRequest(projectId, requestId) {
    return api.post(`/projects/${projectId}/join-requests/${requestId}/reject`)
  },
  getMembers(id) {
    return api.get(`/projects/${id}/members`)
  },
  updateMemberRole(projectId, studentId, role) {
    return api.post(`/projects/${projectId}/members/${studentId}/role`, { role })
  },
  removeMember(projectId, studentId) {
    return api.delete(`/projects/${projectId}/members/${studentId}`)
  },
  getTasks(id) {
    return api.get(`/projects/${id}/tasks`)
  },
  createTask(projectId, data) {
    return api.post(`/projects/${projectId}/tasks`, data)
  },
  updateTask(projectId, taskId, data) {
    return api.put(`/projects/${projectId}/tasks/${taskId}`, data)
  },
  updateTaskStatus(projectId, taskId, status) {
    return api.patch(`/projects/${projectId}/tasks/${taskId}/status`, null, { params: { status } })
  },
  deleteTask(projectId, taskId) {
    return api.delete(`/projects/${projectId}/tasks/${taskId}`)
  },
  getProgress(id) {
    return api.get(`/projects/${id}/progress`)
  },
  submitForVerification(id, data) {
    return api.post(`/projects/${id}/verification`, data)
  },
  getVerificationStatus(id) {
    return api.get(`/projects/${id}/verification`)
  }
}
