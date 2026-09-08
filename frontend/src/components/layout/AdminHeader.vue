<template>
  <header class="admin-header">
    <div class="header-left">
      <div class="brand">
        <AppSvgIcon name="shield" size="22" class="brand-icon" />
        <span class="brand-text">CareerPilot <span class="brand-ai">AI</span></span>
        <span class="admin-badge">Admin Portal</span>
      </div>
    </div>

    <div class="header-right">
      <div class="admin-user-info">
        <span class="admin-name">{{ authStore.user?.full_name || 'Administrator' }}</span>
        <span class="admin-role-chip">Platform Admin</span>
      </div>
      <router-link to="/settings" class="btn btn-secondary btn-sm flex-btn">
        <AppSvgIcon name="settings" size="14" /> Settings
      </router-link>
      <button class="btn btn-secondary btn-sm flex-btn" @click="handleLogout">
        <AppSvgIcon name="logout" size="14" /> Logout
      </button>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppSvgIcon from '@/components/common/AppSvgIcon.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-header {
  height: 64px;
  background-color: #0f172a;
  color: #ffffff;
  border-bottom: 1px solid #1e293b;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left { display: flex; align-items: center; gap: 1rem; }

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 1.25rem;
}

.brand-icon { color: #ef4444; }
.brand-ai { color: #3b82f6; }

.admin-badge {
  font-size: 0.6875rem;
  font-weight: 700;
  padding: 0.125rem 0.5rem;
  border-radius: var(--radius-full);
  background-color: #ef4444;
  color: #ffffff;
  text-transform: uppercase;
}

.header-right { display: flex; align-items: center; gap: 0.75rem; }

.flex-btn { display: flex; align-items: center; gap: 0.375rem; }

.admin-user-info { display: flex; flex-direction: column; text-align: right; }
.admin-name { font-size: 0.875rem; font-weight: 600; color: #f8fafc; }
.admin-role-chip { font-size: 0.6875rem; color: #94a3b8; text-transform: uppercase; }
</style>
