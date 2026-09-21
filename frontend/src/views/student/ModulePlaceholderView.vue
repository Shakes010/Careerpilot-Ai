<template>
  <div class="space-y-6">
    <!-- Header Card -->
    <div class="bg-white rounded-2xl p-6 md:p-8 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <span>Student Module</span>
          <span>•</span>
          <span>CareerPilot AI</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">{{ moduleName }}</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1 max-w-2xl">{{ description }}</p>
      </div>

      <div class="flex items-center space-x-3 shrink-0">
        <button class="px-4 py-2 bg-blue-50 text-[#2563EB] font-bold text-xs rounded-xl hover:bg-blue-100 transition-colors">
          Export Report
        </button>
        <button class="px-4 py-2 bg-[#2563EB] text-white font-bold text-xs rounded-xl hover:bg-blue-600 transition-colors shadow-sm">
          + Add New Entry
        </button>
      </div>
    </div>

    <!-- Active Feature Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div class="bg-white p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-2">
        <div class="w-8 h-8 rounded-lg bg-blue-50 text-[#2563EB] flex items-center justify-center font-bold text-sm">
          01
        </div>
        <h3 class="font-bold text-sm text-[#0F172A]">Real-time Student Tracking</h3>
        <p class="text-xs text-slate-500 leading-relaxed">
          Integrated directly with your backend database and student authentication token.
        </p>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-2">
        <div class="w-8 h-8 rounded-lg bg-purple-50 text-[#8B5CF6] flex items-center justify-center font-bold text-sm">
          02
        </div>
        <h3 class="font-bold text-sm text-[#0F172A]">AI Match & Analytics</h3>
        <p class="text-xs text-slate-500 leading-relaxed">
          Automated evaluation algorithms powered by sentence-transformers and Scikit-Learn.
        </p>
      </div>

      <div class="bg-white p-6 rounded-2xl border border-[#E2E8F0] shadow-sm space-y-2">
        <div class="w-8 h-8 rounded-lg bg-emerald-50 text-[#10B981] flex items-center justify-center font-bold text-sm">
          03
        </div>
        <h3 class="font-bold text-sm text-[#0F172A]">Verified Trust Meter</h3>
        <p class="text-xs text-slate-500 leading-relaxed">
          Tamper-proof student record verification for recruiter applications.
        </p>
      </div>
    </div>

    <!-- Main Module Section Placeholder -->
    <div class="bg-white rounded-2xl p-8 border border-[#E2E8F0] shadow-sm text-center py-16 space-y-4">
      <div class="w-14 h-14 mx-auto rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center">
        <Sparkles class="w-7 h-7" />
      </div>
      <div class="max-w-md mx-auto">
        <h2 class="text-lg font-bold text-[#0F172A]">{{ moduleName }} Feature Section</h2>
        <p class="text-xs text-slate-500 mt-1">
          Connected to student account <span class="font-semibold text-slate-700">{{ authStore.studentEmail }}</span>.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { Sparkles } from 'lucide-vue-next';

defineProps({
  moduleName: {
    type: String,
    default: 'Student Feature'
  },
  description: {
    type: String,
    default: 'Manage and optimize your student career progress with CareerPilot AI.'
  }
});

const authStore = useAuthStore();
</script>
