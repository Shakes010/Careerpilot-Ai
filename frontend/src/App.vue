<template>
  <div class="min-h-screen bg-[#F5F8FA]">
    <!-- Authenticated Layout with Sidebar & Navbar -->
    <div v-if="authStore.isAuthenticated" class="flex h-screen overflow-hidden">
      <!-- Reusable Sidebar -->
      <AppSidebar 
        :is-mobile-open="isMobileOpen" 
        @close-mobile="isMobileOpen = false" 
      />

      <!-- Backdrop for mobile sidebar overlay -->
      <div 
        v-if="isMobileOpen" 
        @click="isMobileOpen = false"
        class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-20 md:hidden"
      ></div>

      <!-- Main Layout Body -->
      <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
        <!-- Reusable Navbar -->
        <AppNavbar @toggle-mobile="isMobileOpen = !isMobileOpen" />

        <!-- Main Dynamic Content Scrollable Area -->
        <main class="flex-1 overflow-y-auto p-4 md:p-8">
          <div class="max-w-7xl mx-auto">
            <router-view />
          </div>
        </main>
      </div>
    </div>

    <!-- Unauthenticated Auth Views (Login / Register) -->
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import AppSidebar from '@/components/layout/AppSidebar.vue';
import AppNavbar from '@/components/layout/AppNavbar.vue';

const authStore = useAuthStore();
const isMobileOpen = ref(false);

onMounted(async () => {
  if (authStore.token) {
    await authStore.fetchCurrentUser();
  }
});
</script>
