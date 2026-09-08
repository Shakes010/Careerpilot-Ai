import api from './api'

export default {
  listChallenges(params = {}) {
    return api.get('/career-sandbox/challenges', { params })
  },
  getChallengeDetails(id) {
    return api.get(`/career-sandbox/challenges/${id}`)
  },
  startAttempt(id) {
    return api.post(`/career-sandbox/challenges/${id}/start`)
  },
  getAttemptDetails(id) {
    return api.get(`/career-sandbox/attempts/${id}`)
  },
  submitAttempt(id, submission) {
    return api.post(`/career-sandbox/attempts/${id}/submit`, { submission })
  },
  getMyAttempts() {
    return api.get('/career-sandbox/my-attempts')
  }
}
