<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-brand">
        <span class="brand-logo">🚀</span>
        <h2>CareerPilot <span class="text-primary">AI</span></h2>
        <p class="auth-subtitle">Recruiter Portal Login</p>
      </div>

      <div v-if="errorMessage" class="auth-error-alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin">
        <AppInput
          v-model="email"
          label="Work Email"
          type="email"
          placeholder="name@company.com"
          required
        />

        <AppInput
          v-model="password"
          label="Password"
          type="password"
          placeholder="••••••••"
          required
        />

        <div class="auth-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>Remember me</span>
          </label>
          <a href="#" class="forgot-pass-link" @click.prevent="handleForgotPass">Forgot password?</a>
        </div>

        <AppButton
          type="submit"
          variant="primary"
          class="w-full mt-4"
          :loading="authStore.loading"
        >
          Login to CareerPilot AI
        </AppButton>
      </form>

      <div class="auth-footer">
        Don't have a recruiter account?
        <router-link to="/recruiter/register">Register Company</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'
import { useToast } from '@/components/common/AppToast.vue'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    const res = await authStore.login({
      email: email.value,
      password: password.value
    })
    toast.show(`Welcome back, ${res.data.full_name}!`)
    router.push('/recruiter/dashboard')
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || 'Login failed. Please check your credentials.'
  }
}

const handleForgotPass = () => {
  toast.show('Password reset link sent to your registered work email.', 'info')
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background);
  padding: 1.5rem;
}

.auth-card {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 440px;
  box-shadow: var(--shadow-md);
}

.auth-brand {
  text-align: center;
  margin-bottom: 2rem;
}

.brand-logo {
  font-size: 2.5rem;
}

.auth-brand h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 0.25rem;
}

.text-primary {
  color: var(--primary);
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

.auth-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.8125rem;
  margin-bottom: 1rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  cursor: pointer;
}

.forgot-pass-link {
  font-weight: 500;
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
</style>
