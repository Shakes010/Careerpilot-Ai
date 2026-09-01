<template>
  <div class="dashboard-layout">
    <AppHeader @toggle-sidebar="sidebarOpen = !sidebarOpen" />
    <div class="layout-body">
      <AppSidebar :is-open="sidebarOpen" />
      <main class="main-content">
        <VerificationBanner v-if="showVerificationBanner" />
        <slot></slot>
      </main>
    </div>
    <AppToast />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import AppToast from '@/components/common/AppToast.vue'
import VerificationBanner from '@/components/recruiter/VerificationBanner.vue'
import { useAuthStore } from '@/stores/auth'

const sidebarOpen = ref(false)
const authStore = useAuthStore()

const showVerificationBanner = computed(() => {
  return authStore.companyVerificationStatus !== 'VERIFIED'
})
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--background);
}

.layout-body {
  display: flex;
  flex: 1;
}

.main-content {
  flex: 1;
  padding: 1.5rem 2rem;
  max-width: 1400px;
  width: 100%;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
}
</style>
