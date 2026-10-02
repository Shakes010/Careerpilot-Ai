import { useAuthStore } from '../store'

const BASE_URL = 'http://127.0.0.1:8000'

export async function apiFetch(endpoint, options = {}) {
  const authStore = useAuthStore()
  
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }

  if (authStore.token) {
    headers['Authorization'] = `Bearer ${authStore.token}`
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  })

  if (response.status === 401) {
    authStore.logout()
    window.location.href = '/login'
    throw new Error('Unauthorized')
  }

  const data = await response.json()
  if (!response.ok) {
    throw new Error(data.detail || 'API Request Failed')
  }

  return data
}
