<template>
  <aside class="student-sidebar">
    <div class="sidebar-nav">
      <div class="nav-section-title">STUDENT PORTAL</div>

      <router-link to="/student/projects" class="nav-item" active-class="active">
        <AppSvgIcon name="project" size="18" class="nav-icon" />
        <span class="nav-label">Projects</span>
      </router-link>

      <router-link to="/student/career-sandbox" class="nav-item" active-class="active">
        <AppSvgIcon name="flask" size="18" class="nav-icon" />
        <span class="nav-label">Career Sandbox</span>
      </router-link>
    </div>
  </aside>
</template>

<script setup>
import AppSvgIcon from '@/components/common/AppSvgIcon.vue'
</script>

<style scoped>
.student-sidebar {
  width: 240px;
  background-color: var(--surface);
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
  margin-top: 0.25rem;
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
  background-color: #d1fae5;
  color: #065f46;
}

.nav-item.active {
  background-color: #d1fae5;
  color: #065f46;
  font-weight: 600;
  border-left: 3px solid #10b981;
}

.nav-icon { color: var(--text-muted); }
.nav-item.active .nav-icon { color: #059669; }
</style>
