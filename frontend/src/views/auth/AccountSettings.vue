<template>
  <component :is="layoutComponent">
    <div class="settings-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Account Settings ⚙️</h1>
          <p class="page-subtitle">Manage your account credentials, email address, and security password.</p>
        </div>
      </div>

      <div class="settings-grid">
        <!-- Change Email Card -->
        <AppCard title="📧 Change Email Address" subtitle="Update your registered account email. Password verification required.">
          <form @submit.prevent="handleEmailSubmit">
            <div class="form-group">
              <label class="form-label">Current Email Address</label>
              <input type="text" :value="authStore.user?.email" class="form-input readonly-input" readonly />
            </div>

            <AppInput
              v-model="emailForm.new_email"
              label="New Email Address *"
              type="email"
              placeholder="new.email@careerpilot.ai"
              required
            />

            <AppInput
              v-model="emailForm.password"
              label="Current Password (to confirm identity) *"
              type="password"
              placeholder="••••••••"
              required
            />

            <div class="card-footer">
              <AppButton type="submit" variant="primary" :loading="emailLoading">
                Update Email
              </AppButton>
            </div>
          </form>
        </AppCard>

        <!-- Change Password Card -->
        <AppCard title="🔒 Change Password" subtitle="Ensure your account is using a strong, secure password.">
          <form @submit.prevent="handlePasswordSubmit">
            <AppInput
              v-model="passwordForm.current_password"
              label="Current Password *"
              type="password"
              placeholder="••••••••"
              required
            />

            <AppInput
              v-model="passwordForm.new_password"
              label="New Password *"
              type="password"
              placeholder="Minimum 6 characters"
              required
            />

            <AppInput
              v-model="passwordForm.confirm_password"
              label="Confirm New Password *"
              type="password"
              placeholder="Re-enter new password"
              required
            />

            <div class="card-footer">
              <AppButton type="submit" variant="primary" :loading="passwordLoading">
                Update Password
              </AppButton>
            </div>
          </form>
        </AppCard>
      </div>
    </div>
  </component>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import StudentLayout from '@/components/layout/StudentLayout.vue'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'
import { useToast } from '@/components/common/AppToast.vue'

const authStore = useAuthStore()
const toast = useToast()

const emailLoading = ref(false)
const passwordLoading = ref(false)

const emailForm = reactive({
  new_email: '',
  password: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const layoutComponent = computed(() => {
  const role = authStore.user?.role
  if (role === 'ADMIN') return AdminLayout
  if (role === 'STUDENT') return StudentLayout
  return DashboardLayout
})

const handleEmailSubmit = async () => {
  if (!emailForm.new_email.trim() || !emailForm.password) return

  emailLoading.value = true
  try {
    const res = await authStore.changeEmail({
      new_email: emailForm.new_email,
      password: emailForm.password
    })
    toast.show('✓ Email address updated successfully!')
    emailForm.new_email = ''
    emailForm.password = ''
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to update email address.', 'error')
  } finally {
    emailLoading.value = false
  }
}

const handlePasswordSubmit = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    toast.show('New password and confirmation password do not match.', 'error')
    return
  }

  if (passwordForm.new_password.length < 6) {
    toast.show('New password must be at least 6 characters long.', 'error')
    return
  }

  passwordLoading.value = true
  try {
    await authStore.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })
    toast.show('✓ Password updated successfully!')
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to update password.', 'error')
  } finally {
    passwordLoading.value = false
  }
}
</script>

<style scoped>
.settings-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.settings-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.5rem; }
.readonly-input { background-color: var(--background); color: var(--text-muted); cursor: not-allowed; }
.card-footer { margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; }
</style>
