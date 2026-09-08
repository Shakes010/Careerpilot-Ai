<template>
  <DashboardLayout>
    <div class="projects-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Project Collaboration Hub 🤝</h1>
          <p class="page-subtitle">Discover open projects, build verified portfolio experience, or assemble a team.</p>
        </div>
        <router-link to="/projects/create" class="btn btn-primary">
          + Start New Project
        </router-link>
      </div>

      <!-- Search & Filters -->
      <AppCard class="filter-card">
        <div class="filter-row">
          <AppInput
            v-model="search"
            placeholder="Search projects by title, skills or description..."
            @keyup.enter="handleSearch"
          />
          <AppSelect
            v-model="category"
            :options="categoryOptions"
            placeholder="All Categories"
            @change="handleSearch"
          />
        </div>
      </AppCard>

      <!-- Projects Grid -->
      <AppLoader v-if="projectsStore.loading && projectsStore.projects.length === 0" message="Loading projects..." />

      <AppEmptyState
        v-else-if="projectsStore.projects.length === 0"
        title="No Collaboration Projects Found"
        message="Be the first to start a project and invite team members!"
      >
        <template #action>
          <router-link to="/projects/create" class="btn btn-primary">
            + Start a Project
          </router-link>
        </template>
      </AppEmptyState>

      <div v-else class="projects-grid">
        <AppCard
          v-for="project in projectsStore.projects"
          :key="project.id"
          class="project-card"
          hoverable
        >
          <div class="project-card-header">
            <div>
              <h3 class="project-title">{{ project.title }}</h3>
              <span class="project-category">{{ project.category }}</span>
            </div>
            <AppBadge :status="project.status" />
          </div>

          <p class="project-desc">{{ truncateText(project.description, 140) }}</p>

          <div v-if="project.required_skills" class="skills-tags">
            <span v-for="skill in parseSkills(project.required_skills)" :key="skill" class="skill-tag">
              {{ skill }}
            </span>
          </div>

          <div class="project-footer">
            <div class="meta-info">
              <span>👤 Lead: {{ project.owner_name || 'Anonymous' }}</span>
              <span>👥 Max Members: {{ project.max_members }}</span>
            </div>
            <router-link :to="`/projects/${project.id}`" class="btn btn-secondary btn-sm">
              View Project →
            </router-link>
          </div>
        </AppCard>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppEmptyState from '@/components/common/AppEmptyState.vue'
import { useProjectsStore } from '@/stores/projects'

const projectsStore = useProjectsStore()

const search = ref('')
const category = ref('')

const categoryOptions = [
  { label: 'All Categories', value: '' },
  { label: 'Software Engineering', value: 'Software Engineering' },
  { label: 'AI & Data Science', value: 'AI & Data Science' },
  { label: 'Web & Mobile Dev', value: 'Web & Mobile Dev' },
  { label: 'UI/UX Design', value: 'UI/UX Design' }
]

const parseSkills = (str) => str ? str.split(',').map(s => s.trim()).filter(Boolean) : []
const truncateText = (str, len) => str && str.length > len ? str.substring(0, len) + '...' : str

const handleSearch = () => {
  projectsStore.fetchProjects({
    search: search.value || undefined,
    category: category.value || undefined
  })
}

onMounted(() => {
  projectsStore.fetchProjects()
})
</script>

<style scoped>
.projects-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.filter-row { display: grid; grid-template-columns: 3fr 1fr; gap: 1rem; }

.projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.25rem; }
.project-card { display: flex; flex-direction: column; gap: 0.75rem; }
.project-card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.project-title { font-size: 1.125rem; font-weight: 700; color: var(--text-heading); }
.project-category { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }

.project-desc { font-size: 0.875rem; color: var(--text-primary); line-height: 1.4; }

.skills-tags { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.skill-tag { font-size: 0.75rem; background-color: var(--primary-light); color: var(--primary); padding: 0.125rem 0.5rem; border-radius: var(--radius-sm); font-weight: 600; }

.project-footer { margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; font-size: 0.8125rem; color: var(--text-secondary); }
.meta-info { display: flex; flex-direction: column; gap: 0.125rem; }
</style>
