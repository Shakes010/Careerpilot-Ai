<template>
  <div class="app-page">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">My Job &amp; Internship Applications</h1>
        <p class="page-sub">Real-time status tracking across your submitted applications, recruiter reviews, and interview schedules.</p>
      </div>
      <router-link to="/opportunities" class="page-btn-primary">
        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        Explore More Opportunities
      </router-link>
    </div>

    <!-- Stat Cards -->
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-icon-box" style="background:#EFF6FF;">
          <svg width="20" height="20" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="1.8">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">Total Applications</div>
          <div class="stat-value">{{ applications.length }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-box" style="background:#FFFBEB;">
          <svg width="20" height="20" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="1.8">
            <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">Shortlisted / Review</div>
          <div class="stat-value" style="color:#D97706;">{{ shortlistedCount }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-box" style="background:#F5F3FF;">
          <svg width="20" height="20" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="1.8">
            <rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">Interview Scheduled</div>
          <div class="stat-value" style="color:#7C3AED;">{{ interviewCount }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-box" style="background:#ECFDF5;">
          <svg width="20" height="20" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="1.8">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">Active Offers</div>
          <div class="stat-value" style="color:#10B981;">{{ offerCount }}</div>
        </div>
      </div>
    </div>

    <!-- Applications List -->
    <div class="content-card">

      <!-- Filter Bar -->
      <div class="filter-bar">
        <div class="filter-tabs">
          <button
            v-for="tab in filterTabs"
            :key="tab.value"
            @click="activeFilter = tab.value"
            :class="['filter-tab', activeFilter === tab.value ? 'filter-tab--active' : '']"
          >
            {{ tab.label }}
            <span v-if="tab.count !== undefined" class="filter-tab-count">{{ tab.count }}</span>
          </button>
        </div>
        <button @click="loadApplications" class="refresh-btn">
          <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
            <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          Refresh Status
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="empty-state">
        <div class="spinner"></div>
        <p>Loading your applications...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="!filteredApplications.length" class="empty-state">
        <div class="empty-icon">💼</div>
        <h3 class="empty-title">No Applications in this Category</h3>
        <p class="empty-desc">Browse live jobs and internships to submit new verified applications.</p>
        <router-link to="/opportunities" class="page-btn-primary" style="margin-top:8px;">
          Browse Opportunities →
        </router-link>
      </div>

      <!-- Application Cards -->
      <div v-else class="app-list">
        <div
          v-for="app in filteredApplications"
          :key="app.id"
          class="app-card"
        >
          <!-- Left: Company Icon -->
          <div class="app-company-icon">
            <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
              <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
            </svg>
          </div>

          <!-- Middle: Job Info -->
          <div class="app-info">
            <div class="app-title-row">
              <span class="app-job-title">{{ app.title }}</span>
              <span class="app-status-badge" :class="statusBadgeClass(app.status)">
                {{ (app.status || '').replace(/_/g, ' ').toUpperCase() }}
              </span>
            </div>
            <div class="app-org-row">
              <span class="app-org">{{ app.organizer }}</span>
              <span class="app-dot">•</span>
              <span class="app-date">Applied on: {{ app.applied_at ? new Date(app.applied_at).toLocaleDateString('en-IN') : 'Recent' }}</span>
            </div>
            <div v-if="app.required_skills && app.required_skills.length" class="app-skills">
              <span v-for="sk in app.required_skills" :key="sk" class="skill-chip">{{ sk }}</span>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="app-actions">
            <router-link to="/passport" class="app-btn-outline">View Verified Passport</router-link>
            <router-link to="/opportunities" class="app-btn-primary">Opportunity Details →</router-link>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const applications = ref([])
const loading = ref(false)
const activeFilter = ref('all')

const filterTabs = computed(() => [
  { label: 'All', value: 'all', count: applications.value.length },
  { label: 'Applied', value: 'applied', count: applications.value.filter(a => a.status === 'applied').length },
  { label: 'Under Review', value: 'shortlisted', count: shortlistedCount.value },
  { label: 'Interview', value: 'interview_scheduled', count: interviewCount.value },
  { label: 'Offers', value: 'offer_received', count: offerCount.value }
])

const shortlistedCount = computed(() => applications.value.filter(a => a.status === 'shortlisted').length)
const interviewCount = computed(() => applications.value.filter(a => a.status === 'interview_scheduled').length)
const offerCount = computed(() => applications.value.filter(a => a.status === 'offer_received').length)

const filteredApplications = computed(() => {
  if (activeFilter.value === 'all') return applications.value
  return applications.value.filter(a => a.status === activeFilter.value)
})

const statusBadgeClass = (status) => {
  const s = (status || '').toLowerCase()
  if (s.includes('offer')) return 'badge--green'
  if (s.includes('shortlisted') || s.includes('review')) return 'badge--amber'
  if (s.includes('interview')) return 'badge--purple'
  if (s.includes('applied')) return 'badge--blue'
  return 'badge--gray'
}

onMounted(async () => { await loadApplications() })

const loadApplications = async () => {
  loading.value = true
  try {
    applications.value = await apiFetch('/opportunities/my-applications') || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ── Page Shell ────────────────────────────────────── */
.app-page { display: flex; flex-direction: column; gap: 24px; max-width: 1360px; margin: 0 auto; }

/* ── Header ────────────────────────────────────────── */
.page-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.page-title { font-size: 22px; font-weight: 800; color: #0F172A; letter-spacing: -0.3px; }
.page-sub { font-size: 13px; color: #6B7280; margin-top: 4px; line-height: 1.5; }
.page-btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; background: #2563EB; color: #fff;
  font-size: 13px; font-weight: 700; border-radius: 10px;
  text-decoration: none; border: none; cursor: pointer;
  transition: background 0.12s; white-space: nowrap; flex-shrink: 0;
}
.page-btn-primary:hover { background: #1D4ED8; }

/* ── Stat Grid ─────────────────────────────────────── */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.stat-card {
  background: #fff; border: 1px solid #E8ECF4; border-radius: 16px;
  padding: 22px 20px; display: flex; align-items: center; gap: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: box-shadow 0.15s;
}
.stat-card:hover { box-shadow: 0 4px 16px rgba(37,99,235,0.08); }
.stat-icon-box { width: 46px; height: 46px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-content { flex: 1; }
.stat-label { font-size: 12px; font-weight: 600; color: #6B7280; margin-bottom: 4px; }
.stat-value { font-size: 28px; font-weight: 900; color: #0F172A; line-height: 1.1; letter-spacing: -0.5px; }

/* ── Content Card ──────────────────────────────────── */
.content-card {
  background: #fff; border: 1px solid #E8ECF4; border-radius: 16px;
  padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  display: flex; flex-direction: column; gap: 20px;
}

/* ── Filter Bar ────────────────────────────────────── */
.filter-bar { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding-bottom: 16px; border-bottom: 1px solid #F0F4FF; }
.filter-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
.filter-tab {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;
  background: #F1F5F9; color: #64748B; border: none; cursor: pointer;
  transition: all 0.12s;
}
.filter-tab:hover { background: #E0E8FF; color: #2563EB; }
.filter-tab--active { background: #2563EB; color: #fff; }
.filter-tab-count {
  display: inline-flex; align-items: center; justify-content: center;
  width: 18px; height: 18px; border-radius: 50%; background: rgba(255,255,255,0.25);
  font-size: 10px; font-weight: 700;
}
.filter-tab--active .filter-tab-count { background: rgba(255,255,255,0.3); }
.refresh-btn {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 600; color: #2563EB; background: none; border: none; cursor: pointer;
}
.refresh-btn:hover { text-decoration: underline; }

/* ── Empty / Loading ───────────────────────────────── */
.empty-state { text-align: center; padding: 48px 20px; display: flex; flex-direction: column; align-items: center; gap: 8px; }
.empty-icon { font-size: 36px; }
.empty-title { font-size: 15px; font-weight: 700; color: #0F172A; }
.empty-desc { font-size: 13px; color: #6B7280; max-width: 340px; }
.spinner { width: 32px; height: 32px; border: 3px solid #DBEAFE; border-top-color: #2563EB; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Application Cards ─────────────────────────────── */
.app-list { display: flex; flex-direction: column; gap: 12px; }
.app-card {
  display: flex; align-items: center; gap: 16px;
  padding: 18px 20px; background: #FAFBFF; border: 1px solid #E8ECF4; border-radius: 14px;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.app-card:hover { border-color: #93C5FD; box-shadow: 0 2px 12px rgba(37,99,235,0.07); }
.app-company-icon {
  width: 42px; height: 42px; border-radius: 10px; background: #EFF6FF;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.app-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; }
.app-title-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.app-job-title { font-size: 14px; font-weight: 800; color: #0F172A; }
.app-status-badge { padding: 3px 10px; border-radius: 20px; font-size: 9px; font-weight: 800; letter-spacing: 0.6px; flex-shrink: 0; }
.badge--blue { background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; }
.badge--amber { background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; }
.badge--green { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; }
.badge--purple { background: #F5F3FF; color: #7C3AED; border: 1px solid #DDD6FE; }
.badge--gray { background: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }
.app-org-row { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #6B7280; }
.app-org { font-weight: 700; color: #374151; }
.app-dot { color: #CBD5E1; }
.app-date { color: #9CA3AF; }
.app-skills { display: flex; flex-wrap: wrap; gap: 6px; }
.skill-chip { padding: 3px 10px; background: #fff; border: 1px solid #E5E7EB; border-radius: 6px; font-size: 11px; font-weight: 600; color: #374151; }
.app-actions { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.app-btn-outline {
  padding: 8px 16px; background: #fff; border: 1px solid #E5E7EB; border-radius: 10px;
  font-size: 12px; font-weight: 700; color: #374151; text-decoration: none; white-space: nowrap;
  transition: background 0.12s;
}
.app-btn-outline:hover { background: #F8FAFC; }
.app-btn-primary {
  padding: 8px 16px; background: #2563EB; border-radius: 10px;
  font-size: 12px; font-weight: 700; color: #fff; text-decoration: none; white-space: nowrap;
  transition: background 0.12s;
}
.app-btn-primary:hover { background: #1D4ED8; }

@media (max-width: 900px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  .app-card { flex-wrap: wrap; }
  .app-actions { width: 100%; justify-content: flex-end; }
}
@media (max-width: 560px) {
  .stat-grid { grid-template-columns: 1fr; }
}
</style>
