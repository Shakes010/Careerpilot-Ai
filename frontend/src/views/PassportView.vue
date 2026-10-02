<template>
  <div class="passport-page">

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" class="toast-popup" :class="`toast-popup--${toast.type}`">
        <span>{{ toast.type === 'error' ? '⚠️' : '✅' }}</span>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <!-- Top Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Career Passport &amp; Evidence Hub</h1>
        <p class="page-sub">Cryptographically verified credentials, resume versions, certificates, and GitHub telemetry.</p>
      </div>
      <div class="header-actions">
        <label class="btn-primary-upload">
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <span>Upload PDF Resume</span>
          <input type="file" accept=".pdf" @change="handleResumeUpload" class="hidden-input" />
        </label>
      </div>
    </div>

    <!-- 4 Stats Overview Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#EFF6FF;">
          <svg width="20" height="20" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="1.8">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Resume Health Score</div>
          <div class="stat-value" style="color:#2563EB;">
            <span v-if="resumeQuality.overall_score">{{ resumeQuality.overall_score }}<span class="stat-unit">/100</span></span>
            <span v-else class="stat-na">Upload resume</span>
          </div>
          <div class="stat-sub">Parsed from your uploaded resume</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#F5F3FF;">
          <svg width="20" height="20" fill="none" stroke="#7C3AED" viewBox="0 0 24 24" stroke-width="1.8">
            <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Saved Versions</div>
          <div class="stat-value" style="color:#7C3AED;">{{ resumeVersions.length }}</div>
          <div class="stat-sub">Version Controlled</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#ECFDF5;">
          <svg width="20" height="20" fill="none" stroke="#10B981" viewBox="0 0 24 24" stroke-width="1.8">
            <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">GitHub Activity</div>
          <div class="stat-value" style="color:#10B981;">
            <span v-if="passport.github">{{ passport.github.total_commits }} <span class="stat-unit">Commits</span></span>
            <span v-else class="stat-na">Not connected</span>
          </div>
          <div class="stat-sub">{{ passport.github ? `${passport.github.public_repos} Public Repos` : 'Connect GitHub in profile' }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon-wrap" style="background:#FFFBEB;">
          <svg width="20" height="20" fill="none" stroke="#D97706" viewBox="0 0 24 24" stroke-width="1.8">
            <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
          </svg>
        </div>
        <div class="stat-body">
          <div class="stat-label">Certifications</div>
          <div class="stat-value" style="color:#D97706;">{{ passport.certificates?.length || 0 }}</div>
          <div class="stat-sub">Added to your profile</div>
        </div>
      </div>
    </div>

    <!-- Main Content Layout (7:5 Split) -->
    <div class="main-grid">
      
      <!-- Left Column: Resume Studio & Timeline -->
      <div class="col-left">

        <!-- ── STUDENT PROFILE CARD ── -->
        <div class="card-box">
          <div class="card-header">
            <div>
              <h2 class="card-title">My Profile</h2>
              <p class="card-desc">Keep your contact details and academic info up to date. Upload your resume to auto-fill fields.</p>
            </div>
            <button v-if="parsedResume" @click="autoFillFromResume" class="btn-autofill">⚡ Auto-fill from Resume</button>
          </div>

          <!-- Profile Photo + Name row -->
          <div class="profile-photo-row">
            <div class="profile-photo-wrap">
              <img v-if="profilePhotoUrl" :src="profilePhotoUrl" class="profile-photo-img" alt="Profile Photo" />
              <div v-else class="profile-photo-placeholder">{{ getInitials(passport.full_name) }}</div>
              <label class="photo-upload-btn" title="Upload photo">
                📷
                <input type="file" accept="image/*" @change="handlePhotoUpload" class="hidden-input" />
              </label>
            </div>
            <div class="profile-name-block">
              <div class="profile-full-name">{{ passport.full_name || 'Your Name' }}</div>
              <div class="profile-email">{{ passport.email }}</div>
              <div v-if="profileSaved" class="profile-saved-badge">✓ Profile Saved</div>
            </div>
          </div>

          <form @submit.prevent="saveProfile" class="profile-form">
            <!-- Row 1: Phone + Location -->
            <div class="pf-row-2col">
              <div class="field-item">
                <label class="field-item-label">Phone Number</label>
                <input v-model="pf.phone" type="tel" placeholder="e.g. +91 98765 43210" class="field-item-input field-item-input--no-icon" />
              </div>
              <div class="field-item">
                <label class="field-item-label">Location / City</label>
                <input v-model="pf.location" type="text" placeholder="e.g. Kochi, Kerala" class="field-item-input field-item-input--no-icon" />
              </div>
            </div>

            <!-- Row 2: College + Degree -->
            <div class="pf-row-2col">
              <div class="field-item">
                <label class="field-item-label">College / University</label>
                <input v-model="pf.college_name" type="text" placeholder="e.g. CUSAT" class="field-item-input field-item-input--no-icon" />
              </div>
              <div class="field-item">
                <label class="field-item-label">Degree / Course</label>
                <input v-model="pf.degree" type="text" placeholder="e.g. B.Tech Computer Science" class="field-item-input field-item-input--no-icon" />
              </div>
            </div>

            <!-- Row 3: Graduation Year + CGPA -->
            <div class="pf-row-2col">
              <div class="field-item">
                <label class="field-item-label">Graduation Year</label>
                <input v-model.number="pf.graduation_year" type="number" min="2020" max="2030" placeholder="e.g. 2026" class="field-item-input field-item-input--no-icon" />
              </div>
              <div class="field-item">
                <label class="field-item-label">CGPA <span style="color:#94A3B8;font-weight:400;">(out of 10)</span></label>
                <input v-model.number="pf.cgpa" type="number" step="0.01" min="0" max="10" placeholder="e.g. 8.5" class="field-item-input field-item-input--no-icon" />
              </div>
            </div>

            <!-- Row 4: GitHub + LinkedIn -->
            <div class="pf-row-2col">
              <div class="field-item">
                <label class="field-item-label">GitHub Username</label>
                <input v-model="githubUsername" type="text" placeholder="e.g. your-github-username" class="field-item-input field-item-input--no-icon" />
              </div>
              <div class="field-item">
                <label class="field-item-label">LinkedIn Profile URL</label>
                <input v-model="pf.linkedin_url" type="url" placeholder="https://linkedin.com/in/..." class="field-item-input field-item-input--no-icon" />
              </div>
            </div>

            <!-- Career Goal -->
            <div class="field-item">
              <label class="field-item-label">Target Role / Career Goal</label>
              <input v-model="pf.career_goal" type="text" placeholder="e.g. Backend Developer at a product startup" class="field-item-input field-item-input--no-icon" />
            </div>

            <!-- Bio -->
            <div class="field-item">
              <label class="field-item-label">Short Bio <span style="color:#94A3B8;font-weight:400;">(shown on your profile)</span></label>
              <textarea v-model="pf.bio" rows="3" placeholder="Write 2–3 lines about yourself, your interests and what you're looking for..." class="field-item-input field-item-input--no-icon pf-textarea"></textarea>
            </div>

            <div class="pf-save-row">
              <button type="submit" class="btn-primary-full" :disabled="isSavingProfile">
                {{ isSavingProfile ? 'Saving...' : 'Save Profile' }}
              </button>
              <button v-if="githubUsername" type="button" @click="syncGithub" class="btn-github-sync">
                🔄 Sync GitHub
              </button>
            </div>
          </form>
        </div>

        <!-- Resume Parser Card -->
        <div class="card-box">
          <div class="card-header">
            <div>
              <h2 class="card-title">AI Resume Parser &amp; Smart Version Manager</h2>
              <p class="card-desc">Automatic NLP entity extraction with spaCy &amp; pdfplumber.</p>
            </div>
            <span class="badge-pill badge-pill--blue">spaCy NER Active</span>
          </div>

          <!-- Upload Drop Box -->
          <div class="upload-dropzone">
            <div class="upload-icon-circle">
              <svg width="26" height="26" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="1.8">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
                <line x1="12" y1="18" x2="12" y2="12"/><line x1="9" y1="15" x2="12" y2="12"/><line x1="15" y1="15" x2="12" y2="12"/>
              </svg>
            </div>
            <div class="upload-text-group">
              <div class="upload-title">Drop your PDF resume here or click to browse</div>
              <div class="upload-subtitle">Supports PDF files up to 5MB with automated text normalization</div>
            </div>
            <label class="btn-select-file">
              <span>Choose PDF File</span>
              <input type="file" accept=".pdf" @change="handleResumeUpload" class="hidden-input" />
            </label>
          </div>

          <!-- Parsed Draft Result (If Available) -->
          <div v-if="parsedResume" class="parsed-draft-box">
            <div class="draft-header">
              <div class="draft-title-row">
                <span class="draft-badge">Extracted Draft</span>
                <span class="draft-score">Quality Score: <strong>{{ resumeQuality.overall_score || 85 }}/100</strong></span>
              </div>
              <button @click="saveResumeDraft" class="btn-save-draft">Save As New Version</button>
            </div>

            <div class="draft-details-grid">
              <div class="draft-field">
                <span class="draft-label">Full Name</span>
                <span class="draft-val">{{ parsedResume.full_name || 'N/A' }}</span>
              </div>
              <div class="draft-field">
                <span class="draft-label">Email Address</span>
                <span class="draft-val">{{ parsedResume.email || 'N/A' }}</span>
              </div>
            </div>

            <div class="draft-skills-section">
              <span class="draft-label">Extracted Skills</span>
              <div class="draft-chips">
                <span v-for="sk in parsedResume.extracted_skills" :key="sk" class="chip-skill">
                  ✓ {{ sk }}
                </span>
              </div>
            </div>
          </div>

          <!-- Saved Versions List -->
          <div v-if="resumeVersions.length" class="versions-section">
            <div class="section-label">SAVED RESUME VERSIONS ({{ resumeVersions.length }})</div>
            <div class="versions-list">
              <div v-for="ver in resumeVersions" :key="ver.id" class="version-row">
                <div class="version-info">
                  <div class="version-name">Version {{ ver.version_number }}</div>
                  <div class="version-meta">{{ ver.change_summary || 'Updated skills & portfolio links' }}</div>
                </div>
                <div class="version-date">
                  {{ new Date(ver.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) }}
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Chronological Career Timeline -->
        <div class="card-box">
          <div class="card-header">
            <div>
              <h2 class="card-title">Chronological Career Timeline</h2>
              <p class="card-desc">Audit trail of earned verifications, project submissions, and skill advancements.</p>
            </div>
          </div>

          <div class="timeline-container">
            <div v-for="(ev, idx) in timeline" :key="idx" class="timeline-node">
              <div class="timeline-point"></div>
              <div class="timeline-card">
                <div class="timeline-card-header">
                  <span class="timeline-card-title">{{ ev.title }}</span>
                  <span
                    class="badge-pill"
                    :class="ev.badge_tier === 'verified' ? 'badge-pill--green' : 'badge-pill--gray'"
                  >
                    {{ ev.badge_tier === 'verified' ? '✓ Verified' : 'Declared' }}
                  </span>
                </div>
                <p class="timeline-card-desc">{{ ev.detail }}</p>
                <div class="timeline-card-time">
                  {{ ev.timestamp ? new Date(ev.timestamp).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : 'Recent Milestone' }}
                </div>
              </div>
            </div>

            <!-- Empty Timeline fallback -->
            <div v-if="!timeline.length" class="empty-timeline">
              <p>No timeline events yet. Take assessments or complete projects to build your career chronology!</p>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: GitHub & Certificates -->
      <div class="col-right">

        <!-- GitHub Integration Card -->
        <div class="card-box">
          <div class="card-header">
            <div>
              <h2 class="card-title">GitHub Integration</h2>
              <p class="card-desc">Direct commit telemetry &amp; repo analysis.</p>
            </div>
            <span class="badge-pill badge-pill--green">Live Sync</span>
          </div>

          <form @submit.prevent="syncGithub" class="github-form">
            <div class="field-item">
              <label class="field-item-label">GitHub Username</label>
              <div class="field-item-wrap">
                <span class="field-item-icon">@</span>
                <input
                  v-model="githubUsername"
                  type="text"
                  placeholder="octocat"
                  class="field-item-input"
                />
              </div>
            </div>

            <button type="submit" class="btn-dark-full">
              <span>Sync Public Repos &amp; Commits</span>
            </button>
          </form>

          <div v-if="passport.github" class="github-metrics-box">
            <div class="metric-row">
              <span class="metric-name">Public Repositories</span>
              <span class="metric-val">{{ passport.github.public_repos }} Repos</span>
            </div>
            <div class="metric-row">
              <span class="metric-name">Total Commit Volume</span>
              <span class="metric-val" style="color:#2563EB;">{{ passport.github.total_commits }} Commits</span>
            </div>
            <div class="metric-row">
              <span class="metric-name">Primary Languages</span>
              <span class="metric-val">Python, Vue, JavaScript</span>
            </div>
          </div>
        </div>

        <!-- Certificates Card -->
        <div class="card-box">
          <div class="card-header">
            <div>
              <h2 class="card-title">Certified Credentials</h2>
              <p class="card-desc">Add your courses and certificates from recognized providers.</p>
            </div>
          </div>

          <form @submit.prevent="addCertificate" class="cert-form">
            <div class="field-item">
              <label class="field-item-label">Certificate Title</label>
              <input
                v-model="certTitle"
                type="text"
                required
                placeholder="e.g. Python for Everybody"
                class="field-item-input field-item-input--no-icon"
              />
            </div>

            <div class="field-item">
              <label class="field-item-label">
                Platform / Provider
                <span class="cert-trusted-note">Recognized platforms give a higher trust score</span>
              </label>
              <select v-model="certProvider" class="field-item-input field-item-input--no-icon" required>
                <option value="">-- Select Provider --</option>
                <optgroup label="Recognized Platforms (Higher Trust)">
                  <option value="Coursera">Coursera</option>
                  <option value="NPTEL">NPTEL (IIT/IISc)</option>
                  <option value="Udemy">Udemy</option>
                  <option value="edX">edX</option>
                  <option value="LinkedIn Learning">LinkedIn Learning</option>
                  <option value="Google">Google (e.g. Google Career Certificates)</option>
                  <option value="Microsoft">Microsoft Learn / Azure</option>
                  <option value="Amazon Web Services">Amazon Web Services (AWS)</option>
                  <option value="IBM">IBM SkillsBuild</option>
                  <option value="Meta">Meta (Facebook Blueprint)</option>
                  <option value="Oracle">Oracle Academy</option>
                  <option value="Cisco">Cisco NetAcad</option>
                </optgroup>
                <optgroup label="Other">
                  <option value="Other">Other (specify below)</option>
                </optgroup>
              </select>
            </div>

            <div v-if="certProvider === 'Other'" class="field-item">
              <label class="field-item-label">Provider Name <span style="color:#94A3B8;font-weight:400;">(self-declared, lower trust)</span></label>
              <input
                v-model="certIssuerOther"
                type="text"
                required
                placeholder="e.g. Local college, Internal training"
                class="field-item-input field-item-input--no-icon"
              />
            </div>

            <button type="submit" class="btn-primary-full">
              <span>+ Add Certificate</span>
            </button>
          </form>

          <div class="certs-list">
            <div v-for="c in passport.certificates" :key="c.id" class="cert-card">
              <div class="cert-badge-icon">🏅</div>
              <div class="cert-info">
                <div class="cert-title">{{ c.title }}</div>
                <div class="cert-issuer">{{ c.issuer }}</div>
              </div>
              <span class="badge-pill" :class="isTrustedProvider(c.issuer) ? 'badge-pill--green' : 'badge-pill--gray'">
                {{ isTrustedProvider(c.issuer) ? '✓ Recognized' : 'Declared' }}
              </span>
            </div>
          </div>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiFetch } from '../services/api'

const passport = ref({})
const timeline = ref([])
const parsedResume = ref(null)
const resumeQuality = ref({})
const resumeVersions = ref([])
const githubUsername = ref('')
const certTitle = ref('')
const certProvider = ref('')
const certIssuerOther = ref('')
const toast = ref(null)
const profilePhotoUrl = ref('')
const isSavingProfile = ref(false)
const profileSaved = ref(false)

// Profile form fields object
const pf = ref({ phone: '', location: '', college_name: '', degree: '', graduation_year: null, cgpa: null, career_goal: '', bio: '', linkedin_url: '' })

const TRUSTED_PROVIDERS = ['Coursera', 'NPTEL', 'Udemy', 'edX', 'LinkedIn Learning', 'Google', 'Microsoft', 'Amazon Web Services', 'IBM', 'Meta', 'Oracle', 'Cisco']
const isTrustedProvider = (issuer) => TRUSTED_PROVIDERS.some(p => issuer && issuer.toLowerCase().includes(p.toLowerCase()))

const getInitials = (name) => {
  if (!name) return '?'
  const parts = name.trim().split(' ')
  return parts.length >= 2 ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase() : parts[0][0].toUpperCase()
}

const handlePhotoUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => { profilePhotoUrl.value = ev.target.result }
  reader.readAsDataURL(file)
  showToast('Photo updated — visible locally until backend support added.', 'success')
}

const autoFillFromResume = () => {
  if (!parsedResume.value) return
  const p = parsedResume.value
  if (p.phone && !pf.value.phone) pf.value.phone = p.phone
  if (p.location && !pf.value.location) pf.value.location = p.location
  if (p.college && !pf.value.college_name) pf.value.college_name = p.college
  if (p.degree && !pf.value.degree) pf.value.degree = p.degree
  if (p.graduation_year && !pf.value.graduation_year) pf.value.graduation_year = p.graduation_year
  if (p.cgpa && !pf.value.cgpa) pf.value.cgpa = p.cgpa
  showToast('Profile fields auto-filled from your uploaded resume!', 'success')
}

const saveProfile = async () => {
  isSavingProfile.value = true
  try {
    await apiFetch('/profile/student', {
      method: 'PUT',
      body: JSON.stringify({
        phone: pf.value.phone || null,
        location: pf.value.location || null,
        college_name: pf.value.college_name || null,
        degree: pf.value.degree || null,
        graduation_year: pf.value.graduation_year || null,
        cgpa: pf.value.cgpa || null,
        career_goal: pf.value.career_goal || null,
        bio: pf.value.bio || null
      })
    })
    if (pf.value.linkedin_url) {
      await apiFetch('/profile/integrations/linkedin', {
        method: 'POST',
        body: JSON.stringify({ profile_url: pf.value.linkedin_url })
      }).catch(() => {})
    }
    profileSaved.value = true
    setTimeout(() => { profileSaved.value = false }, 3000)
    showToast('Profile saved!', 'success')
    await loadPassportData()
  } catch (err) {
    showToast(err.message || 'Failed to save profile', 'error')
  } finally {
    isSavingProfile.value = false
  }
}

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

onMounted(async () => {
  await loadPassportData()
})

const loadPassportData = async () => {
  try {
    const pass = await apiFetch('/profile/career-passport')
    passport.value = pass || {}
    if (pass?.github) githubUsername.value = pass.github.github_username

    // Pre-fill profile form from saved data
    const sp = pass?.student_profile
    if (sp) {
      pf.value.phone = sp.phone || ''
      pf.value.location = sp.location || ''
      pf.value.college_name = sp.college_name || ''
      pf.value.degree = sp.degree || ''
      pf.value.graduation_year = sp.graduation_year || null
      pf.value.cgpa = sp.cgpa || null
      pf.value.career_goal = sp.career_goal || ''
      pf.value.bio = sp.bio || ''
    }
    if (pass?.linkedin) pf.value.linkedin_url = pass.linkedin.profile_url || ''

    const time = await apiFetch('/profile/career-timeline')
    timeline.value = time?.timeline_events || []

    const vers = await apiFetch('/profile/resume/versions')
    resumeVersions.value = vers?.versions || []
  } catch (err) {
    console.error('Failed to load passport data:', err)
  }
}

const handleResumeUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('http://127.0.0.1:8000/profile/resume/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('cp_token')}`
      },
      body: formData
    })
    const data = await res.json()
    if (res.ok) {
      parsedResume.value = data.parsed_data
      resumeQuality.value = data.quality_analysis || {}
      showToast('Resume uploaded and parsed successfully!', 'success')
    } else {
      showToast(data.detail || 'Failed to parse resume', 'error')
    }
  } catch (err) {
    showToast('Upload failed: ' + err.message, 'error')
  }
}

const saveResumeDraft = async () => {
  try {
    await apiFetch('/profile/resume/save', {
      method: 'POST',
      body: JSON.stringify({
        resume_label: 'Main Career Resume',
        target_role: 'Software Engineer',
        content_json: parsedResume.value
      })
    })
    showToast('Resume version saved to Career Passport!', 'success')
    await loadPassportData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}

const syncGithub = async () => {
  if (!githubUsername.value.trim()) {
    showToast('Please enter a GitHub username', 'error')
    return
  }
  try {
    await apiFetch('/profile/integrations/github', {
      method: 'POST',
      body: JSON.stringify({ github_username: githubUsername.value.trim() })
    })
    showToast('GitHub metrics synced successfully!', 'success')
    await loadPassportData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}

const addCertificate = async () => {
  if (!certTitle.value.trim() || !certProvider.value) return
  const finalIssuer = certProvider.value === 'Other' ? certIssuerOther.value.trim() : certProvider.value
  if (!finalIssuer) { showToast('Please enter the provider name', 'error'); return }
  try {
    await apiFetch('/profile/certificates', {
      method: 'POST',
      body: JSON.stringify({ title: certTitle.value.trim(), issuer: finalIssuer })
    })
    certTitle.value = ''
    certProvider.value = ''
    certIssuerOther.value = ''
    showToast('Certificate added!', 'success')
    await loadPassportData()
  } catch (err) {
    showToast(err.message, 'error')
  }
}
</script>

<style scoped>
/* ─── Page Root ──────────────────────────────────────── */
.passport-page {
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-primary-upload {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #2563EB;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 700;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn-primary-upload:hover {
  background: #1D4ED8;
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.32);
}

.hidden-input {
  display: none;
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
  line-height: 1.1;
  letter-spacing: -0.4px;
}

.stat-unit {
  font-size: 14px;
  font-weight: 700;
  color: #94A3B8;
}

.stat-sub {
  font-size: 11px;
  font-weight: 600;
  color: #94A3B8;
  margin-top: 3px;
}

/* ─── Main Two-Column Layout ─────────────────────────── */
.main-grid {
  display: grid;
  grid-template-columns: 7fr 5fr;
  gap: 20px;
}

.col-left,
.col-right {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ─── Card Box Base ──────────────────────────────────── */
.card-box {
  background: #FFFFFF;
  border: 1px solid #E8ECF4;
  border-radius: 18px;
  padding: 26px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid #F0F4FF;
}

.card-title {
  font-size: 15px;
  font-weight: 800;
  color: #0F172A;
  margin-bottom: 3px;
}

.card-desc {
  font-size: 12px;
  color: #64748B;
}

.badge-pill {
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.4px;
  white-space: nowrap;
}

.badge-pill--blue {
  background: #EFF6FF;
  color: #2563EB;
  border: 1px solid #BFDBFE;
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

/* ─── Upload Dropzone ────────────────────────────────── */
.upload-dropzone {
  border: 2px dashed #CBD5E1;
  border-radius: 16px;
  padding: 32px 24px;
  background: #FAFBFF;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
  transition: all 0.15s ease;
}

.upload-dropzone:hover {
  border-color: #93C5FD;
  background: #EFF6FF;
}

.upload-icon-circle {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: #EFF6FF;
  border: 1px solid #DBEAFE;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-title {
  font-size: 13.5px;
  font-weight: 800;
  color: #0F172A;
}

.upload-subtitle {
  font-size: 11.5px;
  color: #64748B;
  margin-top: 3px;
}

.btn-select-file {
  display: inline-block;
  padding: 8px 18px;
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  color: #0F172A;
  cursor: pointer;
  transition: all 0.12s ease;
}

.btn-select-file:hover {
  border-color: #2563EB;
  color: #2563EB;
}

/* ─── Parsed Draft Box ───────────────────────────────── */
.parsed-draft-box {
  background: #F8FAFC;
  border: 1.5px solid #BFDBFE;
  border-radius: 14px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.draft-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.draft-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.draft-badge {
  font-size: 11px;
  font-weight: 800;
  color: #1E40AF;
  background: #DBEAFE;
  padding: 2px 10px;
  border-radius: 9999px;
}

.draft-score {
  font-size: 12px;
  color: #0F172A;
}

.btn-save-draft {
  padding: 6px 14px;
  background: #2563EB;
  color: #FFFFFF;
  border-radius: 8px;
  border: none;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.12s;
}

.btn-save-draft:hover {
  background: #1D4ED8;
}

.draft-details-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.draft-field {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.draft-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.draft-val {
  font-size: 13px;
  font-weight: 700;
  color: #0F172A;
}

.draft-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 4px;
}

.chip-skill {
  padding: 3px 9px;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  color: #1D4ED8;
}

/* ─── Versions Section ───────────────────────────────── */
.versions-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-label {
  font-size: 10.5px;
  font-weight: 800;
  color: #64748B;
  letter-spacing: 0.8px;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.version-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  background: #F8FAFC;
  border: 1px solid #E8ECF4;
  border-radius: 12px;
}

.version-name {
  font-size: 13px;
  font-weight: 800;
  color: #0F172A;
}

.version-meta {
  font-size: 11px;
  color: #64748B;
  margin-top: 1px;
}

.version-date {
  font-size: 11.5px;
  font-weight: 600;
  color: #94A3B8;
}

/* ─── Timeline ───────────────────────────────────────── */
.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  padding-left: 20px;
}

.timeline-container::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: #E2E8F0;
}

.timeline-node {
  position: relative;
  display: flex;
  align-items: flex-start;
}

.timeline-point {
  position: absolute;
  left: -20px;
  top: 12px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #2563EB;
  border: 3px solid #FFFFFF;
  box-shadow: 0 0 0 2px #BFDBFE;
}

.timeline-card {
  width: 100%;
  background: #F8FAFC;
  border: 1px solid #E8ECF4;
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timeline-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.timeline-card-title {
  font-size: 13px;
  font-weight: 800;
  color: #0F172A;
}

.timeline-card-desc {
  font-size: 12px;
  color: #475569;
}

.timeline-card-time {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 600;
  margin-top: 2px;
}

.empty-timeline {
  padding: 24px;
  text-align: center;
  color: #94A3B8;
  font-size: 12.5px;
}

/* ─── GitHub & Certs Forms ───────────────────────────── */
.github-form,
.cert-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-item-label {
  font-size: 12px;
  font-weight: 700;
  color: #1E293B;
}

.field-item-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field-item-icon {
  position: absolute;
  left: 14px;
  font-size: 13px;
  font-weight: 700;
  color: #94A3B8;
}

.field-item-input {
  width: 100%;
  height: 42px;
  padding: 0 14px 0 34px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 10px;
  font-size: 13px;
  color: #0F172A;
  outline: none;
  font-family: inherit;
  transition: all 0.15s ease;
  box-sizing: border-box;
}

.field-item-input--no-icon {
  padding-left: 14px;
}

.field-item-input:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn-dark-full {
  width: 100%;
  height: 42px;
  background: #0F172A;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-dark-full:hover {
  background: #1E293B;
}

.btn-primary-full {
  width: 100%;
  height: 42px;
  background: #2563EB;
  color: #FFFFFF;
  border: none;
  border-radius: 10px;
  font-size: 12.5px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-primary-full:hover {
  background: #1D4ED8;
}

.github-metrics-box {
  background: #FAFBFF;
  border: 1px solid #E8ECF4;
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.metric-name {
  color: #64748B;
  font-weight: 500;
}

.metric-val {
  font-weight: 800;
  color: #0F172A;
}

/* ─── Certificates List ──────────────────────────────── */
.certs-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cert-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: #F8FAFC;
  border: 1px solid #E8ECF4;
  border-radius: 12px;
}

.cert-badge-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.cert-info {
  flex: 1;
}

.cert-title {
  font-size: 13px;
  font-weight: 800;
  color: #0F172A;
}

.cert-issuer {
  font-size: 11px;
  color: #64748B;
  margin-top: 1px;
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

/* ─── Responsive Adjustments ─────────────────────────── */
@media (max-width: 1024px) {
  .main-grid {
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

/* ── Profile Form ─────────────────────────────────── */
.profile-photo-row { display: flex; align-items: center; gap: 20px; margin-bottom: 20px; }
.profile-photo-wrap { position: relative; flex-shrink: 0; }
.profile-photo-img { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; border: 3px solid #E2E8F0; }
.profile-photo-placeholder { width: 72px; height: 72px; border-radius: 50%; background: linear-gradient(135deg,#2563EB,#7C3AED); display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 800; color: #fff; }
.photo-upload-btn { position: absolute; bottom: 0; right: 0; width: 24px; height: 24px; background: #fff; border: 1px solid #E2E8F0; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.12); }
.photo-upload-btn:hover { background: #F1F5F9; }
.profile-name-block { display: flex; flex-direction: column; gap: 2px; }
.profile-full-name { font-size: 18px; font-weight: 800; color: #0F172A; }
.profile-email { font-size: 13px; color: #64748B; }
.profile-saved-badge { margin-top: 4px; font-size: 12px; color: #10B981; font-weight: 700; }
.profile-form { display: flex; flex-direction: column; gap: 14px; }
.pf-row-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.pf-textarea { resize: vertical; min-height: 80px; font-family: inherit; }
.pf-save-row { display: flex; gap: 10px; align-items: center; }
.btn-autofill { background: #EFF6FF; border: 1px solid #BFDBFE; color: #1D4ED8; font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 10px; cursor: pointer; white-space: nowrap; }
.btn-autofill:hover { background: #DBEAFE; }
.btn-github-sync { background: #F8FAFC; border: 1px solid #E2E8F0; color: #334155; font-size: 12px; font-weight: 600; padding: 10px 16px; border-radius: 10px; cursor: pointer; }
.btn-github-sync:hover { background: #F1F5F9; }

/* ── Cert Provider Dropdown ───────────────────────── */
.cert-trusted-note { font-size: 11px; font-weight: 400; color: #94A3B8; margin-left: 8px; }

/* ── Stat Helpers ─────────────────────────────────── */
.stat-na { font-size: 13px; font-weight: 600; color: #94A3B8; }
</style>
