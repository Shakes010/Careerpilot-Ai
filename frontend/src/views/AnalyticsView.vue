<template>
  <div class="app-page">

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Student Career &amp; Readiness Analytics</h1>
        <p class="page-sub">Deep performance metrics, skill acquisition velocity, and competitive market benchmark percentiles.</p>
      </div>
      <router-link to="/assessments" class="page-btn-primary">
        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
        Boost Score with Assessments
      </router-link>
    </div>

    <!-- Career Readiness Hero Card -->
    <div class="hero-card">
      <!-- Background decoration -->
      <div class="hero-glow hero-glow--1"></div>
      <div class="hero-glow hero-glow--2"></div>

      <div class="hero-content">
        <div class="hero-badges-row">
          <span class="hero-badge">AI READINESS INDEX</span>
          <span class="hero-trend">{{ readinessTrend }}</span>
        </div>
        <h2 class="hero-headline">{{ readinessHeadline }}</h2>
        <p class="hero-desc">{{ readinessDesc }}</p>
      </div>

      <!-- Readiness Dial -->
      <div class="hero-dial-wrap">
        <svg viewBox="0 0 36 36" class="hero-dial-svg">
          <path stroke="rgba(255,255,255,0.2)" stroke-width="3.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
          <path stroke="#fff" :stroke-dasharray="`${readinessScore},100`" stroke-width="3.5" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" style="transform:rotate(-90deg);transform-origin:50% 50%"/>
        </svg>
        <div class="hero-dial-center">
          <span class="hero-dial-value">{{ readinessScore }}%</span>
          <span class="hero-dial-label">READINESS</span>
        </div>
      </div>
    </div>

    <!-- 4 Stat Cards -->
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-label">Verified Skills Count</div>
        <div class="stat-value">{{ verifiedSkillsCount }} Skills</div>
        <div class="stat-trend" :class="verifiedSkillsCount > 0 ? 'stat-trend--green' : ''" :style="{ color: verifiedSkillsCount > 0 ? '#10B981' : '#94A3B8' }">
          {{ verifiedSkillsCount > 0 ? '✓ Cryptographically Verified' : 'Awaiting verification tests' }}
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Skill Trust Score</div>
        <div class="stat-value" :style="{ color: avgTrustScore > 0 ? '#2563EB' : '#94A3B8' }">
          {{ avgTrustScore > 0 ? avgTrustScore + '/100' : '0/100' }}
        </div>
        <div class="stat-trend" :class="avgTrustScore >= 60 ? 'stat-trend--blue' : ''" :style="{ color: avgTrustScore >= 60 ? '#2563EB' : (avgTrustScore > 0 ? '#6B7280' : '#94A3B8') }">
          {{ avgTrustScore >= 60 ? '▲ High Recruiter Confidence' : (avgTrustScore > 0 ? 'Declared Baseline' : 'No skills declared yet') }}
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Opportunity Match Velocity</div>
        <div class="stat-value" :style="{ color: oppMatchVelocity > 0 ? '#7C3AED' : '#94A3B8' }">
          {{ oppMatchVelocity }}% Avg
        </div>
        <div class="stat-trend" style="color:#6B7280;">Across {{ opportunitiesCount }} live postings</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Integrity Trust Rating</div>
        <div class="stat-value" :style="{ color: antiCheatFlags === 0 ? '#10B981' : '#DC2626' }">
          {{ integrityRatingPct }}%
        </div>
        <div class="stat-trend" :class="antiCheatFlags === 0 ? 'stat-trend--green' : ''" :style="{ color: antiCheatFlags === 0 ? '#10B981' : '#DC2626' }">
          {{ antiCheatFlags === 0 ? '0 Anti-Cheat Flags' : antiCheatFlags + ' Anomaly Flags' }}
        </div>
      </div>
    </div>

    <!-- Main Analytics Grid -->
    <div class="analytics-grid">

      <!-- Left: Skill Proficiency -->
      <div class="content-card">
        <div class="card-header">
          <div>
            <h3 class="card-title">Skill Proficiency &amp; Benchmark Breakdown</h3>
            <p class="card-sub">Your verified competencies vs industry cohort average</p>
          </div>
          <router-link to="/skills" class="card-link">Manage Skills →</router-link>
        </div>

        <div class="skills-list">
          <div v-for="sk in studentSkills" :key="sk.id" class="skill-row">
            <div class="skill-meta">
              <div class="skill-name-row">
                <span class="skill-name">{{ sk.skill_name }}</span>
                <span v-if="sk.badge_tier === 'verified'" class="skill-verified">✓ Verified</span>
                <span v-else style="font-size:10px;font-weight:700;color:#64748B;background:#F1F5F9;padding:1px 8px;border-radius:20px;">Declared</span>
              </div>
              <span class="skill-score">{{ sk.trust_score }} / 100</span>
            </div>
            <div class="skill-bar-bg">
              <div
                class="skill-bar-fill"
                :style="`width:${Math.max(sk.trust_score, 8)}%;background:${sk.badge_tier === 'verified' ? '#2563EB' : '#94A3B8'};`"
              ></div>
            </div>
          </div>

          <!-- Placeholder if no skills -->
          <div v-if="!studentSkills.length" class="empty-skills">
            <p style="font-size:13px;color:#64748B;margin-bottom:8px;">No technical skills declared yet for your profile.</p>
            <router-link to="/skills" class="page-btn-primary" style="font-size:12px;padding:8px 16px;">
              + Declare Skills in Passport
            </router-link>
          </div>
        </div>

        <!-- Dynamic AI Recommendation -->
        <div class="ai-callout">
          <div class="ai-callout-icon">💡</div>
          <div class="ai-callout-body">
            <div class="ai-callout-title">{{ aiRecommendation.title }}</div>
            <p class="ai-callout-text">{{ aiRecommendation.text }}</p>
          </div>
        </div>
      </div>

      <!-- Right: Assessment Performance -->
      <div class="content-card">
        <div class="card-header">
          <div>
            <h3 class="card-title">Assessment Performance Metrics</h3>
            <p class="card-sub">Live code execution and checkpoint milestones</p>
          </div>
        </div>

        <div class="perf-list">
          <div class="perf-item">
            <div class="perf-info">
              <div class="perf-label">Automated Test Pass Rate</div>
              <div class="perf-sublabel">Code execution pass percentage</div>
            </div>
            <span class="perf-value" :style="{ color: totalAttempts > 0 ? (testPassRate >= 50 ? '#10B981' : '#D97706') : '#94A3B8' }">
              {{ totalAttempts > 0 ? `${testPassRate}%` : 'N/A (0 Attempts)' }}
            </span>
          </div>

          <div class="perf-item">
            <div class="perf-info">
              <div class="perf-label">Avg Time per Checkpoint</div>
              <div class="perf-sublabel">Sequential checkpoint solve velocity</div>
            </div>
            <span class="perf-value" style="color:#2563EB;">{{ avgTimePerCheckpoint }}</span>
          </div>

          <div class="perf-item">
            <div class="perf-info">
              <div class="perf-label">Behavioral Anti-Cheat Integrity</div>
              <div class="perf-sublabel">Paste event heuristics &amp; tab switches</div>
            </div>
            <span class="perf-value" :style="{ color: antiCheatFlags === 0 ? '#10B981' : '#DC2626' }">
              {{ integrityStatus }}
            </span>
          </div>

          <div class="perf-item">
            <div class="perf-info">
              <div class="perf-label">Verified Career Passport Badges</div>
              <div class="perf-sublabel">Blockchain-ready cryptographic seals</div>
            </div>
            <span class="perf-value" style="color:#7C3AED;">{{ verifiedSkillsCount }} Earned</span>
          </div>
        </div>

        <router-link to="/passport" class="passport-cta">
          View Career Passport &amp; Certs →
        </router-link>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const studentSkills = ref([])
const opportunitiesCount = ref(0)
const oppMatchVelocity = ref(0)
const readinessScore = ref(0)
const readinessHeadline = ref('0% Industry Deployment Ready')
const readinessDesc = ref('Calibrating career profile...')
const readinessTrend = ref('Baseline')
const avgTrustScore = ref(0)
const totalAttempts = ref(0)
const testPassRate = ref(0.0)
const avgTimePerCheckpoint = ref('N/A')
const antiCheatFlags = ref(0)
const integrityRatingPct = ref(100)
const integrityStatus = ref('Optimal (0 Flags)')
const aiRecommendation = ref({
  title: 'Calibrating Recommendations',
  text: 'Analyzing your skill portfolio and job market trends...'
})

onMounted(async () => { await loadAnalyticsData() })

const loadAnalyticsData = async () => {
  try {
    const data = await apiFetch('/profile/student-analytics')
    if (data) {
      readinessScore.value = data.readiness_score || 0
      readinessHeadline.value = data.readiness_headline || `${readinessScore.value}% Industry Deployment Ready`
      readinessDesc.value = data.readiness_description || 'Track your career readiness.'
      readinessTrend.value = data.readiness_trend || 'Baseline'
      studentSkills.value = data.skills || []
      opportunitiesCount.value = data.opportunities_count || 0
      oppMatchVelocity.value = data.opportunity_match_velocity || 0
      avgTrustScore.value = data.avg_trust_score || 0
      totalAttempts.value = data.total_attempts || 0
      testPassRate.value = data.test_pass_rate || 0.0
      avgTimePerCheckpoint.value = data.avg_time_per_checkpoint || 'N/A'
      antiCheatFlags.value = data.anti_cheat_flags || 0
      integrityRatingPct.value = data.integrity_rating_pct ?? 100
      integrityStatus.value = data.integrity_status || 'Optimal (0 Flags)'
      if (data.ai_recommendation) {
        aiRecommendation.value = data.ai_recommendation
      }
    }
  } catch (err) {
    console.error('Failed to load student-analytics:', err)
    // Graceful fallback to passport
    try {
      const passport = await apiFetch('/profile/career-passport')
      studentSkills.value = passport?.skills || []
      const opps = await apiFetch('/opportunities/radar')
      opportunitiesCount.value = (opps || []).length
    } catch (e) {
      console.error(e)
    }
  }
}

const verifiedSkillsCount = computed(() => (studentSkills.value || []).filter(s => s.badge_tier === 'verified').length)
</script>

<style scoped>
/* ── Page Shell ────────────────────────────────────── */
.app-page { display: flex; flex-direction: column; gap: 24px; max-width: 1360px; margin: 0 auto; }

/* ── Header ────────────────────────────────────────── */
.page-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.page-title { font-size: 22px; font-weight: 800; color: #0F172A; letter-spacing: -0.3px; }
.page-sub { font-size: 13px; color: #6B7280; margin-top: 4px; }
.page-btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 20px; background: #2563EB; color: #fff;
  font-size: 13px; font-weight: 700; border-radius: 10px;
  text-decoration: none; border: none; cursor: pointer;
  transition: background 0.12s; flex-shrink: 0; white-space: nowrap;
}
.page-btn-primary:hover { background: #1D4ED8; }

/* ── Hero Card ─────────────────────────────────────── */
.hero-card {
  background: linear-gradient(135deg, #1E40AF 0%, #2563EB 55%, #4F46E5 100%);
  border-radius: 20px; padding: 32px 36px;
  display: flex; align-items: center; justify-content: space-between; gap: 24px;
  position: relative; overflow: hidden;
  box-shadow: 0 8px 32px rgba(37,99,235,0.22);
}
.hero-glow {
  position: absolute; border-radius: 50%;
  pointer-events: none; background: rgba(255,255,255,0.08); filter: blur(40px);
}
.hero-glow--1 { width: 240px; height: 240px; top: -60px; right: -60px; }
.hero-glow--2 { width: 180px; height: 180px; bottom: -40px; right: 28%; }
.hero-content { position: relative; z-index: 1; flex: 1; }
.hero-badges-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.hero-badge {
  padding: 4px 14px; background: rgba(255,255,255,0.18); color: #fff;
  border: 1px solid rgba(255,255,255,0.3); border-radius: 20px;
  font-size: 10px; font-weight: 800; letter-spacing: 0.8px;
}
.hero-trend { font-size: 12px; font-weight: 700; color: #6EE7B7; }
.hero-headline { font-size: 28px; font-weight: 900; color: #fff; letter-spacing: -0.5px; margin-bottom: 10px; }
.hero-desc { font-size: 13px; color: rgba(255,255,255,0.8); max-width: 520px; line-height: 1.6; }
.hero-desc strong { color: #fff; }
.hero-dial-wrap { position: relative; width: 110px; height: 110px; flex-shrink: 0; z-index: 1; display: flex; align-items: center; justify-content: center; }
.hero-dial-svg { width: 110px; height: 110px; }
.hero-dial-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.hero-dial-value { font-size: 22px; font-weight: 900; color: #fff; line-height: 1; }
.hero-dial-label { font-size: 8px; font-weight: 800; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 1px; }

/* ── Stat Grid ─────────────────────────────────────── */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.stat-card {
  background: #fff; border: 1px solid #E8ECF4; border-radius: 16px;
  padding: 20px 22px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  display: flex; flex-direction: column; gap: 6px;
  transition: box-shadow 0.15s;
}
.stat-card:hover { box-shadow: 0 4px 16px rgba(37,99,235,0.08); }
.stat-label { font-size: 12px; font-weight: 600; color: #6B7280; }
.stat-value { font-size: 24px; font-weight: 900; color: #0F172A; letter-spacing: -0.4px; }
.stat-trend { font-size: 11px; font-weight: 700; }
.stat-trend--green { color: #10B981; }
.stat-trend--blue { color: #2563EB; }

/* ── Analytics Grid ────────────────────────────────── */
.analytics-grid { display: grid; grid-template-columns: 7fr 5fr; gap: 20px; }

/* ── Content Card ──────────────────────────────────── */
.content-card {
  background: #fff; border: 1px solid #E8ECF4; border-radius: 16px;
  padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  display: flex; flex-direction: column; gap: 20px;
}
.card-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; padding-bottom: 16px; border-bottom: 1px solid #F0F4FF; }
.card-title { font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 3px; }
.card-sub { font-size: 12px; color: #6B7280; }
.card-link { font-size: 12px; font-weight: 700; color: #2563EB; text-decoration: none; white-space: nowrap; flex-shrink: 0; }
.card-link:hover { text-decoration: underline; }

/* ── Skill List ────────────────────────────────────── */
.skills-list { display: flex; flex-direction: column; gap: 14px; }
.skill-row { display: flex; flex-direction: column; gap: 6px; }
.skill-meta { display: flex; justify-content: space-between; align-items: center; }
.skill-name-row { display: flex; align-items: center; gap: 8px; }
.skill-name { font-size: 13px; font-weight: 700; color: #0F172A; }
.skill-verified { font-size: 10px; font-weight: 800; color: #059669; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 1px 8px; border-radius: 20px; }
.skill-score { font-size: 12px; font-weight: 700; color: #374151; }
.skill-bar-bg { width: 100%; height: 8px; background: #EEF2FF; border-radius: 999px; overflow: hidden; }
.skill-bar-fill { height: 100%; border-radius: 999px; transition: width 0.5s ease; }
.empty-skills { text-align: center; padding: 20px; color: #6B7280; font-size: 13px; display: flex; flex-direction: column; align-items: center; }

/* ── AI Callout ────────────────────────────────────── */
.ai-callout {
  display: flex; align-items: flex-start; gap: 12px;
  background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 12px; padding: 16px;
}
.ai-callout-icon { font-size: 18px; flex-shrink: 0; }
.ai-callout-title { font-size: 13px; font-weight: 700; color: #1E40AF; margin-bottom: 4px; }
.ai-callout-text { font-size: 12px; color: #1E40AF; line-height: 1.6; }

/* ── Performance List ──────────────────────────────── */
.perf-list { display: flex; flex-direction: column; gap: 10px; }
.perf-item {
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  padding: 14px 16px; background: #FAFBFF; border: 1px solid #E8ECF4; border-radius: 12px;
  transition: border-color 0.12s;
}
.perf-item:hover { border-color: #BFDBFE; }
.perf-info { flex: 1; }
.perf-label { font-size: 13px; font-weight: 700; color: #0F172A; }
.perf-sublabel { font-size: 11px; color: #9CA3AF; margin-top: 2px; }
.perf-value { font-size: 14px; font-weight: 900; flex-shrink: 0; }

/* ── Passport CTA ──────────────────────────────────── */
.passport-cta {
  display: flex; align-items: center; justify-content: center;
  padding: 12px; background: #0F172A; color: #fff; border-radius: 12px;
  font-size: 13px; font-weight: 700; text-decoration: none;
  transition: background 0.12s; margin-top: auto;
}
.passport-cta:hover { background: #1E293B; }

@media (max-width: 1080px) {
  .analytics-grid { grid-template-columns: 1fr; }
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .stat-grid { grid-template-columns: 1fr; }
  .hero-card { flex-direction: column; align-items: flex-start; }
}
</style>
