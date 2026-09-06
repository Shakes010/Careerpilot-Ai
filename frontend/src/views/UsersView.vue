<template>
  <div>
    <!-- ================================================================
         Page header
         ================================================================ -->
    <div class="page-header mb-6">
      <div>
        <h2 class="page-header__title">User Management</h2>
        <p class="page-header__sub">View and manage all registered users (admin)</p>
      </div>
      <button
        id="refresh-users-btn"
        class="btn btn--outline"
        :disabled="loading"
        @click="loadUsers"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="1 4 1 10 7 10"/><polyline points="23 20 23 14 17 14"/>
          <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4-4.64 4.36A9 9 0 0 1 3.51 15"/>
        </svg>
        Refresh
      </button>
    </div>

    <!-- ================================================================
         Loading state
         ================================================================ -->
    <div v-if="loading" class="loading-overlay card">
      <span class="spinner" aria-label="Loading users…" />
      Loading users…
    </div>

    <!-- ================================================================
         Error state
         ================================================================ -->
    <div v-else-if="error" class="card">
      <div class="empty-state">
        <div class="empty-state__icon" aria-hidden="true">⚠️</div>
        <div class="empty-state__text">{{ error }}</div>
        <button class="btn btn--primary" @click="loadUsers">Retry</button>
      </div>
    </div>

    <!-- ================================================================
         Empty state
         ================================================================ -->
    <div v-else-if="!users.length" class="card">
      <div class="empty-state">
        <div class="empty-state__icon" aria-hidden="true">👤</div>
        <div class="empty-state__text">No users found in the database.</div>
      </div>
    </div>

    <!-- ================================================================
         Users table
         ================================================================ -->
    <div v-else class="card">
      <!-- Summary bar -->
      <div class="card__header">
        <div>
          <div class="card__title">All Users</div>
          <div class="card__subtitle">
            {{ users.length }} users total —
            {{ activeCount }} active,
            {{ users.length - activeCount }} suspended
          </div>
        </div>
        <!-- Search -->
        <div class="search-box">
          <input
            id="user-search-input"
            v-model="searchQuery"
            type="search"
            class="form-input"
            placeholder="Filter by name or email…"
            style="max-width: 260px;"
          />
        </div>
      </div>

      <div class="table-wrapper">
        <table class="table" aria-label="Users table">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Email</th>
              <th scope="col">Role</th>
              <th scope="col">Status</th>
              <th scope="col">Joined</th>
              <th scope="col" style="text-align: right;">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!filteredUsers.length">
              <td colspan="6" style="text-align:center; color: var(--color-gray-400); padding: 2rem;">
                No users match your search.
              </td>
            </tr>
            <tr v-for="user in filteredUsers" :key="user.id">
              <!-- Name -->
              <td>
                <div class="user-cell">
                  <div class="user-avatar" :style="{ background: avatarColor(user.full_name) }" aria-hidden="true">
                    {{ initials(user.full_name) }}
                  </div>
                  <span class="font-medium truncate" style="max-width: 160px;" :title="user.full_name">
                    {{ user.full_name }}
                  </span>
                </div>
              </td>

              <!-- Email -->
              <td class="text-gray truncate" style="max-width: 200px;" :title="user.email">
                {{ user.email }}
              </td>

              <!-- Role -->
              <td>
                <span :class="['badge', roleBadgeClass(user.role)]">
                  {{ user.role }}
                </span>
              </td>

              <!-- Status -->
              <td>
                <span :class="['badge', user.is_active ? 'badge--green' : 'badge--red']">
                  {{ user.is_active ? 'Active' : 'Suspended' }}
                </span>
              </td>

              <!-- Joined -->
              <td class="text-gray text-sm">
                {{ formatDate(user.created_at) }}
              </td>

              <!-- Actions -->
              <td style="text-align: right;">
                <button
                  :id="`toggle-status-btn-${user.id}`"
                  :class="['btn', 'btn--sm', user.is_active ? 'btn--danger' : 'btn--success']"
                  :disabled="togglingId === user.id"
                  :aria-label="`${user.is_active ? 'Suspend' : 'Activate'} ${user.full_name}`"
                  @click="toggleStatus(user)"
                >
                  <span v-if="togglingId === user.id" class="spinner" style="width:12px;height:12px;" aria-hidden="true"/>
                  {{ togglingId === user.id ? '…' : user.is_active ? 'Suspend' : 'Activate' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Toast -->
    <ToastNotification ref="toast" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { userApi } from '@/api/index.js'
import ToastNotification from '@/components/ToastNotification.vue'

// ---- State ----
const users = ref([])
const loading = ref(false)
const error = ref('')
const togglingId = ref(null)
const searchQuery = ref('')
const toast = ref(null)

// ---- Computed ----
const activeCount = computed(() => users.value.filter((u) => u.is_active).length)

const filteredUsers = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return users.value
  return users.value.filter(
    (u) =>
      u.full_name.toLowerCase().includes(q) ||
      u.email.toLowerCase().includes(q)
  )
})

// ---- Helpers ----
function formatDate(isoString) {
  if (!isoString) return '—'
  return new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(
    new Date(isoString)
  )
}

function initials(name) {
  return (name || '?')
    .split(' ')
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() ?? '')
    .join('')
}

const AVATAR_COLORS = [
  '#2563eb', '#7c3aed', '#db2777', '#ea580c',
  '#16a34a', '#0891b2', '#9333ea', '#b45309',
]
function avatarColor(name) {
  let hash = 0
  for (const ch of name ?? '') hash = ch.charCodeAt(0) + ((hash << 5) - hash)
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length]
}

function roleBadgeClass(role) {
  const map = { admin: 'badge--red', recruiter: 'badge--blue', student: 'badge--gray' }
  return map[role] ?? 'badge--gray'
}

// ---- API calls ----
async function loadUsers() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await userApi.list()
    users.value = data
  } catch (err) {
    error.value = err.message
    toast.value?.show(err.message, 'error')
  } finally {
    loading.value = false
  }
}

async function toggleStatus(user) {
  togglingId.value = user.id
  try {
    const { data } = await userApi.toggleStatus(user.id)
    const idx = users.value.findIndex((u) => u.id === user.id)
    if (idx !== -1) users.value[idx].is_active = data.is_active
    toast.value?.show(data.message, 'success')
  } catch (err) {
    toast.value?.show(err.message, 'error')
  } finally {
    togglingId.value = null
  }
}

// Load on mount
onMounted(loadUsers)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}
.page-header__title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  line-height: 1.2;
}
.page-header__sub {
  font-size: 0.875rem;
  color: var(--color-gray-500);
  margin-top: 0.25rem;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.search-box {
  display: flex;
  align-items: center;
}
</style>
