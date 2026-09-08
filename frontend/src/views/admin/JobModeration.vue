<template>
  <AdminLayout>
    <div class="moderation-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Job Requisition Moderation 🔍</h1>
          <p class="page-subtitle">Inspect job requisitions for quality, anti-spam compliance, and description accuracy.</p>
        </div>
      </div>

      <!-- Moderation Filter Card -->
      <AppCard class="filter-card">
        <div class="filter-row">
          <AppInput
            v-model="search"
            placeholder="Search jobs by title, description or category..."
            @keyup.enter="handleFilter"
          />
          <AppSelect
            v-model="statusFilter"
            :options="statusOptions"
            placeholder="All Moderation Statuses"
            @change="handleFilter"
          />
        </div>
      </AppCard>

      <!-- Jobs Table -->
      <div class="jobs-table-container">
        <AppTable
          :columns="columns"
          :data="adminStore.moderationJobs"
          :loading="adminStore.loading"
          empty-message="No jobs found matching moderation criteria."
        >
          <template #title="{ row }">
            <div class="job-title">{{ row.title }}</div>
            <div class="job-meta">📍 {{ row.location }} • {{ row.employment_type }}</div>
          </template>

          <template #moderation_status="{ row }">
            <AppBadge :status="row.moderation_status" />
          </template>

          <template #status="{ row }">
            <AppBadge :status="row.status" />
          </template>

          <template #actions="{ row }">
            <div class="table-actions">
              <button
                v-if="row.moderation_status !== 'APPROVED'"
                class="btn btn-primary btn-sm"
                @click="moderate(row, 'APPROVED')"
              >
                Approve
              </button>
              <button
                v-if="row.moderation_status !== 'FLAGGED'"
                class="btn btn-secondary btn-sm"
                @click="moderate(row, 'FLAGGED')"
              >
                Flag
              </button>
              <button
                v-if="row.moderation_status !== 'TAKEN_DOWN'"
                class="btn btn-danger btn-sm"
                @click="moderate(row, 'TAKEN_DOWN')"
              >
                Take Down
              </button>
            </div>
          </template>
        </AppTable>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppTable from '@/components/common/AppTable.vue'
import { useAdminStore } from '@/stores/admin'
import { useToast } from '@/components/common/AppToast.vue'

const adminStore = useAdminStore()
const toast = useToast()

const search = ref('')
const statusFilter = ref('')

const columns = [
  { label: 'Job Title & Details', key: 'title' },
  { label: 'Recruiter Status', key: 'status' },
  { label: 'Moderation Status', key: 'moderation_status' },
  { label: 'Actions', key: 'actions' }
]

const statusOptions = [
  { label: 'All Moderation Statuses', value: '' },
  { label: 'APPROVED', value: 'APPROVED' },
  { label: 'FLAGGED', value: 'FLAGGED' },
  { label: 'TAKEN_DOWN', value: 'TAKEN_DOWN' }
]

const handleFilter = () => {
  adminStore.fetchJobsForModeration({
    search: search.value || undefined,
    status: statusFilter.value || undefined
  })
}

const moderate = async (job, status) => {
  try {
    await adminStore.moderateJob(job.id, status)
    toast.show(`✓ Job '${job.title}' moderation status set to ${status}`)
  } catch (err) {
    toast.show('Failed to moderate job.', 'error')
  }
}

onMounted(() => {
  adminStore.fetchJobsForModeration()
})
</script>

<style scoped>
.moderation-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.filter-row { display: grid; grid-template-columns: 3fr 1fr; gap: 1rem; }
.job-title { font-weight: 600; color: var(--text-heading); }
.job-meta { font-size: 0.75rem; color: var(--text-secondary); }
.table-actions { display: flex; gap: 0.375rem; }
</style>
