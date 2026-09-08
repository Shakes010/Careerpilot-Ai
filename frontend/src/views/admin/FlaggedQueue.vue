<template>
  <AdminLayout>
    <div class="flagged-queue-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Flagged Activity Review Queue 🚩</h1>
          <p class="page-subtitle">Trust & safety moderation queue for reported profiles, suspicious job requisitions, and audit logs.</p>
        </div>
      </div>

      <!-- Filters Card -->
      <AppCard class="filter-card">
        <div class="filter-row">
          <AppSelect
            v-model="statusFilter"
            :options="statusOptions"
            placeholder="All Moderation Statuses"
            @change="handleFilter"
          />
        </div>
      </AppCard>

      <!-- Flagged Table -->
      <div class="flagged-table-container">
        <AppTable
          :columns="columns"
          :data="adminStore.flaggedActivities"
          :loading="adminStore.loading"
          empty-message="No flagged activity reports in queue."
        >
          <template #target="{ row }">
            <span class="target-chip">{{ row.target_type }}</span>
            <div class="text-xs text-muted">ID: {{ row.target_id }}</div>
          </template>

          <template #reason="{ row }">
            <div class="font-semibold">{{ row.reason }}</div>
            <div class="text-xs text-muted">Reporter: {{ row.reporter_name }}</div>
          </template>

          <template #risk_score="{ row }">
            <span :class="`risk-score score-${getRiskClass(row.risk_score)}`">
              {{ row.risk_score }} / 100
            </span>
          </template>

          <template #status="{ row }">
            <AppBadge :status="row.status" />
          </template>

          <template #actions="{ row }">
            <div v-if="row.status === 'PENDING'" class="table-actions">
              <button class="btn btn-secondary btn-sm" @click="resolve(row, 'WARNING_ISSUED')">
                Issue Warning
              </button>
              <button class="btn btn-danger btn-sm" @click="resolve(row, 'SUSPENDED')">
                Suspend
              </button>
              <button class="btn btn-primary btn-sm" @click="resolve(row, 'DISMISSED')">
                Dismiss
              </button>
            </div>
            <span v-else class="text-xs text-muted">Resolved</span>
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
import AppSelect from '@/components/common/AppSelect.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppTable from '@/components/common/AppTable.vue'
import { useAdminStore } from '@/stores/admin'
import { useToast } from '@/components/common/AppToast.vue'

const adminStore = useAdminStore()
const toast = useToast()

const statusFilter = ref('')

const columns = [
  { label: 'Target Type & ID', key: 'target' },
  { label: 'Reason & Reporter', key: 'reason' },
  { label: 'Risk Score', key: 'risk_score' },
  { label: 'Status', key: 'status' },
  { label: 'Actions', key: 'actions' }
]

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'Pending', value: 'PENDING' },
  { label: 'Warning Issued', value: 'WARNING_ISSUED' },
  { label: 'Suspended', value: 'SUSPENDED' },
  { label: 'Dismissed', value: 'DISMISSED' }
]

const getRiskClass = (score) => {
  if (score >= 75) return 'high'
  if (score >= 40) return 'medium'
  return 'low'
}

const handleFilter = () => {
  adminStore.fetchFlaggedActivities({
    status: statusFilter.value || undefined
  })
}

const resolve = async (flag, status) => {
  try {
    await adminStore.resolveFlaggedActivity(flag.id, status, `Resolution: ${status}`)
    toast.show(`✓ Report resolution updated to ${status}`)
  } catch (err) {
    toast.show('Failed to resolve report.', 'error')
  }
}

onMounted(() => {
  adminStore.fetchFlaggedActivities()
})
</script>

<style scoped>
.flagged-queue-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.filter-row { display: grid; grid-template-columns: 1fr; max-width: 300px; }

.target-chip { font-size: 0.75rem; font-weight: 700; background-color: #e0e7ff; color: #3730a3; padding: 0.125rem 0.5rem; border-radius: 4px; }
.risk-score { font-size: 0.8125rem; font-weight: 700; padding: 0.125rem 0.5rem; border-radius: 4px; }
.score-high { background-color: #fee2e2; color: #991b1b; }
.score-medium { background-color: #fef3c7; color: #92400e; }
.score-low { background-color: #dcfce7; color: #166534; }

.table-actions { display: flex; gap: 0.375rem; }
.font-semibold { font-weight: 600; }
.text-xs { font-size: 0.75rem; }
.text-muted { color: var(--text-muted); }
</style>
