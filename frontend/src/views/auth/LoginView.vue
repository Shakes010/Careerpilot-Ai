<template>
  <div class="min-h-screen bg-[#F5F8FA] flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Top Brand Header -->
      <div class="text-center mb-8">
        <div class="flex justify-center mb-3">
          <img 
            src="@/assets/logo.png" 
            alt="CareerPilot AI" 
            class="h-10 w-auto object-contain select-none" 
          />
        </div>
        <p class="text-xs text-slate-500 font-medium">Student Career Development Platform</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-2xl border border-[#E2E8F0] shadow-xl p-8">
        <div class="mb-6">
          <h2 class="text-lg font-bold text-[#0F172A]">Student Sign In</h2>
          <p class="text-xs text-slate-500 mt-1">Access your career passport, applications, and AI recommendations</p>
        </div>

        <!-- Alert Message -->
        <div v-if="authStore.error" class="mb-5 p-3 rounded-xl bg-red-50 border border-red-100 text-red-600 text-xs flex items-start space-x-2">
          <AlertCircle class="w-4 h-4 shrink-0 mt-0.5" />
          <span>{{ authStore.error }}</span>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1.5">Student Email Address</label>
            <div class="relative">
              <Mail class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="email" 
                type="email" 
                required 
                placeholder="student@careerpilot.ai"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-xs font-semibold text-slate-700">Password</label>
              <a href="#" class="text-[11px] font-semibold text-[#2563EB] hover:underline">Forgot password?</a>
            </div>
            <div class="relative">
              <Lock class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="password" 
                type="password" 
                required 
                placeholder="••••••••"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="authStore.loading"
            class="w-full mt-2 py-3 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-semibold text-sm rounded-xl shadow-md shadow-blue-500/20 transition-all flex items-center justify-center space-x-2 disabled:opacity-60"
          >
            <Loader2 v-if="authStore.loading" class="w-4 h-4 animate-spin" />
            <span>{{ authStore.loading ? 'Signing in...' : 'Sign In to Student Dashboard' }}</span>
          </button>
        </form>

        <!-- Quick Demo Login Shortcut Button -->
        <div class="mt-6 pt-5 border-t border-slate-100">
          <button 
            @click="fillDemoCredentials"
            type="button" 
            class="w-full py-2 px-3 bg-blue-50 hover:bg-blue-100 text-[#2563EB] text-xs font-bold rounded-xl transition-colors flex items-center justify-center space-x-1.5"
          >
            <Sparkles class="w-3.5 h-3.5 text-[#2563EB]" />
            <span>Auto-fill Demo Student Credentials</span>
          </button>
        </div>
      </div>

      <!-- Footer Link -->
      <div class="text-center mt-6 text-xs text-slate-500">
        Don't have a student account yet? 
        <router-link to="/register" class="font-bold text-[#2563EB] hover:underline">Register here</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Mail, Lock, AlertCircle, Loader2, Sparkles } from 'lucide-vue-next';

const email = ref('');
const password = ref('');

const authStore = useAuthStore();
const router = useRouter();

const fillDemoCredentials = () => {
  email.value = 'student@careerpilot.ai';
  password.value = 'password123';
};

const handleSubmit = async () => {
  const success = await authStore.login({
    email: email.value,
    password: password.value
  });
  if (success) {
    router.push('/dashboard');
  }
};
</script>
