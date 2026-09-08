<template>
  <StudentLayout>
    <div class="projects-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Projects</h1>
          <p class="page-subtitle">Collaborate, build and showcase real-world projects.</p>
        </div>
        <router-link to="/student/projects/create" class="btn btn-primary">
          + Create Project
        </router-link>
      </div>

      <!-- Search & Filters -->
      <AppCard class="filter-card">
        <div class="filter-grid">
          <AppInput
            v-model="search"
            placeholder="Search projects..."
            @keyup.enter="handleSearch"
          />
          <AppSelect
            v-model="category"
            :options="categoryOptions"
            placeholder="Category"
            @change="handleSearch"
          />
          <AppSelect
            v-model="statusFilter"
            :options="statusOptions"
            placeholder="Status"
            @change="handleSearch"
          />
          <AppSelect
            v-model="visibilityFilter"
            :options="visibilityOptions"
            placeholder="Visibility"
            @change="handleSearch"
          />
        </div>
      </AppCard>

      <!-- Loading State -->
      <AppLoader v-if="projectsStore.loading && projectsStore.projects.length === 0" message="Loading projects..." />

      <!-- Empty State -->
      <AppEmptyState
        v-else-if="projectsStore.projects.length === 0"
        title="No projects available."
        message="Be the first student to create a project and assemble a team!"
      >
        <template #action>
          <router-link to="/student/projects/create" class="btn btn-primary">
            + Create Project
          </router-link>
        </template>
      </AppEmptyState>

      <!-- Projects Grid -->
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
              <span class="project-creator">Creator: {{ project.owner_name || 'Student' }}</span>
            </div>
            <AppBadge :status="project.status" />
          </div>

          <p class="project-desc">{{ truncateText(project.description, 140) }}</p>

          <div v-if="project.technology_stack" class="tech-stack-wrap">
            <span v-for="tech in parseStack(project.technology_stack)" :key="tech" class="tech-tag">
              {{ tech }}
            </span>
          </div>

          <div class="project-footer">
            <div class="team-count">
              <strong>Team:</strong> {{ project.members ? project.members.length : 1 }} / {{ project.maximum_members }}
            </div>
            <router-link :to="`/student/projects/${project.id}`" class="btn btn-secondary btn-sm">
              View Project
            </router-link>
          </div>
        </AppCard>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StudentLayout from '@/components/layout/StudentLayout.vue'
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
const statusFilter = ref('')
const visibilityFilter = ref('PUBLIC')

const categoryOptions = [
  { label: 'All Categories', value: '' },
  { label: 'Software Engineering', value: 'Software Engineering' },
  { label: 'AI & Data Science', value: 'AI & Data Science' },
  { label: 'Web & Mobile Dev', value: 'Web & Mobile Dev' },
  { label: 'UI/UX Design', value: 'UI/UX Design' }
]

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'Open', value: 'OPEN' },
  { label: 'In Progress', value: 'IN_PROGRESS' },
  { label: 'Completed', value: 'COMPLETED' }
]

const visibilityOptions = [
  { label: 'Public Projects', value: 'PUBLIC' },
  { label: 'Private Projects', value: 'PRIVATE' }
]

const parseStack = (str) => str ? str.split(',').map(s => s.trim()).filter(Boolean) : []
const truncateText = (str, len) => str && str.length > len ? str.substring(0, len) + '...' : str

const handleSearch = () => {
  projectsStore.fetchProjects({
    search: search.value || undefined,
    category: category.value || undefined,
    status: statusFilter.value || undefined,
    visibility: visibilityFilter.value || undefined
  })
}

onMounted(() => {
  projectsStore.fetchProjects({ visibility: 'PUBLIC' })
})
</script>

<style scoped>
.projects-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 1.625rem; font-weight: 700; color: var(--text-heading); }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.filter-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 1rem; }

.projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem; }
.project-card { display: flex; flex-direction: column; gap: 0.75rem; }
.project-card-header { display: flex; justify-content: space-between; align-items: flex-start; }
.project-title { font-size: 1.125rem; font-weight: 700; color: var(--text-heading); }
.project-creator { font-size: 0.75rem; color: var(--text-muted); font-weight: 500; display: block; margin-top: 0.125rem; }

.project-desc { font-size: 0.875rem; color: var(--text-primary); line-height: 1.45; }

.tech-stack-wrap { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.tech-tag { font-size: 0.75rem; background-color: var(--primary-light); color: var(--primary); padding: 0.125rem 0.5rem; border-radius: var(--radius-sm); font-weight: 600; }

.project-footer { margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.team-count { font-size: 0.8125rem; color: var(--text-secondary); }

@media (max-width: 768px) { .filter-grid { grid-template-columns: 1fr; } }
</style>
