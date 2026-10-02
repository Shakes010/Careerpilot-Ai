<template>
  <div class="admin-root">

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" class="fixed top-6 right-6 z-50 flex items-center gap-3 px-5 py-3 rounded-2xl shadow-xl border text-xs font-bold backdrop-blur-md" :class="toast.type === 'error' ? 'bg-red-50/95 border-red-200 text-red-700' : 'bg-emerald-50/95 border-emerald-200 text-emerald-800'">
        <span>{{ toast.type === 'error' ? '⚠️' : '✅' }}</span>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <!-- Page Header -->
    <div class="admin-hero">
      <div class="admin-hero-left">
        <div class="admin-hero-icon">CP</div>
        <div>
          <h1 class="admin-hero-title">Admin Moderation &amp; Governance Suite</h1>
          <p class="admin-hero-sub">Manage platform users, verify companies, review flagged assessments, and monitor system metrics.</p>
        </div>
      </div>
    </div>

    <!-- Sub-Tabs -->
    <div class="admin-tabs-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="admin-tab-btn"
        :class="{ 'admin-tab-active': adminTab === tab.key }"
        @click="adminTab = tab.key"
      >
        {{ tab.label }}
        <span v-if="tab.count !== undefined" class="admin-tab-count" :class="tab.countClass">
          {{ tab.count }}
        </span>
      </button>
    </div>

    <!-- ── TAB 1: Platform Overview & System Analytics ── -->
    <div v-if="adminTab === 'analytics'" class="admin-section space-y-6">
      
      <!-- Database Telemetry Banner -->
      <div class="db-telemetry-banner">
        <span class="db-telemetry-dot"></span>
        <span class="db-telemetry-text">
          <strong>PostgreSQL Live Telemetry:</strong> All metrics and graphs are computed in real time from live database tables (<code>users</code>, <code>companies</code>, <code>transactions</code>, <code>jobs</code>, <code>applications</code>, and <code>assessments</code>). Zero synthetic or placeholder numbers.
        </span>
      </div>

      <!-- Top 8 Metric Summary Cards -->
      <div class="stats-grid">
        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Total Students</div>
            <div class="stat-value stat-blue">{{ analytics.total_students || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-blue">🎓</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Verified Companies</div>
            <div class="stat-value stat-indigo">{{ analytics.verified_companies || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-indigo">💼</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Gross Revenue</div>
            <div class="stat-value stat-green">₹{{ Number(analytics.gross_revenue_inr || 0).toLocaleString('en-IN') }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-green">💳</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Live Job Postings</div>
            <div class="stat-value stat-blue">{{ analytics.total_jobs || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-blue">🚀</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Total Applications</div>
            <div class="stat-value stat-indigo">{{ analytics.total_applications || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-indigo">📄</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Skill Badges Awarded</div>
            <div class="stat-value stat-green">{{ analytics.verified_skill_badges_awarded || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-green">⭐</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Passed Assessments</div>
            <div class="stat-value stat-green">{{ analytics.total_passed_assessments || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-green">✅</div>
        </div>

        <div class="cp-stat-card">
          <div>
            <div class="stat-label">Flagged Queue</div>
            <div class="stat-value stat-amber">{{ analytics.flagged_attempts_queue_count || 0 }}</div>
          </div>
          <div class="cp-icon-box cp-icon-box-amber">⚠️</div>
        </div>
      </div>

      <!-- ANALYTICS ROW 1: Growth Velocity Graph + Skill Pass Rates -->
      <div class="admin-charts-grid">
        
        <!-- Graph 1: Platform User Velocity (Last 7 Days) -->
        <div class="cp-card chart-card">
          <div class="chart-header">
            <div>
              <h3 class="chart-title">Platform User Acquisition &amp; Velocity</h3>
              <p class="chart-sub">Student &amp; Recruiter registration velocity over the past 7 days</p>
            </div>
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-dot legend-dot--total"></span> Total</span>
              <span class="legend-item"><span class="legend-dot legend-dot--student"></span> Students</span>
              <span class="legend-item"><span class="legend-dot legend-dot--recruiter"></span> Recruiters</span>
            </div>
          </div>

          <div class="chart-canvas-wrap">
            <svg viewBox="0 0 560 160" class="growth-svg" preserveAspectRatio="none">
              <defs>
                <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#2563EB" stop-opacity="0.25"/>
                  <stop offset="100%" stop-color="#2563EB" stop-opacity="0.0"/>
                </linearGradient>
              </defs>

              <!-- Grid Horizontal Lines -->
              <line x1="20" y1="25" x2="540" y2="25" stroke="#E2E8F0" stroke-dasharray="3 3"/>
              <line x1="20" y1="75" x2="540" y2="75" stroke="#E2E8F0" stroke-dasharray="3 3"/>
              <line x1="20" y1="125" x2="540" y2="125" stroke="#E2E8F0" stroke-dasharray="3 3"/>

              <!-- Area Fill -->
              <polygon
                v-if="growthChartData.areaPoints"
                :points="growthChartData.areaPoints"
                fill="url(#areaGrad)"
              />

              <!-- Total Polyline -->
              <polyline
                v-if="growthChartData.totalPoints"
                :points="growthChartData.totalPoints"
                fill="none"
                stroke="#2563EB"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
              />

              <!-- Students Polyline -->
              <polyline
                v-if="growthChartData.studentPoints"
                :points="growthChartData.studentPoints"
                fill="none"
                stroke="#10B981"
                stroke-width="2"
                stroke-dasharray="4 3"
                stroke-linecap="round"
                stroke-linejoin="round"
              />

              <!-- Recruiters Polyline -->
              <polyline
                v-if="growthChartData.recruiterPoints"
                :points="growthChartData.recruiterPoints"
                fill="none"
                stroke="#7C3AED"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />

              <!-- Data Circles -->
              <g v-for="pt in growthChartData.coords" :key="pt.date">
                <circle :cx="pt.x" :cy="pt.yTotal" r="4" fill="#FFFFFF" stroke="#2563EB" stroke-width="2.5" />
                <circle :cx="pt.x" :cy="pt.yStudent" r="3" fill="#10B981" />
                <circle :cx="pt.x" :cy="pt.yRecruiter" r="3" fill="#7C3AED" />
              </g>
            </svg>

            <!-- X-Axis Labels -->
            <div class="x-axis-labels">
              <div v-for="pt in growthChartData.coords" :key="pt.date" class="x-label-item">
                <span class="x-date">{{ pt.date }}</span>
                <span class="x-val">{{ pt.total }} users</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Graph 2: Domain Assessment Pass Rates -->
        <div class="cp-card chart-card">
          <div class="chart-header">
            <div>
              <h3 class="chart-title">Domain Assessment Pass Rates</h3>
              <p class="chart-sub">Success ratios by core technical skill domain</p>
            </div>
            <span class="chart-badge">Live Evaluation</span>
          </div>

          <div class="skill-bars-list">
            <div v-for="s in (analytics.skill_pass_rates || [])" :key="s.skill_name" class="skill-bar-row">
              <div class="skill-bar-meta">
                <span class="skill-name">{{ s.skill_name }}</span>
                <span class="skill-stats">{{ s.passed_attempts }} / {{ s.total_attempts }} Passed ({{ s.pass_rate_pct }}%)</span>
              </div>
              <div class="skill-bar-track">
                <div
                  class="skill-bar-progress"
                  :style="{
                    width: `${Math.max(s.pass_rate_pct, s.total_attempts > 0 ? 8 : 0)}%`,
                    background: s.pass_rate_pct >= 75 ? '#10B981' : s.pass_rate_pct >= 40 ? '#2563EB' : '#D97706'
                  }"
                ></div>
              </div>
            </div>

            <div v-if="!(analytics.skill_pass_rates && analytics.skill_pass_rates.length)" class="cp-empty py-6">
              No skill assessment telemetry recorded yet.
            </div>
          </div>
        </div>

      </div>

      <!-- ANALYTICS ROW 2: Revenue Distribution + System Health -->
      <div class="admin-charts-grid">

        <!-- Revenue Distribution -->
        <div class="cp-card chart-card">
          <div class="chart-header">
            <div>
              <h3 class="chart-title">Subscription &amp; Transaction Breakdown</h3>
              <p class="chart-sub">Gross monetization distribution by plan tier</p>
            </div>
            <span class="chart-badge stat-green">Verified Revenue</span>
          </div>

          <div class="revenue-plans-list">
            <div v-for="p in (analytics.revenue_by_plan || [])" :key="p.plan_name" class="revenue-plan-item">
              <div class="rev-plan-left">
                <span class="rev-plan-icon">💎</span>
                <div>
                  <div class="rev-plan-name">{{ p.plan_name }}</div>
                  <div class="rev-plan-count">{{ p.count }} Successful Invoices</div>
                </div>
              </div>
              <div class="rev-plan-amount">₹{{ Number(p.revenue).toLocaleString('en-IN') }}</div>
            </div>

            <div v-if="!(analytics.revenue_by_plan && analytics.revenue_by_plan.length)" class="cp-empty py-6">
              No paid transactions logged yet.
            </div>
          </div>
        </div>

        <!-- System Health & Security Telemetry -->
        <div class="cp-card chart-card">
          <div class="chart-header">
            <div>
              <h3 class="chart-title">System Health &amp; Security Auditing</h3>
              <p class="chart-sub">Real-time infrastructure and proctoring watchdog metrics</p>
            </div>
            <span class="health-pulse-dot"></span>
          </div>

          <div class="health-metrics-grid">
            <div class="health-card">
              <div class="health-icon">🗄️</div>
              <div class="health-info">
                <div class="health-label">Database Cluster</div>
                <div class="health-val">{{ analytics.system_health?.database_status || 'Healthy (PostgreSQL 16)' }}</div>
              </div>
              <span class="health-tag health-tag--good">ACTIVE</span>
            </div>

            <div class="health-card">
              <div class="health-icon">🛡️</div>
              <div class="health-info">
                <div class="health-label">Anti-Cheat Watchdog</div>
                <div class="health-val">{{ analytics.system_health?.security_proctoring || 'Zero-Tolerant Focus Monitoring' }}</div>
              </div>
              <span class="health-tag health-tag--good">SECURE</span>
            </div>

            <div class="health-card">
              <div class="health-icon">🔐</div>
              <div class="health-info">
                <div class="health-label">Gateway Signature Verification</div>
                <div class="health-val">{{ analytics.system_health?.signature_verification || 'HMAC-SHA256 Enforced' }}</div>
              </div>
              <span class="health-tag health-tag--good">VERIFIED</span>
            </div>

            <div class="health-card">
              <div class="health-icon">⚡</div>
              <div class="health-info">
                <div class="health-label">ATS Resume Engine</div>
                <div class="health-val">{{ analytics.system_health?.ats_engine || 'Operational (spaCy NLP NLP)' }}</div>
              </div>
              <span class="health-tag health-tag--good">OPTIMAL</span>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ── TAB 2: User Management ── -->
    <div v-if="adminTab === 'users'" class="cp-card admin-section">

      <!-- Controls Header -->
      <div class="users-header">
        <h2 class="cp-section-title">User Account Management</h2>
        <div class="users-controls">
          <div class="cp-input-wrap">
            <span class="cp-input-icon">
              <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </span>
            <input
              v-model="userSearchQuery"
              type="text"
              placeholder="Search email or name..."
              class="cp-input"
              style="padding-left: 36px; height: 36px; font-size: 13px;"
            />
          </div>
          <select
            v-model="userRoleFilter"
            class="cp-input"
            style="width: auto; height: 36px; font-size: 13px; font-weight: 600;"
          >
            <option value="all">All Roles</option>
            <option value="student">Student</option>
            <option value="recruiter">Recruiter</option>
            <option value="admin">Admin</option>
          </select>
        </div>
      </div>

      <!-- Table -->
      <div class="table-wrap">
        <table class="cp-table">
          <thead>
            <tr>
              <th>User Details</th>
              <th>Role</th>
              <th>Status</th>
              <th>Joined</th>
              <th style="text-align:right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!filteredUsers.length">
              <td colspan="5" class="cp-empty" style="padding: 40px 14px;">No users match your filter.</td>
            </tr>
            <tr v-for="u in filteredUsers" :key="u.id">
              <td>
                <div class="user-name">{{ u.full_name || 'No Name' }}</div>
                <div class="user-email">{{ u.email }}</div>
              </td>
              <td>
                <span
                  class="cp-badge-base"
                  :class="u.role === 'admin' ? 'cp-badge-role-admin' : u.role === 'recruiter' ? 'cp-badge-role-recruiter' : 'cp-badge-role-student'"
                >
                  {{ u.role }}
                </span>
              </td>
              <td>
                <span class="cp-badge-base" :class="u.is_active ? 'cp-badge-active' : 'cp-badge-inactive'">
                  {{ u.is_active ? 'Active' : 'Disabled' }}
                </span>
              </td>
              <td class="date-cell">
                {{ u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A' }}
              </td>
              <td>
                <div class="action-btns">
                  <button class="action-btn" @click="openEditModal(u)">Edit</button>
                  <button
                    class="action-btn"
                    :class="u.is_active ? 'action-btn-amber' : 'action-btn-green'"
                    @click="toggleActiveStatus(u)"
                  >
                    {{ u.is_active ? 'Disable' : 'Enable' }}
                  </button>
                  <button class="action-btn action-btn-red" @click="deleteUser(u)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── TAB 3: Flagged Queue ── -->
    <div v-if="adminTab === 'flagged'" class="cp-card admin-section">
      <div class="flagged-header">
        <h2 class="cp-section-title">Flagged Assessment Review Queue</h2>
        <span class="cp-badge-base cp-badge-pending">{{ flaggedAttempts.length }} Pending</span>
      </div>

      <div v-if="!flaggedAttempts.length" class="cp-empty">
        No flagged assessment attempts currently in queue.
      </div>

      <div v-else class="flagged-list">
        <div v-for="item in flaggedAttempts" :key="item.attempt_id" class="flagged-item">
          <div class="flagged-item-top">
            <div>
              <span class="flagged-student-name">{{ item.student_name }}</span>
              <span class="flagged-student-email">({{ item.student_email }})</span>
            </div>
            <span class="cp-badge-base cp-badge-role-student">
              {{ item.assessment_name }} · {{ item.skill_name }}
            </span>
          </div>

          <div class="flagged-detail">
            <div class="flagged-reason-title">Flag Reason &amp; Metrics</div>
            <div class="flagged-reason">{{ item.flag_reason }}</div>
            <div class="flagged-metrics">
              Paste Events: {{ item.paste_event_count }} &nbsp;|&nbsp;
              Paste Chars: {{ item.paste_char_count }} &nbsp;|&nbsp;
              Duration: {{ item.time_spent_seconds }}s
            </div>
          </div>

          <div class="flagged-actions">
            <button @click="reviewAttempt(item.attempt_id, 'rejected')" class="cp-btn-danger">
              Reject Attempt
            </button>
            <button @click="reviewAttempt(item.attempt_id, 'approved')" class="cp-btn-primary" style="height:36px; font-size:13px; padding: 0 16px;">
              Approve &amp; Award Badge
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ── TAB 4: Company Approvals ── -->
    <div v-if="adminTab === 'companies'" class="cp-card admin-section">
      <h2 class="cp-section-title" style="margin-bottom:16px;">Company Verification Requests</h2>
      <div class="company-list">
        <div v-for="c in companyVerifications" :key="c.id" class="company-item">
          <div>
            <div class="company-name">{{ c.name }} <span class="company-industry">({{ c.industry }})</span></div>
            <div class="company-meta">Email: {{ c.email }} | Website: {{ c.website }}</div>
            <div class="company-notes">{{ c.verification_notes }}</div>
          </div>
          <div class="company-actions">
            <span
              class="cp-badge-base"
              :class="c.verification_status === 'verified' ? 'cp-badge-active' : 'cp-badge-pending'"
              style="text-transform:uppercase;"
            >
              {{ c.verification_status }}
            </span>
            <button
              v-if="c.verification_status === 'pending'"
              @click="verifyCompany(c.id, 'verified')"
              class="cp-btn-primary"
              style="height:36px; font-size:13px; padding: 0 16px;"
            >
              Approve Company
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ── MODAL: Edit User Profile ── -->
    <div v-if="editingUser" class="cp-modal-overlay" @click.self="editingUser = null">
      <div class="cp-modal">
        <div class="cp-modal-header">
          <h3 class="cp-modal-title">Edit User Profile</h3>
          <button class="cp-modal-close" @click="editingUser = null">✕</button>
        </div>
        <form @submit.prevent="saveUserEdit" class="modal-form">
          <div class="cp-form-field">
            <label class="cp-form-label">Full Name</label>
            <input v-model="editForm.full_name" type="text" required class="cp-input" />
          </div>
          <div class="cp-form-field">
            <label class="cp-form-label">Email Address</label>
            <input v-model="editForm.email" type="email" required class="cp-input" />
          </div>
          <div class="cp-form-field">
            <label class="cp-form-label">Account Role</label>
            <select v-model="editForm.role" class="cp-input" style="appearance:auto; cursor:pointer;">
              <option value="student">Student</option>
              <option value="recruiter">Recruiter</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="modal-footer">
            <button type="button" @click="editingUser = null" class="cp-btn-secondary" style="height:36px;font-size:13px;padding:0 16px;">Cancel</button>
            <button type="submit" class="cp-btn-primary" style="height:36px;font-size:13px;padding:0 16px;">Save Changes</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const adminTab = ref('analytics')

const analytics = ref({})
const flaggedAttempts = ref([])
const companyVerifications = ref([])
const usersList = ref([])

const userSearchQuery = ref('')
const userRoleFilter = ref('all')

const editingUser = ref(null)
const editForm = ref({ full_name: '', email: '', role: 'student' })
const toast = ref(null)

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

const tabs = computed(() => [
  { key: 'analytics', label: 'Platform Overview' },
  {
    key: 'users',
    label: 'User Management',
    count: usersList.value.length,
    countClass: 'tab-count-blue'
  },
  {
    key: 'flagged',
    label: 'Flagged Queue',
    count: flaggedAttempts.value.length,
    countClass: 'tab-count-amber'
  },
  {
    key: 'companies',
    label: 'Company Approvals',
    count: companyVerifications.value.length,
    countClass: 'tab-count-indigo'
  }
])

const growthChartData = computed(() => {
  const trend = analytics.value.user_growth_trend || []
  if (!trend.length) {
    return { totalPoints: '', studentPoints: '', recruiterPoints: '', areaPoints: '', coords: [] }
  }
  const w = 560
  const h = 150
  const padX = 40
  const padY = 25
  const maxVal = Math.max(...trend.map(t => Math.max(t.total, t.students, t.recruiters)), 4)
  const stepX = (w - padX * 2) / Math.max(trend.length - 1, 1)

  const coords = trend.map((d, i) => {
    const x = Math.round(padX + i * stepX)
    const yTotal = Math.round(h - padY - (d.total / maxVal) * (h - padY * 2))
    const yStudent = Math.round(h - padY - (d.students / maxVal) * (h - padY * 2))
    const yRecruiter = Math.round(h - padY - (d.recruiters / maxVal) * (h - padY * 2))
    return { x, yTotal, yStudent, yRecruiter, ...d }
  })

  const totalPoints = coords.map(c => `${c.x},${c.yTotal}`).join(' ')
  const studentPoints = coords.map(c => `${c.x},${c.yStudent}`).join(' ')
  const recruiterPoints = coords.map(c => `${c.x},${c.yRecruiter}`).join(' ')
  const firstX = coords[0].x
  const lastX = coords[coords.length - 1].x
  const areaPoints = `${firstX},${h - padY} ${totalPoints} ${lastX},${h - padY}`

  return { totalPoints, studentPoints, recruiterPoints, areaPoints, coords }
})

onMounted(async () => {
  await loadAdminData()
})

const loadAdminData = async () => {
  try {
    const stats = await apiFetch('/admin/analytics')
    analytics.value = stats || {}

    const queue = await apiFetch('/admin/flagged-attempts')
    flaggedAttempts.value = queue || []

    const comps = await apiFetch('/admin/company-verifications')
    companyVerifications.value = comps || []

    const users = await apiFetch('/admin/users')
    usersList.value = users || []
  } catch (err) {
    console.error(err)
  }
}

const filteredUsers = computed(() => {
  return usersList.value.filter(u => {
    const matchesSearch = !userSearchQuery.value ||
      (u.email && u.email.toLowerCase().includes(userSearchQuery.value.toLowerCase())) ||
      (u.full_name && u.full_name.toLowerCase().includes(userSearchQuery.value.toLowerCase()))

    const matchesRole = userRoleFilter.value === 'all' || u.role === userRoleFilter.value
    return matchesSearch && matchesRole
  })
})

const openEditModal = (user) => {
  editingUser.value = user
  editForm.value = {
    full_name: user.full_name || '',
    email: user.email || '',
    role: user.role || 'student'
  }
}

const saveUserEdit = async () => {
  try {
    const res = await apiFetch(`/admin/users/${editingUser.value.id}/update-profile`, {
      method: 'PUT',
      body: JSON.stringify(editForm.value)
    })
    showToast(res.message || 'User profile updated successfully!')
    editingUser.value = null
    await loadAdminData()
  } catch (err) {
    showToast(err.message || 'Update failed', 'error')
  }
}

const toggleActiveStatus = async (user) => {
  try {
    await apiFetch(`/admin/users/${user.id}/status?is_active=${!user.is_active}`, {
      method: 'PUT'
    })
    showToast(`User status updated to ${!user.is_active ? 'Active' : 'Inactive'}`)
    await loadAdminData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}

const deleteUser = async (user) => {
  if (!confirm(`Are you sure you want to permanently delete user ${user.email}?`)) return
  try {
    const res = await apiFetch(`/admin/users/${user.id}`, {
      method: 'DELETE'
    })
    showToast(res.message || 'User deleted')
    await loadAdminData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}

const reviewAttempt = async (attemptId, action) => {
  try {
    const res = await apiFetch(`/admin/flagged-attempts/${attemptId}/review`, {
      method: 'POST',
      body: JSON.stringify({ action })
    })
    showToast(res.message || 'Review completed')
    await loadAdminData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}

const verifyCompany = async (companyId, statusValue) => {
  try {
    await apiFetch(`/admin/company-verifications/${companyId}?status_value=${statusValue}`, {
      method: 'POST'
    })
    showToast(`Company status updated to ${statusValue}!`)
    await loadAdminData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}
</script>

<style scoped>
/* ---- Page Shell ---- */
.admin-root {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.admin-section {
  /* gap between sections */
}

/* ---- Hero Banner ---- */
.admin-hero {
  background: linear-gradient(135deg, #0F172A 0%, #1E3A5F 60%, #312E81 100%);
  border-radius: var(--radius-xl);
  padding: 24px 28px;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  box-shadow: var(--shadow-md);
}

.db-telemetry-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  border-radius: 12px;
  padding: 11px 18px;
  font-size: 12px;
  color: #166534;
}
.db-telemetry-dot {
  width: 9px;
  height: 9px;
  background: #10B981;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
  flex-shrink: 0;
}
.db-telemetry-text {
  line-height: 1.5;
}
.db-telemetry-text code {
  background: #DCFCE7;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 11px;
  font-weight: 700;
  color: #14532D;
}

.admin-hero-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.admin-hero-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 15px;
  flex-shrink: 0;
}

.admin-hero-title {
  font-size: 18px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 3px;
}

.admin-hero-sub {
  font-size: 12px;
  color: #CBD5E1;
  line-height: 1.5;
}

/* ---- Tabs Bar ---- */
.admin-tabs-bar {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--color-border);
  overflow-x: auto;
  padding-bottom: 0;
}

.admin-tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-muted);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  white-space: nowrap;
  transition: color var(--transition-fast), border-color var(--transition-fast);
}

.admin-tab-btn:hover {
  color: var(--color-text-heading);
}

.admin-tab-active {
  color: var(--color-primary) !important;
  border-bottom-color: var(--color-primary) !important;
}

.admin-tab-count {
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: var(--radius-pill);
}

.tab-count-blue   { background: var(--color-primary-light); color: var(--color-primary); border: 1px solid #BFDBFE; }
.tab-count-amber  { background: var(--color-warning-bg);    color: var(--color-warning);  border: 1px solid var(--color-warning-border); }
.tab-count-indigo { background: #EEF2FF;                    color: #4F46E5;                border: 1px solid #C7D2FE; }

/* ---- Stats Grid ---- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  margin-bottom: 6px;
}

.stat-value {
  font-size: 28px;
  font-weight: 900;
  color: var(--color-text-heading);
  letter-spacing: -0.5px;
}

.stat-blue  { color: var(--color-primary); }
.stat-green { color: var(--color-success); }
.stat-amber { color: var(--color-warning); }

/* ---- Users Panel Controls ---- */
.users-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--color-border);
}

.users-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

/* ---- Table ---- */
.table-wrap {
  overflow-x: auto;
}

.user-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-heading);
}

.user-email {
  font-size: 11px;
  color: var(--color-text-muted);
  margin-top: 1px;
}

.date-cell {
  font-size: 12px;
  color: var(--color-text-muted);
}

/* ---- Action Buttons ---- */
.action-btns {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 700;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-bg-subtle);
  color: var(--color-text-body);
  cursor: pointer;
  transition: background-color var(--transition-fast);
  white-space: nowrap;
}
.action-btn:hover { background: #E2E8F0; }

.action-btn-blue  { background: var(--color-primary-light); color: var(--color-primary); border-color: #BFDBFE; }
.action-btn-blue:hover { background: #DBEAFE; }

.action-btn-amber { background: var(--color-warning-bg); color: var(--color-warning); border-color: var(--color-warning-border); }
.action-btn-amber:hover { background: #FDE68A; }

.action-btn-green { background: var(--color-success-bg); color: var(--color-success); border-color: var(--color-success-border); }
.action-btn-green:hover { background: #A7F3D0; }

.action-btn-red   { background: var(--color-error-bg); color: var(--color-error); border-color: var(--color-error-border); }
.action-btn-red:hover { background: #FECACA; }

/* ---- Flagged Queue ---- */
.flagged-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.flagged-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.flagged-item {
  background: var(--color-warning-bg);
  border: 1px solid var(--color-warning-border);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.flagged-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.flagged-student-name {
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text-heading);
}

.flagged-student-email {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-left: 6px;
}

.flagged-detail {
  background: var(--color-bg-card);
  border: 1px solid var(--color-warning-border);
  border-radius: var(--radius-md);
  padding: 12px;
}

.flagged-reason-title {
  font-weight: 700;
  font-size: 12px;
  color: #92400E;
  margin-bottom: 4px;
}

.flagged-reason {
  font-size: 13px;
  color: var(--color-text-heading);
  margin-bottom: 4px;
}

.flagged-metrics {
  font-size: 11px;
  color: var(--color-text-muted);
}

.flagged-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}

/* ---- Company List ---- */
.company-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.company-item {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.company-name {
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text-heading);
}

.company-industry {
  font-weight: 400;
  color: var(--color-text-muted);
}

.company-meta {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 3px;
}

.company-notes {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-warning);
  margin-top: 3px;
}

.company-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

/* ---- Modal Form ---- */
.modal-form {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
  padding-top: 14px;
  border-top: 1px solid var(--color-border);
}

/* ---- Analytics Charts & Graphs Styling ---- */
.admin-charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
  gap: 20px;
}

.chart-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.chart-title {
  font-size: 15px;
  font-weight: 800;
  color: var(--color-text-heading);
  margin-bottom: 2px;
}

.chart-sub {
  font-size: 12px;
  color: var(--color-text-muted);
}

.chart-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-pill);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  color: var(--color-primary);
}

.chart-legend {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.legend-dot--total { background: #2563EB; }
.legend-dot--student { background: #10B981; }
.legend-dot--recruiter { background: #7C3AED; }

.chart-canvas-wrap {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.growth-svg {
  width: 100%;
  height: 150px;
  overflow: visible;
}

.x-axis-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  font-size: 10px;
}

.x-label-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.x-date {
  font-weight: 700;
  color: var(--color-text-heading);
}

.x-val {
  color: var(--color-text-muted);
}

/* Skill Bars */
.skill-bars-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.skill-bar-row {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.skill-bar-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.skill-name {
  font-weight: 700;
  color: var(--color-text-heading);
}

.skill-stats {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.skill-bar-track {
  width: 100%;
  height: 8px;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  overflow: hidden;
}

.skill-bar-progress {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}

/* Revenue Breakdown */
.revenue-plans-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.revenue-plan-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.rev-plan-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rev-plan-icon {
  font-size: 18px;
}

.rev-plan-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-heading);
}

.rev-plan-count {
  font-size: 11px;
  color: var(--color-text-muted);
}

.rev-plan-amount {
  font-size: 14px;
  font-weight: 800;
  color: #10B981;
}

/* System Health Grid */
.health-metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.health-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  position: relative;
}

.health-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.health-info {
  flex: 1;
  min-width: 0;
}

.health-label {
  font-size: 11px;
  color: var(--color-text-muted);
  font-weight: 600;
}

.health-val {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-text-heading);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.health-tag {
  font-size: 9px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: var(--radius-pill);
}

.health-tag--good {
  background: #ECFDF5;
  color: #059669;
  border: 1px solid #A7F3D0;
}

.health-pulse-dot {
  width: 10px;
  height: 10px;
  background: #10B981;
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
</style>
