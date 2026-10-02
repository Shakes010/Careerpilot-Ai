<template>
  <div class="proj-page">

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" class="toast-popup" :class="`toast-popup--${toast.type}`">
        <span>{{ toast.type === 'error' ? '⚠️' : '✅' }}</span>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Project Collaboration &amp; Sandbox Missions</h1>
        <p class="page-sub">Peer and admin-verified project submissions directly calibrate your Skill Trust Meter™.</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary-add">
        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>Create Team Project</span>
      </button>
    </div>

    <!-- Stat Metrics Row -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#EFF6FF;">
          <svg width="20" height="20" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="1.8">
            <polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Total Projects</div>
          <div class="stat-value">{{ projects.length }}</div>
          <div class="stat-sub">Collaborative Builds</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#ECFDF5;">
          <svg width="20" height="20" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="1.8">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Verified Completions</div>
          <div class="stat-value" style="color:#10B981;">{{ verifiedCount }}</div>
          <div class="stat-sub">Peer / Recruiter Signed</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#F5F3FF;">
          <svg width="20" height="20" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="1.8">
            <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Average Completion</div>
          <div class="stat-value" style="color:#7C3AED;">{{ avgProgress }}%</div>
          <div class="stat-sub">Milestone Progress</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#FFFBEB;">
          <svg width="20" height="20" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="1.8">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Sandbox Challenges</div>
          <div class="stat-value" style="color:#D97706;">{{ sandboxChallenges.length || 4 }}</div>
          <div class="stat-sub">Active Missions</div>
        </div>
      </div>
    </div>

    <!-- Active Projects Section -->
    <div class="section-container">
      <div class="section-header">
        <h2 class="section-title">Active Engineering Projects</h2>
        <span class="section-counter">{{ projects.length }} Active</span>
      </div>

      <div class="projects-grid">
        <div v-for="p in projects" :key="p.id" class="project-card">
          <div>
            <div class="card-top-row">
              <span class="badge-pill" :class="p.is_verified ? 'badge-pill--green' : 'badge-pill--blue'">
                {{ p.is_verified ? '✓ Verified Completion' : 'In Progress' }}
              </span>
              <span class="progress-val">{{ p.progress_pct }}% Completed</span>
            </div>

            <h3 class="project-title">{{ p.title }}</h3>
            <p class="project-desc">{{ p.description || 'Production-grade collaborative software architecture project.' }}</p>

            <!-- Tech stack chips -->
            <div class="tech-stack-row">
              <span v-for="tech in p.tech_stack" :key="tech" class="tech-chip">
                {{ tech }}
              </span>
            </div>

            <!-- Progress bar -->
            <div class="bar-bg">
              <div class="bar-fill" :style="{ width: `${p.progress_pct}%` }"></div>
            </div>
          </div>

          <div class="card-bottom-actions">
            <span class="task-count">{{ p.done_tasks }}/{{ p.total_tasks }} Tasks Cleared</span>
            <button
              v-if="!p.is_verified"
              @click="verifyProject(p)"
              class="btn-verify"
            >
              Request Verification →
            </button>
            <span v-else class="verified-label">✓ Cryptographically Signed</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Career Sandbox Challenges Section -->
    <div class="section-container">
      <div class="section-header">
        <h2 class="section-title">Career Sandbox Practice Challenges</h2>
        <span class="section-desc-inline">Interactive problem scenarios to strengthen practical problem-solving.</span>
      </div>

      <div class="sandbox-grid">
        <div v-for="c in sandboxChallenges" :key="c.id" class="challenge-card">
          <div class="challenge-left">
            <div class="challenge-icon-box">⚡</div>
            <div class="challenge-info">
              <h3 class="challenge-title">{{ c.title }}</h3>
              <p class="challenge-desc">{{ c.description }}</p>
              <div class="challenge-meta">
                <span class="badge-pill badge-pill--blue">{{ c.skill_name }}</span>
                <span class="difficulty-tag">Difficulty: <strong>{{ c.difficulty }}</strong></span>
              </div>
            </div>
          </div>

          <router-link to="/assessments" class="btn-start-challenge">
            Start Challenge →
          </router-link>
        </div>
      </div>
    </div>

    <!-- Create Project Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <div>
            <h3 class="modal-title">Create New Team Project</h3>
            <p class="modal-sub">Document an end-to-end project to unlock peer validation.</p>
          </div>
          <button @click="showCreateModal = false" class="btn-modal-close">✕</button>
        </div>

        <form @submit.prevent="createProject" class="modal-form">
          <div class="form-item">
            <label class="form-item-label">Project Title</label>
            <input
              v-model="newTitle"
              type="text"
              required
              placeholder="e.g. Distributed Order Dispatcher"
              class="form-item-input"
            />
          </div>

          <div class="form-item">
            <label class="form-item-label">Project Description</label>
            <textarea
              v-model="newDesc"
              rows="3"
              placeholder="Key technical capabilities, architecture patterns and features..."
              class="form-item-textarea"
            ></textarea>
          </div>

          <div class="form-item">
            <label class="form-item-label">Technologies (comma separated)</label>
            <input
              v-model="newTech"
              type="text"
              placeholder="Python, FastAPI, Vue.js, PostgreSQL"
              class="form-item-input"
            />
          </div>

          <div class="modal-footer">
            <button type="button" @click="showCreateModal = false" class="btn-outline">Cancel</button>
            <button type="submit" class="btn-submit-modal">Create Project →</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const projects = ref([])
const sandboxChallenges = ref([])
const showCreateModal = ref(false)
const newTitle = ref('')
const newDesc = ref('')
const newTech = ref('Python, FastAPI, PostgreSQL')
const toast = ref(null)

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

const verifiedCount = computed(() => {
  return projects.value.filter(p => p.is_verified).length
})

const avgProgress = computed(() => {
  if (!projects.value.length) return 80
  const sum = projects.value.reduce((acc, p) => acc + (p.progress_pct || 0), 0)
  return Math.round(sum / projects.value.length)
})

onMounted(async () => {
  await loadProjectsData()
})

const loadProjectsData = async () => {
  try {
    const list = await apiFetch('/projects')
    projects.value = list || []

    const sandbox = await apiFetch('/projects/sandbox/challenges')
    sandboxChallenges.value = sandbox || []
  } catch (err) {
    console.error('Failed to load projects:', err)
  }
}

const createProject = async () => {
  try {
    const stack = newTech.value.split(',').map(s => s.trim()).filter(Boolean)
    await apiFetch('/projects', {
      method: 'POST',
      body: JSON.stringify({
        title: newTitle.value.trim(),
        description: newDesc.value.trim(),
        tech_stack: stack
      })
    })
    showCreateModal.value = false
    newTitle.value = ''
    newDesc.value = ''
    showToast('Team project created successfully!')
    await loadProjectsData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}

const verifyProject = async (proj) => {
  try {
    const res = await apiFetch(`/projects/${proj.id}/verify`, { method: 'POST' })
    showToast(res.message || 'Verification submitted!')
    await loadProjectsData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}
</script>

<style scoped>
/* ─── Page Root ──────────────────────────────────────── */
.proj-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 1360px;
  margin: 0 auto;
}

/* ─── Page Header ────────────────────────────────────── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.page-title {
  font-size: 22px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.3px;
}

.page-sub {
  font-size: 13px;
  color: #64748B;
  margin-top: 4px;
}

.btn-primary-add {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #2563EB;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 700;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-primary-add:hover {
  background: #1D4ED8;
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.32);
}

/* ─── Stats Grid ─────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  transition: box-shadow 0.15s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
}

.stat-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-body {
  flex: 1;
}

.stat-label {
  font-size: 11.5px;
  font-weight: 600;
  color: #64748B;
  margin-bottom: 2px;
}

.stat-value {
  font-size: 26px;
  font-weight: 900;
  color: #0F172A;
  line-height: 1.1;
  letter-spacing: -0.4px;
}

.stat-sub {
  font-size: 11px;
  font-weight: 600;
  color: #94A3B8;
  margin-top: 3px;
}

/* ─── Section Container ──────────────────────────────── */
.section-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2px;
}

.section-title {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
}

.section-counter {
  font-size: 12px;
  font-weight: 700;
  color: #2563EB;
  background: #EFF6FF;
  padding: 3px 10px;
  border-radius: 9999px;
  border: 1px solid #BFDBFE;
}

.section-desc-inline {
  font-size: 12.5px;
  color: #64748B;
}

/* ─── Projects Grid ──────────────────────────────────── */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.project-card {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 18px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 18px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  transition: all 0.15s ease;
}

.project-card:hover {
  border-color: #93C5FD;
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.07);
}

.card-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-val {
  font-size: 12px;
  font-weight: 800;
  color: #2563EB;
}

.project-title {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
  margin-bottom: 4px;
}

.project-desc {
  font-size: 12.5px;
  color: #64748B;
  line-height: 1.55;
  margin-bottom: 12px;
}

.tech-stack-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.tech-chip {
  padding: 3px 9px;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #475569;
}

.bar-bg {
  width: 100%;
  height: 6px;
  background: #EEF2FF;
  border-radius: 9999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #2563EB;
  border-radius: 9999px;
  transition: width 0.4s ease;
}

.card-bottom-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid #F0F4FF;
}

.task-count {
  font-size: 12px;
  color: #64748B;
  font-weight: 600;
}

.btn-verify {
  padding: 7px 14px;
  background: #EFF6FF;
  border: 1.5px solid #BFDBFE;
  border-radius: 9px;
  font-size: 11.5px;
  font-weight: 700;
  color: #2563EB;
  cursor: pointer;
  transition: all 0.12s ease;
}

.btn-verify:hover {
  background: #2563EB;
  color: #FFFFFF;
}

.verified-label {
  font-size: 11px;
  font-weight: 800;
  color: #059669;
}

/* ─── Sandbox Challenges Grid ────────────────────────── */
.sandbox-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.challenge-card {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  transition: all 0.15s ease;
}

.challenge-card:hover {
  border-color: #BFDBFE;
  box-shadow: 0 4px 16px rgba(37, 99, 235, 0.06);
}

.challenge-left {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.challenge-icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.challenge-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.challenge-title {
  font-size: 14px;
  font-weight: 800;
  color: #0F172A;
}

.challenge-desc {
  font-size: 12px;
  color: #64748B;
  line-height: 1.45;
}

.challenge-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.difficulty-tag {
  font-size: 11px;
  color: #64748B;
}

.difficulty-tag strong {
  color: #0F172A;
}

.btn-start-challenge {
  padding: 8px 16px;
  background: #F8FAFC;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  color: #0F172A;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.12s ease;
}

.btn-start-challenge:hover {
  background: #2563EB;
  border-color: #2563EB;
  color: #FFFFFF;
}

/* ─── Badge Pills ────────────────────────────────────── */
.badge-pill {
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.4px;
  white-space: nowrap;
}

.badge-pill--green {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
}

.badge-pill--blue {
  background: #EFF6FF;
  color: #2563EB;
  border: 1px solid #BFDBFE;
}

/* ─── Modal ─────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-box {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 28px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.modal-title {
  font-size: 17px;
  font-weight: 800;
  color: #0F172A;
}

.modal-sub {
  font-size: 12px;
  color: #64748B;
  margin-top: 2px;
}

.btn-modal-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #F1F5F9;
  border: none;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-modal-close:hover {
  background: #E2E8F0;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item-label {
  font-size: 12px;
  font-weight: 700;
  color: #1E293B;
}

.form-item-input {
  width: 100%;
  height: 42px;
  padding: 0 14px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 13px;
  color: #0F172A;
  outline: none;
  font-family: inherit;
  box-sizing: border-box;
}

.form-item-input:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-item-textarea {
  width: 100%;
  padding: 10px 14px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 13px;
  color: #0F172A;
  outline: none;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}

.form-item-textarea:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
  border-top: 1px solid #F0F4FF;
}

.btn-outline {
  padding: 9px 18px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
}

.btn-submit-modal {
  padding: 9px 18px;
  background: #2563EB;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
}

.btn-submit-modal:hover {
  background: #1D4ED8;
}

/* ─── Toast Popup ────────────────────────────────────── */
.toast-popup {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(8px);
}

.toast-popup--success {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  color: #065F46;
}

.toast-popup--error {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #991B1B;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.25s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 1024px) {
  .projects-grid,
  .sandbox-grid {
    grid-template-columns: 1fr;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .challenge-card {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
