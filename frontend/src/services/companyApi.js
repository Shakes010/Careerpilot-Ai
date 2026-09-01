import api from './api'

export default {
  getCompanyProfile() {
    return api.get('/recruiter/company')
  },
  updateCompanyProfile(data) {
    return api.put('/recruiter/company', data)
  }
}
