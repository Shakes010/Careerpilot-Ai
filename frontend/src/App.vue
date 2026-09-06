<template>
  <div id="app-shell">
    <!-- ================================================================
         Sidebar
         ================================================================ -->
    <aside class="sidebar" role="navigation" aria-label="Main navigation">
      <!-- Logo -->
      <div class="sidebar__logo">
        <div class="sidebar__logo-mark" aria-hidden="true">CP</div>
        <div>
          <div class="sidebar__logo-text">CareerPilot</div>
          <div class="sidebar__logo-sub">Admin Panel</div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="sidebar__nav">
        <div class="sidebar__section-label">Recruiter Module</div>

        <RouterLink id="nav-notifications" to="/notifications" class="sidebar__link">
          <!-- Bell icon -->
          <svg class="sidebar__link-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          Notifications
        </RouterLink>

        <RouterLink id="nav-users" to="/users" class="sidebar__link">
          <!-- Users icon -->
          <svg class="sidebar__link-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          User Management
        </RouterLink>
      </nav>

      <!-- Sidebar footer -->
      <div class="sidebar__footer">
        <div class="sidebar__branch-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">
            <circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/>
            <path d="M6 9v1a2 2 0 0 0 2 2h4a2 2 0 0 1 2 2v1"/>
          </svg>
          feature/sid-recruiter-payments
        </div>
      </div>
    </aside>

    <!-- ================================================================
         Main Content Area
         ================================================================ -->
    <div class="main-content">
      <!-- Top bar -->
      <header class="topbar">
        <h1 class="topbar__title">{{ currentPageTitle }}</h1>
        <div class="topbar__actions">
          <NotificationBell
            :unread-count="globalUnreadCount"
            @click="$router.push('/notifications')"
          />
        </div>
      </header>

      <!-- Router view -->
      <main class="page-body" role="main">
        <RouterView @unread-count-change="globalUnreadCount = $event" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import NotificationBell from './components/NotificationBell.vue'

const route = useRoute()
const globalUnreadCount = ref(0)

const currentPageTitle = computed(() => route.meta?.title ?? 'CareerPilot-AI')
</script>

<style scoped>
#app-shell {
  display: flex;
  min-height: 100vh;
}

.sidebar__footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-border);
}

.sidebar__branch-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: var(--color-gray-100);
  color: var(--color-gray-500);
  font-size: 0.7rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  font-family: monospace;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.topbar__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
