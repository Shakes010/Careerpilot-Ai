<template>
  <DashboardLayout>
    <div class="project-details-page">
      <div class="page-header">
        <router-link to="/projects" class="back-link">
          ← Back to Projects
        </router-link>
        <div class="header-actions" v-if="project">
          <AppButton variant="primary" @click="joinModal.show = true">
            🤝 Request to Join Team
          </AppButton>
        </div>
      </div>

      <AppLoader v-if="projectsStore.loading && !project" message="Loading project details..." />

      <div v-else-if="project" class="details-grid">
        <!-- Main Info -->
        <div class="main-column">
          <AppCard class="project-main-card">
            <div class="title-row">
              <div>
                <h1 class="project-title">{{ project.title }}</h1>
                <p class="project-meta">Category: {{ project.category }} • Lead: {{ project.owner_name }}</p>
              </div>
              <AppBadge :status="project.status" size="lg" />
            </div>

            <div class="divider"></div>

            <div class="section-block">
              <h3>About the Project</h3>
              <p class="description-text">{{ project.description }}</p>
            </div>

            <div class="section-block" v-if="project.required_skills">
              <h3>Required Skills</h3>
              <div class="skills-wrap">
                <span v-for="skill in parseSkills(project.required_skills)" :key="skill" class="skill-tag">
                  {{ skill }}
                </span>
              </div>
            </div>
          </AppCard>

          <!-- Team Formation Section -->
          <AppCard title="👥 Team Formation & Members">
            <div class="members-list">
              <div v-for="member in project.members" :key="member.id" class="member-item">
                <div class="member-info">
                  <span class="member-name">{{ member.user_name || 'Team Member' }}</span>
                  <span class="member-role-badge">{{ member.role }}</span>
                  <p class="pitch-text" v-if="member.pitch_message">"{{ member.pitch_message }}"</p>
                </div>
                <div class="member-status-box">
                  <AppBadge :status="member.status" />

                  <!-- Lead actions for pending requests -->
                  <div v-if="isOwner && member.status === 'PENDING'" class="lead-actions">
                    <button class="btn btn-primary btn-sm" @click="updateMember(member.id, 'ACCEPTED')">Accept</button>
                    <button class="btn btn-danger btn-sm" @click="updateMember(member.id, 'REJECTED')">Reject</button>
                  </div>
                </div>
              </div>
            </div>
          </AppCard>

          <!-- Task Assignment Section -->
          <AppCard title="📋 Task Assignment Board">
            <template #header>
              <div class="task-card-header">
                <h3>📋 Task Assignment Board</h3>
                <AppButton variant="secondary" size="sm" @click="taskModal.show = true">
                  + Add Task
                </AppButton>
              </div>
            </template>

            <AppEmptyState
              v-if="project.tasks.length === 0"
              title="No Tasks Created Yet"
              message="Click '+ Add Task' to assign tasks to team members."
            />

            <div v-else class="tasks-list">
              <div v-for="task in project.tasks" :key="task.id" class="task-item">
                <div class="task-main">
                  <h4 class="task-title">{{ task.title }}</h4>
                  <p class="task-desc" v-if="task.description">{{ task.description }}</p>
                  <div class="task-meta">
                    <span>👤 Assignee: {{ task.assignee_name || 'Unassigned' }}</span>
                    <span>Priority: <strong :class="`priority-${task.priority.toLowerCase()}`">{{ task.priority }}</strong></span>
                  </div>
                </div>
                <div class="task-status-column">
                  <AppSelect
                    :model-value="task.status"
                    :options="taskStatusOptions"
                    size="sm"
                    @update:model-value="val => updateTaskStatus(task.id, val)"
                  />
                </div>
              </div>
            </div>
          </AppCard>

          <!-- Phase 2 Placeholders (Disabled) -->
          <AppCard class="phase2-card">
            <div class="phase2-header">
              <h3>Progress Tracking & Completion Verification</h3>
              <span class="phase2-tag">Phase 2 Features</span>
            </div>
            <p class="phase2-desc">
              Visual Kanban milestone tracking, evidence video submission, and verified project completion badge issuance will be enabled in Phase 2.
            </p>
          </AppCard>
        </div>

        <!-- Sidebar Specs -->
        <div class="side-column">
          <AppCard class="specs-card">
            <h3>Project Details</h3>

            <div class="spec-item">
              <span class="spec-label">Project Status</span>
              <AppBadge :status="project.status" />
            </div>

            <div class="spec-item">
              <span class="spec-label">Max Members</span>
              <span class="spec-val">{{ project.members.length }} / {{ project.max_members }} Members</span>
            </div>

            <div class="spec-item" v-if="project.github_url">
              <span class="spec-label">GitHub Repository</span>
              <a :href="project.github_url" target="_blank" class="spec-link">View Repo ↗</a>
            </div>

            <div class="spec-item">
              <span class="spec-label">Created Date</span>
              <span class="spec-val">{{ formatDate(project.created_at) }}</span>
            </div>
          </AppCard>
        </div>
      </div>

      <!-- Join Request Modal -->
      <AppModal
        :show="joinModal.show"
        title="Request to Join Project Team"
        @close="joinModal.show = false"
      >
        <form @submit.prevent="submitJoin">
          <AppSelect
            v-model="joinModal.role"
            label="Preferred Team Role *"
            :options="roleChoices"
            required
          />

          <div class="form-group">
            <label class="form-label">Pitch Message to Project Lead</label>
            <textarea
              v-model="joinModal.pitch_message"
              rows="3"
              class="form-textarea"
              placeholder="Explain your relevant skills and why you want to contribute to this project..."
            ></textarea>
          </div>
        </form>

        <template #footer>
          <AppButton variant="secondary" @click="joinModal.show = false">Cancel</AppButton>
          <AppButton variant="primary" :loading="joinModal.loading" @click="submitJoin">
            Submit Application
          </AppButton>
        </template>
      </AppModal>

      <!-- Add Task Modal -->
      <AppModal
        :show="taskModal.show"
        title="Add Project Task"
        @close="taskModal.show = false"
      >
        <form @submit.prevent="submitTask">
          <AppInput
            v-model="taskModal.form.title"
            label="Task Title *"
            placeholder="e.g. Implement Vue Router auth guards"
            required
          />

          <AppSelect
            v-model="taskModal.form.priority"
            label="Priority"
            :options="['LOW', 'MEDIUM', 'HIGH']"
          />

          <div class="form-group">
            <label class="form-label">Task Description</label>
            <textarea
              v-model="taskModal.form.description"
              rows="3"
              class="form-textarea"
              placeholder="Task details and acceptance criteria..."
            ></textarea>
          </div>
        </form>

        <template #footer>
          <AppButton variant="secondary" @click="taskModal.show = false">Cancel</AppButton>
          <AppButton variant="primary" :loading="taskModal.loading" @click="submitTask">
            Create Task
          </AppButton>
        </template>
      </AppModal>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppEmptyState from '@/components/common/AppEmptyState.vue'
import AppModal from '@/components/common/AppModal.vue'
import { useProjectsStore } from '@/stores/projects'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/components/common/AppToast.vue'

const route = useRoute()
const projectsStore = useProjectsStore()
const authStore = useAuthStore()
const toast = useToast()

const projectId = route.params.id
const project = computed(() => projectsStore.currentProject)

const isOwner = computed(() => {
  return project.value && authStore.user && project.value.owner_id === authStore.user.id
})

const roleChoices = [
  { label: 'Frontend Developer', value: 'FRONTEND' },
  { label: 'Backend Developer', value: 'BACKEND' },
  { label: 'UI/UX Designer', value: 'DESIGNER' },
  { label: 'QA Engineer', value: 'QA' },
  { label: 'General Team Member', value: 'MEMBER' }
]

const taskStatusOptions = [
  { label: 'To Do', value: 'TODO' },
  { label: 'In Progress', value: 'IN_PROGRESS' },
  { label: 'Completed', value: 'COMPLETED' }
]

const joinModal = reactive({
  show: false,
  role: 'FRONTEND',
  pitch_message: '',
  loading: false
})

const taskModal = reactive({
  show: false,
  form: { title: '', description: '', priority: 'MEDIUM' },
  loading: false
})

const parseSkills = (str) => str ? str.split(',').map(s => s.trim()).filter(Boolean) : []
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' }) : ''

const submitJoin = async () => {
  joinModal.loading = true
  try {
    await projectsStore.joinProject(projectId, {
      role: joinModal.role,
      pitch_message: joinModal.pitch_message
    })
    toast.show('✓ Application to join team submitted!')
    joinModal.show = false
    projectsStore.fetchProjectDetails(projectId)
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to submit request.', 'error')
  } finally {
    joinModal.loading = false
  }
}

const updateMember = async (memberId, status) => {
  try {
    await projectsStore.updateMemberStatus(projectId, memberId, status)
    toast.show(`✓ Member request ${status.toLowerCase()}`)
  } catch (err) {
    toast.show('Failed to update member status.', 'error')
  }
}

const submitTask = async () => {
  if (!taskModal.form.title.trim()) return

  taskModal.loading = true
  try {
    await projectsStore.createTask(projectId, taskModal.form)
    toast.show('✓ Task created')
    taskModal.show = false
    taskModal.form.title = ''
    taskModal.form.description = ''
  } catch (err) {
    toast.show('Failed to create task.', 'error')
  } finally {
    taskModal.loading = false
  }
}

const updateTaskStatus = async (taskId, newStatus) => {
  try {
    await projectsStore.updateTask(projectId, taskId, { status: newStatus })
    toast.show('✓ Task status updated')
  } catch (err) {
    toast.show('Failed to update task status.', 'error')
  }
}

onMounted(() => {
  projectsStore.fetchProjectDetails(projectId)
})
</script>

<style scoped>
.project-details-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; }
.back-link { font-size: 0.875rem; font-weight: 600; }
.header-actions { display: flex; gap: 0.75rem; }

.details-grid { display: grid; grid-template-columns: 3fr 1fr; gap: 1.5rem; }
.main-column { display: flex; flex-direction: column; gap: 1.5rem; }

.title-row { display: flex; justify-content: space-between; align-items: flex-start; }
.project-title { font-size: 1.625rem; font-weight: 700; }
.project-meta { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.divider { height: 1px; background-color: var(--border); margin: 1.25rem 0; }

.section-block { margin-bottom: 1.25rem; }
.section-block h3 { font-size: 1rem; margin-bottom: 0.5rem; }
.description-text { font-size: 0.9375rem; line-height: 1.6; white-space: pre-wrap; color: var(--text-primary); }

.skills-wrap { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.skill-tag { background-color: var(--primary-light); color: var(--primary); padding: 0.25rem 0.625rem; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600; }

.members-list { display: flex; flex-direction: column; gap: 0.75rem; }
.member-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: var(--background); border-radius: var(--radius-sm); border: 1px solid var(--border); }
.member-name { font-weight: 600; color: var(--text-heading); font-size: 0.9375rem; }
.member-role-badge { font-size: 0.6875rem; font-weight: 700; background-color: #e0e7ff; color: #3730a3; padding: 0.125rem 0.5rem; border-radius: 4px; margin-left: 0.5rem; }
.pitch-text { font-size: 0.8125rem; color: var(--text-secondary); font-style: italic; margin-top: 0.25rem; }

.member-status-box { display: flex; align-items: center; gap: 0.75rem; }
.lead-actions { display: flex; gap: 0.375rem; }

.task-card-header { display: flex; justify-content: space-between; align-items: center; }
.tasks-list { display: flex; flex-direction: column; gap: 0.75rem; }
.task-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: var(--background); border-radius: var(--radius-sm); border: 1px solid var(--border); }
.task-title { font-weight: 600; font-size: 0.9375rem; }
.task-desc { font-size: 0.8125rem; color: var(--text-secondary); margin-top: 0.125rem; }
.task-meta { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.375rem; display: flex; gap: 1rem; }
.priority-high { color: var(--danger); }
.priority-medium { color: var(--warning); }
.priority-low { color: var(--success); }

.phase2-card { border-style: dashed; }
.phase2-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.phase2-tag { font-size: 0.6875rem; font-weight: 700; background-color: #f1f5f9; color: var(--text-secondary); padding: 0.125rem 0.5rem; border-radius: 4px; }
.phase2-desc { font-size: 0.8125rem; color: var(--text-secondary); }

.specs-card h3 { font-size: 1rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
.spec-item { display: flex; flex-direction: column; gap: 0.25rem; margin-bottom: 1rem; }
.spec-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }
.spec-val { font-size: 0.875rem; font-weight: 600; color: var(--text-heading); }
.spec-link { color: var(--primary); font-weight: 600; }

@media (max-width: 900px) { .details-grid { grid-template-columns: 1fr; } }
</style>
