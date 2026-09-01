<template>
  <div class="job-card">
    <div class="job-card-header">
      <div>
        <h4 class="job-title">{{ job.title }}</h4>
        <div class="job-meta">
          <span class="meta-item">📍 {{ job.location }} ({{ job.work_mode }})</span>
          <span class="meta-item">💼 {{ formatType(job.employment_type) }}</span>
          <span class="meta-item">⏱️ {{ job.experience_min }}-{{ job.experience_max }} yrs exp</span>
        </div>
      </div>
      <AppBadge :status="job.status" />
    </div>

    <p class="job-description">{{ truncateText(job.description, 140) }}</p>

    <div class="skills-tags">
      <span v-for="skill in job.skills" :key="skill.id || skill" class="skill-tag">
        {{ skill.skill_name || skill }}
      </span>
    </div>

    <div class="job-card-footer">
      <div class="salary-text" v-if="job.salary_min || job.salary_max">
        💰 ₹{{ formatSalary(job.salary_min) }} - ₹{{ formatSalary(job.salary_max) }}
      </div>
      <div class="deadline-text">
        Deadline: {{ formatDate(job.application_deadline) }}
      </div>
      <div class="action-buttons">
        <router-link :to="`/recruiter/jobs/${job.id}`" class="btn btn-secondary btn-sm">
          View
        </router-link>
        <router-link v-if="job.status !== 'CLOSED'" :to="`/recruiter/jobs/${job.id}/edit`" class="btn btn-secondary btn-sm">
          Edit
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppBadge from '@/components/common/AppBadge.vue'

defineProps({
  job: { type: Object, required: true }
})

const formatType = (type) => {
  if (!type) return ''
  return type.replace('_', ' ')
}

const formatSalary = (val) => {
  if (!val) return 'N/A'
  if (val >= 100000) return `${(val / 100000).toFixed(1)}L`
  if (val >= 1000) return `${(val / 1000).toFixed(0)}K`
  return val
}

const formatDate = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
}

const truncateText = (str, len) => {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '...' : str
}
</script>

<style scoped>
.job-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.15s ease;
}

.job-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--border-focus);
}

.job-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.job-title {
  font-size: 1.0625rem;
  font-weight: 600;
  color: var(--text-heading);
}

.job-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.job-description {
  font-size: 0.875rem;
  color: var(--text-primary);
  line-height: 1.4;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.skill-tag {
  font-size: 0.75rem;
  background-color: var(--background);
  border: 1px solid var(--border);
  padding: 0.125rem 0.5rem;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.job-card-footer {
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
  font-size: 0.8125rem;
}

.salary-text {
  font-weight: 600;
  color: var(--text-heading);
}

.deadline-text {
  color: var(--text-muted);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}
</style>
