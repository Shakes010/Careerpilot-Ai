<template>
  <StudentLayout>
    <div class="project-details-page">
      <!-- Top Navigation -->
      <div class="page-header">
        <router-link to="/student/projects" class="back-link">
          ← Back to Projects
        </router-link>

        <div class="header-actions" v-if="project">
          <AppButton
            v-if="!isOwner && !isMember && project.visibility === 'PUBLIC'"
            variant="primary"
            :loading="projectsStore.loading"
            @click="handleRequestToJoin"
          >
            Request to Join
          </AppButton>
        </div>
      </div>

      <!-- Loading State -->
      <AppLoader v-if="projectsStore.loading && !project" message="Loading project details..." />

      <div v-else-if="project" class="project-container">
        <!-- Main Header Card -->
        <AppCard class="header-card">
          <div class="title-bar">
            <div>
              <h1 class="project-title">{{ project.title }}</h1>
              <p class="project-subtitle">Category: {{ project.category }} • Owner: {{ project.owner_name }}</p>
            </div>
            <AppBadge :status="project.status" size="lg" />
          </div>

          <div class="nav-tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              class="tab-btn"
              :class="{ active: activeTab === tab.id }"
              @click="activeTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>
        </AppCard>

        <!-- TAB 1: OVERVIEW -->
        <div v-if="activeTab === 'overview'" class="tab-content">
          <AppCard title="Project Overview">
            <p class="desc-text">{{ project.description }}</p>

            <div class="meta-section">
              <h4>Technology Stack</h4>
              <div class="tech-wrap">
                <span v-for="tech in parseStack(project.technology_stack)" :key="tech" class="tech-chip">
                  {{ tech }}
                </span>
              </div>
            </div>

            <div class="grid-details">
              <div class="detail-box">
                <span class="detail-label">Team Capacity</span>
                <span class="detail-val">{{ activeMembersCount }} / {{ project.maximum_members }} Members</span>
              </div>
              <div class="detail-box">
                <span class="detail-label">Visibility</span>
                <span class="detail-val">{{ project.visibility }}</span>
              </div>
              <div class="detail-box">
                <span class="detail-label">Created Date</span>
                <span class="detail-val">{{ formatDate(project.created_at) }}</span>
              </div>
            </div>
          </AppCard>
        </div>

        <!-- TAB 2: TEAM (Feature 32) -->
        <div v-if="activeTab === 'team'" class="tab-content">
          <!-- Pending Join Requests (Project Owner Only) -->
          <AppCard v-if="isOwner" title="Pending Join Requests" subtitle="Review requests from students wanting to join your team.">
            <AppEmptyState
              v-if="joinRequests.length === 0"
              title="No pending join requests."
              message="Students requesting to join will appear here."
            />

            <div v-else class="requests-list">
              <div v-for="req in joinRequests" :key="req.id" class="request-item">
                <div>
                  <span class="student-name">{{ req.student_name }}</span>
                  <span class="req-date">Requested: {{ formatDate(req.created_at) }}</span>
                </div>
                <div class="request-actions">
                  <AppButton variant="primary" size="sm" @click="acceptRequest(req.id)">Accept</AppButton>
                  <AppButton variant="danger" size="sm" @click="rejectRequest(req.id)">Reject</AppButton>
                </div>
              </div>
            </div>
          </AppCard>

          <!-- Active Team Members -->
          <AppCard title="Team Members">
            <div class="members-grid">
              <div v-for="member in activeMembers" :key="member.id" class="member-card">
                <div class="member-header">
                  <div>
                    <h4 class="member-name">{{ member.student_name }}</h4>
                    <span class="role-badge">{{ member.role }}</span>
                  </div>
                  <span class="joined-date">Joined {{ formatDate(member.joined_at) }}</span>
                </div>

                <!-- Owner Actions -->
                <div v-if="isOwner && member.student_id !== project.owner_id" class="member-owner-actions">
                  <AppSelect
                    :model-value="member.role"
                    :options="roleOptions"
                    size="sm"
                    @update:model-value="val => changeMemberRole(member.student_id, val)"
                  />
                  <AppButton variant="danger" size="sm" @click="removeTeamMember(member.student_id)">
                    Remove
                  </AppButton>
                </div>
              </div>
            </div>
          </AppCard>
        </div>

        <!-- TAB 3: TASKS (Feature 32) -->
        <div v-if="activeTab === 'tasks'" class="tab-content">
          <AppCard title="Project Tasks">
            <template #header>
              <div class="task-card-header">
                <h3>Project Tasks</h3>
                <AppButton v-if="isMember" variant="primary" size="sm" @click="taskModal.show = true">
                  + Create Task
                </AppButton>
              </div>
            </template>

            <AppEmptyState
              v-if="project.tasks.length === 0"
              title="No tasks created yet."
              message="Create tasks to organize project deliverables and track progress."
            />

            <AppTable
              v-else
              :columns="taskColumns"
              :data="project.tasks"
            >
              <template #title="{ row }">
                <div class="font-semibold">{{ row.title }}</div>
                <div class="text-xs text-muted" v-if="row.description">{{ row.description }}</div>
              </template>

              <template #assigned_to="{ row }">
                <span>{{ row.assignee_name || 'Unassigned' }}</span>
              </template>

              <template #priority="{ row }">
                <span :class="`priority-badge priority-${row.priority.toLowerCase()}`">{{ row.priority }}</span>
              </template>

              <template #status="{ row }">
                <AppSelect
                  v-if="isMember"
                  :model-value="row.status"
                  :options="taskStatusOptions"
                  size="sm"
                  @update:model-value="val => updateTaskStatus(row.id, val)"
                />
                <span v-else>{{ row.status }}</span>
              </template>
            </AppTable>
          </AppCard>
        </div>

        <!-- TAB 4: PROGRESS TRACKING (Feature 33) -->
        <div v-if="activeTab === 'progress'" class="tab-content">
          <AppCard title="Project Progress Dashboard">
            <div class="progress-display-box">
              <div class="pct-header">
                <span>Overall Progress</span>
                <span class="pct-number">{{ projectProgress.progress_percentage }}%</span>
              </div>
              <div class="progress-bar-container">
                <div class="progress-bar-fill" :style="{ width: `${projectProgress.progress_percentage}%` }"></div>
              </div>
            </div>

            <div class="metrics-summary-grid">
              <div class="summary-card">
                <span class="summary-label">Total Tasks</span>
                <h3 class="summary-val">{{ projectProgress.total_tasks }}</h3>
              </div>
              <div class="summary-card success-card">
                <span class="summary-label">Completed Tasks</span>
                <h3 class="summary-val">{{ projectProgress.completed_tasks }}</h3>
              </div>
              <div class="summary-card warning-card">
                <span class="summary-label">In Progress</span>
                <h3 class="summary-val">{{ projectProgress.in_progress_tasks }}</h3>
              </div>
              <div class="summary-card info-card">
                <span class="summary-label">To Do</span>
                <h3 class="summary-val">{{ projectProgress.todo_tasks }}</h3>
              </div>
            </div>
          </AppCard>
        </div>

        <!-- TAB 5: COMPLETION VERIFICATION (Feature 34) -->
        <div v-if="activeTab === 'verification'" class="tab-content">
          <AppCard title="Project Completion Verification">
            <div class="verification-status-banner">
              <span class="ver-label">Current Verification Status:</span>
              <AppBadge :status="verificationStatusText" size="lg" />
            </div>

            <p class="ver-info">
              A completed project must undergo formal verification before earning verified skill credentials for student portfolios.
            </p>

            <div v-if="project.verification && project.verification.verification_notes" class="notes-box">
              <strong>Notes:</strong> {{ project.verification.verification_notes }}
            </div>

            <div v-if="isOwner && project.status !== 'VERIFIED'" class="ver-action-area">
              <AppButton
                variant="primary"
                :loading="projectsStore.loading"
                @click="submitVerification"
              >
                Submit for Verification
              </AppButton>
            </div>
          </AppCard>
        </div>
      </div>

      <!-- Create Task Modal -->
      <AppModal
        :show="taskModal.show"
        title="Create Project Task"
        @close="taskModal.show = false"
      >
        <form @submit.prevent="submitCreateTask">
          <AppInput
            v-model="taskModal.form.title"
            label="Task Title *"
            placeholder="e.g. Implement Vue Router Guards"
            required
          />

          <AppSelect
            v-model="taskModal.form.assigned_to"
            label="Assign To Member *"
            :options="memberAssignOptions"
          />

          <AppSelect
            v-model="taskModal.form.priority"
            label="Priority *"
            :options="['LOW', 'MEDIUM', 'HIGH']"
            required
          />

          <div class="form-group">
            <label class="form-label">Task Description</label>
            <textarea
              v-model="taskModal.form.description"
              rows="3"
              class="form-textarea"
              placeholder="Detailed instructions for assignee..."
            ></textarea>
          </div>
        </form>

        <template #footer>
          <AppButton variant="secondary" @click="taskModal.show = false">Cancel</AppButton>
          <AppButton variant="primary" :loading="taskModal.loading" @click="submitCreateTask">
            Create Task
          </AppButton>
        </template>
      </AppModal>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import StudentLayout from '@/components/layout/StudentLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppTable from '@/components/common/AppTable.vue'
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
const activeTab = ref('overview')

const tabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'team', label: 'Team' },
  { id: 'tasks', label: 'Tasks' },
  { id: 'progress', label: 'Progress' },
  { id: 'verification', label: 'Verification' }
]

const project = computed(() => projectsStore.currentProject)
const joinRequests = computed(() => projectsStore.joinRequests)

const currentUser = computed(() => authStore.user)
const isOwner = computed(() => project.value && currentUser.value && project.value.owner_id === currentUser.value.id)
const isMember = computed(() => {
  if (!project.value || !currentUser.value) return false
  if (isOwner.value) return true
  return project.value.members.some(m => m.student_id === currentUser.value.id && m.status === 'ACTIVE')
})

const activeMembers = computed(() => project.value ? project.value.members.filter(m => m.status === 'ACTIVE') : [])
const activeMembersCount = computed(() => activeMembers.value.length)

const projectProgress = computed(() => {
  if (project.value && project.value.progress) return project.value.progress
  return { total_tasks: 0, completed_tasks: 0, todo_tasks: 0, in_progress_tasks: 0, progress_percentage: 0 }
})

const verificationStatusText = computed(() => {
  if (project.value && project.value.verification) {
    return project.value.verification.status
  }
  return 'Not Submitted'
})

const roleOptions = [
  { label: 'Owner', value: 'OWNER' },
  { label: 'Member', value: 'MEMBER' },
  { label: 'Team Lead', value: 'TEAM_LEAD' },
  { label: 'Frontend', value: 'FRONTEND' },
  { label: 'Backend', value: 'BACKEND' },
  { label: 'UI/UX', value: 'UI_UX' },
  { label: 'Testing', value: 'TESTING' }
]

const taskStatusOptions = [
  { label: 'To Do', value: 'TODO' },
  { label: 'In Progress', value: 'IN_PROGRESS' },
  { label: 'Completed', value: 'COMPLETED' }
]

const taskColumns = [
  { label: 'Task Title', key: 'title' },
  { label: 'Assigned Member', key: 'assigned_to' },
  { label: 'Priority', key: 'priority' },
  { label: 'Status', key: 'status' }
]

const memberAssignOptions = computed(() => {
  return activeMembers.value.map(m => ({
    label: m.student_name,
    value: m.student_id
  }))
})

const taskModal = reactive({
  show: false,
  form: { title: '', description: '', assigned_to: '', priority: 'MEDIUM' },
  loading: false
})

const parseStack = (str) => str ? str.split(',').map(s => s.trim()).filter(Boolean) : []
const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' }) : ''

const handleRequestToJoin = async () => {
  try {
    await projectsStore.requestToJoin(projectId)
    toast.show('✓ Join request submitted.')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Unable to join project.', 'error')
  }
}

const acceptRequest = async (requestId) => {
  try {
    await projectsStore.acceptJoinRequest(projectId, requestId)
    toast.show('✓ Member accepted')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to accept request.', 'error')
  }
}

const rejectRequest = async (requestId) => {
  try {
    await projectsStore.rejectJoinRequest(projectId, requestId)
    toast.show('✓ Member rejected', 'info')
  } catch (err) {
    toast.show('Failed to reject request.', 'error')
  }
}

const changeMemberRole = async (studentId, newRole) => {
  try {
    await projectsStore.updateMemberRole(projectId, studentId, newRole)
    toast.show(`✓ Role updated to ${newRole}`)
  } catch (err) {
    toast.show('Failed to update role.', 'error')
  }
}

const removeTeamMember = async (studentId) => {
  if (confirm('Are you sure you want to remove this member from the project?')) {
    try {
      await projectsStore.removeMember(projectId, studentId)
      toast.show('✓ Member removed from project.')
    } catch (err) {
      toast.show(err.response?.data?.detail || 'Failed to remove member.', 'error')
    }
  }
}

const submitCreateTask = async () => {
  if (!taskModal.form.title.trim()) return

  taskModal.loading = true
  try {
    await projectsStore.createTask(projectId, taskModal.form)
    toast.show('✓ Task created')
    taskModal.show = false
    taskModal.form.title = ''
    taskModal.form.description = ''
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Unable to create task.', 'error')
  } finally {
    taskModal.loading = false
  }
}

const updateTaskStatus = async (taskId, statusVal) => {
  try {
    await projectsStore.updateTaskStatus(projectId, taskId, statusVal)
    toast.show('✓ Task updated')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Unable to update task.', 'error')
  }
}

const submitVerification = async () => {
  try {
    await projectsStore.submitForVerification(projectId, "Work completed and ready for verification.")
    toast.show('✓ Project submitted for verification')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Unable to submit project for verification.', 'error')
  }
}

onMounted(async () => {
  await projectsStore.fetchProjectDetails(projectId)
  if (isOwner.value) {
    projectsStore.fetchJoinRequests(projectId)
  }
})
</script>

<style scoped>
.project-details-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; }
.back-link { font-size: 0.875rem; font-weight: 600; color: var(--primary); }
.header-actions { display: flex; gap: 0.75rem; }

.header-card { padding-bottom: 0; }
.title-bar { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; }
.project-title { font-size: 1.625rem; font-weight: 700; color: var(--text-heading); }
.project-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.nav-tabs { display: flex; gap: 0.5rem; border-top: 1px solid var(--border); padding-top: 0.75rem; overflow-x: auto; }
.tab-btn { padding: 0.625rem 1.25rem; font-size: 0.875rem; font-weight: 600; border: none; background: none; color: var(--text-secondary); cursor: pointer; border-bottom: 2px solid transparent; }
.tab-btn.active { color: var(--primary); border-bottom-color: var(--primary); }

.tab-content { display: flex; flex-direction: column; gap: 1.5rem; }

.desc-text { font-size: 0.9375rem; line-height: 1.6; color: var(--text-primary); }
.meta-section { margin-top: 1.25rem; }
.meta-section h4 { font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem; }
.tech-wrap { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.tech-chip { background-color: var(--primary-light); color: var(--primary); padding: 0.25rem 0.625rem; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600; }

.grid-details { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border); }
.detail-box { display: flex; flex-direction: column; }
.detail-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }
.detail-val { font-size: 0.9375rem; font-weight: 600; color: var(--text-heading); margin-top: 0.125rem; }

.requests-list { display: flex; flex-direction: column; gap: 0.75rem; margin-top: 0.75rem; }
.request-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: var(--background); border-radius: var(--radius-sm); border: 1px solid var(--border); }
.student-name { font-weight: 600; display: block; }
.req-date { font-size: 0.75rem; color: var(--text-muted); }
.request-actions { display: flex; gap: 0.5rem; }

.members-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
.member-card { padding: 1rem; background-color: var(--background); border-radius: var(--radius-sm); border: 1px solid var(--border); display: flex; flex-direction: column; gap: 0.75rem; }
.member-header { display: flex; justify-content: space-between; align-items: flex-start; }
.member-name { font-weight: 600; font-size: 0.9375rem; }
.role-badge { font-size: 0.6875rem; font-weight: 700; background-color: #e0e7ff; color: #3730a3; padding: 0.125rem 0.5rem; border-radius: 4px; display: inline-block; margin-top: 0.25rem; }
.joined-date { font-size: 0.75rem; color: var(--text-muted); }
.member-owner-actions { display: flex; gap: 0.5rem; align-items: center; margin-top: auto; }

.task-card-header { display: flex; justify-content: space-between; align-items: center; }
.priority-badge { font-size: 0.75rem; font-weight: 700; padding: 0.125rem 0.5rem; border-radius: 4px; }
.priority-high { background-color: #fee2e2; color: #991b1b; }
.priority-medium { background-color: #fef3c7; color: #92400e; }
.priority-low { background-color: #dcfce7; color: #166534; }

.progress-display-box { margin-bottom: 1.5rem; }
.pct-header { display: flex; justify-content: space-between; font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem; }
.pct-number { color: var(--primary); font-size: 1.25rem; font-weight: 700; }
.progress-bar-container { height: 14px; background-color: #e2e8f0; border-radius: var(--radius-full); overflow: hidden; }
.progress-bar-fill { height: 100%; background-color: var(--primary); transition: width 0.3s ease; }

.metrics-summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; }
.summary-card { padding: 1rem; background-color: var(--background); border-radius: var(--radius-sm); border: 1px solid var(--border); }
.summary-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }
.summary-val { font-size: 1.5rem; font-weight: 700; margin-top: 0.25rem; }
.success-card .summary-val { color: var(--success); }
.warning-card .summary-val { color: var(--warning); }
.info-card .summary-val { color: var(--primary); }

.verification-status-banner { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.ver-label { font-weight: 600; font-size: 1rem; }
.ver-info { font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5; }
.notes-box { background-color: var(--background); padding: 0.875rem; border-radius: var(--radius-sm); font-size: 0.875rem; margin-top: 1rem; }
.ver-action-area { margin-top: 1.5rem; }

.font-semibold { font-weight: 600; }
.text-xs { font-size: 0.75rem; }
.text-muted { color: var(--text-muted); }
</style>
