<template>
  <aside class="app-sidebar" :class="{ 'is-open': isOpen }">
    <div class="sidebar-nav">
      <div class="nav-section-title">RECRUITER MODULE</div>
      
      <router-link to="/recruiter/dashboard" class="nav-item" active-class="active">
        <span class="nav-icon">📊</span>
        <span class="nav-label">Dashboard</span>
      </router-link>

      <router-link to="/recruiter/company" class="nav-item" active-class="active">
        <span class="nav-icon">🏢</span>
        <span class="nav-label">Company Profile</span>
      </router-link>

      <router-link to="/recruiter/jobs" class="nav-item" active-class="active">
        <span class="nav-icon">💼</span>
        <span class="nav-label">Jobs & Postings</span>
      </router-link>

      <div class="nav-divider"></div>
      <div class="nav-section-title">PHASE 2 FEATURES</div>

      <div v-for="item in phase2Items" :key="item.name" class="nav-item disabled" :title="`${item.name} - Coming in Phase 2`">
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-label">{{ item.name }}</span>
        <span class="phase-chip">Phase 2</span>
      </div>

      <div class="nav-divider"></div>

      <div class="nav-item disabled" title="Settings - Coming Soon">
        <span class="nav-icon">⚙️</span>
        <span class="nav-label">Settings</span>
      </div>

      <button class="nav-item logout-nav-item" @click="handleLogout">
        <span class="nav-icon">🚪</span>
        <span class="nav-label">Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineProps({
  isOpen: { type: Boolean, default: false }
})

const router = useRouter()
const authStore = useAuthStore()

const phase2Items = [
  { name: 'Candidates', icon: '👥' },
  { name: 'Applications', icon: '📄' },
  { name: 'Hiring Pipeline', icon: '🔄' },
  { name: 'Interviews', icon: '📅' },
  { name: 'AI Candidate Match', icon: '✨' },
  { name: 'Recruiter Analytics', icon: '📈' },
  { name: 'Subscriptions', icon: '💳' },
  { name: 'Credit Balance', icon: '🪙' },
  { name: 'Billing & Invoices', icon: '🧾' }
]

const handleLogout = () => {
  authStore.logout()
  router.push('/recruiter/login')
}
</script>

<style scoped>
.app-sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid var(--border);
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  padding: 1.25rem 0.75rem;
  transition: transform 0.2s ease;
}

.nav-section-title {
  font-size: 0.6875rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  padding: 0.5rem 0.75rem;
  margin-top: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
  margin-bottom: 0.25rem;
}

.nav-item:hover:not(.disabled) {
  background-color: var(--primary-light);
  color: var(--primary);
  text-decoration: none;
}

.nav-item.active {
  background-color: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
  border-left: 3px solid var(--primary);
}

.nav-icon {
  font-size: 1.125rem;
}

.nav-divider {
  height: 1px;
  background-color: var(--border);
  margin: 0.75rem 0;
}

.nav-item.disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.phase-chip {
  margin-left: auto;
  font-size: 0.625rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  background-color: #f1f5f9;
  color: var(--text-secondary);
}

.logout-nav-item {
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  color: var(--danger);

}
.logout-nav-item:hover {
  background-color: var(--danger-bg);
}

@media (max-width: 768px) {
  .app-sidebar {
    position: fixed;
    left: -260px;
    top: 64px;
    z-index: 90;
    height: calc(100vh - 64px);
  }
  .app-sidebar.is-open {
    transform: translateX(260px);
  }
}
</style>
