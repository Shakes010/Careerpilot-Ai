<template>
  <div class="auth-root">
    
    <!-- Background Ambient Elements -->
    <div class="ambient-glow ambient-glow--1"></div>
    <div class="ambient-glow ambient-glow--2"></div>

    <div class="auth-container">
      
      <!-- Top Brand Header -->
      <div class="auth-brand-bar">
        <router-link to="/" class="brand-link">
          <div class="brand-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M3 12l19-9-9 19-2-8-8-2z" />
            </svg>
          </div>
          <span class="brand-text">CareerPilot <em>AI</em></span>
        </router-link>
        <div class="brand-pill">Enterprise Career Intelligence</div>
      </div>

      <!-- Main Authentic Card -->
      <div class="auth-card">
        
        <!-- Left Showcase Panel (Classy Executive Gradient) -->
        <div class="showcase-panel">
          <div class="showcase-content">
            <div class="badge-featured">Verified Talent Network</div>
            
            <h1 class="showcase-headline" v-if="!isRegister">
              Propel your career with <span class="text-gradient">evidence-based</span> intelligence.
            </h1>
            <h1 class="showcase-headline" v-else>
              Join the next generation of <span class="text-gradient">verified builders</span>.
            </h1>

            <p class="showcase-desc">
              CareerPilot AI connects verified student competency directly with top recruiting pipelines, cutting out recruitment noise with cryptographically verifiable proofs.
            </p>

            <!-- Value Highlights -->
            <div class="value-stack">
              <div class="value-item">
                <div class="value-icon-box">
                  <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <div>
                  <div class="value-title">Skill Trust Meter™</div>
                  <div class="value-sub">Weighted Noisy-OR evidence verification</div>
                </div>
              </div>

              <div class="value-item">
                <div class="value-icon-box">
                  <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
                    <rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                  </svg>
                </div>
                <div>
                  <div class="value-title">Semantic Opportunity Radar</div>
                  <div class="value-sub">Vector-matched internships &amp; high-impact roles</div>
                </div>
              </div>

              <div class="value-item">
                <div class="value-icon-box">
                  <svg width="18" height="18" fill="none" stroke="#2563EB" viewBox="0 0 24 24" stroke-width="2">
                    <polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                  </svg>
                </div>
                <div>
                  <div class="value-title">Anti-Cheat Code Checkpoints</div>
                  <div class="value-sub">Automated live execution with real-time telemetry</div>
                </div>
              </div>
            </div>

            <!-- Testimonial/Metrics Card -->
            <div class="showcase-stats">
              <div class="stat-pill">
                <span class="stat-number">98.4%</span>
                <span class="stat-desc">ATS Parsing Precision</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-pill">
                <span class="stat-number">10k+</span>
                <span class="stat-desc">Verified Students</span>
              </div>
            </div>

          </div>
        </div>

        <!-- Right Form Panel -->
        <div class="form-panel">
          
          <!-- Mode Tabs (Login / Sign Up) -->
          <div class="mode-switcher">
            <button
              type="button"
              @click="switchMode(false)"
              :class="['mode-btn', !isRegister && 'mode-btn--active']"
            >
              Sign In
            </button>
            <button
              type="button"
              @click="switchMode(true)"
              :class="['mode-btn', isRegister && 'mode-btn--active']"
            >
              Create Account
            </button>
          </div>

          <!-- Form Header -->
          <div class="form-title-group">
            <h2 class="form-heading">{{ isRegister ? 'Create Your Account' : 'Welcome Back' }}</h2>
            <p class="form-subtext">
              {{ isRegister ? 'Register to start building your verified Career Passport.' : 'Sign in to access your personalized career hub.' }}
            </p>
          </div>

          <!-- Banner Error Notification -->
          <transition name="fade">
            <div v-if="errorMsg" class="error-banner">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <span>{{ errorMsg }}</span>
            </div>
          </transition>

          <!-- ─── LOGIN FORM ───────────────────────────── -->
          <form v-if="!isRegister" @submit.prevent="handleLogin" class="form-body" novalidate>
            
            <!-- Email -->
            <div class="form-group">
              <label class="form-label" for="login-email">Email Address</label>
              <div class="input-wrap" :class="{ 'input-wrap--invalid': loginErrors.email }">
                <span class="input-icon">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
                  </svg>
                </span>
                <input
                  id="login-email"
                  v-model="loginEmail"
                  type="email"
                  placeholder="name@example.com"
                  class="field-control"
                  @blur="validateLoginEmail"
                />
              </div>
              <span v-if="loginErrors.email" class="error-hint">{{ loginErrors.email }}</span>
            </div>

            <!-- Password -->
            <div class="form-group">
              <div class="label-with-link">
                <label class="form-label" for="login-password">Password</label>
                <span class="hint-text">Demo password auto-filled</span>
              </div>
              <div class="input-wrap" :class="{ 'input-wrap--invalid': loginErrors.password }">
                <span class="input-icon">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                </span>
                <input
                  id="login-password"
                  v-model="loginPassword"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Enter password"
                  class="field-control"
                  @blur="validateLoginPassword"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="pw-toggle-btn"
                  aria-label="Toggle password"
                >
                  <svg v-if="!showPassword" width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
              <span v-if="loginErrors.password" class="error-hint">{{ loginErrors.password }}</span>
            </div>

            <!-- Remember me row -->
            <div class="form-row-actions">
              <label class="checkbox-label">
                <input v-model="rememberMe" type="checkbox" class="styled-checkbox" />
                <span>Remember this workstation</span>
              </label>
            </div>

            <!-- Submit CTA -->
            <button
              type="submit"
              :disabled="loading"
              class="btn-submit"
            >
              <span v-if="loading" class="spinner"></span>
              <span v-else>Login →</span>
            </button>

            <!-- Social Logins -->
            <div class="divider-label">
              <span>Or sign in with</span>
            </div>

            <div class="social-row">
              <button type="button" @click="handleSocialLogin('Google')" class="btn-social">
                <svg width="16" height="16" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/>
                  <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"/>
                  <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.99 0 12s.45 3.82 1.25 5.42l4.03-3.15z"/>
                  <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"/>
                </svg>
                <span>Google</span>
              </button>

              <button type="button" @click="handleSocialLogin('LinkedIn')" class="btn-social">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="#0A66C2">
                  <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
                <span>LinkedIn</span>
              </button>
            </div>

          </form>

          <!-- ─── SIGNUP FORM WITH STRICT NAME & INPUT VALIDATION ──── -->
          <form v-else @submit.prevent="handleRegister" class="form-body" novalidate>
            
            <!-- Full Name (Strict: NO INTEGERS/DIGITS) -->
            <div class="form-group">
              <label class="form-label" for="reg-fullname">
                Full Name <span class="required-star">*</span>
              </label>
              <div class="input-wrap" :class="{ 'input-wrap--invalid': regErrors.fullName, 'input-wrap--valid': regFullName && !regErrors.fullName }">
                <span class="input-icon">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                  </svg>
                </span>
                <input
                  id="reg-fullname"
                  v-model="regFullName"
                  type="text"
                  placeholder="e.g. Alexander Rivera"
                  class="field-control"
                  @input="validateFullNameOnInput"
                  @blur="validateFullName"
                />
                <span v-if="regFullName && !regErrors.fullName" class="valid-mark">✓</span>
              </div>
              <span v-if="regErrors.fullName" class="error-hint">
                {{ regErrors.fullName }}
              </span>
              <span v-else class="field-hint">
                Letters, spaces, hyphens, and apostrophes only (no numbers).
              </span>
            </div>

            <!-- Email -->
            <div class="form-group">
              <label class="form-label" for="reg-email">
                Email Address <span class="required-star">*</span>
              </label>
              <div class="input-wrap" :class="{ 'input-wrap--invalid': regErrors.email, 'input-wrap--valid': regEmail && !regErrors.email }">
                <span class="input-icon">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>
                  </svg>
                </span>
                <input
                  id="reg-email"
                  v-model="regEmail"
                  type="email"
                  placeholder="name@university.edu"
                  class="field-control"
                  @blur="validateRegEmail"
                />
                <span v-if="regEmail && !regErrors.email" class="valid-mark">✓</span>
              </div>
              <span v-if="regErrors.email" class="error-hint">{{ regErrors.email }}</span>
            </div>

            <!-- Phone Number -->
            <div class="form-group">
              <label class="form-label" for="reg-phone">
                Contact Phone <span class="text-slate-400 font-normal">(for recruiter interview reachouts)</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                  </svg>
                </span>
                <input
                  id="reg-phone"
                  v-model="regPhone"
                  type="tel"
                  placeholder="+91 98765 43210"
                  class="field-control"
                />
              </div>
            </div>

            <!-- Password & Confirm Password in 2-Col -->
            <div class="grid-2col">
              <div class="form-group">
                <label class="form-label" for="reg-password">
                  Password <span class="required-star">*</span>
                </label>
                <div class="input-wrap" :class="{ 'input-wrap--invalid': regErrors.password }">
                  <input
                    id="reg-password"
                    v-model="regPassword"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Min 6 characters"
                    class="field-control field-control--no-left-icon"
                    @blur="validateRegPassword"
                  />
                </div>
                <span v-if="regErrors.password" class="error-hint">{{ regErrors.password }}</span>
              </div>

              <div class="form-group">
                <label class="form-label" for="reg-confirm">
                  Confirm Password <span class="required-star">*</span>
                </label>
                <div class="input-wrap" :class="{ 'input-wrap--invalid': regErrors.confirmPassword }">
                  <input
                    id="reg-confirm"
                    v-model="regConfirmPassword"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Re-enter password"
                    class="field-control field-control--no-left-icon"
                    @blur="validateConfirmPassword"
                  />
                </div>
                <span v-if="regErrors.confirmPassword" class="error-hint">{{ regErrors.confirmPassword }}</span>
              </div>
            </div>

            <!-- Student Profile Details: Strictly IT/CS & Recent Passouts -->
            <div v-if="selectedUserRole === 'student'" class="student-eligibility-block">
              <div class="eligibility-notice">
                <span class="eligibility-icon">🎯</span>
                <div class="eligibility-text">
                  <div class="eligibility-title">Exclusive IT &amp; Computer Science Portal</div>
                  <div class="eligibility-sub">Platform restricted to students and recent graduates with an IT background (Classes 2023–2028).</div>
                </div>
              </div>

              <div class="grid-2col">
                <div class="form-group">
                  <label class="form-label">Degree / Program <span class="required-star">*</span></label>
                  <select v-model="regDegree" class="select-control">
                    <option value="B.Tech Computer Science">B.Tech Computer Science &amp; Eng (CSE)</option>
                    <option value="B.Tech Information Technology">B.Tech Information Technology (IT)</option>
                    <option value="BCA">BCA (Bachelor of Computer Apps)</option>
                    <option value="MCA">MCA (Master of Computer Apps)</option>
                    <option value="B.Tech Data Science & AI">B.Tech Data Science &amp; AI</option>
                    <option value="B.E. Software Engineering">B.E. Software Engineering</option>
                    <option value="M.Tech Computer Science">M.Tech Computer Science / IT</option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">Graduation Year <span class="required-star">*</span></label>
                  <select v-model.number="regGradYear" class="select-control">
                    <option :value="2023">2023 (Recent Graduate)</option>
                    <option :value="2024">2024 (Recent Graduate)</option>
                    <option :value="2025">2025 (Recent Graduate / Final Year)</option>
                    <option :value="2026">2026 (Graduating Batch)</option>
                    <option :value="2027">2027 (Pre-Final Year)</option>
                    <option :value="2028">2028 (Undergraduate)</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Terms agreement -->
            <div class="form-group">
              <label class="checkbox-label">
                <input v-model="agreeTerms" type="checkbox" class="styled-checkbox" />
                <span>I accept the Terms of Service and Privacy Policy</span>
              </label>
              <span v-if="regErrors.terms" class="error-hint">{{ regErrors.terms }}</span>
            </div>

            <!-- Submit Registration -->
            <button
              type="submit"
              :disabled="loading"
              class="btn-submit"
            >
              <span v-if="loading" class="spinner"></span>
              <span v-else>Create Account →</span>
            </button>

          </form>

        </div>

      </div>

      <!-- Trust Footer -->
      <div class="auth-footer">
        <div class="trust-badge">
          <span class="trust-dot"></span>
          <span>End-to-End Encrypted Authentication</span>
        </div>
        <div class="trust-badge">
          <span class="trust-dot"></span>
          <span>Zero Knowledge Resume Privacy</span>
        </div>
        <div class="trust-badge">
          <span class="trust-dot"></span>
          <span>Verified University &amp; Recruiter Network</span>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../store'
import { apiFetch } from '../services/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isRegister = ref(false)
const loading = ref(false)
const showPassword = ref(false)
const errorMsg = ref('')

const rememberMe = ref(true)
const agreeTerms = ref(true)

// User role: STRICTLY Student or Recruiter (Admin REMOVED from public UI)
const selectedUserRole = ref('student')

// Login form state
const loginEmail = ref('')
const loginPassword = ref('')
const loginErrors = reactive({
  email: '',
  password: ''
})

// Registration form state
const regFullName = ref('')
const regEmail = ref('')
const regPhone = ref('')
const regPassword = ref('')
const regConfirmPassword = ref('')
const regDegree = ref('B.Tech Computer Science')
const regGradYear = ref(2026)
const regErrors = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: ''
})

onMounted(() => {
  if (route.query.signup === 'true') {
    isRegister.value = true
  }
  if (route.query.role === 'recruiter') {
    selectRole('recruiter')
  } else {
    selectRole('student')
  }
})

const switchMode = (toRegister) => {
  isRegister.value = toRegister
  errorMsg.value = ''
}

const selectRole = (role) => {
  if (role !== 'student' && role !== 'recruiter') {
    role = 'student'
  }
  selectedUserRole.value = role
  errorMsg.value = ''
  
  // Set default demo credentials according to role
  if (role === 'recruiter') {
    loginEmail.value = 'recruiter@careerpilot.ai'
    loginPassword.value = 'recruiter123'
  } else {
    loginEmail.value = 'student@careerpilot.ai'
    loginPassword.value = 'student123'
  }
}

// ─── VALIDATION ENGINE ─────────────────────────────────

// Name validation: Strictly NO INTEGERS/NUMBERS allowed
const validateFullNameOnInput = () => {
  const value = regFullName.value
  if (/\d/.test(value)) {
    regErrors.fullName = 'Full Name cannot contain numbers or digits.'
  } else {
    regErrors.fullName = ''
  }
}

const validateFullName = () => {
  const name = regFullName.value.trim()
  if (!name) {
    regErrors.fullName = 'Full name is required.'
    return false
  }
  if (/\d/.test(name)) {
    regErrors.fullName = 'Full name cannot contain numbers or digits.'
    return false
  }
  // Allow letters, spaces, hyphens, periods, apostrophes
  const nameRegex = /^[a-zA-Z\s.'-]+$/
  if (!nameRegex.test(name)) {
    regErrors.fullName = 'Full name contains invalid special characters.'
    return false
  }
  if (name.length < 2) {
    regErrors.fullName = 'Full name must be at least 2 characters.'
    return false
  }
  regErrors.fullName = ''
  return true
}

const validateEmailFormat = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const validateLoginEmail = () => {
  if (!loginEmail.value.trim()) {
    loginErrors.email = 'Email address is required.'
    return false
  }
  if (!validateEmailFormat(loginEmail.value.trim())) {
    loginErrors.email = 'Please enter a valid email address.'
    return false
  }
  loginErrors.email = ''
  return true
}

const validateLoginPassword = () => {
  if (!loginPassword.value) {
    loginErrors.password = 'Password is required.'
    return false
  }
  loginErrors.password = ''
  return true
}

const validateRegEmail = () => {
  if (!regEmail.value.trim()) {
    regErrors.email = 'Email address is required.'
    return false
  }
  if (!validateEmailFormat(regEmail.value.trim())) {
    regErrors.email = 'Please enter a valid email address.'
    return false
  }
  regErrors.email = ''
  return true
}

const validateRegPassword = () => {
  if (!regPassword.value) {
    regErrors.password = 'Password is required.'
    return false
  }
  if (regPassword.value.length < 6) {
    regErrors.password = 'Password must be at least 6 characters long.'
    return false
  }
  regErrors.password = ''
  return true
}

const validateConfirmPassword = () => {
  if (!regConfirmPassword.value) {
    regErrors.confirmPassword = 'Confirming your password is required.'
    return false
  }
  if (regPassword.value !== regConfirmPassword.value) {
    regErrors.confirmPassword = 'Passwords do not match.'
    return false
  }
  regErrors.confirmPassword = ''
  return true
}

// ─── LOGIN ACTION ──────────────────────────────────────
const handleLogin = async () => {
  errorMsg.value = ''
  const isEmailValid = validateLoginEmail()
  const isPwValid = validateLoginPassword()

  if (!isEmailValid || !isPwValid) {
    return
  }

  loading.value = true
  try {
    const res = await apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email: loginEmail.value.trim(),
        password: loginPassword.value
      })
    })

    authStore.setAuth(res)

    // Direct user according to their verified role from database
    if (res.role === 'admin') {
      router.push('/admin')
    } else if (res.role === 'recruiter') {
      router.push('/recruiter')
    } else {
      router.push('/dashboard')
    }
  } catch (err) {
    errorMsg.value = err.message || 'Invalid email or password. Please verify credentials.'
  } finally {
    loading.value = false
  }
}

// ─── REGISTRATION ACTION ───────────────────────────────
const handleRegister = async () => {
  errorMsg.value = ''
  
  const isNameValid = validateFullName()
  const isEmailValid = validateRegEmail()
  const isPwValid = validateRegPassword()
  const isConfirmValid = validateConfirmPassword()

  if (!agreeTerms.value) {
    regErrors.terms = 'You must accept the terms and privacy policy to continue.'
  } else {
    regErrors.terms = ''
  }

  if (!isNameValid || !isEmailValid || !isPwValid || !isConfirmValid || !agreeTerms.value) {
    return
  }

  // Strict student eligibility validation (IT background & recent years)
  if (selectedUserRole.value === 'student') {
    if (!regDegree.value || !regGradYear.value || regGradYear.value < 2023 || regGradYear.value > 2028) {
      errorMsg.value = 'CareerPilot AI is strictly reserved for students & recent graduates with an IT/CS background (Classes of 2023–2028).'
      return
    }
  }

  loading.value = true
  try {
    const payload = {
      email: regEmail.value.trim(),
      password: regPassword.value,
      role: selectedUserRole.value,
      full_name: regFullName.value.trim(),
      phone: regPhone.value.trim() || '+91 98765 43210',
      degree: selectedUserRole.value === 'student' ? regDegree.value : 'Professional Recruiter',
      graduation_year: selectedUserRole.value === 'student' ? regGradYear.value : 2024
    }

    const res = await apiFetch('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload)
    })

    authStore.setAuth(res)

    if (res.role === 'admin') {
      router.push('/admin')
    } else if (res.role === 'recruiter') {
      router.push('/recruiter')
    } else {
      router.push('/dashboard')
    }
  } catch (err) {
    errorMsg.value = err.message || 'Registration failed. Please check your details.'
  } finally {
    loading.value = false
  }
}

const handleSocialLogin = (provider) => {
  errorMsg.value = `${provider} authentication initialized in sandbox preview mode.`
}
</script>

<style scoped>
/* ─── Page Container ─────────────────────────────────── */
.auth-root {
  min-height: 100vh;
  width: 100%;
  background-color: #F8FAFC;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Ambient glow accents */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(80px);
  z-index: 0;
}

.ambient-glow--1 {
  width: 500px;
  height: 500px;
  top: -150px;
  left: -150px;
  background: rgba(37, 99, 235, 0.08);
}

.ambient-glow--2 {
  width: 450px;
  height: 450px;
  bottom: -100px;
  right: -100px;
  background: rgba(99, 102, 241, 0.08);
}

.auth-container {
  width: 100%;
  max-width: 1140px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  z-index: 1;
}

/* ─── Top Brand Bar ──────────────────────────────────── */
.auth-brand-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 4px;
}

.brand-link {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #2563EB;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
  flex-shrink: 0;
}

.brand-text {
  font-size: 20px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.4px;
}

.brand-text em {
  font-style: normal;
  color: #2563EB;
}

.brand-pill {
  font-size: 11px;
  font-weight: 700;
  color: #475569;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  padding: 6px 14px;
  border-radius: 9999px;
  letter-spacing: 0.2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

/* ─── Main Two-Column Card ───────────────────────────── */
.auth-card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 28px;
  box-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.06), 0 4px 16px -2px rgba(15, 23, 42, 0.03);
  display: grid;
  grid-template-columns: 1fr;
  overflow: hidden;
}

@media (min-width: 960px) {
  .auth-card {
    grid-template-columns: 5fr 6fr;
  }
}

/* ─── Left Showcase Panel ────────────────────────────── */
.showcase-panel {
  background: linear-gradient(145deg, #0F172A 0%, #1E293B 45%, #1E3A8A 100%);
  padding: 48px 44px;
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.showcase-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.badge-featured {
  display: inline-block;
  align-self: flex-start;
  padding: 5px 14px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #93C5FD;
  backdrop-filter: blur(8px);
}

.showcase-headline {
  font-size: 32px;
  font-weight: 900;
  line-height: 1.25;
  letter-spacing: -0.6px;
  color: #FFFFFF;
}

.text-gradient {
  background: linear-gradient(135deg, #60A5FA 0%, #93C5FD 50%, #C7D2FE 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.showcase-desc {
  font-size: 13.5px;
  line-height: 1.65;
  color: #CBD5E1;
  max-width: 440px;
}

.value-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-top: 8px;
}

.value-item {
  display: flex;
  align-items: center;
  gap: 14px;
}

.value-icon-box {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #93C5FD;
}

.value-title {
  font-size: 13px;
  font-weight: 800;
  color: #FFFFFF;
}

.value-sub {
  font-size: 11.5px;
  color: #94A3B8;
  margin-top: 1px;
}

.showcase-stats {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  margin-top: 12px;
}

.stat-pill {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 22px;
  font-weight: 900;
  color: #FFFFFF;
  line-height: 1;
}

.stat-desc {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 600;
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 32px;
  background: rgba(255, 255, 255, 0.15);
}

/* ─── Right Form Panel ───────────────────────────────── */
.form-panel {
  padding: 44px 40px;
  background: #FFFFFF;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* Mode Switcher (Sign In vs Create Account) */
.mode-switcher {
  display: flex;
  background: #F1F5F9;
  padding: 4px;
  border-radius: 14px;
  gap: 4px;
}

.mode-btn {
  flex: 1;
  height: 38px;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  color: #64748B;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mode-btn--active {
  background: #FFFFFF;
  color: #0F172A;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

/* Title */
.form-title-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-heading {
  font-size: 22px;
  font-weight: 900;
  color: #0F172A;
  letter-spacing: -0.3px;
}

.form-subtext {
  font-size: 12.5px;
  color: #64748B;
}

/* Role Selector Pills (Student & Recruiter only) */
.role-selector-wrap {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.role-field-label {
  font-size: 11px;
  font-weight: 800;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.6px;
}

.role-pills-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.role-pill {
  padding: 10px 14px;
  background: #F8FAFC;
  border: 1.5px solid #E2E8F0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.role-pill:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
}

.role-pill--active {
  background: #EFF6FF !important;
  border-color: #2563EB !important;
  box-shadow: 0 0 0 1px #2563EB;
}

.role-emoji {
  font-size: 16px;
}

.role-pill-text {
  font-size: 12px;
  font-weight: 700;
  color: #0F172A;
}

.role-pill--active .role-pill-text {
  color: #2563EB;
}

/* Error Banner */
.error-banner {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #DC2626;
  font-size: 12px;
  font-weight: 600;
  padding: 10px 14px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ─── Form Controls ──────────────────────────────────── */
.form-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-with-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-label {
  font-size: 12.5px;
  font-weight: 700;
  color: #1E293B;
}

.required-star {
  color: #EF4444;
}

.hint-text {
  font-size: 11px;
  color: #94A3B8;
  font-weight: 500;
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #94A3B8;
  pointer-events: none;
  display: flex;
  align-items: center;
}

.field-control {
  width: 100%;
  height: 44px;
  padding: 0 14px 0 40px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 12px;
  font-size: 13.5px;
  color: #0F172A;
  outline: none;
  font-family: inherit;
  transition: all 0.15s ease;
  box-sizing: border-box;
}

.field-control--no-left-icon {
  padding-left: 14px;
}

.field-control:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.input-wrap--invalid .field-control {
  border-color: #EF4444 !important;
  background-color: #FFFDFD;
}

.input-wrap--invalid .field-control:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
}

.input-wrap--valid .field-control {
  border-color: #10B981;
}

.valid-mark {
  position: absolute;
  right: 14px;
  color: #10B981;
  font-weight: 800;
  font-size: 13px;
  pointer-events: none;
}

.pw-toggle-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #94A3B8;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}

.pw-toggle-btn:hover {
  color: #475569;
}

.select-control {
  width: 100%;
  height: 44px;
  padding: 0 14px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  color: #0F172A;
  outline: none;
  cursor: pointer;
  transition: border-color 0.15s ease;
}

.select-control:focus {
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.error-hint {
  font-size: 11.5px;
  color: #DC2626;
  font-weight: 600;
}

.field-hint {
  font-size: 11px;
  color: #64748B;
}

.grid-2col {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

@media (min-width: 500px) {
  .grid-2col {
    grid-template-columns: 1fr 1fr;
  }
}

/* Student Eligibility Notice */
.student-eligibility-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.eligibility-notice {
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 12px;
  padding: 10px 14px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.eligibility-icon {
  font-size: 16px;
  flex-shrink: 0;
  margin-top: 1px;
}

.eligibility-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.eligibility-title {
  font-size: 12px;
  font-weight: 800;
  color: #1E40AF;
}

.eligibility-sub {
  font-size: 11px;
  color: #3B82F6;
  line-height: 1.4;
}

/* Checkbox */
.form-row-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
}

.styled-checkbox {
  width: 15px;
  height: 15px;
  accent-color: #2563EB;
  cursor: pointer;
}

/* Submit CTA */
.btn-submit {
  width: 100%;
  height: 46px;
  background: #2563EB;
  color: #FFFFFF;
  font-size: 13.5px;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.28);
  transition: all 0.15s ease;
}

.btn-submit:hover {
  background: #1D4ED8;
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

.btn-submit:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #FFFFFF;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Dividers */
.divider-label {
  position: relative;
  text-align: center;
  margin: 4px 0;
}

.divider-label::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background: #E2E8F0;
}

.divider-label span {
  position: relative;
  background: #FFFFFF;
  padding: 0 12px;
  font-size: 11px;
  font-weight: 700;
  color: #94A3B8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Social Buttons */
.social-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.btn-social {
  height: 42px;
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-social:hover {
  background: #F8FAFC;
  border-color: #CBD5E1;
}

/* ─── Trust Footer Bar ───────────────────────────────── */
.auth-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  padding: 6px 0;
}

.trust-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11.5px;
  font-weight: 600;
  color: #64748B;
}

.trust-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10B981;
}

/* ─── Fade Transition ────────────────────────────────── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
