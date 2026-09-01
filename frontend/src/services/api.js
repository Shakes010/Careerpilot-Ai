import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request Interceptor: Attach JWT Bearer Token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cp_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// Response Interceptor: Catch 401 Unauthorized
api.interceptors.response.use((response) => {
  return response.data
}, (error) => {
  if (error.response && error.response.status === 401) {
    localStorage.removeItem('cp_token')
    localStorage.removeItem('cp_user')
    // Redirect to login if unauthenticated on protected route
    if (!window.location.pathname.includes('/recruiter/login') && !window.location.pathname.includes('/recruiter/register')) {
      window.location.href = '/recruiter/login'
    }
  }
  return Promise.reject(error)
})

export default api
