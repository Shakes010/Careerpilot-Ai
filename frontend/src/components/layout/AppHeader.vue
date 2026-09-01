<template>
  <header class="app-header">
    <div class="header-left">
      <button class="mobile-toggle" @click="$emit('toggle-sidebar')">
        ☰
      </button>
      <div class="brand">
        <span class="brand-icon">🚀</span>
        <span class="brand-text">CareerPilot <span class="brand-ai">AI</span></span>
        <span class="portal-badge">Recruiter</span>
      </div>
    </div>

    <div class="header-center">
      <div class="search-bar">
        <span class="search-icon">🔍</span>
        <input type="text" placeholder="Search jobs, candidates, keywords..." class="search-input" />
      </div>
    </div>

    <div class="header-right">
      <button class="icon-btn" title="Notifications">
        🔔
      </button>

      <div class="user-menu-container">
        <div class="user-menu-trigger" @click="menuOpen = !menuOpen">
          <div class="avatar">{{ userInitials }}</div>
          <div class="user-info">
            <span class="user-name">{{ authStore.user?.full_name || 'Recruiter' }}</span>
            <span class="company-status-chip" :class="companyStatusClass">
              {{ authStore.companyVerificationStatus || 'PENDING' }}
            </span>
          </div>
          <span class="caret">▼</span>
        </div>

        <div v-if="menuOpen" class="dropdown-menu" @click="menuOpen = false">
          <div class="dropdown-header">
            <p class="dropdown-user-email">{{ authStore.user?.email }}</p>
            <p class="dropdown-company-name">{{ authStore.companyName }}</p>
          </div>
          <hr />
          <router-link to="/recruiter/company" class="dropdown-item">
            🏢 Company Profile
          </router-link>
          <router-link to="/recruiter/jobs" class="dropdown-item">
            💼 Manage Jobs
          </router-link>
          <hr />
          <button class="dropdown-item logout-btn" @click="handleLogout">
            🚪 Logout
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineEmits(['toggle-sidebar'])

const router = useRouter()
const authStore = useAuthStore()
const menuOpen = ref(false)

const userInitials = computed(() => {
  const name = authStore.user?.full_name || 'R'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
})

const companyStatusClass = computed(() => {
  const status = (authStore.companyVerificationStatus || 'PENDING').toLowerCase()
  return `status-${status}`
})

const handleLogout = () => {
  authStore.logout()
  router.push('/recruiter/login')
}
</script>

<style scoped>
.app-header {
  height: 64px;
  background-color: #ffffff;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--text-heading);
}

.brand-ai {
  color: var(--primary);
}

.portal-badge {
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: var(--radius-full);
  background-color: var(--primary-light);
  color: var(--primary);
  text-transform: uppercase;
}

.header-center {
  flex: 1;
  max-width: 480px;
  margin: 0 2rem;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--background);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  padding: 0.375rem 1rem;
}

.search-icon {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-right: 0.5rem;
}

.search-input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: 0.875rem;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-btn {
  background: var(--background);
  border: 1px solid var(--border);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.user-menu-container {
  position: relative;
}

.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
}

.user-menu-trigger:hover {
  background-color: var(--surface-hover);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary);
  color: #ffffff;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-heading);
}

.company-status-chip {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-pending { color: var(--warning); }
.status-verified { color: var(--success); }
.status-rejected { color: var(--danger); }

.caret {
  font-size: 0.625rem;
  color: var(--text-muted);
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 0.5rem);
  width: 220px;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 0.5rem 0;
  z-index: 200;
}

.dropdown-header {
  padding: 0.5rem 1rem;
}

.dropdown-user-email {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.dropdown-company-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-heading);
}

hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 0.375rem 0;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  color: var(--text-primary);
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.dropdown-item:hover {
  background-color: var(--surface-hover);
  color: var(--primary);
  text-decoration: none;
}

.logout-btn {
  color: var(--danger);
}

@media (max-width: 768px) {
  .mobile-toggle { display: block; }
  .header-center { display: none; }
  .user-info { display: none; }
}
</style>
