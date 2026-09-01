<template>
  <DashboardLayout>
    <div class="company-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Company Profile</h1>
          <p class="page-subtitle">Manage your organization's public information and verification status.</p>
        </div>
        <div class="header-right">
          <AppBadge :status="form.verification_status" size="lg" />
        </div>
      </div>

      <AppLoader v-if="recruiterStore.loading && !company" message="Loading company profile..." />

      <div v-else class="profile-grid">
        <!-- Main Form Card -->
        <AppCard class="main-profile-card">
          <div class="card-title-row">
            <h3>Organization Information</h3>
            <AppButton
              v-if="!isEditing"
              variant="secondary"
              size="sm"
              @click="isEditing = true"
            >
              ✏️ Edit Details
            </AppButton>
          </div>

          <form @submit.prevent="handleSave">
            <div class="form-row">
              <AppInput
                v-model="form.name"
                label="Company Name"
                :disabled="!isEditing"
                required
              />

              <AppInput
                v-model="form.legal_name"
                label="Legal Entity Name"
                placeholder="e.g. CareerPilot AI Private Limited"
                :disabled="!isEditing"
              />
            </div>

            <div class="form-row">
              <AppInput
                v-model="form.website"
                label="Official Website"
                placeholder="https://company.com"
                :disabled="!isEditing"
              />

              <AppInput
                v-model="form.industry"
                label="Industry / Domain"
                placeholder="e.g. Software & Technology"
                :disabled="!isEditing"
              />
            </div>

            <div class="form-row">
              <AppSelect
                v-model="form.company_size"
                label="Company Size"
                :options="sizeOptions"
                placeholder="Select company size"
                :disabled="!isEditing"
              />

              <AppInput
                v-model="form.location"
                label="Headquarters / Location"
                placeholder="e.g. Bengaluru, Karnataka, India"
                :disabled="!isEditing"
              />
            </div>

            <div class="form-row">
              <AppInput
                v-model="form.email"
                label="Contact Email"
                type="email"
                placeholder="contact@company.com"
                :disabled="!isEditing"
              />

              <AppInput
                v-model="form.phone"
                label="Contact Phone"
                placeholder="+91 80 1234 5678"
                :disabled="!isEditing"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Company Overview / Description</label>
              <textarea
                v-model="form.description"
                rows="4"
                class="form-textarea"
                placeholder="Provide a detailed summary of your company culture, mission, and focus area..."
                :disabled="!isEditing"
              ></textarea>
            </div>

            <div v-if="isEditing" class="form-actions">
              <AppButton type="button" variant="secondary" @click="cancelEdit">
                Cancel
              </AppButton>
              <AppButton type="submit" variant="primary" :loading="recruiterStore.loading">
                Save Company Profile
              </AppButton>
            </div>
          </form>
        </AppCard>

        <!-- Status & Verification Side Card -->
        <AppCard class="status-side-card">
          <h3 class="side-card-title">Verification Status</h3>
          <div class="status-box">
            <AppBadge :status="form.verification_status" />
            <p class="status-explanation">
              <template v-if="form.verification_status === 'VERIFIED'">
                ✅ Your organization is officially verified on CareerPilot AI. You have full access to publish opportunities.
              </template>
              <template v-else-if="form.verification_status === 'PENDING'">
                ⏳ Your company verification is currently pending admin review. You can create draft jobs while waiting for approval.
              </template>
              <template v-else-if="form.verification_status === 'REJECTED'">
                ⚠️ Your verification was rejected.
                <span v-if="form.verification_notes" class="block font-semibold mt-1">Reason: {{ form.verification_notes }}</span>
              </template>
            </p>
          </div>

          <div class="help-box mt-4">
            <h4>Need Verification Assistance?</h4>
            <p>Verification normally completes within 24 business hours. Ensure official website and domain work email match.</p>
          </div>
        </AppCard>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import { useRecruiterStore } from '@/stores/recruiter'
import { useToast } from '@/components/common/AppToast.vue'

const recruiterStore = useRecruiterStore()
const toast = useToast()
const isEditing = ref(false)

const company = computed(() => recruiterStore.company)

const sizeOptions = [
  { label: '1-10 employees', value: '1-10 employees' },
  { label: '11-50 employees', value: '11-50 employees' },
  { label: '51-200 employees', value: '51-200 employees' },
  { label: '201-500 employees', value: '201-500 employees' },
  { label: '500+ employees', value: '500+ employees' }
]

const form = reactive({
  name: '',
  legal_name: '',
  email: '',
  phone: '',
  website: '',
  industry: '',
  company_size: '',
  description: '',
  location: '',
  verification_status: 'PENDING',
  verification_notes: ''
})

const populateForm = (data) => {
  if (!data) return
  form.name = data.name || ''
  form.legal_name = data.legal_name || ''
  form.email = data.email || ''
  form.phone = data.phone || ''
  form.website = data.website || ''
  form.industry = data.industry || ''
  form.company_size = data.company_size || ''
  form.description = data.description || ''
  form.location = data.location || ''
  form.verification_status = data.verification_status || 'PENDING'
  form.verification_notes = data.verification_notes || ''
}

const handleSave = async () => {
  try {
    await recruiterStore.updateCompanyProfile(form)
    toast.show('✓ Company profile updated successfully')
    isEditing.value = false
  } catch (err) {
    toast.show('Failed to update company profile.', 'error')
  }
}

const cancelEdit = () => {
  populateForm(company.value)
  isEditing.value = false
}

onMounted(async () => {
  const res = await recruiterStore.fetchCompanyProfile()
  if (res.data) {
    populateForm(res.data)
  }
})
</script>

<style scoped>
.company-page {
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

.profile-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}

.card-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}

.side-card-title {
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.status-box {
  background-color: var(--background);
  border: 1px solid var(--border);
  padding: 1rem;
  border-radius: var(--radius-sm);
}

.status-explanation {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  margin-top: 0.75rem;
  line-height: 1.4;
}

.help-box {
  background-color: var(--primary-light);
  border: 1px solid var(--primary-border);
  padding: 1rem;
  border-radius: var(--radius-sm);

}
.help-box h4 {
  font-size: 0.875rem;
  color: var(--primary);
  margin-bottom: 0.25rem;
}
.help-box p {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.mt-4 { margin-top: 1rem; }

@media (max-width: 900px) {
  .profile-grid { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
