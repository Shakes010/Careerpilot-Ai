<template>
  <header class="h-16 bg-white border-b border-[#E2E8F0] px-4 md:px-8 flex items-center justify-between sticky top-0 z-20">
    <!-- Left Section: Mobile Menu Toggle & Search Bar -->
    <div class="flex items-center space-x-4 flex-1">
      <button 
        @click="$emit('toggle-mobile')" 
        class="md:hidden text-slate-500 hover:text-slate-700 p-2 rounded-lg hover:bg-slate-100"
        aria-label="Toggle Navigation"
      >
        <Menu class="w-5 h-5" />
      </button>

      <!-- Global Search -->
      <div class="relative max-w-md w-full hidden sm:block">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
          <Search class="w-4 h-4" />
        </div>
        <input 
          type="text" 
          placeholder="Search jobs, assessments, skills, projects..." 
          class="w-full pl-9 pr-4 py-2 text-xs md:text-sm bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-[#0F172A] placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
        />
      </div>
    </div>

    <!-- Right Section: Readiness Score Indicator, Notifications & Student Menu -->
    <div class="flex items-center space-x-3 md:space-x-5">
      <!-- Quick Readiness Pill -->
      <div class="hidden lg:flex items-center space-x-2 bg-blue-50 border border-blue-100 px-3 py-1.5 rounded-full">
        <span class="w-2 h-2 rounded-full bg-[#10B981] animate-pulse"></span>
        <span class="text-xs font-semibold text-slate-700">Readiness:</span>
        <span class="text-xs font-bold text-[#2563EB]">{{ authStore.profile?.career_readiness_score ?? 0 }}%</span>
      </div>

      <!-- Notifications -->
      <div class="relative">
        <button 
          @click="showNotifications = !showNotifications"
          class="relative p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
        >
          <Bell class="w-5 h-5" />
          <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-[#2563EB] rounded-full ring-2 ring-white"></span>
        </button>

        <!-- Notifications Dropdown -->
        <div 
          v-if="showNotifications"
          @click.outside="showNotifications = false"
          class="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-[#E2E8F0] py-2 z-50 animate-in fade-in slide-in-from-top-2 duration-200"
        >
          <div class="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
            <span class="font-bold text-sm text-[#0F172A]">Notifications</span>
            <span class="text-[11px] font-semibold text-[#2563EB] cursor-pointer hover:underline">Mark all read</span>
          </div>
          <div class="divide-y divide-slate-100 max-h-64 overflow-y-auto">
            <div class="px-4 py-3 hover:bg-slate-50 cursor-pointer">
              <p class="text-xs font-semibold text-slate-800">New Opportunity Match (96%)</p>
              <p class="text-[11px] text-slate-500 mt-0.5">Junior AI Developer at DeepTech AI</p>
              <span class="text-[10px] text-slate-400 block mt-1">10 mins ago</span>
            </div>
            <div class="px-4 py-3 hover:bg-slate-50 cursor-pointer">
              <p class="text-xs font-semibold text-slate-800">Assessment Result Verified</p>
              <p class="text-[11px] text-slate-500 mt-0.5">Python Core Assessment: Passed (94%)</p>
              <span class="text-[10px] text-slate-400 block mt-1">2 hours ago</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Profile Dropdown -->
      <div class="relative">
        <button 
          @click="showProfileMenu = !showProfileMenu"
          class="flex items-center space-x-3 p-1 rounded-xl hover:bg-slate-100 transition-colors"
        >
          <div class="w-9 h-9 rounded-full bg-[#2563EB] text-white flex items-center justify-center font-bold text-sm shadow-sm ring-2 ring-blue-100 overflow-hidden shrink-0">
            <img 
              v-if="formattedNavbarAvatar" 
              :src="formattedNavbarAvatar" 
              alt="Student Avatar" 
              class="w-full h-full object-cover" 
            />
            <span v-else>{{ avatarInitials }}</span>
          </div>
          <div class="hidden md:block text-left pr-1">
            <div class="text-xs font-bold text-[#0F172A] leading-tight">{{ authStore.studentName }}</div>
            <div class="text-[10px] font-medium text-slate-500 truncate max-w-[130px]">{{ authStore.studentMajor }}</div>
          </div>
          <ChevronDown class="w-4 h-4 text-slate-400 hidden md:block" />
        </button>

        <!-- Profile Menu Dropdown -->
        <div 
          v-if="showProfileMenu"
          class="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-xl border border-[#E2E8F0] py-2 z-50"
        >
          <div class="px-4 py-3 border-b border-slate-100">
            <p class="text-xs font-bold text-[#0F172A]">{{ authStore.studentName }}</p>
            <p class="text-[11px] text-slate-500 truncate">{{ authStore.studentEmail }}</p>
            <span class="inline-block mt-1.5 px-2 py-0.5 bg-blue-50 text-[#2563EB] text-[10px] font-bold rounded-md">
              Student Account
            </span>
          </div>

          <div class="py-1">
            <router-link 
              to="/profile" 
              @click="showProfileMenu = false"
              class="flex items-center px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-[#2563EB]"
            >
              <User class="w-4 h-4 mr-2.5 text-slate-400" />
              Student Profile & Details
            </router-link>
            <router-link 
              to="/dashboard" 
              @click="showProfileMenu = false"
              class="flex items-center px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 hover:text-[#2563EB]"
            >
              <Award class="w-4 h-4 mr-2.5 text-slate-400" />
              Career Passport & Overview
            </router-link>
          </div>

          <div class="border-t border-slate-100 pt-1">
            <button 
              @click="handleLogout"
              class="w-full flex items-center px-4 py-2 text-xs font-semibold text-red-600 hover:bg-red-50"
            >
              <LogOut class="w-4 h-4 mr-2.5 text-red-500" />
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Menu, Search, Bell, ChevronDown, User, Award, LogOut } from 'lucide-vue-next';

defineEmits(['toggle-mobile']);

const authStore = useAuthStore();
const router = useRouter();

const showNotifications = ref(false);
const showProfileMenu = ref(false);

const avatarInitials = computed(() => {
  const name = authStore.studentName || 'Student';
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
});

const formattedNavbarAvatar = computed(() => {
  const pic = authStore.profile?.profile_picture;
  if (!pic) return null;
  if (pic.startsWith('http://') || pic.startsWith('https://') || pic.startsWith('data:')) {
    return pic;
  }
  return `http://127.0.0.1:8000${pic.startsWith('/') ? '' : '/'}${pic}`;
});

const handleLogout = () => {
  showProfileMenu.value = false;
  authStore.logout();
  router.push('/login');
};
</script>
