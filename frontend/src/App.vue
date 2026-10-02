<template>
  <div class="app-root">
    
    <!-- Permanent Left Sidebar for Authenticated Student View -->
    <aside
      v-if="authStore.isAuthenticated && authStore.role === 'student'"
      class="cp-sidebar"
    >
      <!-- Logo -->
      <div class="cp-sidebar-logo-wrap">
        <router-link to="/dashboard" class="cp-logo-link">
          <div class="cp-logo-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M3 12l19-9-9 19-2-8-8-2z" />
            </svg>
          </div>
          <span class="cp-logo-text">CareerPilot <em>AI</em></span>
        </router-link>
      </div>

      <!-- Main Nav -->
      <nav class="cp-sidebar-nav">
        <router-link
          to="/dashboard"
          :class="['cp-nav-item', ($route.path === '/dashboard' || $route.path === '/') && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <rect x="3" y="3" width="7" height="7" rx="1" stroke-width="2"/>
              <rect x="14" y="3" width="7" height="7" rx="1" stroke-width="2"/>
              <rect x="3" y="14" width="7" height="7" rx="1" stroke-width="2"/>
              <rect x="14" y="14" width="7" height="7" rx="1" stroke-width="2"/>
            </svg>
          </span>
          Dashboard
        </router-link>

        <router-link
          to="/passport"
          :class="['cp-nav-item', $route.path === '/passport' && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </span>
          Career Passport
        </router-link>

        <router-link
          to="/opportunities"
          :class="['cp-nav-item', $route.path === '/opportunities' && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
          </span>
          Opportunities
        </router-link>

        <router-link
          to="/applications"
          :class="['cp-nav-item', $route.path === '/applications' && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
          </span>
          Applications
        </router-link>

        <router-link
          to="/assessments"
          :class="['cp-nav-item', $route.path.includes('/assessments') && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2m-6 9l2 2 4-4"/>
            </svg>
          </span>
          Assessments
        </router-link>

        <router-link
          to="/skills"
          :class="['cp-nav-item', $route.path === '/skills' && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
            </svg>
          </span>
          Skill Builder
        </router-link>

        <router-link
          to="/projects"
          :class="['cp-nav-item', $route.path === '/projects' && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </span>
          Career Sandbox
        </router-link>

        <router-link
          to="/analytics"
          :class="['cp-nav-item', $route.path === '/analytics' && 'cp-nav-active']"
        >
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
          </span>
          Analytics
        </router-link>

        <div class="cp-sidebar-divider"></div>

        <button class="cp-nav-item cp-nav-logout" @click="handleLogout">
          <span class="cp-nav-icon">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </span>
          Logout
        </button>
      </nav>

      <!-- Bottom Section: Upgrade Card + Help -->
      <div class="cp-sidebar-bottom">
        <div v-if="authStore.isUserPremium" class="cp-upgrade-card cp-upgrade-card--active">
          <div class="cp-upgrade-crown">⭐ Student PRO Active</div>
          <p class="cp-upgrade-desc">Premium features unlocked: Granular Match, Pro Templates &amp; Badges.</p>
          <router-link to="/billing" class="cp-upgrade-btn cp-upgrade-btn--active">View Invoices / Perks →</router-link>
        </div>
        <div v-else class="cp-upgrade-card">
          <div class="cp-upgrade-crown">👑 Upgrade to Pro</div>
          <p class="cp-upgrade-desc">Unlock advanced insights, AI coaching and exclusive opportunities.</p>
          <router-link to="/billing" class="cp-upgrade-btn">Upgrade Now (₹499) →</router-link>
        </div>
      </div>
    </aside>

    <!-- Main Container -->
    <div class="app-main">
      <AppNavbar v-if="authStore.isAuthenticated && authStore.role !== 'student'" />
      <main :class="authStore.isAuthenticated ? 'app-content' : 'app-content-full'">
        <router-view />
      </main>
    </div>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppNavbar from './components/AppNavbar.vue'
import { useAuthStore } from './store'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.refreshProfile()
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
@import './style.css';
</style>

<style scoped>
/* ---- App Shell ---- */
.app-root {
  display: flex;
  min-height: 100vh;
  background-color: #F0F4FF;
  font-family: 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-content {
  flex: 1;
  padding: 28px 32px;
  width: 100%;
}

.app-content-full {
  flex: 1;
  width: 100%;
  margin: 0;
  padding: 0;
}

/* ---- Sidebar ---- */
.cp-sidebar {
  width: 220px;
  min-width: 220px;
  background: #FFFFFF;
  border-right: 1px solid #E8ECF0;
  display: none;
  flex-direction: column;
  min-height: 100vh;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  flex-shrink: 0;
  box-shadow: 2px 0 8px rgba(0,0,0,0.04);
}

@media (min-width: 1024px) {
  .cp-sidebar { display: flex; }
}

/* Logo Row */
.cp-sidebar-logo-wrap {
  padding: 22px 20px 16px;
  border-bottom: 1px solid #F0F0F0;
  margin-bottom: 8px;
}

.cp-logo-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.cp-logo-icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: #2563EB;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(37,99,235,0.25);
}

.cp-logo-text {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.3px;
  font-style: normal;
}

.cp-logo-text em {
  font-style: normal;
  color: #2563EB;
}

/* Nav */
.cp-sidebar-nav {
  flex: 1;
  padding: 6px 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* Nav icon wrapper */
.cp-nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  flex-shrink: 0;
  color: currentColor;
}

/* Logout button */
.cp-nav-logout {
  color: #6B7280 !important;
  margin-top: 4px;
}
.cp-nav-logout:hover {
  background-color: #FEF2F2 !important;
  color: #EF4444 !important;
}

/* Sidebar divider */
.cp-sidebar-divider {
  height: 1px;
  background-color: #F0F0F0;
  margin: 10px 0;
}

/* Bottom section */
.cp-sidebar-bottom {
  padding: 12px 12px 20px;
  border-top: 1px solid #F0F0F0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Upgrade Card */
.cp-upgrade-card {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  border: 1px solid #BFDBFE;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.cp-upgrade-crown {
  font-size: 12px;
  font-weight: 800;
  color: #0F172A;
}

.cp-upgrade-desc {
  font-size: 11px;
  color: #475569;
  line-height: 1.5;
}

.cp-upgrade-btn {
  display: block;
  width: 100%;
  padding: 8px;
  background: #2563EB;
  color: #fff;
  text-align: center;
  font-weight: 700;
  font-size: 12px;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.12s ease;
  box-shadow: 0 4px 12px rgba(37,99,235,0.22);
}

.cp-upgrade-btn:hover {
  background: #1D4ED8;
}

/* Help Link */
.cp-help-link {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 600;
  color: #6B7280;
  text-decoration: none;
  padding: 0 4px;
  transition: color 0.12s ease;
}

.cp-help-link:hover {
  color: #0F172A;
}
</style>
