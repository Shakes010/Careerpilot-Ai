<template>
  <div v-if="status === 'PENDING'" class="banner banner-pending">
    <div class="banner-icon">⏳</div>
    <div class="banner-content">
      <h4 class="banner-title">Company Verification Pending</h4>
      <p class="banner-desc">Your company profile is currently under review by CareerPilot AI Administrators. You can prepare and save job drafts, but full job publishing requires verified status.</p>
    </div>
    <router-link to="/recruiter/company" class="banner-action-btn">
      View Company Profile
    </router-link>
  </div>

  <div v-else-if="status === 'REJECTED'" class="banner banner-rejected">
    <div class="banner-icon">⚠️</div>
    <div class="banner-content">
      <h4 class="banner-title">Company Verification Rejected</h4>
      <p class="banner-desc">Your company verification request was not approved. Please update your official details or contact support.</p>
    </div>
    <router-link to="/recruiter/company" class="banner-action-btn">
      Update Company Profile
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const status = computed(() => {
  return authStore.companyVerificationStatus || 'PENDING'
})
</script>

<style scoped>
.banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
}

.banner-pending {
  background-color: var(--warning-bg);
  border: 1px solid var(--warning-border);
  color: #92400e;
}

.banner-rejected {
  background-color: var(--danger-bg);
  border: 1px solid var(--danger-border);
  color: #991b1b;
}

.banner-icon {
  font-size: 1.5rem;
}

.banner-content {
  flex: 1;
}

.banner-title {
  font-size: 0.9375rem;
  font-weight: 600;
}

.banner-desc {
  font-size: 0.8125rem;
  margin-top: 0.125rem;
}

.banner-action-btn {
  font-size: 0.8125rem;
  font-weight: 600;
  padding: 0.5rem 0.875rem;
  border-radius: var(--radius-sm);
  background-color: #ffffff;
  border: 1px solid currentColor;
  color: inherit;
  text-decoration: none;
  white-space: nowrap;
}

.banner-action-btn:hover {
  text-decoration: none;
  opacity: 0.9;
}
</style>
