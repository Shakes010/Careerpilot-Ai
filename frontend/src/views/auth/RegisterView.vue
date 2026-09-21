<template>
  <div class="min-h-screen bg-[#F5F8FA] flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Top Brand Header -->
      <div class="text-center mb-6">
        <div class="flex justify-center mb-3">
          <img 
            src="@/assets/logo.png" 
            alt="CareerPilot AI" 
            class="h-10 w-auto object-contain select-none" 
          />
        </div>
        <p class="text-xs text-slate-500 font-medium">Student Module Registration</p>
      </div>

      <!-- Register Card -->
      <div class="bg-white rounded-2xl border border-[#E2E8F0] shadow-xl p-8">
        <div class="mb-5">
          <h2 class="text-lg font-bold text-[#0F172A]">Create Student Profile</h2>
          <p class="text-xs text-slate-500 mt-1">Start building your verified skills & career passport</p>
        </div>

        <div v-if="authStore.error" class="mb-5 p-3 rounded-xl bg-red-50 border border-red-100 text-red-600 text-xs flex items-start space-x-2">
          <AlertCircle class="w-4 h-4 shrink-0 mt-0.5" />
          <span>{{ authStore.error }}</span>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-3.5">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
            <div class="relative">
              <User class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="fullName" 
                type="text" 
                required 
                placeholder="Alex Morgan"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">University / Institute</label>
            <div class="relative">
              <GraduationCap class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="university" 
                type="text" 
                placeholder="National Institute of Technology"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Degree / Major</label>
            <div class="relative">
              <BookOpen class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="major" 
                type="text" 
                placeholder="Master of Computer Applications (MCA)"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
            <div class="relative">
              <Mail class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="email" 
                type="email" 
                required 
                placeholder="alex.morgan@student.edu"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <div class="relative">
              <Lock class="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input 
                v-model="password" 
                type="password" 
                required 
                placeholder="At least 6 characters"
                class="w-full pl-10 pr-4 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs md:text-sm text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"
              />
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="authStore.loading"
            class="w-full mt-3 py-3 bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-semibold text-sm rounded-xl shadow-md shadow-blue-500/20 transition-all flex items-center justify-center space-x-2 disabled:opacity-60"
          >
            <Loader2 v-if="authStore.loading" class="w-4 h-4 animate-spin" />
            <span>{{ authStore.loading ? 'Creating Profile...' : 'Register & Enter Dashboard' }}</span>
          </button>
        </form>
      </div>

      <div class="text-center mt-5 text-xs text-slate-500">
        Already registered? 
        <router-link to="/login" class="font-bold text-[#2563EB] hover:underline">Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { User, GraduationCap, BookOpen, Mail, Lock, AlertCircle, Loader2 } from 'lucide-vue-next';

const fullName = ref('');
const university = ref('National Institute of Technology');
const major = ref('Master of Computer Applications (MCA)');
const email = ref('');
const password = ref('');

const authStore = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  const success = await authStore.register({
    full_name: fullName.value,
    university: university.value,
    major: major.value,
    email: email.value,
    password: password.value
  });
  if (success) {
    router.push('/dashboard');
  }
};
</script>
