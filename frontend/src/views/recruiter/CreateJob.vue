<template>
  <DashboardLayout>
    <div class="create-job-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Post a New Job Requisition</h1>
          <p class="page-subtitle">Fill in opportunity details to find top verified candidates.</p>
        </div>
        <router-link to="/recruiter/jobs" class="btn btn-secondary btn-sm">
          ← Back to Jobs
        </router-link>
      </div>

      <AppCard>
        <form @submit.prevent="handleSubmit">
          <!-- Section 1: Basic Information -->
          <div class="form-section">
            <h3 class="section-heading">1. Basic Information</h3>
            <div class="form-row">
              <AppInput
                v-model="form.title"
                label="Job Title"
                placeholder="e.g. Senior Frontend Developer"
                required
                :error="errors.title"
              />

              <AppInput
                v-model="form.job_category"
                label="Job Category / Function"
                placeholder="e.g. Software Engineering"
              />
            </div>

            <div class="form-group">
              <label class="form-label">Job Description *</label>
              <textarea
                v-model="form.description"
                rows="6"
                class="form-textarea"
                :class="{ 'has-error': errors.description }"
                placeholder="Describe roles, responsibilities, daily workflows, team expectations, and project focus..."
                required
              ></textarea>
              <span v-if="errors.description" class="form-error">{{ errors.description }}</span>
            </div>
          </div>

          <!-- Section 2: Job Type & Location -->
          <div class="form-section">
            <h3 class="section-heading">2. Employment & Location</h3>
            <div class="form-row trio">
              <AppSelect
                v-model="form.employment_type"
                label="Employment Type"
                :options="typeOptions"
                required
              />

              <AppSelect
                v-model="form.work_mode"
                label="Work Mode"
                :options="workModeOptions"
                required
              />

              <AppInput
                v-model="form.location"
                label="Job Location"
                placeholder="e.g. Bengaluru, India or Remote"
                required
                :error="errors.location"
              />
            </div>
          </div>

          <!-- Section 3: Experience & Compensation -->
          <div class="form-section">
            <h3 class="section-heading">3. Experience & Compensation</h3>
            <div class="form-row">
              <AppInput
                v-model.number="form.experience_min"
                label="Minimum Experience (Years)"
                type="number"
                min="0"
                required
              />

              <AppInput
                v-model.number="form.experience_max"
                label="Maximum Experience (Years)"
                type="number"
                min="0"
                required
                :error="errors.experience"
              />
            </div>

            <div class="form-row trio">
              <AppInput
                v-model.number="form.salary_min"
                label="Minimum Salary (Annual / Monthly)"
                type="number"
                min="0"
                placeholder="e.g. 600000"
              />

              <AppInput
                v-model.number="form.salary_max"
                label="Maximum Salary"
                type="number"
                min="0"
                placeholder="e.g. 1000000"
                :error="errors.salary"
              />

              <AppSelect
                v-model="form.salary_currency"
                label="Currency"
                :options="['INR', 'USD', 'EUR', 'GBP']"
              />
            </div>
          </div>

          <!-- Section 4: Requirements & Skills -->
          <div class="form-section">
            <h3 class="section-heading">4. Requirements & Skills</h3>
            <AppInput
              v-model="form.education_requirements"
              label="Education Requirements"
              placeholder="e.g. B.Tech / MCA / BE in Computer Science"
            />

            <AppInput
              v-model="skillsInput"
              label="Required Skills (Comma separated) *"
              placeholder="e.g. Python, FastAPI, Vue.js, PostgreSQL, Git"
              required
              :error="errors.skills"
              hint="Type key skills separated by commas."
            />
          </div>

          <!-- Section 5: Openings & Deadline -->
          <div class="form-section border-none">
            <h3 class="section-heading">5. Openings & Application Deadline</h3>
            <div class="form-row">
              <AppInput
                v-model.number="form.number_of_openings"
                label="Number of Openings"
                type="number"
                min="1"
                required
              />

              <AppInput
                v-model="form.application_deadline"
                label="Application Deadline"
                type="date"
                required
                :error="errors.deadline"
              />
            </div>
          </div>

          <!-- Form Buttons -->
          <div class="form-footer">
            <AppButton type="button" variant="secondary" @click="saveDraft" :loading="saving">
              Save Draft
            </AppButton>
            <AppButton type="button" variant="primary" @click="openPreview">
              Preview Job Posting →
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- Preview Modal -->
      <AppModal
        :show="showPreview"
        title="Job Posting Preview"
        width="720px"
        @close="showPreview = false"
      >
        <div class="preview-content">
          <div class="preview-header">
            <div>
              <h2 class="preview-title">{{ form.title }}</h2>
              <p class="preview-company">{{ authStore.companyName }} • {{ form.location }} ({{ form.work_mode }})</p>
            </div>
            <AppBadge status="DRAFT" />
          </div>

          <div class="preview-meta-bar">
            <span>💼 {{ form.employment_type }}</span>
            <span>⏱️ {{ form.experience_min }}-{{ form.experience_max }} Years Exp</span>
            <span>💰 ₹{{ form.salary_min }} - ₹{{ form.salary_max }} {{ form.salary_currency }}</span>
            <span>📅 Deadline: {{ form.application_deadline }}</span>
          </div>

          <div class="preview-section">
            <h4>Description</h4>
            <p class="whitespace-pre">{{ form.description }}</p>
          </div>

          <div class="preview-section">
            <h4>Required Skills</h4>
            <div class="skills-tags">
              <span v-for="s in parsedSkills" :key="s" class="skill-chip">{{ s }}</span>
            </div>
          </div>
        </div>

        <template #footer>
          <AppButton variant="secondary" @click="showPreview = false">Back to Edit</AppButton>
          <AppButton variant="primary" :loading="publishing" @click="publishJob">
            Publish Job Posting
          </AppButton>
        </template>
      </AppModal>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppModal from '@/components/common/AppModal.vue'
import { useJobsStore } from '@/stores/jobs'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/components/common/AppToast.vue'

const router = useRouter()
const jobsStore = useJobsStore()
const authStore = useAuthStore()
const toast = useToast()

const skillsInput = ref('Python, FastAPI, PostgreSQL')
const saving = ref(false)
const publishing = ref(false)
const showPreview = ref(false)

// Default 30 days from today
const defaultDeadline = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]

const form = reactive({
  title: '',
  description: '',
  employment_type: 'FULL_TIME',
  location: '',
  work_mode: 'ONSITE',
  experience_min: 0,
  experience_max: 2,
  salary_min: 500000,
  salary_max: 900000,
  salary_currency: 'INR',
  education_requirements: 'B.Tech / MCA',
  job_category: 'Software Engineering',
  number_of_openings: 1,
  application_deadline: defaultDeadline
})

const errors = reactive({})

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

const parsedSkills = computed(() => {
  return skillsInput.value.split(',').map(s => s.trim()).filter(Boolean)
})

const validate = () => {
  Object.keys(errors).forEach(k => delete errors[k])
  let valid = true

  if (!form.title.trim()) { errors.title = 'Job title is required.'; valid = false }
  if (!form.description.trim() || form.description.length < 10) { errors.description = 'Description must be at least 10 characters.'; valid = false }
  if (!form.location.trim()) { errors.location = 'Location is required.'; valid = false }
  if (form.experience_max < form.experience_min) { errors.experience = 'Max experience must be ≥ Min experience.'; valid = false }
  if (form.salary_min && form.salary_max && form.salary_max < form.salary_min) { errors.salary = 'Max salary must be ≥ Min salary.'; valid = false }
  if (parsedSkills.value.length === 0) { errors.skills = 'At least one skill is required.'; valid = false }
  if (!form.application_deadline) { errors.deadline = 'Deadline is required.'; valid = false }

  return valid
}

const preparePayload = () => ({
  ...form,
  skills: parsedSkills.value
})

const saveDraft = async () => {
  if (!form.title.trim()) {
    toast.show('Job title is required to save draft.', 'error')
    return
  }

  saving.value = true
  try {
    const res = await jobsStore.createJob(preparePayload(), false)
    toast.show('✓ Job saved as draft')
    router.push('/recruiter/jobs')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to save draft.', 'error')
  } finally {
    saving.value = false
  }
}

const openPreview = () => {
  if (!validate()) {
    toast.show('Please fix form validation errors before proceeding.', 'error')
    return
  }
  showPreview.value = true
}

const publishJob = async () => {
  publishing.value = true
  try {
    const res = await jobsStore.createJob(preparePayload(), true)
    toast.show('✓ Job published successfully')
    showPreview.value = false
    router.push('/recruiter/jobs')
  } catch (err) {
    const errorDetail = err.response?.data?.detail || 'Failed to publish job.'
    toast.show(errorDetail, 'error')
  } finally {
    publishing.value = false
  }
}
</script>

<style scoped>
.create-job-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.form-section {
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.border-none { border-bottom: none; }

.section-heading {
  font-size: 1.0625rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  color: var(--primary);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-row.trio {
  grid-template-columns: 1fr 1fr 1fr;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
}

.preview-content { display: flex; flex-direction: column; gap: 1rem; }
.preview-header { display: flex; justify-content: space-between; align-items: flex-start; }
.preview-title { font-size: 1.25rem; font-weight: 700; }
.preview-company { font-size: 0.875rem; color: var(--text-secondary); }

.preview-meta-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  background-color: var(--background);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.8125rem;
  font-weight: 500;
}

.preview-section h4 { font-size: 0.9375rem; margin-bottom: 0.375rem; }
.whitespace-pre { white-space: pre-wrap; font-size: 0.875rem; color: var(--text-primary); }

.skills-tags { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.skill-chip { background-color: var(--primary-light); color: var(--primary); padding: 0.25rem 0.625rem; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600; }

@media (max-width: 768px) {
  .form-row, .form-row.trio { grid-template-columns: 1fr; }
}
</style>
