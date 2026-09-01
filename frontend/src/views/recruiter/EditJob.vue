<template>
  <DashboardLayout>
    <div class="edit-job-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Edit Job Posting</h1>
          <p class="page-subtitle">Update job details, requirements, or application deadline.</p>
        </div>
        <router-link :to="`/recruiter/jobs/${jobId}`" class="btn btn-secondary btn-sm">
          ← Cancel
        </router-link>
      </div>

      <AppLoader v-if="jobsStore.loading && !form.title" message="Loading job details..." />

      <AppCard v-else>
        <form @submit.prevent="handleUpdate">
          <div class="form-section">
            <h3 class="section-heading">Basic Information</h3>
            <div class="form-row">
              <AppInput
                v-model="form.title"
                label="Job Title"
                required
              />

              <AppInput
                v-model="form.job_category"
                label="Category"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Description *</label>
              <textarea
                v-model="form.description"
                rows="6"
                class="form-textarea"
                required
              ></textarea>
            </div>
          </div>

          <div class="form-section">
            <h3 class="section-heading">Employment & Compensation</h3>
            <div class="form-row trio">
              <AppSelect
                v-model="form.employment_type"
                label="Employment Type"
                :options="typeOptions"
              />

              <AppSelect
                v-model="form.work_mode"
                label="Work Mode"
                :options="workModeOptions"
              />

              <AppInput
                v-model="form.location"
                label="Location"
                required
              />
            </div>

            <div class="form-row trio">
              <AppInput
                v-model.number="form.experience_min"
                label="Min Exp (Yrs)"
                type="number"
                min="0"
              />

              <AppInput
                v-model.number="form.experience_max"
                label="Max Exp (Yrs)"
                type="number"
                min="0"
              />

              <AppInput
                v-model="form.application_deadline"
                label="Deadline"
                type="date"
                required
              />
            </div>

            <div class="form-row trio">
              <AppInput
                v-model.number="form.salary_min"
                label="Min Salary"
                type="number"
              />

              <AppInput
                v-model.number="form.salary_max"
                label="Max Salary"
                type="number"
              />

              <AppSelect
                v-model="form.salary_currency"
                label="Currency"
                :options="['INR', 'USD', 'EUR', 'GBP']"
              />
            </div>
          </div>

          <div class="form-section border-none">
            <h3 class="section-heading">Requirements & Skills</h3>
            <AppInput
              v-model="form.education_requirements"
              label="Education"
            />

            <AppInput
              v-model="skillsInput"
              label="Required Skills (Comma separated)"
            />
          </div>

          <div class="form-footer">
            <router-link :to="`/recruiter/jobs/${jobId}`" class="btn btn-secondary">
              Cancel
            </router-link>
            <AppButton type="submit" variant="primary" :loading="jobsStore.loading">
              Save Changes
            </AppButton>
          </div>
        </form>
      </AppCard>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import { useJobsStore } from '@/stores/jobs'
import { useToast } from '@/components/common/AppToast.vue'

const route = useRoute()
const router = useRouter()
const jobsStore = useJobsStore()
const toast = useToast()

const jobId = route.params.id
const skillsInput = ref('')

const form = reactive({
  title: '',
  description: '',
  employment_type: 'FULL_TIME',
  location: '',
  work_mode: 'ONSITE',
  experience_min: 0,
  experience_max: 0,
  salary_min: null,
  salary_max: null,
  salary_currency: 'INR',
  education_requirements: '',
  job_category: '',
  number_of_openings: 1,
  application_deadline: ''
})

const typeOptions = [
  { label: 'Full-Time', value: 'FULL_TIME' },
  { label: 'Part-Time', value: 'PART_TIME' },
  { label: 'Internship', value: 'INTERNSHIP' },
  { label: 'Contract', value: 'CONTRACT' }
]

const workModeOptions = [
  { label: 'Onsite', value: 'ONSITE' },
  { label: 'Remote', value: 'REMOTE' },
  { label: 'Hybrid', value: 'HYBRID' }
]

const populateForm = (data) => {
  if (!data) return
  form.title = data.title || ''
  form.description = data.description || ''
  form.employment_type = data.employment_type || 'FULL_TIME'
  form.location = data.location || ''
  form.work_mode = data.work_mode || 'ONSITE'
  form.experience_min = data.experience_min ?? 0
  form.experience_max = data.experience_max ?? 0
  form.salary_min = data.salary_min
  form.salary_max = data.salary_max
  form.salary_currency = data.salary_currency || 'INR'
  form.education_requirements = data.education_requirements || ''
  form.job_category = data.job_category || ''
  form.number_of_openings = data.number_of_openings || 1
  form.application_deadline = data.application_deadline || ''

  if (data.skills && Array.isArray(data.skills)) {
    skillsInput.value = data.skills.map(s => s.skill_name || s).join(', ')
  }
}

const handleUpdate = async () => {
  const parsedSkills = skillsInput.value.split(',').map(s => s.trim()).filter(Boolean)
  const payload = {
    ...form,
    skills: parsedSkills
  }

  try {
    await jobsStore.updateJob(jobId, payload)
    toast.show('✓ Job updated successfully')
    router.push(`/recruiter/jobs/${jobId}`)
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to update job.', 'error')
  }
}

onMounted(async () => {
  const res = await jobsStore.fetchJobDetails(jobId)
  if (res.data) {
    populateForm(res.data)
  }
})
</script>

<style scoped>
.edit-job-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.form-section { padding-bottom: 1.5rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
.border-none { border-bottom: none; }
.section-heading { font-size: 1.0625rem; font-weight: 600; margin-bottom: 1.25rem; color: var(--primary); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-row.trio { grid-template-columns: 1fr 1fr 1fr; }
.form-footer { display: flex; justify-content: flex-end; gap: 1rem; padding-top: 1.25rem; border-top: 1px solid var(--border); }
@media (max-width: 768px) { .form-row, .form-row.trio { grid-template-columns: 1fr; } }
</style>
