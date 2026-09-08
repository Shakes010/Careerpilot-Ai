import api from './api'

export default {
  registerRecruiter(data) {
    return api.post('/auth/register', data)
  },
  login(data) {
    return api.post('/auth/login', data)
  },
  loginRecruiter(data) {
    return api.post('/auth/login', data)
  },
  changePassword(data) {
    return api.put('/auth/change-password', data)
  },
  changeEmail(data) {
    return api.put('/auth/change-email', data)
  },
  getCurrentUser() {
    return api.get('/auth/me')
  },
  logout() {
    return api.post('/auth/logout')
  }
}
