<template>
  <aside 
    :class="[
      'bg-white border-r border-[#E2E8F0] flex flex-col justify-between transition-all duration-300 z-30 shrink-0',
      isMobileOpen ? 'fixed inset-y-0 left-0 w-64 shadow-2xl' : 'hidden md:flex md:w-64'
    ]"
  >
    <!-- Top Branding & Navigation -->
    <div class="flex flex-col h-full overflow-y-auto">
      <!-- Brand Logo Header -->
      <div class="h-16 flex items-center justify-between px-5 border-b border-[#E2E8F0] bg-white sticky top-0 z-10">
        <router-link to="/dashboard" class="flex items-center cursor-pointer py-1" title="CareerPilot AI Dashboard">
          <img 
            src="@/assets/logo.png" 
            alt="CareerPilot AI" 
            class="h-8 w-auto max-w-[170px] object-contain select-none transition-transform hover:scale-[1.02]" 
          />
        </router-link>

        <!-- Mobile Close Button -->
        <button 
          @click="$emit('close-mobile')" 
          class="md:hidden text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Navigation Menu Links -->
      <div class="px-3 py-4 space-y-1">
        <div class="px-3 pb-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
          Student Navigation
        </div>

        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          @click="$emit('close-mobile')"
          v-slot="{ isActive }"
          class="block rounded-lg transition-all duration-150"
        >
          <div 
            :class="[
              'flex items-center px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors',
              isActive 
                ? 'bg-[#2563EB] text-white shadow-sm font-semibold' 
                : 'text-slate-600 hover:bg-slate-50 hover:text-[#0F172A]'
            ]"
          >
            <component 
              :is="item.icon" 
              :class="['w-4 h-4 mr-3 shrink-0', isActive ? 'text-white' : 'text-slate-400']" 
            />
            <span class="truncate">{{ item.label }}</span>

            <!-- Optional Badge -->
            <span 
              v-if="item.badge" 
              :class="[
                'ml-auto text-[10px] font-bold px-2 py-0.5 rounded-full',
                isActive ? 'bg-white/20 text-white' : 'bg-blue-50 text-[#2563EB]'
              ]"
            >
              {{ item.badge }}
            </span>
          </div>
        </router-link>
      </div>

      <!-- Skill Trust Meter Widget at bottom of Sidebar -->
      <div class="mt-auto px-4 py-4 m-3 bg-slate-50 rounded-xl border border-slate-200/80">
        <div class="flex items-center justify-between text-xs mb-1.5">
          <span class="font-semibold text-slate-700">Skill Trust Score</span>
          <span class="font-bold text-[#2563EB]">{{ authStore.profile?.skill_trust_meter ?? 0 }}%</span>
        </div>
        <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden mb-2">
          <div 
            class="bg-gradient-to-r from-[#2563EB] to-[#10B981] h-full rounded-full transition-all duration-700" 
            :style="{ width: (authStore.profile?.skill_trust_meter ?? 0) + '%' }"
          ></div>
        </div>
        <div class="flex justify-between items-center text-[10px] text-slate-500">
          <span>Verified Skills: {{ authStore.profile?.verified_skills_count ?? 0 }}</span>
          <span :class="authStore.profile?.skill_trust_meter >= 70 ? 'text-[#10B981] font-semibold' : 'text-slate-400 font-semibold'">
            {{ authStore.profile?.skill_trust_meter >= 70 ? 'High Trust' : authStore.profile?.skill_trust_meter > 0 ? 'Building Trust' : 'Unverified' }}
          </span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { 
  LayoutDashboard, 
  User, 
  BookOpen,
  GraduationCap, 
  Zap, 
  Award,
  Github,
  FileText, 
  Layers,
  Sparkles,
  History,
  Sliders, 
  Target
} from 'lucide-vue-next';

defineProps({
  isMobileOpen: {
    type: Boolean,
    default: false
  }
});

defineEmits(['close-mobile']);

const authStore = useAuthStore();

const menuItems = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Student Profile', path: '/profile', icon: User },
  { label: 'Career Passport', path: '/passport', icon: BookOpen, badge: 'ID' },
  { label: 'Education', path: '/education', icon: GraduationCap },
  { label: 'Skills & Tech Stack', path: '/skills', icon: Zap },
  { label: 'Certificates', path: '/certificates', icon: Award },
  { label: 'GitHub Profile', path: '/github', icon: Github },
  { label: 'Resume & ATS Parser', path: '/resume', icon: FileText },
  { label: 'Resume Versions', path: '/resume-versions', icon: Layers },
  { label: 'AI Resume Generator', path: '/resume-generator', icon: Sparkles, badge: 'AI' },
  { label: 'Career Timeline', path: '/timeline', icon: History },
  { label: 'Career Preferences', path: '/preferences', icon: Sliders },
  { label: 'Skill Gap & Learning', path: '/skill-builder', icon: Target },
];

</script>
