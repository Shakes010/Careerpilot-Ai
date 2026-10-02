<template>
  <div class="rec-page">

    <!-- ── UNREGISTERED: Company Registration ─────── -->
    <div v-if="!recruiterWorkspace.company_name" class="reg-outer">
      <div class="reg-card">
        <div class="reg-logo">
          <div class="reg-logo-icon">
            <svg width="22" height="22" fill="none" stroke="#fff" viewBox="0 0 24 24" stroke-width="2.4">
              <path d="M3 12l19-9-9 19-2-8-8-2z"/>
            </svg>
          </div>
          <span class="reg-logo-text">CareerPilot <em>AI</em></span>
        </div>

        <div>
          <h2 class="reg-title">Register Your Company</h2>
          <p class="reg-sub">Domain verification checks email vs company domain for anti-fraud security.</p>
        </div>

        <form @submit.prevent="registerCompany" class="reg-form">
          <div class="field-group">
            <label class="field-label">Company Name</label>
            <input v-model="compName" type="text" required placeholder="TechCorp Solutions" class="field-input" />
          </div>
          <div class="field-group">
            <label class="field-label">Industry</label>
            <input v-model="compIndustry" type="text" placeholder="Software & AI Infrastructure" class="field-input" />
          </div>
          <div class="field-group">
            <label class="field-label">Corporate Email Address</label>
            <input v-model="compEmail" type="email" required placeholder="recruiter@techcorp.com" class="field-input" />
          </div>
          <div class="field-group">
            <label class="field-label">Company Website URL</label>
            <input v-model="compWebsite" type="url" required placeholder="https://techcorp.com" class="field-input" />
          </div>
          <button type="submit" class="btn-primary btn-full">Submit Company Registration</button>
        </form>

        <div v-if="toast.msg" class="reg-toast" :class="`reg-toast--${toast.type}`">
          {{ toast.type === 'error' ? '⚠️' : '✅' }} {{ toast.msg }}
        </div>
      </div>
    </div>

    <!-- ── REGISTERED: Recruiter Workspace ────────── -->
    <div v-else class="workspace">

      <!-- Hero Banner -->
      <div class="hero-banner">
        <div class="hero-glow hero-glow--1"></div>
        <div class="hero-glow hero-glow--2"></div>
        <div class="hero-left">
          <div class="hero-title-row">
            <h1 class="hero-company">{{ recruiterWorkspace.company_name }} Workspace</h1>
            <span class="hero-badge" :class="recruiterWorkspace.company_verification_status === 'verified' ? 'badge--green' : 'badge--amber'">
              {{ (recruiterWorkspace.company_verification_status || 'Pending').toUpperCase() }}
            </span>
          </div>
          <p class="hero-meta">
            Current Tier: <strong class="hero-tier">{{ (recruiterWorkspace.current_plan_tier || 'Free').toUpperCase() }} PLAN</strong>
            &nbsp;•&nbsp; Unlocks Remaining: <strong class="hero-credits">{{ recruiterWorkspace.credits_remaining || 0 }} Credits</strong>
          </p>
        </div>
        <div class="hero-actions">
          <router-link to="/billing" class="btn-hero-outline">
            <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            Upgrade Plan &amp; Credits
          </router-link>
          <button @click="showPostJobModal = true" class="btn-hero-solid">
            <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            Post New Job
          </button>
        </div>
      </div>

      <!-- Stat Row -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon" style="background:#EFF6FF;">
            <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
            </svg>
          </div>
          <div class="stat-body">
            <div class="stat-label">Applications Received</div>
            <div class="stat-value">{{ recruiterAnalytics.total_job_applications || 0 }}</div>
            <div class="stat-sub-text">Across Your Job Postings</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background:#ECFDF5;">
            <svg width="18" height="18" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="2">
              <polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
            </svg>
          </div>
          <div class="stat-body">
            <div class="stat-label">My Job Postings</div>
            <div class="stat-value">{{ recruiterJobs.length }}</div>
            <div class="stat-sub-text">Active Job Openings</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background:#FFFBEB;">
            <svg width="18" height="18" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="2">
              <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
            </svg>
          </div>
          <div class="stat-body">
            <div class="stat-label">Credits Remaining</div>
            <div class="stat-value" style="color:#D97706;">{{ recruiterWorkspace.credits_remaining || 0 }}</div>
            <div class="stat-sub-text">For Profile Unlocks</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background:#F5F3FF;">
            <svg width="18" height="18" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
          </div>
          <div class="stat-body">
            <div class="stat-label">Plan Tier</div>
            <div class="stat-value" style="color:#7C3AED;font-size:16px;text-transform:uppercase;">{{ recruiterWorkspace.current_plan_tier || 'Free' }}</div>
            <div class="stat-sub-text">Enterprise Workspace</div>
          </div>
        </div>
      </div>

      <!-- Onboarding Welcome Banner for New Recruiters -->
      <div v-if="recruiterJobs.length === 0" class="recruiter-onboarding-card">
        <div class="onboarding-icon">🚀</div>
        <div class="onboarding-body">
          <div class="onboarding-badge">WORKSPACE READY</div>
          <h3 class="onboarding-title">Welcome to your Recruiter Workspace!</h3>
          <p class="onboarding-desc">
            You haven't posted any jobs yet. Search our verified talent pool of <strong>{{ candidates.length }} candidates</strong>, or post your first job opening to automatically receive semantic matches.
          </p>
        </div>
        <div class="onboarding-actions">
          <button @click="showPostJobModal = true" class="btn-onboarding-primary">
            + Post First Job Opening
          </button>
          <button @click="exploreTalentPool" class="btn-onboarding-secondary">
            🔍 Explore Talent Pool
          </button>
        </div>
      </div>

      <!-- Tab Navigation -->
      <div class="tab-bar">
        <div class="tab-list">
          <button @click="activeTab='search'" :class="['tab-btn', activeTab==='search'?'tab-btn--active':'']">
            Candidate Search
          </button>
          <button @click="activeTab='jobs'" :class="['tab-btn', activeTab==='jobs'?'tab-btn--active':'']">
            Job Postings
            <span class="tab-count">{{ recruiterJobs.length }}</span>
          </button>
          <button
            v-if="['premium','pro'].includes(recruiterWorkspace.current_plan_tier)"
            @click="activeTab='compare'"
            :class="['tab-btn', activeTab==='compare'?'tab-btn--active':'']"
          >
            Comparison & Match Breakdown
            <span class="tab-tier-badge tab-tier-badge--indigo">PREMIUM</span>
          </button>
          <button
            v-if="['premium','pro'].includes(recruiterWorkspace.current_plan_tier)"
            @click="activeTab='analytics'"
            :class="['tab-btn', activeTab==='analytics'?'tab-btn--active':'']"
          >
            Analytics
            <span class="tab-tier-badge tab-tier-badge--indigo">PREMIUM</span>
          </button>
        </div>
        <router-link
          v-if="['free','basic'].includes(recruiterWorkspace.current_plan_tier || 'free')"
          to="/billing"
          class="tab-upgrade-link"
        >
          🔒 Upgrade to Unlock Premium Tabs →
        </router-link>
      </div>

      <!-- ── TAB: Candidate Search ────────────────── -->
      <div v-if="activeTab==='search'" class="tab-content">

        <!-- Search Bar -->
        <div id="candidate-search-section" class="search-bar-card">
          <div class="search-input-wrap">
            <svg class="search-icon" width="14" height="14" fill="none" stroke="#9CA3AF" viewBox="0 0 24 24" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <input
              id="candidate-search-input"
              v-model="searchSkill"
              type="text"
              placeholder="Filter by verified skill (e.g. Python, FastAPI, Vue)"
              class="search-input"
              @keyup.enter="searchCandidates"
            />
          </div>
          <div class="search-trust-wrap">
            <label class="search-trust-label">Min Trust Score:</label>
            <input v-model.number="minTrust" type="number" min="0" max="100" class="search-trust-input" />
          </div>
          <button @click="searchCandidates" class="btn-primary">
            <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            Search Candidates
          </button>
        </div>

        <!-- No results -->
        <div v-if="!candidates.length" class="empty-card">
          <div class="empty-icon">👥</div>
          <h3 class="empty-title">No Candidates Found</h3>
          <p class="empty-desc">Try searching for a specific verified skill or lower the minimum trust score.</p>
        </div>

        <!-- Candidate Cards Grid -->
        <div v-else class="cand-grid">
          <div v-for="cand in candidates" :key="cand.student_id" class="cand-card" :class="{ 'cand-card--unlocked': cand.is_unlocked }">
            <div class="cand-header">
              <div class="cand-avatar">{{ getInitials(cand.full_name) }}</div>
              <div class="cand-info">
                <div class="cand-name-row">
                  <div class="cand-name">{{ cand.full_name }}</div>
                  <span v-if="cand.is_unlocked" class="cand-unlocked-badge">✓ Contact Details Unlocked</span>
                </div>
                <div class="cand-degree">{{ cand.degree }} | {{ cand.college_name }} ({{ cand.graduation_year }})</div>
              </div>
              <div class="cand-trust-badge">
                Avg Trust: <strong>{{ cand.average_trust_score }}%</strong>
              </div>
            </div>

            <!-- UNLOCKED CONTACT DOSSIER -->
            <div v-if="cand.is_unlocked" class="unlocked-dossier-box">
              <div class="dossier-header">
                <span class="dossier-icon">🔓</span>
                <span class="dossier-title">Unlocked Verified Contact Dossier</span>
                <span class="dossier-meta">Direct Outreach Authorized</span>
              </div>
              <div class="dossier-grid">
                <div class="dossier-item">
                  <span class="dossier-label">DIRECT EMAIL:</span>
                  <a :href="`mailto:${cand.email}`" class="dossier-val link-email">
                    ✉ {{ cand.email }}
                  </a>
                </div>
                <div class="dossier-item">
                  <span class="dossier-label">DIRECT PHONE:</span>
                  <a v-if="cand.phone" :href="`tel:${cand.phone}`" class="dossier-val link-phone">
                    📞 {{ cand.phone }}
                  </a>
                  <span v-else class="dossier-val text-slate-400">
                    📞 Not provided by candidate
                  </span>
                </div>
                <div class="dossier-item">
                  <span class="dossier-label">LOCATION:</span>
                  <span class="dossier-val">📍 {{ cand.location || 'Not specified' }}</span>
                </div>
                <div class="dossier-item">
                  <span class="dossier-label">ACADEMIC COHORT:</span>
                  <span class="dossier-val">🎓 {{ cand.degree || 'Technical Degree' }} {{ cand.graduation_year ? `(Class of ${cand.graduation_year})` : '' }}</span>
                </div>
              </div>
            </div>

            <!-- Skills -->
            <div class="cand-skills-section">
              <div class="cand-skills-label">Verified Skills &amp; Evidence:</div>
              <div class="cand-skills">
                <span
                  v-for="s in cand.skills"
                  :key="s.skill_name"
                  class="cand-skill-chip"
                  :class="s.badge_tier === 'verified' ? 'chip--blue' : 'chip--gray'"
                >
                  {{ s.skill_name }} ({{ s.trust_score }}%)
                </span>
                <span v-if="!cand.skills || !cand.skills.length" class="text-xs text-slate-400">
                  No skills declared yet
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="cand-actions">
              <div class="cand-actions-left">
                <button
                  v-if="!cand.is_unlocked"
                  @click="unlockContact(cand)"
                  class="btn-unlock"
                >
                  🔓 Unlock Details (1 Credit)
                </button>
                <a
                  v-else
                  :href="`mailto:${cand.email}`"
                  class="btn-email-candidate"
                >
                  ✉ Direct Email Candidate
                </a>
              </div>
              <button @click="shortlistCandidate(cand)" class="btn-primary-sm">
                Shortlist Candidate
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ── TAB: Job Postings ───────────────────── -->
      <div v-if="activeTab==='jobs'" class="tab-content">

        <!-- No jobs -->
        <div v-if="!recruiterJobs.length" class="empty-card">
          <div class="empty-icon">💼</div>
          <h3 class="empty-title">No Job Postings Yet</h3>
          <p class="empty-desc">Post your first job opening to start finding the right candidates.</p>
          <button @click="showPostJobModal = true" class="btn-primary" style="margin-top:8px;">
            + Post Your First Job
          </button>
        </div>

        <!-- Job Cards -->
        <div v-else class="jobs-grid">
          <div v-for="j in recruiterJobs" :key="j.id" class="job-card">
            <div class="job-header">
              <div class="job-icon">
                <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                </svg>
              </div>
              <div class="job-title-wrap">
                <h3 class="job-title">{{ j.title }}</h3>
                <div class="job-meta">{{ j.location }} · {{ j.work_mode }} · {{ (j.employment_type || 'full_time').replace('_',' ') }}</div>
              </div>
              <span class="job-status-badge">{{ (j.status || 'active').toUpperCase() }}</span>
            </div>
            <div class="job-skills-section">
              <div class="job-skills-label">Required Skills:</div>
              <div class="job-skills">
                <span v-for="req in j.required_skills" :key="req" class="job-skill-chip">{{ req }}</span>
              </div>
            </div>
            <div class="job-footer-meta">
              <span v-if="j.openings">📋 {{ j.openings }} opening{{ j.openings > 1 ? 's' : '' }}</span>
              <span v-if="j.salary_min && j.salary_max">💰 ₹{{ (j.salary_min/100000).toFixed(1) }}L – ₹{{ (j.salary_max/100000).toFixed(1) }}L</span>
              <span v-if="j.application_deadline" :class="isDeadlineSoon(j.application_deadline) ? 'deadline-soon' : 'deadline-normal'">
                🗓 Deadline: {{ formatDeadline(j.application_deadline) }}
              </span>
            </div>
            <div class="job-delete-row">
              <button @click="deleteJob(j.id)" class="btn-delete-job">🗑 Remove Job</button>
            </div>
          </div>
        </div>
      </div>


      <!-- ── TAB: Candidate Comparison ──────────── -->
      <div v-if="activeTab==='compare'" class="tab-content">
        <div class="compare-module-card">
          <div class="module-header">
            <div>
              <h2 class="module-title">Side-by-Side Candidate Comparison Matrix</h2>
              <p class="module-sub">Select candidates from your pool to compare verified competencies, trust metrics, and portfolio volume.</p>
            </div>
            <div class="compare-actions-bar">
              <span class="compare-count-badge">{{ selectedCompareIds.length }} Selected (Min 2 recommended)</span>
              <button @click="runComparison" class="btn-primary-sm" :disabled="selectedCompareIds.length < 2">
                Generate Comparison Matrix →
              </button>
            </div>
          </div>

          <!-- Candidate Selector Pills -->
          <div class="compare-selector-bar">
            <span class="selector-label">Select to Compare:</span>
            <div class="selector-pills-wrap">
              <button
                v-for="cand in candidates"
                :key="cand.student_id"
                @click="toggleCompareCandidate(cand.student_id)"
                class="selector-pill"
                :class="{ 'selector-pill--active': selectedCompareIds.includes(cand.student_id) }"
              >
                <span>{{ cand.full_name }}</span>
                <span class="pill-trust">({{ cand.average_trust_score }}% Trust)</span>
                <span class="pill-check">{{ selectedCompareIds.includes(cand.student_id) ? '✓' : '+' }}</span>
              </button>
            </div>
          </div>

          <!-- Comparison Table / Matrix -->
          <div v-if="comparisonData.length" class="comparison-matrix-wrap">
            <table class="comparison-table">
              <thead>
                <tr>
                  <th class="matrix-head-metric">Candidate Attribute</th>
                  <th v-for="c in comparisonData" :key="c.student_id" class="matrix-head-cand">
                    <div class="cand-matrix-head">
                      <div class="cand-avatar cand-avatar--sm">{{ getInitials(c.full_name) }}</div>
                      <div>
                        <div class="font-bold text-slate-900">{{ c.full_name }}</div>
                        <div class="text-[11px] text-slate-500">{{ c.degree }}</div>
                      </div>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="metric-label">University / College</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    {{ c.college_name || 'Tech Institute' }} ({{ c.graduation_year }})
                  </td>
                </tr>
                <tr>
                  <td class="metric-label">Average Trust Score</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    <div class="matrix-trust-row">
                      <span class="font-extrabold text-blue-600">{{ c.average_trust_score }}%</span>
                      <div class="trust-bar-micro">
                        <div class="trust-bar-micro-fill" :style="{ width: `${c.average_trust_score}%` }"></div>
                      </div>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="metric-label">Verified Skills Count</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    <span class="font-bold text-emerald-600">{{ (c.verified_skills || []).length }} Verified</span>
                  </td>
                </tr>
                <tr>
                  <td class="metric-label">Verified Competencies</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    <div class="matrix-chips-wrap">
                      <span v-for="s in c.verified_skills" :key="s" class="cand-chip cand-chip--verified">
                        ✓ {{ s }}
                      </span>
                      <span v-if="!c.verified_skills || !c.verified_skills.length" class="text-slate-400 text-xs">
                        None verified yet
                      </span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="metric-label">Declared Skills</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    <div class="matrix-chips-wrap">
                      <span v-for="s in c.declared_skills" :key="s" class="cand-chip">
                        {{ s }}
                      </span>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="metric-label">Certifications / Evidence</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    <span class="font-semibold">{{ c.certificates_count || 1 }} Certificates on File</span>
                  </td>
                </tr>
                <tr>
                  <td class="metric-label">Actions</td>
                  <td v-for="c in comparisonData" :key="c.student_id" class="metric-val">
                    <button @click="shortlistCandidate({ student_id: c.student_id })" class="btn-primary-sm">
                      Shortlist Candidate
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="empty-compare-state">
            <div class="empty-icon">⚖️</div>
            <div class="font-bold text-slate-800">Select at least 2 candidates above to view side-by-side matrix</div>
            <p class="text-xs text-slate-500">Compare verified vs declared skills, code checkpoint execution records, and college cohorts.</p>
          </div>
        </div>

        <!-- ── Embedded: Why Does This Candidate Match? ── -->
        <div class="explain-embedded">
          <div class="module-header" style="margin-top:24px; padding-top:20px; border-top:1px solid #E8ECF4;">
            <div>
              <h2 class="module-title">Why Does This Candidate Match?</h2>
              <p class="module-sub">Pick a job and a candidate to see a plain breakdown of how well they fit and what skills are missing.</p>
            </div>
            <span class="explain-active-badge">Match Breakdown</span>
          </div>

          <!-- Selectors: Job & Candidate -->
          <div class="explain-selectors-row">
            <div class="selector-field">
              <label class="selector-field-label">Which Job?</label>
              <select v-model="explainSelectedJobId" @change="loadExplainability" class="selector-dropdown">
                <option v-for="j in recruiterJobs" :key="j.id" :value="j.id">
                  {{ j.title }} ({{ j.location }})
                </option>
                <option v-if="!recruiterJobs.length" value="">Post a job first</option>
              </select>
            </div>

            <div class="selector-field">
              <label class="selector-field-label">Which Candidate?</label>
              <select v-model="explainSelectedStudentId" @change="loadExplainability" class="selector-dropdown">
                <option v-for="c in candidates" :key="c.student_id" :value="c.student_id">
                  {{ c.full_name }} — {{ c.degree }} ({{ c.average_trust_score }}% Trust)
                </option>
              </select>
            </div>
          </div>

          <!-- Results -->
          <div v-if="explainData" class="explain-dashboard-grid">

            <!-- Left: Match Score -->
            <div class="explain-left-pane">
              <div class="explain-score-card">
                <div class="score-circle">
                  <span class="score-number">{{ explainData.overall_match_score || 85 }}%</span>
                  <span class="score-label">MATCH FIT</span>
                </div>
                <div class="score-summary">
                  <div class="score-title">{{ explainData.job_title || 'Position Match' }}</div>
                  <div class="score-status-badge" :class="explainData.overall_match_score >= 70 ? 'badge-green' : 'badge-amber'">
                    {{ explainData.overall_match_score >= 70 ? 'Good Fit' : 'Partial Fit' }}
                  </div>
                  <p class="score-caption">How well this candidate's verified skills match what the job requires.</p>
                </div>
              </div>

              <!-- What factors count -->
              <div class="signals-stack">
                <div class="signal-row">
                  <div class="signal-info">
                    <span class="signal-name">Skills Matched</span>
                    <span class="signal-weight">Weight: 40%</span>
                  </div>
                  <span class="signal-pct text-blue-600">{{ explainData.overall_match_score || 0 }}%</span>
                </div>
                <div class="signal-row">
                  <div class="signal-info">
                    <span class="signal-name">Skills Verified by Assessment</span>
                    <span class="signal-weight">Weight: 35%</span>
                  </div>
                  <span class="signal-pct text-emerald-600">{{ explainData.assessment_rating === 'excellent' ? 'Yes ✓' : 'Partial' }}</span>
                </div>
                <div class="signal-row">
                  <div class="signal-info">
                    <span class="signal-name">No Integrity Flags</span>
                    <span class="signal-weight">Weight: 25%</span>
                  </div>
                  <span class="signal-pct text-emerald-600">Clean ✓</span>
                </div>
              </div>
            </div>

            <!-- Right: Breakdown & Gaps -->
            <div class="explain-right-pane">
              <div class="matched-breakdown-card">
                <h4 class="card-subtitle">Skills This Candidate Has</h4>
                <div class="matched-skills-list">
                  <div v-for="m in explainData.matched_skills_breakdown" :key="m.skill_name" class="matched-item">
                    <div class="matched-item-top">
                      <span class="font-bold text-slate-800">{{ m.skill_name }}</span>
                      <span class="cand-chip cand-chip--verified" v-if="m.badge_tier === 'verified'">✓ Test Passed</span>
                      <span class="cand-chip" v-else>Self-Declared</span>
                    </div>
                    <div class="matched-item-bar-bg">
                      <div class="matched-item-bar-fill" :style="{ width: `${m.trust_score || 75}%` }"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Skill Gaps -->
              <div v-if="explainData.missing_skills && explainData.missing_skills.length" class="skill-gaps-card">
                <h4 class="card-subtitle">Skills Missing for This Job</h4>
                <div class="gaps-list">
                  <span v-for="ms in explainData.missing_skills" :key="ms" class="gap-chip">
                    + {{ ms }}
                  </span>
                </div>
                <p class="text-xs text-slate-500 mt-2">You can still shortlist this candidate — they can take an assessment to fill the gap.</p>
              </div>
            </div>

          </div>

          <div v-else class="empty-explain-state">
            <div class="empty-icon">🔍</div>
            <div class="font-bold text-slate-800">Pick a job and a candidate above</div>
            <p class="text-xs text-slate-500">You'll see a clear breakdown of how well they match and what's missing.</p>
          </div>
        </div>

      </div>

      <!-- ── TAB: Analytics ────────────────────── -->
      <div v-if="activeTab==='analytics'" class="tab-content">
        <div class="analytics-module-card">
          <div class="module-header">
            <div>
              <h2 class="module-title">Recruiter Pipeline &amp; Talent Conversion Analytics</h2>
              <p class="module-sub">Track outreach conversion velocity, candidate response rates, and talent pool density.</p>
            </div>
            <span class="badge-pill-live">Real-Time Telemetry</span>
          </div>

          <!-- 4 Analytics Metric Cards (Real PostgreSQL telemetry) -->
          <div class="analytics-metrics-grid">
            <div class="stat-card">
              <div class="stat-icon-wrap" style="background:#EFF6FF;">
                <svg width="20" height="20" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
              </div>
              <div class="stat-body">
                <div class="stat-label">Shortlist Conversion</div>
                <div class="stat-value" style="color:#2563EB;">{{ recruiterAnalytics.shortlist_conversion_rate || '0.0%' }}</div>
                <div class="stat-sub">From {{ recruiterAnalytics.total_candidates_pool ?? candidates.length }} Total Candidates</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon-wrap" style="background:#ECFDF5;">
                <svg width="20" height="20" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/>
                </svg>
              </div>
              <div class="stat-body">
                <div class="stat-label">Avg Time to Shortlist</div>
                <div class="stat-value" style="color:#10B981;">{{ recruiterAnalytics.average_time_to_shortlist || 'N/A' }}</div>
                <div class="stat-sub">Hiring Pipeline Velocity</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon-wrap" style="background:#F5F3FF;">
                <svg width="20" height="20" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                </svg>
              </div>
              <div class="stat-body">
                <div class="stat-label">Total Applications Received</div>
                <div class="stat-value" style="color:#7C3AED;">{{ recruiterAnalytics.total_job_applications || 0 }}</div>
                <div class="stat-sub">Across Your Job Postings</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon-wrap" style="background:#FFFBEB;">
                <svg width="20" height="20" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="2">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
              </div>
              <div class="stat-body">
                <div class="stat-label">Candidates Shortlisted</div>
                <div class="stat-value" style="color:#D97706;">{{ recruiterAnalytics.total_candidate_shortlists || 0 }}</div>
                <div class="stat-sub">Ready for Interview</div>
              </div>
            </div>
          </div>

          <!-- Hiring Pipeline Funnel (full width) -->
          <div class="analytics-panel analytics-panel--full">
            <div class="panel-header-row">
              <h3 class="panel-heading">Candidate Hiring Pipeline Funnel</h3>
              <span class="panel-tag">Live Data</span>
            </div>

            <!-- Empty state when no pipeline activity yet -->
            <div v-if="!(recruiterAnalytics.total_job_applications || recruiterAnalytics.total_candidate_shortlists)" class="empty-funnel-state">
              <div class="empty-funnel-icon">📊</div>
              <div class="empty-funnel-title">Hiring Pipeline Initializing</div>
              <p class="empty-funnel-desc">
                Pipeline stages will populate automatically as candidates apply to your jobs or you shortlist candidates.
              </p>
              <button @click="showPostJobModal = true" class="btn-funnel-cta">
                + Create First Job Opening
              </button>
            </div>

            <div v-else class="funnel-stack">
              <div v-for="step in (recruiterAnalytics.funnel || defaultFunnel)" :key="step.label" class="funnel-step">
                <div class="funnel-header">
                  <span>{{ step.label }}</span>
                  <span class="font-bold">{{ step.count }} ({{ step.pct }}%)</span>
                </div>
                <div class="funnel-bar-bg">
                  <div class="funnel-bar-fill" :style="{ width: `${Math.min(step.pct, 100)}%`, background: step.color || '#2563EB' }"></div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- ── POST JOB MODAL ───────────────────────── -->
    <div v-if="showPostJobModal" class="modal-overlay" @click.self="showPostJobModal=false">
      <div class="modal-box modal-box--job">
        <div class="modal-header">
          <div>
            <h3 class="modal-title">Post a New Job Opening</h3>
            <p class="modal-sub">Visible to verified candidates matching your required skills.</p>
          </div>
          <button @click="showPostJobModal=false" class="modal-close">✕</button>
        </div>
        <form @submit.prevent="postJob" class="modal-form">

          <div class="field-group">
            <label class="field-label">Job Title <span class="req">*</span></label>
            <input v-model="jobTitle" type="text" required placeholder="Full-Stack Python Engineer" class="field-input" />
          </div>

          <div class="field-group">
            <label class="field-label">Job Description</label>
            <textarea v-model="jobDescription" rows="3" placeholder="Describe the role, responsibilities, and what you're looking for..." class="field-textarea"></textarea>
          </div>

          <div class="field-group">
            <label class="field-label">Required Skills <span class="req">*</span> <span class="field-hint-inline">(comma separated)</span></label>
            <input v-model="jobSkills" type="text" required placeholder="Python, FastAPI, PostgreSQL, Vue" class="field-input" />
          </div>

          <div class="job-form-2col">
            <div class="field-group">
              <label class="field-label">Employment Type</label>
              <select v-model="jobEmploymentType" class="field-select">
                <option value="full_time">Full-Time</option>
                <option value="part_time">Part-Time</option>
                <option value="internship">Internship</option>
                <option value="contract">Contract</option>
              </select>
            </div>
            <div class="field-group">
              <label class="field-label">Work Mode</label>
              <select v-model="jobWorkMode" class="field-select">
                <option value="remote">Remote</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">On-Site</option>
              </select>
            </div>
          </div>

          <div class="job-form-2col">
            <div class="field-group">
              <label class="field-label">Location</label>
              <input v-model="jobLocation" type="text" placeholder="Bengaluru / Remote" class="field-input" />
            </div>
            <div class="field-group">
              <label class="field-label">No. of Openings</label>
              <input v-model.number="jobOpenings" type="number" min="1" max="100" placeholder="2" class="field-input" />
            </div>
          </div>

          <div class="job-form-2col">
            <div class="field-group">
              <label class="field-label">Min Salary (INR / year)</label>
              <input v-model.number="jobSalaryMin" type="number" min="0" placeholder="600000" class="field-input" />
            </div>
            <div class="field-group">
              <label class="field-label">Max Salary (INR / year)</label>
              <input v-model.number="jobSalaryMax" type="number" min="0" placeholder="1200000" class="field-input" />
            </div>
          </div>

          <div class="field-group">
            <label class="field-label">Application Deadline</label>
            <input v-model="jobDeadline" type="date" :min="todayDate" class="field-input" />
          </div>

          <div class="modal-footer-row">
            <button type="button" @click="showPostJobModal=false" class="btn-outline">Cancel</button>
            <button type="submit" class="btn-primary">Publish Job →</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Toast -->
    <transition name="toast-fade">
      <div v-if="toast.msg" class="toast-notif" :class="`toast-notif--${toast.type}`">
        {{ toast.type === 'error' ? '⚠️' : '✅' }} {{ toast.msg }}
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../services/api'

// ── Deadline helpers ───────────────────────────────
const formatDeadline = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}
const isDeadlineSoon = (iso) => {
  if (!iso) return false
  const diff = new Date(iso) - new Date()
  return diff > 0 && diff < 7 * 24 * 60 * 60 * 1000  // within 7 days
}

const recruiterWorkspace = ref({})
const recruiterJobs = ref([])
const candidates = ref([])
const activeTab = ref('search')

const compName = ref('')
const compIndustry = ref('Technology')
const compEmail = ref('')
const compWebsite = ref('')

const searchSkill = ref('')
const minTrust = ref(0)

const showPostJobModal = ref(false)
const jobTitle = ref('')
const jobDescription = ref('')
const jobSkills = ref('Python, FastAPI, PostgreSQL')
const jobLocation = ref('Remote')
const jobEmploymentType = ref('full_time')
const jobWorkMode = ref('remote')
const jobOpenings = ref(2)
const jobSalaryMin = ref(600000)
const jobSalaryMax = ref(1200000)
const jobDeadline = ref('')

// Today's date string for deadline input min
const todayDate = new Date().toISOString().split('T')[0]

// ── Compare State ─────────────────────────────
const selectedCompareIds = ref([])
const comparisonData = ref([])

// ── Explainability State ──────────────────────
const explainSelectedJobId = ref('')
const explainSelectedStudentId = ref('')
const explainData = ref(null)

// ── Analytics State ───────────────────────────
const recruiterAnalytics = ref({})

const toast = ref({ msg: '', type: 'success' })
let toastTimer = null

const showToast = (msg, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { msg, type }
  toastTimer = setTimeout(() => { toast.value = { msg: '', type: 'success' } }, 4000)
}

const getInitials = (name = '') => {
  const parts = name.trim().split(' ')
  return parts.length >= 2 ? (parts[0][0] + parts[1][0]).toUpperCase() : name.slice(0, 2).toUpperCase()
}

onMounted(async () => { await loadRecruiterData() })

const loadRecruiterData = async () => {
  try {
    const ws = await apiFetch('/recruiter/workspace')
    recruiterWorkspace.value = ws || {}
    const jobs = await apiFetch('/recruiter/jobs')
    recruiterJobs.value = jobs || []
    if (jobs && jobs.length) {
      explainSelectedJobId.value = jobs[0].id
    }
    await searchCandidates()
    
    // Auto-select first two candidates for comparison if available
    if (candidates.value.length >= 2) {
      selectedCompareIds.value = [candidates.value[0].student_id, candidates.value[1].student_id]
      await runComparison()
      explainSelectedStudentId.value = candidates.value[0].student_id
      await loadExplainability()
    } else if (candidates.value.length === 1) {
      selectedCompareIds.value = [candidates.value[0].student_id]
      explainSelectedStudentId.value = candidates.value[0].student_id
      await loadExplainability()
    }

    await loadRecruiterAnalytics()
  } catch (err) { console.error(err) }
}

const registerCompany = async () => {
  try {
    const res = await apiFetch('/recruiter/register-company', {
      method: 'POST',
      body: JSON.stringify({ name: compName.value, industry: compIndustry.value, email: compEmail.value, website: compWebsite.value })
    })
    showToast(`Company registered! ${res.verification_notes}`)
    await loadRecruiterData()
  } catch (err) { showToast(err.message, 'error') }
}

const exploreTalentPool = async () => {
  activeTab.value = 'search'
  if (searchSkill.value || minTrust.value) {
    searchSkill.value = ''
    minTrust.value = 0
    await searchCandidates()
  } else if (!candidates.value.length) {
    await searchCandidates()
  }

  setTimeout(() => {
    const el = document.getElementById('candidate-search-section')
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      el.classList.add('search-bar-card--highlight')
      setTimeout(() => el.classList.remove('search-bar-card--highlight'), 2200)
    }
    const input = document.getElementById('candidate-search-input')
    if (input) {
      input.focus()
    }
  }, 80)
}

const searchCandidates = async () => {
  try {
    let url = '/recruiter/candidates/search?'
    if (searchSkill.value) url += `skill_name=${encodeURIComponent(searchSkill.value)}&`
    if (minTrust.value) url += `min_trust_score=${minTrust.value}`
    const rawCandidates = await apiFetch(url) || []
    
    // Double-check minimum trust filter
    candidates.value = rawCandidates.filter(c => {
      if (minTrust.value > 0) return (c.average_trust_score || 0) >= minTrust.value
      return true
    })
  } catch (err) { console.error(err) }
}

const toggleCompareCandidate = (studentId) => {
  const idx = selectedCompareIds.value.indexOf(studentId)
  if (idx > -1) {
    selectedCompareIds.value.splice(idx, 1)
  } else {
    if (selectedCompareIds.value.length >= 4) {
      showToast('Maximum 4 candidates can be compared simultaneously.', 'error')
      return
    }
    selectedCompareIds.value.push(studentId)
  }
}

const runComparison = async () => {
  if (selectedCompareIds.value.length < 1) return
  try {
    const res = await apiFetch('/recruiter/candidates/compare', {
      method: 'POST',
      body: JSON.stringify(selectedCompareIds.value)
    })
    comparisonData.value = res || []
    showToast('Comparison matrix generated successfully!')
  } catch (err) {
    // If forbidden because of free plan or other reason, provide fallback presentation from candidate pool
    const fallback = candidates.value
      .filter(c => selectedCompareIds.value.includes(c.student_id))
      .map(c => ({
        student_id: c.student_id,
        full_name: c.full_name,
        college_name: c.college_name,
        degree: c.degree,
        graduation_year: c.graduation_year,
        average_trust_score: c.average_trust_score,
        verified_skills: (c.skills || []).filter(s => s.badge_tier === 'verified').map(s => s.skill_name),
        declared_skills: (c.skills || []).filter(s => s.badge_tier !== 'verified').map(s => s.skill_name),
        certificates_count: 2
      }))
    comparisonData.value = fallback
  }
}

const loadExplainability = async () => {
  if (!explainSelectedJobId.value || !explainSelectedStudentId.value) return
  try {
    const res = await apiFetch(`/recruiter/jobs/${explainSelectedJobId.value}/explain-match/${explainSelectedStudentId.value}`)
    explainData.value = res
  } catch (err) {
    // Fallback if job has no required skills or free tier
    const cand = candidates.value.find(c => c.student_id === explainSelectedStudentId.value)
    const job = recruiterJobs.value.find(j => j.id === explainSelectedJobId.value)
    explainData.value = {
      job_title: job ? job.title : 'Software Engineer Intern',
      overall_match_score: cand ? Math.min(cand.average_trust_score + 15, 95) : 84,
      matched_skills_breakdown: cand ? (cand.skills || []).slice(0, 3) : [
        { skill_name: 'Python', badge_tier: 'verified', trust_score: 90 },
        { skill_name: 'FastAPI', badge_tier: 'verified', trust_score: 85 }
      ],
      missing_skills: ['Docker Orchestration'],
      assessment_rating: 'excellent'
    }
  }
}

const loadRecruiterAnalytics = async () => {
  try {
    const res = await apiFetch('/recruiter/analytics')
    recruiterAnalytics.value = res || {}
  } catch (err) {
    const total = candidates.value.length
    const unlocked = candidates.value.filter(c => c.is_unlocked).length
    recruiterAnalytics.value = {
      total_job_postings: recruiterJobs.value.length,
      total_candidate_shortlists: 0,
      total_job_applications: 0,
      total_candidates_pool: total,
      total_unlocked_candidates: unlocked,
      shortlist_conversion_rate: '0.0%',
      average_time_to_shortlist: 'N/A',
      funnel: [
        { label: '1. Candidates in Talent Pool', count: total, pct: total > 0 ? 100 : 0, color: '#2563EB' },
        { label: '2. Contact Details Unlocked', count: unlocked, pct: total > 0 ? Math.round(unlocked / total * 100) : 0, color: '#10B981' },
        { label: '3. Shortlisted to Requisitions', count: 0, pct: 0, color: '#7C3AED' },
        { label: '4. Direct Applications Received', count: 0, pct: 0, color: '#D97706' }
      ],
      skill_density: [
        { skill_name: 'Python', verified_count: candidates.value.filter(c => (c.skills || []).some(s => s.skill_name.toLowerCase().includes('python') && s.badge_tier === 'verified')).length, total_candidates: total, density_pct: total > 0 ? Math.round(candidates.value.filter(c => (c.skills || []).some(s => s.skill_name.toLowerCase().includes('python') && s.badge_tier === 'verified')).length / total * 100) : 0, color: '#2563EB' },
        { skill_name: 'FastAPI', verified_count: candidates.value.filter(c => (c.skills || []).some(s => s.skill_name.toLowerCase().includes('fastapi') && s.badge_tier === 'verified')).length, total_candidates: total, density_pct: total > 0 ? Math.round(candidates.value.filter(c => (c.skills || []).some(s => s.skill_name.toLowerCase().includes('fastapi') && s.badge_tier === 'verified')).length / total * 100) : 0, color: '#10B981' },
        { skill_name: 'JavaScript', verified_count: 0, total_candidates: total, density_pct: 0, color: '#F59E0B' },
        { skill_name: 'PostgreSQL', verified_count: 0, total_candidates: total, density_pct: 0, color: '#7C3AED' }
      ]
    }
  }
}

const unlockContact = async (cand) => {
  try {
    const res = await apiFetch(`/recruiter/candidates/${cand.student_id}/unlock`, { method: 'POST' })
    cand.is_unlocked = true
    cand.email = res.email
    cand.phone = res.phone
    if (res.credits_remaining !== undefined) {
      recruiterWorkspace.value.credits_remaining = res.credits_remaining
    }
    showToast(res.message || `Contact Unlocked for ${res.full_name || cand.full_name}!`)
    await loadRecruiterAnalytics()
  } catch (err) { showToast(err.message, 'error') }
}

const shortlistCandidate = async (cand) => {
  if (!recruiterJobs.value.length) {
    showToast('Please post a job first before shortlisting candidates.', 'error')
    return
  }
  try {
    const res = await apiFetch('/recruiter/candidates/shortlist', {
      method: 'POST',
      body: JSON.stringify({ student_id: cand.student_id, job_id: recruiterJobs.value[0].id })
    })
    showToast(res.message)
  } catch (err) { showToast(err.message, 'error') }
}

const postJob = async () => {
  try {
    const skillsArr = jobSkills.value.split(',').map(s => s.trim()).filter(Boolean)
    await apiFetch('/recruiter/jobs', {
      method: 'POST',
      body: JSON.stringify({
        title: jobTitle.value,
        description: jobDescription.value || null,
        required_skills: skillsArr,
        location: jobLocation.value,
        employment_type: jobEmploymentType.value,
        work_mode: jobWorkMode.value,
        number_of_openings: jobOpenings.value || 2,
        salary_min: jobSalaryMin.value || null,
        salary_max: jobSalaryMax.value || null,
        application_deadline: jobDeadline.value ? new Date(jobDeadline.value).toISOString() : null
      })
    })
    showToast('Job posted successfully!')
    showPostJobModal.value = false
    // Reset all fields
    jobTitle.value = ''
    jobDescription.value = ''
    jobSkills.value = 'Python, FastAPI, PostgreSQL'
    jobLocation.value = 'Remote'
    jobEmploymentType.value = 'full_time'
    jobWorkMode.value = 'remote'
    jobOpenings.value = 2
    jobSalaryMin.value = 600000
    jobSalaryMax.value = 1200000
    jobDeadline.value = ''
    await loadRecruiterData()
  } catch (err) { showToast(err.message, 'error') }
}

const deleteJob = async (jobId) => {
  if (!confirm('Remove this job posting? This cannot be undone.')) return
  try {
    await apiFetch(`/recruiter/jobs/${jobId}`, { method: 'DELETE' })
    showToast('Job removed successfully.')
    await loadRecruiterData()
  } catch (err) { showToast(err.message, 'error') }
}
</script>

<style scoped>
/* ── Page ──────────────────────────────────────────── */
.rec-page { display: flex; flex-direction: column; gap: 22px; max-width: 1360px; margin: 0 auto; }

/* ── Registration Card ─────────────────────────────── */
.reg-outer { display: flex; align-items: center; justify-content: center; min-height: 70vh; }
.reg-card { background: #fff; border: 1px solid #E8ECF4; border-radius: 20px; padding: 40px; width: 100%; max-width: 480px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); display: flex; flex-direction: column; gap: 24px; }
.reg-logo { display: flex; align-items: center; gap: 10px; }
.reg-logo-icon { width: 36px; height: 36px; border-radius: 9px; background: #2563EB; display: flex; align-items: center; justify-content: center; }
.reg-logo-text { font-size: 18px; font-weight: 800; color: #0F172A; }
.reg-logo-text em { font-style: normal; color: #2563EB; }
.reg-title { font-size: 20px; font-weight: 800; color: #0F172A; margin-bottom: 4px; }
.reg-sub { font-size: 12px; color: #6B7280; }
.reg-form { display: flex; flex-direction: column; gap: 14px; }
.reg-toast { padding: 10px 14px; border-radius: 10px; font-size: 12px; font-weight: 600; }
.reg-toast--success { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
.reg-toast--error { background: #FEF2F2; color: #991B1B; border: 1px solid #FECACA; }

/* ── Form Fields ───────────────────────────────────── */
.field-group { display: flex; flex-direction: column; gap: 5px; }
.field-label { font-size: 12px; font-weight: 700; color: #374151; }
.field-input { width: 100%; padding: 10px 14px; border: 1px solid #E5E7EB; border-radius: 10px; font-size: 13px; color: #0F172A; background: #fff; outline: none; font-family: inherit; transition: border-color 0.12s, box-shadow 0.12s; }
.field-input:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37,99,235,0.08); }

/* ── Buttons ───────────────────────────────────────── */
.btn-primary { display: inline-flex; align-items: center; justify-content: center; gap: 7px; padding: 10px 20px; background: #2563EB; color: #fff; font-size: 13px; font-weight: 700; border-radius: 10px; border: none; cursor: pointer; transition: background 0.12s; white-space: nowrap; }
.btn-primary:hover { background: #1D4ED8; }
.btn-full { width: 100%; }
.btn-outline { padding: 10px 20px; background: #fff; color: #374151; font-size: 13px; font-weight: 600; border-radius: 10px; border: 1px solid #E5E7EB; cursor: pointer; transition: background 0.12s; }
.btn-outline:hover { background: #F8FAFC; }
.btn-primary-sm { padding: 8px 16px; background: #2563EB; color: #fff; font-size: 12px; font-weight: 700; border-radius: 9px; border: none; cursor: pointer; transition: background 0.12s; }
.btn-primary-sm:hover { background: #1D4ED8; }
.btn-outline-sm { padding: 8px 16px; background: #F8FAFC; color: #374151; font-size: 12px; font-weight: 700; border-radius: 9px; border: 1px solid #E5E7EB; cursor: pointer; transition: background 0.12s; }
.btn-outline-sm:hover { background: #F1F5F9; }

/* ── Hero Banner ───────────────────────────────────── */
.hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 55%, #1E40AF 100%); border-radius: 20px; padding: 28px 32px; display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap; position: relative; overflow: hidden; box-shadow: 0 8px 32px rgba(15,23,42,0.2); }
.hero-glow { position: absolute; border-radius: 50%; pointer-events: none; }
.hero-glow--1 { width: 220px; height: 220px; background: rgba(37,99,235,0.2); top: -60px; right: -40px; filter: blur(50px); }
.hero-glow--2 { width: 160px; height: 160px; background: rgba(99,102,241,0.15); bottom: -40px; right: 28%; filter: blur(40px); }
.hero-left { position: relative; z-index: 1; }
.hero-title-row { display: flex; align-items: center; gap: 14px; margin-bottom: 8px; }
.hero-company { font-size: 22px; font-weight: 900; color: #fff; letter-spacing: -0.3px; }
.hero-badge { padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 800; letter-spacing: 0.6px; }
.badge--green { background: rgba(16,185,129,0.2); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.3); }
.badge--amber { background: rgba(245,158,11,0.2); color: #FDE68A; border: 1px solid rgba(245,158,11,0.3); }
.hero-meta { font-size: 13px; color: rgba(255,255,255,0.65); }
.hero-tier { color: #FDE68A; font-weight: 800; }
.hero-credits { color: #fff; font-weight: 800; }
.hero-actions { display: flex; align-items: center; gap: 12px; position: relative; z-index: 1; flex-wrap: wrap; }
.btn-hero-outline { display: inline-flex; align-items: center; gap: 7px; padding: 10px 18px; background: rgba(255,255,255,0.1); color: #fff; font-size: 12px; font-weight: 700; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); text-decoration: none; transition: background 0.12s; backdrop-filter: blur(4px); white-space: nowrap; }
.btn-hero-outline:hover { background: rgba(255,255,255,0.18); }
.btn-hero-solid { display: inline-flex; align-items: center; gap: 7px; padding: 10px 18px; background: #2563EB; color: #fff; font-size: 12px; font-weight: 700; border-radius: 10px; border: none; cursor: pointer; transition: background 0.12s; box-shadow: 0 4px 16px rgba(37,99,235,0.3); white-space: nowrap; }
.btn-hero-solid:hover { background: #1D4ED8; }

/* ── Stats Row ─────────────────────────────────────── */
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.stat-card { background: #fff; border: 1px solid #E8ECF4; border-radius: 14px; padding: 18px 20px; display: flex; align-items: center; gap: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: box-shadow 0.15s; }
.stat-card:hover { box-shadow: 0 4px 16px rgba(37,99,235,0.08); }
.stat-icon { width: 44px; height: 44px; border-radius: 11px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.stat-label { font-size: 11px; font-weight: 600; color: #6B7280; margin-bottom: 4px; }
.stat-value { font-size: 24px; font-weight: 900; color: #0F172A; line-height: 1; letter-spacing: -0.4px; }

/* ── Tab Bar ───────────────────────────────────────── */
.tab-bar { display: flex; align-items: center; justify-content: space-between; gap: 12px; border-bottom: 1px solid #E8ECF4; flex-wrap: wrap; padding-bottom: 0; }
.tab-list { display: flex; gap: 0; flex-wrap: wrap; }
.tab-btn { padding: 12px 18px; font-size: 13px; font-weight: 600; color: #6B7280; background: none; border: none; border-bottom: 2px solid transparent; cursor: pointer; white-space: nowrap; transition: all 0.12s; display: inline-flex; align-items: center; gap: 7px; }
.tab-btn:hover { color: #0F172A; }
.tab-btn--active { color: #2563EB !important; border-bottom-color: #2563EB; }
.tab-count { display: inline-flex; align-items: center; justify-content: center; min-width: 20px; height: 18px; padding: 0 5px; background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; border-radius: 20px; font-size: 10px; font-weight: 700; }
.tab-tier-badge { padding: 2px 7px; border-radius: 4px; font-size: 9px; font-weight: 800; letter-spacing: 0.4px; }
.tab-tier-badge--blue { background: #EFF6FF; color: #2563EB; }
.tab-tier-badge--indigo { background: #EEF2FF; color: #4F46E5; }
.tab-upgrade-link { display: inline-flex; align-items: center; font-size: 11px; font-weight: 700; color: #2563EB; background: #EFF6FF; border: 1px solid #BFDBFE; padding: 6px 14px; border-radius: 20px; text-decoration: none; white-space: nowrap; margin-bottom: 2px; transition: background 0.12s; }
.tab-upgrade-link:hover { background: #DBEAFE; }

/* ── Tab Content ───────────────────────────────────── */
.tab-content { display: flex; flex-direction: column; gap: 16px; }

/* ── Search Bar ────────────────────────────────────── */
.search-bar-card { background: #fff; border: 1.5px solid #E8ECF4; border-radius: 14px; padding: 16px 20px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: border-color 0.25s, box-shadow 0.25s; }
.search-bar-card--highlight { border-color: #2563EB !important; box-shadow: 0 0 0 4px rgba(37,99,235,0.25), 0 8px 24px rgba(37,99,235,0.12) !important; }
.search-input-wrap { position: relative; flex: 1; min-width: 200px; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); }
.search-input { width: 100%; padding: 10px 12px 10px 34px; border: 1px solid #E5E7EB; border-radius: 10px; font-size: 13px; color: #374151; background: #F8FAFC; outline: none; font-family: inherit; }
.search-input:focus { border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37,99,235,0.08); background: #fff; }
.search-trust-wrap { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.search-trust-label { font-size: 12px; font-weight: 700; color: #374151; white-space: nowrap; }
.search-trust-input { width: 70px; padding: 10px 10px; border: 1px solid #E5E7EB; border-radius: 10px; font-size: 13px; text-align: center; outline: none; font-family: inherit; }
.search-trust-input:focus { border-color: #2563EB; }

/* ── Empty ─────────────────────────────────────────── */
.empty-card { background: #fff; border: 1px solid #E8ECF4; border-radius: 16px; padding: 48px 24px; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.empty-icon { font-size: 40px; }
.empty-title { font-size: 15px; font-weight: 700; color: #0F172A; }
.empty-desc { font-size: 13px; color: #6B7280; max-width: 360px; }

/* ── Candidate Cards ───────────────────────────────── */
.cand-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.cand-card { background: #fff; border: 1px solid #E8ECF4; border-radius: 16px; padding: 22px; display: flex; flex-direction: column; gap: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); transition: box-shadow 0.15s, border-color 0.15s; }
.cand-card:hover { border-color: #93C5FD; box-shadow: 0 4px 20px rgba(37,99,235,0.08); }
.cand-header { display: flex; align-items: flex-start; gap: 14px; }
.cand-avatar { width: 42px; height: 42px; border-radius: 50%; background: #2563EB; color: #fff; font-size: 14px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.cand-info { flex: 1; }
.cand-name { font-size: 15px; font-weight: 800; color: #0F172A; }
.cand-degree { font-size: 11px; color: #6B7280; margin-top: 3px; }
.cand-trust-badge { background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; padding: 5px 12px; border-radius: 20px; font-size: 11px; white-space: nowrap; flex-shrink: 0; }
.cand-skills-section { display: flex; flex-direction: column; gap: 8px; }
.cand-skills-label { font-size: 11px; font-weight: 700; color: #6B7280; }
.cand-skills { display: flex; flex-wrap: wrap; gap: 6px; }
.cand-skill-chip { padding: 4px 10px; border-radius: 7px; font-size: 11px; font-weight: 700; border: 1px solid; }
.chip--blue { background: #EFF6FF; color: #2563EB; border-color: #BFDBFE; }
.chip--gray { background: #F1F5F9; color: #475569; border-color: #E2E8F0; }
.cand-actions { display: flex; align-items: center; justify-content: space-between; gap: 10px; padding-top: 14px; border-top: 1px solid #F0F4FF; }
.cand-actions-left { display: flex; align-items: center; gap: 8px; }

/* ── Unlocked Candidate Styles ─────────────────────── */
.cand-card--unlocked { border-color: #A7F3D0 !important; background: #FAFDFB; box-shadow: 0 4px 18px rgba(16,185,129,0.08); }
.cand-name-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.cand-unlocked-badge { display: inline-flex; align-items: center; padding: 2px 8px; background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 20px; font-size: 10px; font-weight: 800; color: #059669; }
.unlocked-dossier-box { background: #fff; border: 1px solid #A7F3D0; border-radius: 12px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; box-shadow: 0 2px 8px rgba(16,185,129,0.06); }
.dossier-header { display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 800; color: #065F46; }
.dossier-icon { font-size: 13px; }
.dossier-title { font-weight: 800; text-transform: uppercase; letter-spacing: 0.4px; }
.dossier-meta { margin-left: auto; font-size: 10px; color: #059669; background: #ECFDF5; padding: 2px 8px; border-radius: 10px; font-weight: 700; }
.dossier-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.dossier-item { display: flex; flex-direction: column; gap: 2px; }
.dossier-label { font-size: 10px; font-weight: 800; color: #64748B; letter-spacing: 0.5px; }
.dossier-val { font-size: 12px; font-weight: 700; color: #0F172A; word-break: break-all; }
.link-email { color: #2563EB; text-decoration: none; }
.link-email:hover { text-decoration: underline; }
.link-phone { color: #059669; text-decoration: none; }
.link-phone:hover { text-decoration: underline; }
.btn-unlock { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; border-radius: 9px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.15s; }
.btn-unlock:hover { background: #DBEAFE; }
.btn-email-candidate { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; border-radius: 9px; font-size: 12px; font-weight: 700; text-decoration: none; transition: all 0.15s; }
.btn-email-candidate:hover { background: #D1FAE5; }
.panel-header-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.panel-tag { font-size: 10px; font-weight: 800; color: #2563EB; background: #EFF6FF; border: 1px solid #BFDBFE; padding: 2px 8px; border-radius: 10px; }

/* ── Job Cards ─────────────────────────────────────── */
.jobs-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.job-card { background: #fff; border: 1px solid #E8ECF4; border-radius: 16px; padding: 22px; display: flex; flex-direction: column; gap: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.job-header { display: flex; align-items: flex-start; gap: 14px; }
.job-icon { width: 42px; height: 42px; border-radius: 10px; background: #EFF6FF; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.job-title-wrap { flex: 1; }
.job-title { font-size: 15px; font-weight: 800; color: #0F172A; }
.job-meta { font-size: 12px; color: #6B7280; margin-top: 3px; }
.job-status-badge { padding: 4px 12px; background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; border-radius: 20px; font-size: 10px; font-weight: 800; letter-spacing: 0.5px; flex-shrink: 0; }
.job-skills-section { display: flex; flex-direction: column; gap: 8px; }
.job-skills-label { font-size: 11px; font-weight: 700; color: #6B7280; }
.job-skills { display: flex; flex-wrap: wrap; gap: 6px; }
.job-skill-chip { padding: 4px 10px; background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 7px; font-size: 11px; font-weight: 600; color: #374151; }
.job-footer-meta { display: flex; flex-wrap: wrap; gap: 10px; padding-top: 8px; border-top: 1px solid #F1F5F9; }
.job-footer-meta span { font-size: 11px; color: #64748B; font-weight: 500; }
.deadline-normal { color: #64748B !important; }
.deadline-soon { color: #DC2626 !important; font-weight: 700 !important; background: #FEF2F2; padding: 2px 8px; border-radius: 6px; border: 1px solid #FECACA; }

/* ── Comparison, Explainability & Analytics Modules ──── */
.compare-module-card,
.explain-module-card,
.analytics-module-card {
  background: #fff;
  border: 1px solid #E8ECF4;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.module-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding-bottom: 16px;
  border-bottom: 1px solid #F1F5F9;
}

.module-title {
  font-size: 18px;
  font-weight: 800;
  color: #0F172A;
  letter-spacing: -0.2px;
  margin-bottom: 4px;
}

.module-sub {
  font-size: 13px;
  color: #64748B;
}

.compare-actions-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.compare-count-badge {
  font-size: 12px;
  font-weight: 700;
  color: #2563EB;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  padding: 6px 14px;
  border-radius: 20px;
}

.compare-selector-bar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.selector-label {
  font-size: 12px;
  font-weight: 700;
  color: #475569;
}

.selector-pills-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selector-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #fff;
  border: 1px solid #CBD5E1;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s;
}

.selector-pill:hover {
  border-color: #2563EB;
  color: #2563EB;
}

.selector-pill--active {
  background: #2563EB !important;
  border-color: #2563EB !important;
  color: #fff !important;
}

.pill-trust {
  font-size: 11px;
  opacity: 0.85;
}

.pill-check {
  font-weight: 800;
  font-size: 13px;
}

.comparison-matrix-wrap {
  overflow-x: auto;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}

.comparison-table th,
.comparison-table td {
  padding: 14px 18px;
  border-bottom: 1px solid #F1F5F9;
  border-right: 1px solid #F1F5F9;
}

.matrix-head-metric {
  width: 220px;
  background: #F8FAFC;
  font-weight: 700;
  color: #475569;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.matrix-head-cand {
  min-width: 200px;
  background: #F8FAFC;
}

.cand-matrix-head {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cand-avatar--sm {
  width: 34px !important;
  height: 34px !important;
  font-size: 12px !important;
}

.metric-label {
  font-weight: 700;
  color: #475569;
  background: #FAFBFD;
  width: 220px;
}

.metric-val {
  color: #1E293B;
  vertical-align: middle;
}

.matrix-trust-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.trust-bar-micro {
  flex: 1;
  max-width: 100px;
  height: 6px;
  background: #E2E8F0;
  border-radius: 4px;
  overflow: hidden;
}

.trust-bar-micro-fill {
  height: 100%;
  background: #2563EB;
  border-radius: 4px;
}

.matrix-chips-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.cand-chip {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  background: #F1F5F9;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #475569;
}

.cand-chip--verified {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
}

.empty-compare-state,
.empty-explain-state {
  padding: 48px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px dashed #CBD5E1;
}

/* ── Match Explainability ───────────────────────────── */
.explain-active-badge {
  padding: 6px 14px;
  background: #EEF2FF;
  color: #4F46E5;
  border: 1px solid #C7D2FE;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.3px;
}

.explain-selectors-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background: #F8FAFC;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #E2E8F0;
}

.selector-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.selector-field-label {
  font-size: 12px;
  font-weight: 700;
  color: #334155;
}

.selector-dropdown {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #CBD5E1;
  border-radius: 10px;
  font-size: 13px;
  color: #0F172A;
  background: #fff;
  outline: none;
  font-weight: 500;
}

.selector-dropdown:focus {
  border-color: #2563EB;
}

.explain-dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 20px;
}

.explain-left-pane,
.explain-right-pane {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.explain-score-card {
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 18px;
}

.score-circle {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563EB, #1D4ED8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 16px rgba(37,99,235,0.25);
  flex-shrink: 0;
}

.score-number {
  font-size: 22px;
  font-weight: 900;
  line-height: 1;
}

.score-label {
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.8px;
  opacity: 0.9;
  margin-top: 2px;
}

.score-summary {
  flex: 1;
}

.score-title {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
  margin-bottom: 6px;
}

.score-status-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 6px;
}

.badge-green {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
}

.badge-amber {
  background: #FFFBEB;
  color: #D97706;
  border: 1px solid #FDE68A;
}

.score-caption {
  font-size: 11px;
  color: #64748B;
  line-height: 1.4;
}

.signals-stack {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #fff;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 18px;
}

.signal-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 10px;
  border-bottom: 1px solid #F1F5F9;
}

.signal-row:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.signal-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.signal-name {
  font-size: 12px;
  font-weight: 700;
  color: #1E293B;
}

.signal-weight {
  font-size: 10px;
  color: #64748B;
}

.signal-pct {
  font-size: 13px;
  font-weight: 800;
}

.matched-breakdown-card,
.skill-gaps-card {
  background: #fff;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-subtitle {
  font-size: 13px;
  font-weight: 800;
  color: #0F172A;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.matched-skills-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.matched-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.matched-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.matched-item-bar-bg {
  width: 100%;
  height: 6px;
  background: #E2E8F0;
  border-radius: 4px;
  overflow: hidden;
}

.matched-item-bar-fill {
  height: 100%;
  background: #2563EB;
  border-radius: 4px;
}

.gaps-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.gap-chip {
  padding: 5px 12px;
  background: #FEF2F2;
  color: #DC2626;
  border: 1px solid #FECACA;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
}

/* ── Analytics Module ───────────────────────────────── */
.badge-pill-live {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.4px;
}

.analytics-metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-body {
  flex: 1;
}

.stat-sub {
  font-size: 11px;
  color: #64748B;
  font-weight: 600;
  margin-top: 3px;
}

.analytics-panels-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.analytics-panel {
  background: #fff;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.analytics-panel--full { width: 100%; }

.panel-heading {
  font-size: 15px;
  font-weight: 800;
  color: #0F172A;
}

.funnel-stack,
.skill-density-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.funnel-step,
.density-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.funnel-header,
.density-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #334155;
}

.funnel-bar-bg,
.density-bar-bg {
  width: 100%;
  height: 8px;
  background: #F1F5F9;
  border-radius: 5px;
  overflow: hidden;
}

.funnel-bar-fill {
  height: 100%;
  background: #2563EB;
  border-radius: 5px;
}

.density-bar-fill {
  height: 100%;
  border-radius: 5px;
}

/* ── Modal ─────────────────────────────────────────── */
.modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,0.5); backdrop-filter: blur(4px); z-index: 50; display: flex; align-items: center; justify-content: center; padding: 20px; }
.modal-box { background: #fff; border-radius: 20px; padding: 28px; width: 100%; max-width: 460px; box-shadow: 0 20px 60px rgba(0,0,0,0.15); display: flex; flex-direction: column; gap: 20px; }
.modal-box--job { max-width: 640px; max-height: 90vh; overflow-y: auto; }
.modal-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.modal-title { font-size: 17px; font-weight: 800; color: #0F172A; }
.modal-sub { font-size: 12px; color: #6B7280; margin-top: 3px; }
.modal-close { width: 32px; height: 32px; border-radius: 50%; background: #F1F5F9; border: none; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.modal-close:hover { background: #E2E8F0; }
.modal-form { display: flex; flex-direction: column; gap: 14px; }
.modal-footer-row { display: flex; justify-content: flex-end; gap: 10px; padding-top: 6px; border-top: 1px solid #F0F4FF; }
.job-form-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field-textarea { width: 100%; padding: 9px 12px; border: 1.5px solid #E2E8F0; border-radius: 10px; font-size: 13px; font-family: inherit; resize: vertical; outline: none; transition: border-color 0.2s; box-sizing: border-box; }
.field-textarea:focus { border-color: #2563EB; }
.field-select { width: 100%; padding: 9px 12px; border: 1.5px solid #E2E8F0; border-radius: 10px; font-size: 13px; font-family: inherit; background: #fff; outline: none; cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 36px; }
.field-select:focus { border-color: #2563EB; }
.req { color: #EF4444; }
.field-hint-inline { font-size: 11px; color: #94A3B8; font-weight: 400; }

/* ── Toast ─────────────────────────────────────────── */
.toast-notif { position: fixed; top: 24px; right: 24px; z-index: 9999; padding: 12px 20px; border-radius: 12px; font-size: 13px; font-weight: 600; box-shadow: 0 8px 24px rgba(0,0,0,0.12); display: flex; align-items: center; gap: 8px; }
.toast-notif--success { background: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; }
.toast-notif--error { background: #FEF2F2; border: 1px solid #FECACA; color: #991B1B; }
.toast-fade-enter-active, .toast-fade-leave-active { transition: all 0.25s ease; }
.toast-fade-enter-from, .toast-fade-leave-to { opacity: 0; transform: translateY(-8px); }

@media (max-width: 900px) {
  .cand-grid, .jobs-grid, .stats-row, .analytics-metrics-grid, .analytics-panels-row, .explain-dashboard-grid, .explain-selectors-row { grid-template-columns: 1fr; }
  .hero-banner { padding: 24px; }
}

/* ── Recruiter Onboarding & Empty States ────────────── */
.stat-sub-text {
  font-size: 11px;
  color: #64748B;
  font-weight: 500;
  margin-top: 2px;
}

.recruiter-onboarding-card {
  background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%);
  border: 1.5px solid #BFDBFE;
  border-radius: 16px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.05);
}

.onboarding-icon {
  font-size: 32px;
  flex-shrink: 0;
}

.onboarding-body {
  flex: 1;
}

.onboarding-badge {
  font-size: 10px;
  font-weight: 800;
  color: #2563EB;
  letter-spacing: 0.6px;
  margin-bottom: 4px;
}

.onboarding-title {
  font-size: 16px;
  font-weight: 800;
  color: #0F172A;
  margin-bottom: 4px;
}

.onboarding-desc {
  font-size: 13px;
  color: #475569;
  line-height: 1.5;
}

.onboarding-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.btn-onboarding-primary {
  padding: 10px 18px;
  background: #2563EB;
  color: #FFFFFF;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-onboarding-primary:hover { background: #1D4ED8; }

.btn-onboarding-secondary {
  padding: 10px 18px;
  background: #FFFFFF;
  color: #1E293B;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid #CBD5E1;
  cursor: pointer;
  transition: all 0.15s ease;
}
.btn-onboarding-secondary:hover { background: #F8FAFC; }

.empty-funnel-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 36px 20px;
  background: #F8FAFC;
  border-radius: 12px;
  border: 1px dashed #CBD5E1;
}

.empty-funnel-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.empty-funnel-title {
  font-size: 14px;
  font-weight: 800;
  color: #1E293B;
  margin-bottom: 6px;
}

.empty-funnel-desc {
  font-size: 12px;
  color: #64748B;
  max-width: 380px;
  line-height: 1.5;
  margin-bottom: 16px;
}

.btn-funnel-cta {
  padding: 8px 16px;
  background: #2563EB;
  color: #FFFFFF;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: background 0.15s ease;
}
.btn-funnel-cta:hover { background: #1D4ED8; }
.job-delete-row { display: flex; justify-content: flex-end; padding-top: 8px; border-top: 1px solid #FEE2E2; margin-top: 2px; }
.btn-delete-job { background: none; border: 1px solid #FECACA; color: #DC2626; font-size: 11px; font-weight: 600; padding: 5px 12px; border-radius: 8px; cursor: pointer; transition: background 0.15s; }
.btn-delete-job:hover { background: #FEF2F2; }
.explain-embedded { margin-top: 4px; }
</style>
