<template>
  <aside class="admin-sidebar">
    <div class="sidebar-nav">
      <div class="nav-section-title">ADMINISTRATION</div>

      <router-link to="/admin/dashboard" class="nav-item" active-class="active">
        <AppSvgIcon name="dashboard" size="18" class="nav-icon" />
        <span class="nav-label">Admin Dashboard</span>
      </router-link>

      <router-link to="/admin/users" class="nav-item" active-class="active">
        <AppSvgIcon name="users" size="18" class="nav-icon" />
        <span class="nav-label">User Management</span>
      </router-link>

      <router-link to="/admin/verifications" class="nav-item" active-class="active">
        <AppSvgIcon name="building" size="18" class="nav-icon" />
        <span class="nav-label">Recruiter Verification</span>
        <span class="priority-dot" title="High Priority">⚠️</span>
      </router-link>

      <router-link to="/admin/job-moderation" class="nav-item" active-class="active">
        <AppSvgIcon name="search" size="18" class="nav-icon" />
        <span class="nav-label">Job Moderation</span>
      </router-link>

      <router-link to="/admin/skills" class="nav-item" active-class="active">
        <AppSvgIcon name="book" size="18" class="nav-icon" />
        <span class="nav-label">Skill Library</span>
      </router-link>

      <div class="nav-divider"></div>
      <div class="nav-section-title">ANALYTICS & GOVERNANCE</div>

      <router-link to="/admin/analytics" class="nav-item" active-class="active">
        <AppSvgIcon name="chart" size="18" class="nav-icon" />
        <span class="nav-label">Platform Analytics</span>
      </router-link>

      <router-link to="/admin/notifications" class="nav-item" active-class="active">
        <AppSvgIcon name="bell" size="18" class="nav-icon" />
        <span class="nav-label">Notifications</span>
      </router-link>

      <router-link to="/admin/flagged-queue" class="nav-item" active-class="active">
        <AppSvgIcon name="flag" size="18" class="nav-icon" />
        <span class="nav-label">Flagged Review Queue</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup>
import AppSvgIcon from '@/components/common/AppSvgIcon.vue'
</script>

<style scoped>
.admin-sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid var(--border);
  min-height: calc(100vh - 64px);
  padding: 1.25rem 0.75rem;
  display: flex;
  flex-direction: column;
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

.nav-item:hover {
  background-color: var(--primary-light);
  color: var(--primary);
}

.nav-item.active {
  background-color: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
  border-left: 3px solid var(--primary);
}

.nav-icon { color: var(--text-muted); }
.nav-item.active .nav-icon { color: var(--primary); }

.priority-dot { margin-left: auto; font-size: 0.75rem; }

.nav-divider {
  height: 1px;
  background-color: var(--border);
  margin: 0.75rem 0;
}
</style>
