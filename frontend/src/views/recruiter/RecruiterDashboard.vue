<template>
  <DashboardLayout>
    <div class="dashboard-page">
      <!-- Dashboard Header -->
      <div class="dashboard-header">
        <div>
          <h1 class="welcome-heading">Good Morning, {{ authStore.user?.full_name || 'Recruiter' }}! 👋</h1>
          <p class="welcome-subtitle">Manage your company opportunities and track your active job postings.</p>
        </div>
        <div class="header-actions">
          <router-link to="/recruiter/jobs/create" class="btn btn-primary">
            + Create Job
          </router-link>
        </div>
      </div>

      <!-- Statistics Grid -->
      <div class="metrics-grid">
        <AppCard class="metric-card">
          <div class="metric-icon active-icon">💼</div>
          <div class="metric-info">
            <span class="metric-label">Active Published Jobs</span>
            <h3 class="metric-value">{{ metrics.active_jobs ?? 0 }}</h3>
          </div>
        </AppCard>

        <AppCard class="metric-card">
          <div class="metric-icon draft-icon">📝</div>
          <div class="metric-info">
            <span class="metric-label">Draft Jobs</span>
            <h3 class="metric-value">{{ metrics.draft_jobs ?? 0 }}</h3>
          </div>
        </AppCard>

        <AppCard class="metric-card">
          <div class="metric-icon total-icon">📂</div>
          <div class="metric-info">
            <span class="metric-label">Total Jobs Created</span>
            <h3 class="metric-value">{{ metrics.total_jobs ?? 0 }}</h3>
          </div>
        </AppCard>

        <AppCard class="metric-card">
          <div class="metric-icon company-icon">🏢</div>
          <div class="metric-info">
            <span class="metric-label">Company Status</span>
            <div class="mt-1">
              <AppBadge :status="authStore.companyVerificationStatus" />
            </div>
          </div>
        </AppCard>
      </div>

      <!-- Phase 2 Placeholders (Disabled) -->
      <div class="phase2-metrics-row">
        <div class="phase2-card disabled">
          <span class="p2-icon">👥</span>
          <div>
            <span class="p2-label">Total Applications</span>
            <span class="p2-badge">Coming in Phase 2</span>
          </div>
        </div>
        <div class="phase2-card disabled">
          <span class="p2-icon">✨</span>
          <div>
            <span class="p2-label">AI Candidate Matches</span>
            <span class="p2-badge">Coming in Phase 2</span>
          </div>
        </div>
      </div>

      <!-- Quick Actions Bar -->
      <div class="quick-actions-bar">
        <h3 class="section-title">Quick Actions</h3>
        <div class="actions-buttons">
          <router-link to="/recruiter/jobs/create" class="btn btn-primary btn-sm">
            + Create Job
          </router-link>
          <router-link to="/recruiter/jobs" class="btn btn-secondary btn-sm">
            💼 Manage All Jobs
          </router-link>
          <router-link to="/recruiter/company" class="btn btn-secondary btn-sm">
            🏢 Edit Company Profile
          </router-link>
        </div>
      </div>

      <!-- Recent Jobs Section -->
      <div class="recent-jobs-section">
        <div class="section-header">
          <h3 class="section-title">Recent Job Postings</h3>
          <router-link to="/recruiter/jobs" class="view-all-link">View All Jobs →</router-link>
        </div>

        <AppTable
          :columns="jobColumns"
          :data="recentJobs"
          :loading="jobsStore.loading"
          empty-message="No jobs posted yet. Click '+ Create Job' to post your first opportunity!"
        >
          <template #title="{ row }">
            <router-link :to="`/recruiter/jobs/${row.id}`" class="job-table-title">
              {{ row.title }}
            </router-link>
            <div class="job-table-meta">{{ row.location }} • {{ row.work_mode }}</div>
          </template>

          <template #status="{ row }">
            <AppBadge :status="row.status" />
          </template>

          <template #application_deadline="{ row }">
            {{ formatDate(row.application_deadline) }}
          </template>

          <template #created_at="{ row }">
            {{ formatDate(row.created_at) }}
          </template>

          <template #actions="{ row }">
            <div class="table-actions">
              <router-link :to="`/recruiter/jobs/${row.id}`" class="btn btn-secondary btn-sm">
                View
              </router-link>
              <router-link v-if="row.status !== 'CLOSED'" :to="`/recruiter/jobs/${row.id}/edit`" class="btn btn-secondary btn-sm">
                Edit
              </router-link>
            </div>
          </template>
        </AppTable>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppTable from '@/components/common/AppTable.vue'
import { useAuthStore } from '@/stores/auth'
import { useJobsStore } from '@/stores/jobs'

const authStore = useAuthStore()
const jobsStore = useJobsStore()

const metrics = computed(() => {
  return jobsStore.dashboardMetrics?.metrics || {}
})

const recentJobs = computed(() => {
  return jobsStore.jobs.slice(0, 5)
})

const jobColumns = [
  { label: 'Job Title', key: 'title' },
  { label: 'Type', key: 'employment_type' },
  { label: 'Status', key: 'status' },
  { label: 'Deadline', key: 'application_deadline' },
  { label: 'Created', key: 'created_at' },
  { label: 'Actions', key: 'actions' }
]

const formatDate = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
}

onMounted(async () => {
  await authStore.fetchCurrentUser()
  await jobsStore.fetchDashboardMetrics()
  await jobsStore.fetchJobs({ page: 1, page_size: 5 })
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.welcome-heading {
  font-size: 1.625rem;
  font-weight: 700;
}

.welcome-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.active-icon { background: #dbeafe; }
.draft-icon { background: #fef3c7; }
.total-icon { background: #e0e7ff; }
.company-icon { background: #dcfce7; }

.metric-label {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-heading);

}
.mt-1 { margin-top: 0.25rem; }

.phase2-metrics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.phase2-card {
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  opacity: 0.75;
}

.p2-icon { font-size: 1.25rem; }
.p2-label { font-size: 0.875rem; font-weight: 500; color: var(--text-secondary); display: block; }
.p2-badge { font-size: 0.6875rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; }

.quick-actions-bar {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
}

.actions-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.recent-jobs-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.view-all-link {
  font-size: 0.875rem;
  font-weight: 600;
}

.job-table-title {
  font-weight: 600;
  color: var(--text-heading);
}

.job-table-meta {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.table-actions {
  display: flex;
  gap: 0.375rem;
}

@media (max-width: 768px) {
  .phase2-metrics-row { grid-template-columns: 1fr; }
}
</style>
