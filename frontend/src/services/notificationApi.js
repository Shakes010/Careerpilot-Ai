import api from './api'

export default {
  send(data) {
    return api.post('/notifications/', data)
  },
  listByUser(userId) {
    return api.get(`/notifications/user/${userId}`)
  },
  getMyNotifications() {
    return api.get('/notifications/me')
  },
  markRead(notificationId) {
    return api.patch(`/notifications/${notificationId}/read`, { is_read: true })
  }
}
