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
  getCurrentUser() {
    return api.get('/auth/me')
  },
  logout() {
    return api.post('/auth/logout')
  }
}
