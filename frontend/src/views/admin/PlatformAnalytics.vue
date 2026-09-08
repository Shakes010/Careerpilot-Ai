<template>
  <AdminLayout>
    <div class="analytics-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Platform Analytics & Telemetry</h1>
          <p class="page-subtitle">Real-time system telemetry, active engagement rates, and platform placement metrics.</p>
        </div>
      </div>

      <AppLoader v-if="adminStore.loading && !analytics" message="Calculating platform metrics..." />

      <div v-else-if="analytics" class="analytics-content">
        <!-- Primary KPI Grid -->
        <div class="kpi-grid">
          <AppCard class="kpi-card">
            <div class="kpi-icon student-icon">
              <AppSvgIcon name="cap" size="24" />
            </div>
            <div class="kpi-data">
              <span class="kpi-label">Active Students</span>
              <h2 class="kpi-val">{{ analytics.active_students }}</h2>
            </div>
          </AppCard>

          <AppCard class="kpi-card">
            <div class="kpi-icon recruiter-icon">
              <AppSvgIcon name="briefcase" size="24" />
            </div>
            <div class="kpi-data">
              <span class="kpi-label">Active Recruiters</span>
              <h2 class="kpi-val">{{ analytics.active_recruiters }}</h2>
            </div>
          </AppCard>

          <AppCard class="kpi-card">
            <div class="kpi-icon company-icon">
              <AppSvgIcon name="building" size="24" />
            </div>
            <div class="kpi-data">
              <span class="kpi-label">Verified Companies</span>
              <h2 class="kpi-val">{{ analytics.verified_companies }}</h2>
            </div>
          </AppCard>

          <AppCard class="kpi-card">
            <div class="kpi-icon jobs-icon">
              <AppSvgIcon name="chart" size="24" />
            </div>
            <div class="kpi-data">
              <span class="kpi-label">Total Jobs Requisitions</span>
              <h2 class="kpi-val">{{ analytics.total_jobs }}</h2>
            </div>
          </AppCard>
        </div>

        <!-- Telemetry Details Grid -->
        <div class="telemetry-sections-grid">
          <AppCard title="Student Collaboration Telemetry" subtitle="Student project creation and Career Sandbox activity.">
            <div class="stat-rows">
              <div class="stat-item">
                <span class="stat-label">Active Collaboration Projects</span>
                <span class="stat-val">{{ analytics.total_projects }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Published Sandbox Challenges</span>
                <span class="stat-val">{{ analytics.sandbox_challenges_count }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Skills Taxonomy Size</span>
                <span class="stat-val">{{ analytics.skill_taxonomy_count }} Skills</span>
              </div>
            </div>
          </AppCard>

          <AppCard title="Trust & Verification Telemetry" subtitle="Company verification velocity and moderation safety.">
            <div class="stat-rows">
              <div class="stat-item">
                <span class="stat-label">Pending Company Verifications</span>
                <span class="stat-val text-warning">{{ analytics.pending_verifications }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Pending Flagged Safety Reports</span>
                <span class="stat-val text-danger">{{ analytics.flagged_activities_count }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Platform Health Index</span>
                <span class="stat-val text-success">98.5% Healthy</span>
              </div>
            </div>
          </AppCard>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppSvgIcon from '@/components/common/AppSvgIcon.vue'
import { useAdminStore } from '@/stores/admin'

const adminStore = useAdminStore()
const analytics = computed(() => adminStore.analytics)

onMounted(() => {
  adminStore.fetchAnalyticsOverview()
})
</script>

<style scoped>
.analytics-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.analytics-content { display: flex; flex-direction: column; gap: 1.5rem; }

.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; }
.kpi-card { display: flex; align-items: center; gap: 1rem; }
.kpi-icon { width: 48px; height: 48px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; }
.student-icon { background: #dbeafe; color: #1e40af; }
.recruiter-icon { background: #e0e7ff; color: #3730a3; }
.company-icon { background: #dcfce7; color: #166534; }
.jobs-icon { background: #fef3c7; color: #92400e; }

.kpi-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }
.kpi-val { font-size: 1.75rem; font-weight: 700; color: var(--text-heading); margin-top: 0.125rem; }

.telemetry-sections-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; }
.stat-rows { display: flex; flex-direction: column; gap: 1rem; margin-top: 0.75rem; }
.stat-item { display: flex; justify-content: space-between; align-items: center; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border); }
.stat-label { font-size: 0.875rem; color: var(--text-secondary); }
.stat-val { font-size: 1.125rem; font-weight: 700; color: var(--text-heading); }

.text-warning { color: var(--warning); }
.text-danger { color: var(--danger); }
.text-success { color: var(--success); }
</style>
