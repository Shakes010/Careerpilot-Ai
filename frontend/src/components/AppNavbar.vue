<template>
  <header class="bg-white border-b border-[#E5E7EB] sticky top-0 z-50 px-6 py-3 flex items-center justify-between shadow-xs">
    <!-- Paper Plane Line Logo Mark + CareerPilot in #0F172A + AI in #2563EB -->
    <div class="flex items-center gap-8">
      <router-link :to="homeRoute" class="flex items-center gap-2.5 text-decoration-none">
        <div class="w-9 h-9 rounded-lg bg-[#EFF6FF] flex items-center justify-center text-[#2563EB] border border-blue-100 shrink-0" style="width: 36px; height: 36px;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l19-9-9 19-2-8-8-2z" />
          </svg>
        </div>
        <div class="text-xl font-extrabold tracking-tight flex items-center">
          <span class="text-[#0F172A]">CareerPilot</span>
          <span class="text-[#2563EB] ml-0.5">AI</span>
        </div>
      </router-link>

      <!-- Role-Scoped Navigation Links -->
      <nav v-if="authStore.isAuthenticated" class="hidden md:flex items-center gap-1">
        <!-- Student Only Navigation -->
        <template v-if="authStore.role === 'student'">
          <router-link to="/" class="nav-item" :class="{ 'nav-active': $route.path === '/' }">Dashboard</router-link>
          <router-link to="/passport" class="nav-item" :class="{ 'nav-active': $route.path === '/passport' }">Career Passport</router-link>
          <router-link to="/skills" class="nav-item" :class="{ 'nav-active': $route.path === '/skills' }">Skill Trust Meter</router-link>
          <router-link to="/assessments" class="nav-item" :class="{ 'nav-active': $route.path === '/assessments' }">Assessments</router-link>
          <router-link to="/opportunities" class="nav-item" :class="{ 'nav-active': $route.path === '/opportunities' }">Opportunity Radar</router-link>
          <router-link to="/projects" class="nav-item" :class="{ 'nav-active': $route.path === '/projects' }">Project Sandbox</router-link>
        </template>

        <!-- Recruiter Only Navigation -->
        <template v-else-if="authStore.role === 'recruiter'">
          <router-link to="/recruiter" class="nav-item" :class="{ 'nav-active': $route.path === '/recruiter' }">Recruiter Workspace</router-link>
          <router-link to="/billing" class="nav-item" :class="{ 'nav-active': $route.path === '/billing' }">Plans & Billing</router-link>
        </template>

        <!-- Admin Only Navigation -->
        <template v-else-if="authStore.role === 'admin'">
          <router-link to="/admin" class="nav-item" :class="{ 'nav-active': $route.path === '/admin' }">Admin Moderation Suite</router-link>
        </template>
      </nav>
    </div>

    <!-- User Profile & Actions -->
    <div v-if="authStore.isAuthenticated" class="flex items-center gap-3">
      <div class="text-right text-xs hidden sm:block">
        <div class="font-bold text-[#0F172A]">{{ authStore.userFullName }}</div>
        <div class="text-[#6B7280] capitalize">{{ authStore.role }} Account</div>
      </div>

      <!-- Account Settings Button -->
      <button @click="showSettingsModal = true" class="cp-btn-secondary text-xs px-3 py-1.5 h-9 min-h-9 flex items-center gap-1">
        <span>⚙️ Settings</span>
      </button>

      <button @click="handleLogout" class="cp-btn-secondary text-xs px-3 py-1.5 h-9 min-h-9 text-red-600 border-red-200 hover:bg-red-50">
        Logout
      </button>
    </div>
  </header>

  <!-- Account Settings Modal -->
  <div v-if="showSettingsModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4">
    <div class="cp-card max-w-md w-full space-y-4">
      <div class="flex items-center justify-between border-b border-[#E5E7EB] pb-2">
        <h3 class="text-base font-bold text-[#0F172A]">Account Settings</h3>
        <button @click="showSettingsModal = false" class="text-gray-400 hover:text-gray-600 font-bold">✕</button>
      </div>

      <div v-if="statusMsg" class="p-3 rounded-lg text-xs" :class="isSuccess ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'">
        {{ statusMsg }}
      </div>

      <form @submit.prevent="updateAccount" class="space-y-3.5 text-xs">
        <div>
          <label class="block font-semibold mb-1 text-[#0F172A]">Full Name</label>
          <input v-model="editFullName" type="text" required class="cp-input" />
        </div>

        <div>
          <label class="block font-semibold mb-1 text-[#0F172A]">Email Address</label>
          <input v-model="editEmail" type="email" required class="cp-input" />
        </div>

        <div class="pt-2 border-t border-[#E5E7EB] space-y-2">
          <div class="font-bold text-[#0F172A]">Change Password (Optional)</div>
          <div>
            <label class="block font-semibold mb-1 text-[#6B7280]">Current Password</label>
            <input v-model="currentPassword" type="password" placeholder="Required if changing password" class="cp-input" />
          </div>
          <div>
            <label class="block font-semibold mb-1 text-[#6B7280]">New Password</label>
            <input v-model="newPassword" type="password" placeholder="Enter new password" class="cp-input" />
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-3 border-t border-[#E5E7EB]">
          <button type="button" @click="showSettingsModal = false" class="cp-btn-secondary text-xs">Cancel</button>
          <button type="submit" class="cp-btn-primary text-xs">Save Account Changes</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '../store'
import { useRouter } from 'vue-router'
import { apiFetch } from '../services/api'

const authStore = useAuthStore()
const router = useRouter()

const showSettingsModal = ref(false)
const editFullName = ref(authStore.userFullName || '')
const editEmail = ref(authStore.user?.email || '')
const currentPassword = ref('')
const newPassword = ref('')

const statusMsg = ref('')
const isSuccess = ref(false)

const homeRoute = computed(() => {
  if (authStore.role === 'admin') return '/admin'
  if (authStore.role === 'recruiter') return '/recruiter'
  return '/'
})

watch(() => authStore.user, (u) => {
  if (u) {
    editFullName.value = u.full_name || ''
    editEmail.value = u.email || ''
  }
}, { immediate: true })

const updateAccount = async () => {
  statusMsg.value = ''
  isSuccess.value = false
  try {
    const body = {
      full_name: editFullName.value,
      email: editEmail.value
    }
    if (newPassword.value) {
      body.current_password = currentPassword.value
      body.new_password = newPassword.value
    }

    const res = await apiFetch('/auth/account-settings', {
      method: 'PUT',
      body: JSON.stringify(body)
    })

    authStore.user.full_name = res.full_name
    authStore.user.email = res.email
    localStorage.setItem('cp_user', JSON.stringify(authStore.user))

    statusMsg.value = res.message || 'Settings updated successfully!'
    isSuccess.value = true
    currentPassword.value = ''
    newPassword.value = ''

    setTimeout(() => {
      showSettingsModal.value = false
      statusMsg.value = ''
    }, 1500)
  } catch (err) {
    statusMsg.value = err.message || 'Update failed'
    isSuccess.value = false
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Scoped refinements only — base .nav-item and .nav-active are in style.css */
header {
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-xs);
}

.nav-item {
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  font-size: 13.5px;
  font-weight: 500;
  color: var(--color-text-body);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.nav-item:hover {
  background-color: var(--color-bg-subtle);
  color: var(--color-text-heading);
}

.nav-active {
  background-color: var(--color-primary-light) !important;
  color: var(--color-primary) !important;
  font-weight: 600;
}
</style>
