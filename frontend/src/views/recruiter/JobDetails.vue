<template>
  <DashboardLayout>
    <div class="job-details-page">
      <div class="page-header">
        <router-link to="/recruiter/jobs" class="back-link">
          ← Back to All Jobs
        </router-link>
        <div class="header-actions" v-if="job">
          <router-link v-if="job.status !== 'CLOSED'" :to="`/recruiter/jobs/${job.id}/edit`" class="btn btn-secondary">
            ✏️ Edit Job
          </router-link>

          <button
            v-if="['DRAFT', 'PAUSED'].includes(job.status)"
            class="btn btn-primary"
            @click="publishJob"
          >
            🚀 Publish Job
          </button>

          <button
            v-if="job.status === 'PUBLISHED'"
            class="btn btn-secondary"
            @click="pauseJob"
          >
            ⏸️ Pause Job
          </button>

          <button
            v-if="['PUBLISHED', 'PAUSED'].includes(job.status)"
            class="btn btn-secondary"
            @click="closeJob"
          >
            🔒 Close Job
          </button>

          <button
            v-if="job.status === 'DRAFT'"
            class="btn btn-danger"
            @click="deleteJob"
          >
            🗑️ Delete Draft
          </button>
        </div>
      </div>

      <AppLoader v-if="jobsStore.loading && !job" message="Loading job details..." />

      <div v-else-if="job" class="details-grid">
        <!-- Main Job Info -->
        <div class="main-column">
          <AppCard class="job-main-card">
            <div class="title-status-row">
              <div>
                <h1 class="job-title">{{ job.title }}</h1>
                <p class="job-category">{{ job.job_category || 'Software Engineering' }}</p>
              </div>
              <AppBadge :status="job.status" size="lg" />
            </div>

            <div class="meta-badges-row">
              <span class="meta-badge">📍 {{ job.location }} ({{ job.work_mode }})</span>
              <span class="meta-badge">💼 {{ formatType(job.employment_type) }}</span>
              <span class="meta-badge">⏱️ {{ job.experience_min }}-{{ job.experience_max }} Years Experience</span>
              <span class="meta-badge">👥 {{ job.number_of_openings }} Opening(s)</span>
            </div>

            <div class="details-divider"></div>

            <div class="section-block">
              <h3>Job Description</h3>
              <div class="description-text">{{ job.description }}</div>
            </div>

            <div class="section-block" v-if="job.education_requirements">
              <h3>Education & Qualifications</h3>
              <p class="text-body">{{ job.education_requirements }}</p>
            </div>

            <div class="section-block">
              <h3>Required Skills</h3>
              <div class="skills-wrap">
                <span v-for="skill in job.skills" :key="skill.id || skill" class="skill-tag">
                  {{ skill.skill_name || skill }}
                </span>
              </div>
            </div>
          </AppCard>

          <!-- Phase 2 Candidate Applications Placeholder -->
          <AppCard class="phase2-applications-card">
            <div class="phase2-header">
              <h3>Candidate Applications</h3>
              <span class="phase2-tag">Phase 2 Feature</span>
            </div>
            <p class="phase2-desc">
              Applications management, candidate profile unlock, and verified evidence review will be enabled in Phase 2.
            </p>
            <div class="phase2-placeholder-box">
              <span>👥 Candidate applications pipeline will appear here in Phase 2.</span>
            </div>
          </AppCard>
        </div>

        <!-- Sidebar Specs -->
        <div class="side-column">
          <AppCard class="specs-card">
            <h3>Job Specifications</h3>
            
            <div class="spec-item">
              <span class="spec-label">Compensation</span>
              <span class="spec-val" v-if="job.salary_min || job.salary_max">
                ₹{{ formatSalary(job.salary_min) }} - ₹{{ formatSalary(job.salary_max) }} {{ job.salary_currency }}
              </span>
              <span class="spec-val" v-else>Not specified</span>
            </div>

            <div class="spec-item">
              <span class="spec-label">Application Deadline</span>
              <span class="spec-val">{{ formatDate(job.application_deadline) }}</span>
            </div>

            <div class="spec-item">
              <span class="spec-label">Posted Date</span>
              <span class="spec-val">{{ formatDate(job.created_at) }}</span>
            </div>

            <div class="spec-item">
              <span class="spec-label">Last Updated</span>
              <span class="spec-val">{{ formatDate(job.updated_at) }}</span>
            </div>
          </AppCard>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import { useJobsStore } from '@/stores/jobs'
import { useToast } from '@/components/common/AppToast.vue'

const route = useRoute()
const router = useRouter()
const jobsStore = useJobsStore()
const toast = useToast()

const jobId = route.params.id
const job = computed(() => jobsStore.currentJob)

const formatType = (val) => val ? val.replace('_', ' ') : ''
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' }) : ''
const formatSalary = (val) => val ? val.toLocaleString('en-IN') : 'N/A'

const publishJob = async () => {
  try {
    await jobsStore.publishJob(jobId)
    toast.show('✓ Job published successfully')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to publish job.', 'error')
  }
}

const pauseJob = async () => {
  try {
    await jobsStore.pauseJob(jobId)
    toast.show('✓ Job paused')
  } catch (err) {
    toast.show('Failed to pause job.', 'error')
  }
}

const closeJob = async () => {
  try {
    await jobsStore.closeJob(jobId)
    toast.show('✓ Job closed')
  } catch (err) {
    toast.show('Failed to close job.', 'error')
  }
}

const deleteJob = async () => {
  if (confirm('Delete this draft job?')) {
    try {
      await jobsStore.deleteJob(jobId)
      toast.show('✓ Job deleted')
      router.push('/recruiter/jobs')
    } catch (err) {
      toast.show('Failed to delete job.', 'error')
    }
  }
}

onMounted(() => {
  jobsStore.fetchJobDetails(jobId)
})
</script>

<style scoped>
.job-details-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-link {
  font-size: 0.875rem;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.details-grid {
  display: grid;
  grid-template-columns: 3fr 1fr;
  gap: 1.5rem;
}

.main-column { display: flex; flex-direction: column; gap: 1.5rem; }

.title-status-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.job-title { font-size: 1.625rem; font-weight: 700; }
.job-category { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.meta-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.meta-badge {
  background-color: var(--background);
  border: 1px solid var(--border);
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.8125rem;
  color: var(--text-primary);
  font-weight: 500;
}

.details-divider {
  height: 1px;
  background-color: var(--border);
  margin: 1.5rem 0;
}

.section-block {
  margin-bottom: 1.5rem;
}

.section-block h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.description-text {
  font-size: 0.9375rem;
  line-height: 1.6;
  white-space: pre-wrap;
  color: var(--text-primary);
}

.skills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  background-color: var(--primary-light);
  color: var(--primary);
  border: 1px solid var(--primary-border);
  padding: 0.375rem 0.875rem;
  border-radius: var(--radius-full);
  font-size: 0.8125rem;
  font-weight: 600;
}

.phase2-applications-card {
  border-style: dashed;
}

.phase2-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.phase2-tag {
  font-size: 0.6875rem;
  font-weight: 700;
  background-color: #f1f5f9;
  color: var(--text-secondary);
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  text-transform: uppercase;
}

.phase2-desc { font-size: 0.8125rem; color: var(--text-secondary); margin-bottom: 1rem; }

.phase2-placeholder-box {
  background-color: var(--background);
  border: 1px dashed var(--border);
  padding: 2rem;
  text-align: center;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: var(--text-muted);
}

.specs-card h3 { font-size: 1rem; margin-bottom: 1.25rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }

.spec-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.spec-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.spec-val { font-size: 0.875rem; font-weight: 600; color: var(--text-heading); }

@media (max-width: 900px) {
  .details-grid { grid-template-columns: 1fr; }
}
</style>
