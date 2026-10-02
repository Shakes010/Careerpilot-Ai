<template>
  <div class="skills-page">

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
        <h1 class="page-title">Skill Trust Meter &amp; Verification</h1>
        <p class="page-sub">Weighted Noisy-OR Bayesian evidence engine distinguishing Verified from Declared competencies.</p>
      </div>
      <button @click="showAddSkillModal = true" class="btn-primary-add">
        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>+ Declare New Skill</span>
      </button>
    </div>

    <!-- 4 Stats Overview Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#EFF6FF;">
          <svg width="20" height="20" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="1.8">
            <polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Verified Competencies</div>
          <div class="stat-value" style="color:#2563EB;">{{ verifiedSkillsCount }}</div>
          <div class="stat-sub">Cryptographically Proven</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#ECFDF5;">
          <svg width="20" height="20" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="1.8">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Average Trust Score</div>
          <div class="stat-value" style="color:#10B981;">{{ avgTrust }}%</div>
          <div class="stat-sub">Bayesian Confidence</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#F5F3FF;">
          <svg width="20" height="20" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="1.8">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Total Declared Skills</div>
          <div class="stat-value" style="color:#7C3AED;">{{ skills.length }}</div>
          <div class="stat-sub">Profile Portfolio</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#FFFBEB;">
          <svg width="20" height="20" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="1.8">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Missing Evidence Nudges</div>
          <div class="stat-value" style="color:#D97706;">{{ nudges.length }}</div>
          <div class="stat-sub">Action Required</div>
        </div>
      </div>
    </div>

    <!-- Missing Evidence Detector Alert -->
    <div v-if="nudges.length" class="nudges-container">
      <div v-for="n in nudges" :key="n.student_skill_id" class="nudge-banner">
        <div class="nudge-left">
          <span class="nudge-icon">⚠️</span>
          <div>
            <span class="nudge-bold">Missing Evidence Flag:</span>
            <span class="nudge-text">{{ n.message }}</span>
          </div>
        </div>
        <router-link :to="`/assessments?skill_id=${n.skill_id || ''}`" class="btn-nudge-action">
          Verify Skill Now →
        </router-link>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!skills.length" class="empty-box">
      <div class="empty-icon-circle">
        <svg width="28" height="28" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
          <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        </svg>
      </div>
      <h3 class="empty-title">No Skills Declared Yet</h3>
      <p class="empty-desc">Declare your core technical skills or upload your resume in the Career Passport to calibrate your Skill Trust Meter™.</p>
      <button @click="showAddSkillModal = true" class="btn-primary-add" style="margin-top:6px;">
        + Declare Your First Skill
      </button>
    </div>

    <!-- Skills Cards Grid -->
    <div v-else class="skills-grid">
      <div v-for="sk in skills" :key="sk.id" class="skill-card">
        <div>
          <div class="skill-card-top">
            <h3 class="skill-title">{{ sk.skill_name }}</h3>
            <span class="badge-pill" :class="sk.badge_tier === 'verified' ? 'badge-pill--green' : 'badge-pill--gray'">
              {{ sk.badge_tier === 'verified' ? '✓ Verified' : 'Declared' }}
            </span>
          </div>

          <div class="skill-category">Domain: {{ sk.category }}</div>

          <!-- Trust Meter Bar -->
          <div class="trust-meter-block">
            <div class="trust-meter-labels">
              <span class="trust-label">Trust Meter</span>
              <span class="trust-pct" :style="{ color: sk.badge_tier === 'verified' ? '#2563EB' : '#64748B' }">
                {{ sk.trust_score }}%
              </span>
            </div>
            <div class="meter-bar-bg">
              <div
                class="meter-bar-fill"
                :style="{ width: `${sk.trust_score}%`, background: sk.badge_tier === 'verified' ? '#2563EB' : '#94A3B8' }"
              ></div>
            </div>
          </div>
        </div>

        <div class="skill-card-footer">
          <div class="evidence-status-pill" :class="sk.badge_tier === 'verified' ? 'status-pill--verified' : 'status-pill--declared'">
            <span class="status-dot"></span>
            <span>{{ sk.badge_tier === 'verified' ? 'Cryptographically Verified' : 'Awaiting Test Verification' }}</span>
          </div>
          <router-link :to="`/assessments?skill_id=${sk.skill_id}`" class="link-verify">
            {{ sk.badge_tier === 'verified' ? 'Retake Assessment →' : 'Take Verification Test →' }}
          </router-link>
        </div>
      </div>
    </div>

    <!-- Declare Skill Modal -->
    <div v-if="showAddSkillModal" class="modal-overlay" @click.self="showAddSkillModal = false">
      <div class="modal-box">
        <div class="modal-header">
          <div>
            <h3 class="modal-title">Declare a New Skill</h3>
            <p class="modal-sub">Add a competency to track and prove via automated tests.</p>
          </div>
          <button @click="showAddSkillModal = false" class="btn-modal-close">✕</button>
        </div>

        <div class="modal-form">
          <div class="form-item">
            <label class="form-item-label">Select Skill</label>
            <select v-model="selectedSkillId" class="form-item-select">
              <option v-for="s in availableSkills" :key="s.id" :value="s.id">
                {{ s.skill_name }} ({{ s.category }})
              </option>
            </select>
          </div>

          <div class="form-item">
            <label class="form-item-label">Proficiency Level</label>
            <select v-model.number="selfRating" class="form-item-select">
              <option :value="2">Beginner (Foundational)</option>
              <option :value="3">Intermediate (Practical Builder)</option>
              <option :value="5">Advanced / Production Ready</option>
            </select>
          </div>

          <div class="modal-footer">
            <button @click="showAddSkillModal = false" class="btn-outline">Cancel</button>
            <button @click="declareSkill" class="btn-submit-modal">Save &amp; Track Skill</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const skills = ref([])
const availableSkills = ref([])
const nudges = ref([])
const showAddSkillModal = ref(false)
const selectedSkillId = ref('')
const selfRating = ref(3)
const toast = ref(null)

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

const verifiedSkillsCount = computed(() => {
  return skills.value.filter(s => s.badge_tier === 'verified').length
})

const avgTrust = computed(() => {
  if (!skills.value.length) return 75
  const sum = skills.value.reduce((acc, s) => acc + (s.trust_score || 0), 0)
  return Math.round(sum / skills.value.length)
})

onMounted(async () => {
  await loadSkillsData()
})

const loadSkillsData = async () => {
  try {
    const mySkills = await apiFetch('/skills/my-skills')
    skills.value = mySkills || []

    const allSk = await apiFetch('/skills')
    availableSkills.value = allSk || []
    if (availableSkills.value.length && !selectedSkillId.value) {
      selectedSkillId.value = availableSkills.value[0].id
    }

    const ndg = await apiFetch('/skills/missing-evidence')
    nudges.value = ndg || []
  } catch (err) {
    console.error('Failed to load skills data:', err)
  }
}

const declareSkill = async () => {
  try {
    await apiFetch('/skills/my-skills', {
      method: 'POST',
      body: JSON.stringify({
        skill_id: selectedSkillId.value,
        self_rating: selfRating.value
      })
    })
    showAddSkillModal.value = false
    showToast('New skill declared and tracked in Skill Trust Meter!')
    await loadSkillsData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}
</script>

<style scoped>
/* ─── Page Root ──────────────────────────────────────── */
.skills-page {
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

/* ─── Nudges ─────────────────────────────────────────── */
.nudges-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nudge-banner {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: 14px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
}

.nudge-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12.5px;
  color: #92400E;
}

.nudge-icon {
  font-size: 18px;
}

.nudge-bold {
  font-weight: 800;
}

.nudge-text {
  margin-left: 6px;
}

.btn-nudge-action {
  padding: 6px 14px;
  background: #FFFFFF;
  border: 1.5px solid #FCD34D;
  border-radius: 8px;
  font-size: 11.5px;
  font-weight: 700;
  color: #B45309;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.12s ease;
}

.btn-nudge-action:hover {
  background: #FEF3C7;
}

/* ─── Empty State ────────────────────────────────────── */
.empty-box {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 18px;
  padding: 48px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.empty-icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-title {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
}

.empty-desc {
  font-size: 13px;
  color: #64748B;
  max-width: 440px;
  line-height: 1.5;
}

/* ─── Skills Grid ────────────────────────────────────── */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.skill-card {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 18px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 18px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  transition: all 0.15s ease;
}

.skill-card:hover {
  border-color: #93C5FD;
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.07);
}

.skill-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 4px;
}

.skill-title {
  font-size: 15px;
  font-weight: 800;
  color: #0F172A;
}

.skill-category {
  font-size: 11.5px;
  color: #64748B;
  margin-bottom: 16px;
}

.trust-meter-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.trust-meter-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.trust-label {
  color: #64748B;
  font-weight: 600;
}

.trust-pct {
  font-weight: 800;
}

.meter-bar-bg {
  width: 100%;
  height: 7px;
  background: #EEF2FF;
  border-radius: 9999px;
  overflow: hidden;
}

.meter-bar-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.5s ease;
}

.skill-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding-top: 14px;
  border-top: 1px solid #F0F4FF;
  font-size: 12px;
}

.evidence-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
}

.status-pill--verified {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
}

.status-pill--verified .status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10B981;
}

.status-pill--declared {
  background: #F1F5F9;
  color: #64748B;
  border: 1px solid #E2E8F0;
}

.status-pill--declared .status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #94A3B8;
}

.link-verify {
  font-weight: 700;
  color: #2563EB;
  text-decoration: none;
  font-size: 12px;
  transition: all 0.12s ease;
  white-space: nowrap;
}

.link-verify:hover {
  text-decoration: underline;
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

.badge-pill--gray {
  background: #F1F5F9;
  color: #475569;
  border: 1px solid #E2E8F0;
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
  max-width: 440px;
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

.form-item-select,
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

.form-item-select:focus,
.form-item-input:focus {
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
  .skills-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .skills-grid {
    grid-template-columns: 1fr;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
