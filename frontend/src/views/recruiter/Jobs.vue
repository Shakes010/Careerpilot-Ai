<template>
  <DashboardLayout>
    <div class="jobs-page">
      <!-- Header -->
      <div class="page-header">
        <div>
          <h1 class="page-title">Jobs & Opportunities</h1>
          <p class="page-subtitle">Create and manage your company's open requisitions.</p>
        </div>
        <router-link to="/recruiter/jobs/create" class="btn btn-primary">
          + Create Job
        </router-link>
      </div>

      <!-- Search & Filters Bar -->
      <AppCard class="filters-card">
        <div class="filters-grid">
          <div class="search-input-box">
            <AppInput
              v-model="filters.search"
              placeholder="Search by title, description or category..."
              @keyup.enter="handleSearch"
            />
          </div>

          <AppSelect
            v-model="filters.status"
            :options="statusOptions"
            placeholder="All Statuses"
            @change="handleSearch"
          />

          <AppSelect
            v-model="filters.employment_type"
            :options="typeOptions"
            placeholder="All Employment Types"
            @change="handleSearch"
          />

          <AppSelect
            v-model="filters.work_mode"
            :options="workModeOptions"
            placeholder="All Work Modes"
            @change="handleSearch"
          />
        </div>
      </AppCard>

      <!-- Desktop Table / Mobile Cards -->
      <div class="jobs-container">
        <AppTable
          :columns="columns"
          :data="jobsStore.jobs"
          :loading="jobsStore.loading"
          empty-message="No jobs found matching your filters."
        >
          <template #title="{ row }">
            <router-link :to="`/recruiter/jobs/${row.id}`" class="job-table-title">
              {{ row.title }}
            </router-link>
            <div class="job-table-meta">{{ row.location }} • {{ row.work_mode }}</div>
          </template>

          <template #employment_type="{ row }">
            {{ formatType(row.employment_type) }}
          </template>

          <template #status="{ row }">
            <AppBadge :status="row.status" />
          </template>

          <template #application_deadline="{ row }">
            {{ formatDate(row.application_deadline) }}
          </template>

          <template #actions="{ row }">
            <div class="table-actions">
              <router-link :to="`/recruiter/jobs/${row.id}`" class="btn btn-secondary btn-sm" title="View Details">
                View
              </router-link>

              <router-link v-if="row.status !== 'CLOSED'" :to="`/recruiter/jobs/${row.id}/edit`" class="btn btn-secondary btn-sm" title="Edit Job">
                Edit
              </router-link>

              <!-- State-based actions -->
              <button
                v-if="['DRAFT', 'PAUSED'].includes(row.status)"
                class="btn btn-primary btn-sm"
                @click="triggerPublish(row)"
              >
                Publish
              </button>

              <button
                v-if="row.status === 'PUBLISHED'"
                class="btn btn-secondary btn-sm"
                @click="triggerPause(row)"
              >
                Pause
              </button>

              <button
                v-if="['PUBLISHED', 'PAUSED'].includes(row.status)"
                class="btn btn-secondary btn-sm"
                @click="triggerClose(row)"
              >
                Close
              </button>

              <button
                v-if="row.status === 'DRAFT'"
                class="btn btn-danger btn-sm"
                @click="triggerDelete(row)"
              >
                Delete
              </button>
            </div>
          </template>
        </AppTable>
      </div>

      <!-- Confirmation Modal -->
      <AppModal
        :show="confirmModal.show"
        :title="confirmModal.title"
        @close="confirmModal.show = false"
      >
        <p>{{ confirmModal.message }}</p>
        <template #footer>
          <AppButton variant="secondary" @click="confirmModal.show = false">Cancel</AppButton>
          <AppButton :variant="confirmModal.variant" @click="executeConfirmedAction">
            Confirm
          </AppButton>
        </template>
      </AppModal>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppTable from '@/components/common/AppTable.vue'
import AppModal from '@/components/common/AppModal.vue'
import { useJobsStore } from '@/stores/jobs'
import { useToast } from '@/components/common/AppToast.vue'

const jobsStore = useJobsStore()
const toast = useToast()

const filters = reactive({
  search: '',
  status: '',
  employment_type: '',
  work_mode: ''
})

const columns = [
  { label: 'Job Title & Location', key: 'title' },
  { label: 'Employment Type', key: 'employment_type' },
  { label: 'Work Mode', key: 'work_mode' },
  { label: 'Status', key: 'status' },
  { label: 'Deadline', key: 'application_deadline' },
  { label: 'Actions', key: 'actions' }
]

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'DRAFT', value: 'DRAFT' },
  { label: 'PUBLISHED', value: 'PUBLISHED' },
  { label: 'PAUSED', value: 'PAUSED' },
  { label: 'CLOSED', value: 'CLOSED' }
]

const typeOptions = [
  { label: 'All Types', value: '' },
  { label: 'Full-Time', value: 'FULL_TIME' },
  { label: 'Part-Time', value: 'PART_TIME' },
  { label: 'Internship', value: 'INTERNSHIP' },
  { label: 'Contract', value: 'CONTRACT' }
]

const workModeOptions = [
  { label: 'All Work Modes', value: '' },
  { label: 'Remote', value: 'REMOTE' },
  { label: 'Hybrid', value: 'HYBRID' },
  { label: 'Onsite', value: 'ONSITE' }
]

const confirmModal = reactive({
  show: false,
  title: '',
  message: '',
  variant: 'primary',
  actionType: null,
  jobId: null
})

const formatType = (val) => val ? val.replace('_', ' ') : ''
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' }) : ''

const handleSearch = () => {
  jobsStore.fetchJobs({
    search: filters.search || undefined,
    status: filters.status || undefined,
    employment_type: filters.employment_type || undefined,
    work_mode: filters.work_mode || undefined
  })
}

const triggerPublish = (job) => {
  confirmModal.title = 'Publish Job'
  confirmModal.message = `Are you sure you want to publish '${job.title}'? This will make it visible to candidates.`
  confirmModal.variant = 'primary'
  confirmModal.actionType = 'publish'
  confirmModal.jobId = job.id
  confirmModal.show = true
}

const triggerPause = (job) => {
  confirmModal.title = 'Pause Job'
  confirmModal.message = `Pause application intake for '${job.title}'?`
  confirmModal.variant = 'secondary'
  confirmModal.actionType = 'pause'
  confirmModal.jobId = job.id
  confirmModal.show = true
}

const triggerClose = (job) => {
  confirmModal.title = 'Close Job'
  confirmModal.message = `Close '${job.title}' permanently? Closed jobs cannot be republished.`
  confirmModal.variant = 'danger'
  confirmModal.actionType = 'close'
  confirmModal.jobId = job.id
  confirmModal.show = true
}

const triggerDelete = (job) => {
  confirmModal.title = 'Delete Draft Job'
  confirmModal.message = `Delete draft job '${job.title}'? This action cannot be undone.`
  confirmModal.variant = 'danger'
  confirmModal.actionType = 'delete'
  confirmModal.jobId = job.id
  confirmModal.show = true
}

const executeConfirmedAction = async () => {
  const { actionType, jobId } = confirmModal
  confirmModal.show = false

  try {
    if (actionType === 'publish') {
      await jobsStore.publishJob(jobId)
      toast.show('✓ Job published successfully')
    } else if (actionType === 'pause') {
      await jobsStore.pauseJob(jobId)
      toast.show('✓ Job paused')
    } else if (actionType === 'close') {
      await jobsStore.closeJob(jobId)
      toast.show('✓ Job closed')
    } else if (actionType === 'delete') {
      await jobsStore.deleteJob(jobId)
      toast.show('✓ Job deleted')
    }
  } catch (err) {
    const msg = err.response?.data?.detail || 'Operation failed.'
    toast.show(msg, 'error')
  }
}

onMounted(() => {
  jobsStore.fetchJobs()
})
</script>

<style scoped>
.jobs-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
}

.page-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
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
  flex-wrap: wrap;
}

@media (max-width: 900px) {
  .filters-grid { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 600px) {
  .filters-grid { grid-template-columns: 1fr; }
}
</style>
