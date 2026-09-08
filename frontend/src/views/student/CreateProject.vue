<template>
  <StudentLayout>
    <div class="create-project-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Create Project</h1>
          <p class="page-subtitle">Start a new project and invite students to collaborate.</p>
        </div>
        <router-link to="/student/projects" class="btn btn-secondary btn-sm">
          ← Cancel
        </router-link>
      </div>

      <AppCard>
        <form @submit.prevent="handleSubmit">
          <div class="form-grid">
            <AppInput
              v-model="form.title"
              label="Project Title *"
              placeholder="e.g. AI Resume Analyzer"
              required
              :error="errors.title"
            />

            <AppSelect
              v-model="form.category"
              label="Project Category *"
              :options="categoryChoices"
              required
              :error="errors.category"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Description *</label>
            <textarea
              v-model="form.description"
              rows="5"
              class="form-textarea"
              placeholder="Describe your project goals, technology stack, architecture, and team member expectations..."
              required
            ></textarea>
            <span v-if="errors.description" class="form-error">{{ errors.description }}</span>
          </div>

          <div class="form-grid">
            <AppInput
              v-model="form.technology_stack"
              label="Technology Stack *"
              placeholder="e.g. Python, FastAPI, Vue, PostgreSQL"
              hint="Specify technologies (at least one)."
              required
              :error="errors.technology_stack"
            />

            <AppInput
              v-model.number="form.maximum_members"
              label="Maximum Team Members *"
              type="number"
              min="1"
              max="20"
              required
              :error="errors.maximum_members"
            />
          </div>

          <AppSelect
            v-model="form.visibility"
            label="Visibility *"
            :options="[
              { label: 'Public (Any student can request to join)', value: 'PUBLIC' },
              { label: 'Private (Invite only)', value: 'PRIVATE' }
            ]"
            required
          />

          <div class="form-footer">
            <router-link to="/student/projects" class="btn btn-secondary">
              Cancel
            </router-link>
            <AppButton type="submit" variant="primary" :loading="projectsStore.loading">
              Create Project
            </AppButton>
          </div>
        </form>
      </AppCard>
    </div>
  </StudentLayout>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import StudentLayout from '@/components/layout/StudentLayout.vue'
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
  technology_stack: 'Python, FastAPI, Vue, PostgreSQL',
  maximum_members: 4,
  visibility: 'PUBLIC'
})

const errors = reactive({})

const handleSubmit = async () => {
  Object.keys(errors).forEach(k => delete errors[k])

  if (!form.title.trim()) { errors.title = 'Project Title is required.' }
  if (!form.description.trim()) { errors.description = 'Description is required.' }
  if (!form.category.trim()) { errors.category = 'Category is required.' }
  if (!form.technology_stack.trim()) { errors.technology_stack = 'At least one technology is required.' }
  if (!form.maximum_members || form.maximum_members <= 0) { errors.maximum_members = 'Maximum Members must be greater than 0.' }

  if (Object.keys(errors).length > 0) return

  try {
    const res = await projectsStore.createProject(form)
    toast.show('✓ Project created successfully')
    router.push(`/student/projects/${res.data.id}`)
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
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-footer { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border); }
@media (max-width: 640px) { .form-grid { grid-template-columns: 1fr; } }
</style>
