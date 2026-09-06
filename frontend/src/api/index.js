import axios from 'axios'

const api = axios.create({
  // During dev, Vite proxies /api → http://localhost:8000
  // so we don't need an absolute URL here.
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// ---------------------------------------------------------------------------
// Response interceptor — normalize errors
// ---------------------------------------------------------------------------
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred.'
    console.error('[API Error]', message, error)
    return Promise.reject(new Error(message))
  }
)

// ---------------------------------------------------------------------------
// Notification endpoints
// ---------------------------------------------------------------------------
export const notificationApi = {
  /** Send a notification to a user */
  send: (payload) => api.post('/notifications/', payload),

  /** Get all notifications for a user */
  listByUser: (userId) => api.get(`/notifications/user/${userId}`),

  /** Mark a single notification as read */
  markRead: (notificationId) =>
    api.patch(`/notifications/${notificationId}/read`, { is_read: true }),
}

// ---------------------------------------------------------------------------
// User management endpoints (admin)
// ---------------------------------------------------------------------------
export const userApi = {
  /** List all users (paginated) */
  list: (skip = 0, limit = 100) =>
    api.get('/users/', { params: { skip, limit } }),

  /** Get a single user by UUID */
  get: (userId) => api.get(`/users/${userId}`),

  /** Toggle a user's active status */
  toggleStatus: (userId) => api.patch(`/users/${userId}/toggle-status`),
}

export default api
