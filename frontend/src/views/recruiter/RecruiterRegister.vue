<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-brand">
        <span class="brand-logo">🏢</span>
        <h2>Register Company</h2>
        <p class="auth-subtitle">Create your CareerPilot AI Recruiter account</p>
      </div>

      <div v-if="errorMessage" class="auth-error-alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleRegister">
        <AppInput
          v-model="form.full_name"
          label="Full Name"
          placeholder="e.g. Sensha"
          required
        />

        <AppInput
          v-model="form.email"
          label="Work Email"
          type="email"
          placeholder="sensha@company.com"
          required
        />

        <AppInput
          v-model="form.password"
          label="Password (min 8 chars)"
          type="password"
          placeholder="••••••••"
          required
          :hint="passwordStrengthHint"
        />

        <div class="form-row">
          <AppInput
            v-model="form.phone"
            label="Phone Number"
            placeholder="+91 98765 43210"
          />

          <AppInput
            v-model="form.designation"
            label="Designation"
            placeholder="e.g. Senior Recruiter"
          />
        </div>

        <AppInput
          v-model="form.company_name"
          label="Company Name"
          placeholder="e.g. CareerPilot Technologies"
          required
        />

        <AppInput
          v-model="form.company_website"
          label="Company Website (Optional)"
          placeholder="https://company.com"
        />

        <AppButton
          type="submit"
          variant="primary"
          class="w-full mt-4"
          :loading="authStore.loading"
        >
          Register & Continue to Dashboard
        </AppButton>
      </form>

      <div class="auth-footer">
        Already registered?
        <router-link to="/recruiter/login">Login here</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'
import { useToast } from '@/components/common/AppToast.vue'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  full_name: '',
  email: '',
  password: '',
  phone: '',
  designation: 'Senior Recruiter',
  company_name: '',
  company_website: ''
})

const errorMessage = ref('')

const passwordStrengthHint = computed(() => {
  if (!form.password) return 'Minimum 8 characters required.'
  if (form.password.length < 8) return 'Password too short (at least 8 characters).'
  return 'Password strength: Strong ✓'
})

const handleRegister = async () => {
  errorMessage.value = ''
  if (form.password.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long.'
    return
  }

  try {
    const res = await authStore.register(form)
    toast.show('Registration successful! Your company verification is pending.')
    router.push('/recruiter/dashboard')
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || 'Registration failed. Please check form details.'
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background);
  padding: 2rem 1rem;
}

.auth-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 520px;
  box-shadow: var(--shadow-md);
}

.auth-brand {
  text-align: center;
  margin-bottom: 1.5rem;
}

.brand-logo {
  font-size: 2.25rem;
}

.auth-brand h2 {
  font-size: 1.375rem;
  font-weight: 700;
  margin-top: 0.25rem;
}

.auth-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

.auth-error-alert {
  background-color: var(--danger-bg);
  border: 1px solid var(--danger-border);
  color: var(--danger);
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.8125rem;
  margin-bottom: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.w-full { width: 100%; }
.mt-4 { margin-top: 1rem; }

.auth-footer {
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
}

.auth-footer a {
  font-weight: 600;
  margin-left: 0.25rem;
}

@media (max-width: 640px) {
  .form-row { grid-template-columns: 1fr; }
}
</style>
