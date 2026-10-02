<template>
  <div class="opp-page">

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
        <h1 class="page-title">AI Opportunity Radar</h1>
        <p class="page-sub">Real-time semantic skill matching via Sentence-Transformers vector embeddings.</p>
      </div>
      <router-link to="/applications" class="btn-header-link">
        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
        </svg>
        <span>View My Applications</span>
      </router-link>
    </div>

    <!-- Stat Metrics Row -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#EFF6FF;">
          <svg width="20" height="20" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="1.8">
            <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Active Opportunities</div>
          <div class="stat-value">{{ opportunities.length }}</div>
          <div class="stat-sub">Across tech cohorts</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#ECFDF5;">
          <svg width="20" height="20" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="1.8">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">High Skill Matches (&gt;60%)</div>
          <div class="stat-value" style="color:#10B981;">{{ highMatchesCount }}</div>
          <div class="stat-sub">Immediate fit</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#F5F3FF;">
          <svg width="20" height="20" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="1.8">
            <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Applied Pipelines</div>
          <div class="stat-value" style="color:#7C3AED;">{{ appliedCount }}</div>
          <div class="stat-sub">In review &amp; interview</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#FFFBEB;">
          <svg width="20" height="20" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="1.8">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Bookmarked Roles</div>
          <div class="stat-value" style="color:#D97706;">{{ bookmarkedCount }}</div>
          <div class="stat-sub">Saved for later</div>
        </div>
      </div>
    </div>

    <!-- Filter & Precision Slider Bar -->
    <div class="filter-card">
      <div class="filter-chips">
        <button
          v-for="chip in filterChips"
          :key="chip.value"
          @click="selectedFilter = chip.value; loadRadar()"
          :class="['filter-chip', selectedFilter === chip.value ? 'filter-chip--active' : '']"
        >
          {{ chip.label }}
        </button>
      </div>

      <div class="slider-group">
        <span class="slider-label">Minimum Match: <strong>{{ minMatchPct }}%</strong></span>
        <input
          type="range"
          min="0"
          max="90"
          step="5"
          v-model.number="minMatchPct"
          @change="loadRadar"
          class="styled-range"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!opportunities.length" class="empty-box">
      <div class="empty-icon-circle">
        <svg width="28" height="28" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
      </div>
      <h3 class="empty-title">No Matching Opportunities Found</h3>
      <p class="empty-desc">Try lowering the Minimum Match threshold or declaring more skills to discover high-relevance roles.</p>
      <button @click="minMatchPct = 0; selectedFilter = ''; loadRadar()" class="btn-reset">
        Reset Match Filters
      </button>
    </div>

    <!-- Opportunity Cards Grid -->
    <div v-else class="opp-grid">
      <div v-for="opp in opportunities" :key="opp.id" class="opp-card">
        
        <!-- Card Top Header -->
        <div class="opp-card-header">
          <div class="opp-company-badge">
            <div class="opp-company-icon">
              <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
                <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
              </svg>
            </div>
            <div>
              <span class="opp-type-pill">{{ opp.opportunity_type.toUpperCase() }}</span>
              <div class="opp-organizer">{{ opp.organizer }}</div>
            </div>
          </div>

          <div class="match-badge" :class="getMatchBadgeClass(opp.match_percentage)">
            <svg width="12" height="12" fill="currentColor" viewBox="0 0 24 24">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            <span>{{ opp.match_percentage }}% Match</span>
          </div>
        </div>

        <!-- Job Title -->
        <div class="opp-title-wrap">
          <h3 class="opp-title">{{ opp.title }}</h3>
          <div class="opp-location-row">
            <span>📍 {{ opp.location || 'Remote / Hybrid' }}</span>
            <span class="opp-sep">•</span>
            <span>💼 Full-Time / Internship</span>
          </div>
        </div>

        <!-- If Student Pro: Full Explainability & Trust Score -->
        <div v-if="authStore.isUserPremium" class="opp-skills-section">
          <div class="skills-block">
            <div class="skills-heading-row">
              <span class="skills-heading">Matched Competencies (AI Explained):</span>
              <span
                class="trust-telemetry-pill"
                :style="{
                  background: opp.is_trust_qualified ? '#ECFDF5' : '#FFFBEB',
                  color: opp.is_trust_qualified ? '#059669' : '#D97706',
                  borderColor: opp.is_trust_qualified ? '#A7F3D0' : '#FDE68A'
                }"
              >
                ⭐ Skill Trust: {{ opp.candidate_trust_score || 0 }}/100 ({{ opp.is_trust_qualified ? 'Verified Fit' : 'Threshold: ' + (opp.min_trust_score_required || 50) + '+' }})
              </span>
            </div>
            <div class="skills-wrap">
              <span
                v-for="m in opp.matched_skills"
                :key="m.skill_name"
                class="skill-chip"
                :class="m.badge_tier === 'verified' ? 'skill-chip--verified' : 'skill-chip--declared'"
              >
                {{ m.badge_tier === 'verified' ? '✓ ' + m.skill_name + ' (' + m.trust_score + ')' : m.skill_name + ' (Declared: ' + m.trust_score + ')' }}
              </span>
            </div>
          </div>

          <div v-if="opp.missing_skills && opp.missing_skills.length" class="skills-block">
            <span class="skills-heading text-muted">Skill Gap Analysis &amp; Recommended Upskills:</span>
            <div class="skills-wrap">
              <span v-for="ms in opp.missing_skills" :key="ms" class="skill-chip skill-chip--missing">
                + {{ ms }}
              </span>
            </div>
          </div>
        </div>

        <!-- If Free Tier: Gated Pro Telemetry Card -->
        <div v-else class="opp-skills-gated">
          <div class="gated-blurred-content">
            <span class="skill-chip skill-chip--blur">Core Competency 1</span>
            <span class="skill-chip skill-chip--blur">API Architecture</span>
            <span class="skill-chip skill-chip--blur">Database Systems</span>
          </div>
          <div class="gated-overlay">
            <div class="gated-info">
              <span class="gated-lock-icon">🔒</span>
              <div>
                <div class="gated-title">Skill Match Explainability &amp; Trust Score</div>
                <div class="gated-desc">Granular competency breakdown and trust score telemetry are Student Pro features.</div>
              </div>
            </div>
            <router-link to="/billing" class="btn-unlock-pro">
              Unlock with Student Pro (₹499) →
            </router-link>
          </div>
        </div>

        <!-- Card Footer Actions -->
        <div class="opp-card-footer">
          <button
            @click="toggleBookmark(opp)"
            class="btn-bookmark"
            :class="{ 'btn-bookmark--active': opp.is_bookmarked }"
          >
            <span>{{ opp.is_bookmarked ? '★ Saved' : '☆ Bookmark' }}</span>
          </button>

          <button
            @click="applyOpportunity(opp)"
            class="btn-apply"
            :disabled="opp.is_applied"
            :class="{ 'btn-apply--applied': opp.is_applied }"
          >
            <span>{{ opp.is_applied ? '✓ Applied' : 'Apply with Passport →' }}</span>
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'
import { useAuthStore } from '../store'

const authStore = useAuthStore()
const opportunities = ref([])
const minMatchPct = ref(0)
const selectedFilter = ref('')
const toast = ref(null)

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

const filterChips = [
  { label: 'All Opportunities', value: '' },
  { label: 'Jobs & Internships', value: 'job' },
  { label: 'Hackathons', value: 'hackathon' },
  { label: 'Research Labs', value: 'research' }
]

const highMatchesCount = computed(() => {
  return opportunities.value.filter(o => (o.match_percentage || 0) >= 60).length
})

const appliedCount = computed(() => {
  return opportunities.value.filter(o => o.is_applied).length
})

const bookmarkedCount = computed(() => {
  return opportunities.value.filter(o => o.is_bookmarked).length
})

onMounted(async () => {
  await loadRadar()
})

const loadRadar = async () => {
  try {
    let url = `/opportunities/radar?min_match_pct=${minMatchPct.value}`
    if (selectedFilter.value) url += `&type_filter=${selectedFilter.value}`
    const data = await apiFetch(url)
    opportunities.value = data || []
  } catch (err) {
    console.error(err)
  }
}

const getMatchBadgeClass = (score = 0) => {
  if (score >= 70) return 'match-badge--green'
  if (score >= 50) return 'match-badge--blue'
  return 'match-badge--amber'
}

const applyOpportunity = async (opp) => {
  try {
    const res = await apiFetch(`/opportunities/${opp.id}/apply`, { method: 'POST' })
    opp.is_applied = true
    showToast(res.message || 'Application submitted successfully!')
  } catch (err) {
    showToast(err.message || 'Application submission failed', 'error')
  }
}

const toggleBookmark = async (opp) => {
  try {
    const res = await apiFetch(`/opportunities/${opp.id}/bookmark`, { method: 'POST' })
    opp.is_bookmarked = res.bookmarked
    showToast(res.bookmarked ? 'Opportunity saved to bookmarks!' : 'Bookmark removed')
  } catch (err) {
    showToast(err.message, 'error')
  }
}
</script>

<style scoped>
/* ─── Page Root ──────────────────────────────────────── */
.opp-page {
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

.btn-header-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 12px;
  font-size: 12.5px;
  font-weight: 700;
  color: #0F172A;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-header-link:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
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

/* ─── Filter & Slider Card ───────────────────────────── */
.filter-card {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 16px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.filter-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-chip {
  padding: 7px 16px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  background: #F1F5F9;
  border: 1px solid transparent;
  color: #475569;
  cursor: pointer;
  transition: all 0.12s ease;
}

.filter-chip:hover {
  background: #E0E7FF;
  color: #2563EB;
}

.filter-chip--active {
  background: #2563EB !important;
  color: #FFFFFF !important;
  font-weight: 700;
}

.slider-group {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 240px;
}

.slider-label {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  white-space: nowrap;
}

.slider-label strong {
  color: #2563EB;
  font-weight: 800;
}

.styled-range {
  width: 120px;
  accent-color: #2563EB;
  cursor: pointer;
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
  max-width: 420px;
  line-height: 1.5;
}

.btn-reset {
  margin-top: 4px;
  padding: 8px 18px;
  background: #EFF6FF;
  border: 1.5px solid #BFDBFE;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  color: #2563EB;
  cursor: pointer;
  transition: all 0.12s;
}

.btn-reset:hover {
  background: #DBEAFE;
}

/* ─── Opportunity Cards Grid ─────────────────────────── */
.opp-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.opp-card {
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

.opp-card:hover {
  border-color: #93C5FD;
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.07);
}

.opp-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.opp-company-badge {
  display: flex;
  align-items: center;
  gap: 12px;
}

.opp-company-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.opp-type-pill {
  font-size: 10px;
  font-weight: 800;
  color: #2563EB;
  letter-spacing: 0.5px;
}

.opp-organizer {
  font-size: 12px;
  font-weight: 700;
  color: #475569;
  margin-top: 1px;
}

.match-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 800;
}

.match-badge--green {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
}

.match-badge--blue {
  background: #EFF6FF;
  color: #2563EB;
  border: 1px solid #BFDBFE;
}

.match-badge--amber {
  background: #FFFBEB;
  color: #D97706;
  border: 1px solid #FDE68A;
}

.opp-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.opp-title {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
  line-height: 1.3;
}

.opp-location-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  color: #64748B;
}

.opp-sep {
  color: #CBD5E1;
}

.opp-skills-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skills-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.skills-heading {
  font-size: 11px;
  font-weight: 700;
  color: #334155;
}

.skills-heading.text-muted {
  color: #94A3B8;
}

.skills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-chip {
  padding: 3px 9px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
}

.skill-chip--verified {
  background: #EFF6FF;
  color: #1D4ED8;
  border: 1px solid #BFDBFE;
}

.skill-chip--declared {
  background: #F1F5F9;
  color: #475569;
  border: 1px solid #E2E8F0;
}

.skill-chip--missing {
  background: #F8FAFC;
  color: #94A3B8;
  border: 1px dashed #CBD5E1;
}

.opp-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 14px;
  border-top: 1px solid #F0F4FF;
}

.btn-bookmark {
  padding: 8px 14px;
  background: #F8FAFC;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.12s ease;
}

.btn-bookmark:hover {
  background: #F1F5F9;
  color: #0F172A;
}

.btn-bookmark--active {
  background: #FFFBEB;
  border-color: #FDE68A;
  color: #D97706;
}

.btn-apply {
  padding: 8px 18px;
  background: #2563EB;
  border: none;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  color: #FFFFFF;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2);
  transition: all 0.12s ease;
}

.btn-apply:hover {
  background: #1D4ED8;
}

.btn-apply--applied {
  background: #ECFDF5 !important;
  color: #059669 !important;
  border: 1px solid #A7F3D0 !important;
  box-shadow: none !important;
  cursor: default;
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
  .opp-grid {
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
}

/* ─── Pro Gating & Trust Telemetry Styling ───────────── */
.skills-heading-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.trust-telemetry-pill {
  font-size: 10px;
  font-weight: 800;
  color: #059669;
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  padding: 2px 8px;
  border-radius: 999px;
  letter-spacing: 0.2px;
}

.opp-skills-gated {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  padding: 16px;
  min-height: 80px;
}

.gated-blurred-content {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  filter: blur(4px);
  user-select: none;
  pointer-events: none;
  opacity: 0.5;
}

.skill-chip--blur {
  background: #E2E8F0;
  color: #64748B;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
}

.gated-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  gap: 12px;
}

.gated-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.gated-lock-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.gated-title {
  font-size: 12px;
  font-weight: 800;
  color: #1E293B;
}

.gated-desc {
  font-size: 11px;
  color: #64748B;
  line-height: 1.3;
}

.btn-unlock-pro {
  font-size: 11px;
  font-weight: 800;
  color: #2563EB;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  padding: 6px 12px;
  border-radius: 8px;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.btn-unlock-pro:hover {
  background: #2563EB;
  color: #FFFFFF;
}
</style>
