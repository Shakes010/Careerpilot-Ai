<template>
  <AdminLayout>
    <div class="verifications-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Recruiter Company Verification ⚠️</h1>
          <p class="page-subtitle">Review pending company registrations. Verified status unlocks job publishing capability.</p>
        </div>
        <div class="header-actions">
          <AppButton
            :variant="viewMode === 'pending' ? 'primary' : 'secondary'"
            size="sm"
            @click="switchView('pending')"
          >
            Pending Requests ({{ adminStore.pendingCompanies.length }})
          </AppButton>
          <AppButton
            :variant="viewMode === 'all' ? 'primary' : 'secondary'"
            size="sm"
            @click="switchView('all')"
          >
            All Companies
          </AppButton>
        </div>
      </div>

      <!-- Pending Verifications Section -->
      <div v-if="viewMode === 'pending'" class="verifications-container">
        <AppLoader v-if="adminStore.loading && adminStore.pendingCompanies.length === 0" message="Loading verification queue..." />

        <AppEmptyState
          v-else-if="adminStore.pendingCompanies.length === 0"
          title="No Pending Verification Requests"
          message="Great news! All recruiter company registrations have been processed."
        />

        <div v-else class="companies-queue-grid">
          <AppCard
            v-for="company in adminStore.pendingCompanies"
            :key="company.id"
            class="company-verification-card"
          >
            <div class="company-card-header">
              <div>
                <h3 class="company-name">{{ company.name }}</h3>
                <p class="company-legal" v-if="company.legal_name">Legal Name: {{ company.legal_name }}</p>
              </div>
              <AppBadge status="PENDING" />
            </div>

            <div class="company-specs-grid">
              <div class="spec-row">
                <span class="spec-label">Official Website:</span>
                <a :href="formatUrl(company.website)" target="_blank" class="spec-link">{{ company.website || 'Not provided' }}</a>
              </div>
              <div class="spec-row">
                <span class="spec-label">Contact Email:</span>
                <span class="spec-val">{{ company.email || 'N/A' }}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Industry:</span>
                <span class="spec-val">{{ company.industry || 'Tech' }}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Company Size:</span>
                <span class="spec-val">{{ company.company_size || 'N/A' }}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Location:</span>
                <span class="spec-val">{{ company.location || 'N/A' }}</span>
              </div>
            </div>

            <p class="company-desc" v-if="company.description">{{ company.description }}</p>

            <div class="verification-actions">
              <AppButton
                variant="primary"
                size="sm"
                :loading="processingId === company.id"
                @click="approveVerification(company)"
              >
                ✓ Approve Verification
              </AppButton>
              <AppButton
                variant="danger"
                size="sm"
                @click="openRejectModal(company)"
              >
                ✕ Reject Request
              </AppButton>
            </div>
          </AppCard>
        </div>
      </div>

      <!-- All Companies Table View -->
      <div v-else class="all-companies-container">
        <AppTable
          :columns="companyColumns"
          :data="adminStore.allCompanies"
          :loading="adminStore.loading"
          empty-message="No company records found."
        >
          <template #name="{ row }">
            <div class="font-semibold">{{ row.name }}</div>
            <div class="text-xs text-muted">{{ row.website }}</div>
          </template>

          <template #verification_status="{ row }">
            <AppBadge :status="row.verification_status" />
          </template>

          <template #actions="{ row }">
            <div class="table-actions">
              <button
                v-if="row.verification_status !== 'VERIFIED'"
                class="btn btn-primary btn-sm"
                @click="approveVerification(row)"
              >
                Approve
              </button>
              <button
                v-if="row.verification_status !== 'REJECTED'"
                class="btn btn-danger btn-sm"
                @click="openRejectModal(row)"
              >
                Reject
              </button>
            </div>
          </template>
        </AppTable>
      </div>

      <!-- Rejection Modal -->
      <AppModal
        :show="rejectModal.show"
        title="Reject Company Verification"
        @close="rejectModal.show = false"
      >
        <p class="modal-desc">
          Please provide feedback explaining why <strong>{{ rejectModal.companyName }}</strong>'s verification is being rejected. This note will be visible to the recruiter.
        </p>

        <AppInput
          v-model="rejectModal.notes"
          label="Rejection Reason / Feedback Notes *"
          placeholder="e.g. Work email domain does not match official company domain name."
          required
          :error="rejectModal.error"
        />

        <template #footer>
          <AppButton variant="secondary" @click="rejectModal.show = false">Cancel</AppButton>
          <AppButton variant="danger" :loading="rejectModal.loading" @click="executeRejection">
            Confirm Rejection
          </AppButton>
        </template>
      </AppModal>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppTable from '@/components/common/AppTable.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppEmptyState from '@/components/common/AppEmptyState.vue'
import { useAdminStore } from '@/stores/admin'
import { useToast } from '@/components/common/AppToast.vue'

const adminStore = useAdminStore()
const toast = useToast()

const viewMode = ref('pending')
const processingId = ref(null)

const rejectModal = reactive({
  show: false,
  companyId: null,
  companyName: '',
  notes: '',
  error: '',
  loading: false
})

const companyColumns = [
  { label: 'Company Name', key: 'name' },
  { label: 'Industry', key: 'industry' },
  { label: 'Status', key: 'verification_status' },
  { label: 'Contact Email', key: 'email' },
  { label: 'Actions', key: 'actions' }
]

const formatUrl = (url) => {
  if (!url) return '#'
  return url.startsWith('http') ? url : `https://${url}`
}

const switchView = (mode) => {
  viewMode.value = mode
  if (mode === 'pending') {
    adminStore.fetchPendingVerifications()
  } else {
    adminStore.fetchAllCompanies()
  }
}

const approveVerification = async (company) => {
  processingId.value = company.id
  try {
    await adminStore.verifyCompany(company.id)
    toast.show(`✓ Company '${company.name}' has been officially verified!`)
    if (viewMode.value === 'all') adminStore.fetchAllCompanies()
  } catch (err) {
    toast.show('Failed to verify company.', 'error')
  } finally {
    processingId.value = null
  }
}

const openRejectModal = (company) => {
  rejectModal.companyId = company.id
  rejectModal.companyName = company.name
  rejectModal.notes = ''
  rejectModal.error = ''
  rejectModal.show = true
}

const executeRejection = async () => {
  if (!rejectModal.notes.trim()) {
    rejectModal.error = 'Rejection reason notes are required.'
    return
  }

  rejectModal.loading = true
  try {
    await adminStore.rejectCompany(rejectModal.companyId, rejectModal.notes)
    toast.show(`Verification rejected for ${rejectModal.companyName}`, 'info')
    rejectModal.show = false
    if (viewMode.value === 'all') adminStore.fetchAllCompanies()
  } catch (err) {
    toast.show('Failed to reject verification.', 'error')
  } finally {
    rejectModal.loading = false
  }
}

onMounted(() => {
  adminStore.fetchPendingVerifications()
})
</script>

<style scoped>
.verifications-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.header-actions { display: flex; gap: 0.5rem; }

.companies-queue-grid { display: flex; flex-direction: column; gap: 1.25rem; }

.company-card-header { display: flex; justify-content: space-between; align-items: flex-start; padding-bottom: 0.75rem; border-bottom: 1px solid var(--border); }
.company-name { font-size: 1.25rem; font-weight: 700; color: var(--text-heading); }
.company-legal { font-size: 0.8125rem; color: var(--text-secondary); margin-top: 0.125rem; }

.company-specs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin: 1rem 0; background-color: var(--background); padding: 0.875rem; border-radius: var(--radius-sm); font-size: 0.8125rem; }
.spec-row { display: flex; flex-direction: column; }
.spec-label { font-weight: 600; color: var(--text-muted); text-transform: uppercase; font-size: 0.6875rem; }
.spec-val { color: var(--text-heading); font-weight: 500; }
.spec-link { color: var(--primary); text-decoration: underline; word-break: break-all; }

.company-desc { font-size: 0.875rem; color: var(--text-primary); margin-bottom: 1rem; line-height: 1.5; }

.verification-actions { display: flex; gap: 0.75rem; justify-content: flex-end; padding-top: 0.75rem; border-top: 1px solid var(--border); }

.modal-desc { font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem; }
.table-actions { display: flex; gap: 0.375rem; }
.font-semibold { font-weight: 600; }
.text-xs { font-size: 0.75rem; }
.text-muted { color: var(--text-muted); }
</style>
