<template>
  <AdminLayout>
    <div class="admin-dashboard-page">
      <div class="dashboard-header">
        <div>
          <h1 class="welcome-heading">Admin Command Center 🛡️</h1>
          <p class="welcome-subtitle">Platform overview, pending recruiter verification queue, and skill taxonomy.</p>
        </div>
      </div>

      <!-- Telemetry Cards -->
      <div class="metrics-grid">
        <AppCard class="metric-card priority-card">
          <div class="metric-icon warning-icon">⏳</div>
          <div class="metric-info">
            <span class="metric-label">Pending Verifications ⚠️</span>
            <h3 class="metric-value">{{ metrics.pending_verifications ?? 0 }}</h3>
          </div>
          <router-link to="/admin/verifications" class="card-action-link">Review Queue →</router-link>
        </AppCard>

        <AppCard class="metric-card">
          <div class="metric-icon success-icon">🏢</div>
          <div class="metric-info">
            <span class="metric-label">Verified Companies</span>
            <h3 class="metric-value">{{ metrics.verified_companies ?? 0 }}</h3>
          </div>
        </AppCard>

        <AppCard class="metric-card">
          <div class="metric-icon jobs-icon">💼</div>
          <div class="metric-info">
            <span class="metric-label">Total Jobs Requisitions</span>
            <h3 class="metric-value">{{ metrics.total_jobs ?? 0 }}</h3>
          </div>
          <router-link to="/admin/job-moderation" class="card-action-link">Moderate Jobs →</router-link>
        </AppCard>

        <AppCard class="metric-card">
          <div class="metric-icon skills-icon">📚</div>
          <div class="metric-info">
            <span class="metric-label">Skills Library Taxonomy</span>
            <h3 class="metric-value">{{ metrics.total_skills ?? 0 }}</h3>
          </div>
          <router-link to="/admin/skills" class="card-action-link">Manage Skills →</router-link>
        </AppCard>
      </div>

      <!-- Quick Action Modules -->
      <div class="admin-modules-grid">
        <AppCard title="⚠️ Recruiter Company Verifications" subtitle="Approve or reject newly registered recruiter companies.">
          <p class="card-text">
            Recruiters cannot publish job requisitions until their company is verified by an administrator.
          </p>
          <div class="mt-4">
            <router-link to="/admin/verifications" class="btn btn-primary btn-sm">
              Open Verification Queue
            </router-link>
          </div>
        </AppCard>

        <AppCard title="🔍 Job Posting Moderation" subtitle="Inspect newly created or updated job requisitions for policy compliance.">
          <p class="card-text">
            Approve, flag for revisions, or take down non-compliant job postings.
          </p>
          <div class="mt-4">
            <router-link to="/admin/job-moderation" class="btn btn-secondary btn-sm">
              Open Moderation Queue
            </router-link>
          </div>
        </AppCard>

        <AppCard title="📚 Master Skill Taxonomy" subtitle="Manage centralized skills database for student verification and job postings.">
          <p class="card-text">
            Add new skill entries, edit categories, or remove outdated skill tags.
          </p>
          <div class="mt-4">
            <router-link to="/admin/skills" class="btn btn-secondary btn-sm">
              Manage Skill Library
            </router-link>
          </div>
        </AppCard>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import { useAdminStore } from '@/stores/admin'

const adminStore = useAdminStore()
const metrics = computed(() => adminStore.metrics || {})

onMounted(() => {
  adminStore.fetchDashboardMetrics()
})
</script>

<style scoped>
.admin-dashboard-page { display: flex; flex-direction: column; gap: 1.5rem; }
.welcome-heading { font-size: 1.625rem; font-weight: 700; }
.welcome-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; }
.metric-card { display: flex; flex-direction: column; gap: 0.5rem; position: relative; }
.priority-card { border-color: var(--warning-border); background-color: #fffbeb; }
.metric-icon { width: 44px; height: 44px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.warning-icon { background: #fef3c7; }
.success-icon { background: #dcfce7; }
.jobs-icon { background: #dbeafe; }
.skills-icon { background: #f3e8ff; }
.metric-label { font-size: 0.8125rem; color: var(--text-secondary); font-weight: 500; }
.metric-value { font-size: 1.625rem; font-weight: 700; color: var(--text-heading); }
.card-action-link { font-size: 0.75rem; font-weight: 600; color: var(--primary); margin-top: 0.25rem; }

.admin-modules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.card-text { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; }
.mt-4 { margin-top: 1rem; }
</style>
