import api from './api'

export default {
  registerRecruiter(data) {
    return api.post('/auth/recruiter/register', data)
  },
  loginRecruiter(data) {
    return api.post('/auth/recruiter/login', data)
  },
  getCurrentUser() {
    return api.get('/auth/me')
  },
  logout() {
    return api.post('/auth/logout')
  }
}
