<template>
  <DashboardLayout>
    <div class="create-project-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Start a New Collaboration Project</h1>
          <p class="page-subtitle">Assemble a student team, define roles, and build portfolio experience.</p>
        </div>
        <router-link to="/projects" class="btn btn-secondary btn-sm">
          ← Cancel
        </router-link>
      </div>

      <AppCard>
        <form @submit.prevent="handleSubmit">
          <div class="form-row">
            <AppInput
              v-model="form.title"
              label="Project Title *"
              placeholder="e.g. Open AI Resume Reviewer"
              required
              :error="errors.title"
            />

            <AppSelect
              v-model="form.category"
              label="Category *"
              :options="categoryChoices"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Project Overview & Objectives *</label>
            <textarea
              v-model="form.description"
              rows="5"
              class="form-textarea"
              placeholder="Describe what your team is building, technology stack, target outcome, and team expectations..."
              required
            ></textarea>
            <span v-if="errors.description" class="form-error">{{ errors.description }}</span>
          </div>

          <div class="form-row">
            <AppInput
              v-model="form.required_skills"
              label="Required Skills (Comma separated)"
              placeholder="e.g. Python, FastAPI, Vue.js, PostgreSQL"
              hint="List core technologies needed for your team."
            />

            <AppInput
              v-model.number="form.max_members"
              label="Maximum Team Size"
              type="number"
              min="1"
              max="20"
              required
            />
          </div>

          <AppInput
            v-model="form.github_url"
            label="GitHub Repository URL (Optional)"
            placeholder="https://github.com/username/project-repo"
          />

          <div class="form-footer">
            <router-link to="/projects" class="btn btn-secondary">
              Cancel
            </router-link>
            <AppButton type="submit" variant="primary" :loading="projectsStore.loading">
              🚀 Launch Project & Start Recruiting Team
            </AppButton>
          </div>
        </form>
      </AppCard>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppButton from '@/components/common/AppButton.vue'
import { useProjectsStore } from '@/stores/projects'
import { useToast } from '@/components/common/AppToast.vue'

const router = useRouter()
const projectsStore = useProjectsStore()
const toast = useToast()

const categoryChoices = [
  'Software Engineering',
  'AI & Data Science',
  'Web & Mobile Dev',
  'UI/UX Design'
]

const form = reactive({
  title: '',
  description: '',
  category: 'Software Engineering',
  required_skills: 'Python, FastAPI, Vue.js',
  max_members: 4,
  github_url: ''
})

const errors = reactive({})

const handleSubmit = async () => {
  Object.keys(errors).forEach(k => delete errors[k])

  if (!form.title.trim()) { errors.title = 'Title is required.'; return }
  if (!form.description.trim() || form.description.length < 10) { errors.description = 'Description must be at least 10 characters.'; return }

  try {
    const res = await projectsStore.createProject(form)
    toast.show('✓ Collaboration project created!')
    router.push(`/projects/${res.data.id}`)
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to create project.', 'error')
  }
}
</script>

<style scoped>
.create-project-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-footer { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border); }
@media (max-width: 640px) { .form-row { grid-template-columns: 1fr; } }
</style>
