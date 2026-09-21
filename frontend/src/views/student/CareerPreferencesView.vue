<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Sliders class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Target Career Settings</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Career Preferences</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Define your target job roles, preferred industries, work locations, and salary expectations to optimize AI recommendations.
        </p>
      </div>

      <button 
        @click="savePreferences" 
        :disabled="saving"
        class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center space-x-2 shrink-0 disabled:opacity-60"
      >
        <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
        <Save v-else class="w-4 h-4" />
        <span>Save Preferences</span>
      </button>
    </div>

    <!-- Alert Messages -->
    <div v-if="successMsg" class="p-4 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-semibold flex items-center space-x-2">
      <CheckCircle2 class="w-4 h-4 shrink-0 text-[#10B981]" />
      <span>{{ successMsg }}</span>
    </div>
    <div v-if="errorMsg" class="p-4 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-semibold flex items-center space-x-2">
      <AlertCircle class="w-4 h-4 shrink-0 text-red-500" />
      <span>{{ errorMsg }}</span>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-16 text-center text-slate-500 flex justify-center items-center space-x-2">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Loading student career preferences...</span>
    </div>

    <!-- Form Section -->
    <div v-else class="bg-white rounded-2xl p-6 md:p-8 border border-[#E2E8F0] shadow-sm max-w-3xl space-y-6">
      <form @submit.prevent="savePreferences" class="space-y-5">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Preferred Role -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Preferred Job / Career Role *</label>
            <input 
              v-model="prefForm.preferred_role" 
              type="text" 
              required 
              placeholder="e.g. Full Stack Engineer, AI Developer, Data Engineer"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <!-- Preferred Industry -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Target Industry *</label>
            <input 
              v-model="prefForm.preferred_industry" 
              type="text" 
              required 
              placeholder="e.g. Artificial Intelligence, Software & Cloud, FinTech"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <!-- Preferred Location -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Preferred Location *</label>
            <input 
              v-model="prefForm.preferred_location" 
              type="text" 
              required 
              placeholder="e.g. San Francisco, CA / Remote / Open to relocation"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <!-- Expected Salary -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Expected Salary Range</label>
            <input 
              v-model="prefForm.expected_salary" 
              type="text" 
              placeholder="e.g. $85,000 - $120,000 / year"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <!-- Employment Type -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Employment Type</label>
            <select 
              v-model="prefForm.employment_type"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            >
              <option value="Full-Time">Full-Time Job</option>
              <option value="Internship">Internship</option>
              <option value="Contract">Contract / Freelance</option>
              <option value="Part-Time">Part-Time</option>
            </select>
          </div>

          <!-- Work Mode -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Work Mode</label>
            <select 
              v-model="prefForm.work_mode"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            >
              <option value="Remote">Remote Only</option>
              <option value="Hybrid">Hybrid (Remote + Office)</option>
              <option value="On-site">On-site / In-Office</option>
            </select>
          </div>
        </div>

        <div class="pt-4 border-t border-slate-100 flex justify-end">
          <button 
            type="submit" 
            :disabled="saving"
            class="px-5 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl shadow-sm flex items-center space-x-2 disabled:opacity-60"
          >
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <Save v-else class="w-4 h-4" />
            <span>Save & Apply Preferences</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';
import { 
  Sliders, 
  Save, 
  Loader2, 
  CheckCircle2, 
  AlertCircle 
} from 'lucide-vue-next';

const authStore = useAuthStore();
const loading = ref(true);
const saving = ref(false);
const successMsg = ref('');
const errorMsg = ref('');

const prefForm = ref({
  preferred_role: 'Full Stack Software Engineer',
  preferred_industry: 'Software & Cloud Tech',
  preferred_location: 'San Francisco, CA / Remote',
  employment_type: 'Full-Time',
  work_mode: 'Hybrid',
  expected_salary: '$85,000 - $120,000 / year'
});

const loadPreferences = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.get('/student/preferences');
    if (res.data) {
      prefForm.value = {
        preferred_role: res.data.preferred_role || 'Full Stack Software Engineer',
        preferred_industry: res.data.preferred_industry || 'Software & Cloud Tech',
        preferred_location: res.data.preferred_location || 'San Francisco, CA / Remote',
        employment_type: res.data.employment_type || 'Full-Time',
        work_mode: res.data.work_mode || 'Hybrid',
        expected_salary: res.data.expected_salary || '$85,000 - $120,000 / year'
      };
    }
  } catch (err) {
    console.error('Failed to load preferences:', err);
    errorMsg.value = 'Failed to load preferences from database.';
  } finally {
    loading.value = false;
  }
};

const savePreferences = async () => {
  saving.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    await apiClient.put('/student/preferences', prefForm.value);
    successMsg.value = 'Career preferences saved to database!';
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to save preferences:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to save career preferences.';
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadPreferences();
});
</script>
