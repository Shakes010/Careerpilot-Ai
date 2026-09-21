<template>
  <div class="space-y-6">
    <!-- Welcome Header Banner -->
    <div class="bg-gradient-to-r from-[#0F172A] via-[#1E293B] to-[#2563EB] rounded-2xl p-6 md:p-8 text-white shadow-lg relative overflow-hidden">
      <!-- Background subtle grid effect -->
      <div class="absolute inset-0 opacity-10 bg-[radial-gradient(#2563EB_1px,transparent_1px)] [background-size:16px_16px]"></div>
      
      <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center space-x-2 text-xs font-semibold text-blue-300 uppercase tracking-wider mb-1">
            <Sparkles class="w-4 h-4 text-[#10B981]" />
            <span>AI-Powered Student Career Hub</span>
          </div>
          <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">
            Welcome back, {{ dashboardData?.user?.full_name || authStore.studentName }}!
          </h1>
          <p class="text-slate-300 text-xs md:text-sm mt-1 max-w-xl">
            {{ dashboardData?.profile?.headline || 'Master of Computer Applications (MCA) • National Institute of Technology' }}
          </p>
        </div>

        <!-- Quick Actions -->
        <div class="flex items-center space-x-3 shrink-0">
          <router-link 
            to="/profile" 
            class="px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold rounded-xl backdrop-blur-sm transition-all border border-white/10 flex items-center space-x-2"
          >
            <User class="w-4 h-4 text-blue-300" />
            <span>My Profile</span>
          </router-link>
          <router-link 
            to="/opportunities" 
            class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white text-xs font-bold rounded-xl shadow-md shadow-blue-500/30 transition-all flex items-center space-x-2"
          >
            <Compass class="w-4 h-4" />
            <span>Radar Opportunities</span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-12 flex justify-center items-center space-x-3 text-slate-500">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Loading student dashboard data...</span>
    </div>

    <template v-else>
      <!-- 4 Key Metric Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Metric 1: GitHub Integration -->
        <router-link to="/github" class="bg-white rounded-2xl p-5 border border-[#E2E8F0] shadow-sm hover:border-blue-200 transition-all block">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-500">GitHub Profile</span>
            <div class="w-9 h-9 rounded-xl bg-slate-900 text-white flex items-center justify-center">
              <Github class="w-4 h-4" />
            </div>
          </div>
          <div class="mt-3 flex items-baseline justify-between">
            <span class="text-2xl font-extrabold text-[#0F172A]">{{ dashboardData?.profile?.github_url ? 'Connected' : 'Sync' }}</span>
            <span class="text-[11px] font-bold text-[#2563EB] bg-blue-50 px-2 py-0.5 rounded-full">Open Source</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-1">Public repos & stargazers</p>
        </router-link>

        <!-- Metric 2: Verified Skills -->
        <router-link to="/skills" class="bg-white rounded-2xl p-5 border border-[#E2E8F0] shadow-sm hover:border-purple-200 transition-all block">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-500">Verified Skills</span>
            <div class="w-9 h-9 rounded-xl bg-purple-50 text-[#8B5CF6] flex items-center justify-center">
              <Zap class="w-4 h-4" />
            </div>
          </div>
          <div class="mt-3 flex items-baseline justify-between">
            <span class="text-2xl font-extrabold text-[#0F172A]">{{ dashboardData?.skills_count ?? 0 }}</span>
            <span class="text-[11px] font-bold text-[#8B5CF6] bg-purple-50 px-2 py-0.5 rounded-full">Tech Stack</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-1">Skills stored in database</p>
        </router-link>

        <!-- Metric 3: Education Records -->
        <router-link to="/education" class="bg-white rounded-2xl p-5 border border-[#E2E8F0] shadow-sm hover:border-amber-200 transition-all block">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-500">Academic Education</span>
            <div class="w-9 h-9 rounded-xl bg-amber-50 text-[#F59E0B] flex items-center justify-center">
              <GraduationCap class="w-4 h-4" />
            </div>
          </div>
          <div class="mt-3 flex items-baseline justify-between">
            <span class="text-2xl font-extrabold text-[#0F172A]">{{ dashboardData?.education_count ?? 0 }}</span>
            <span class="text-[11px] font-bold text-[#F59E0B] bg-amber-50 px-2 py-0.5 rounded-full">Degrees</span>
          </div>
          <p class="text-[11px] text-slate-400 mt-1">University qualifications</p>
        </router-link>

        <!-- Metric 4: Resume Status -->
        <router-link to="/resume" class="bg-white rounded-2xl p-5 border border-[#E2E8F0] shadow-sm hover:border-emerald-200 transition-all block">
          <div class="flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-500">Resume ATS Score</span>
            <div class="w-9 h-9 rounded-xl bg-emerald-50 text-[#10B981] flex items-center justify-center">
              <FileText class="w-4 h-4" />
            </div>
          </div>
          <div class="mt-3 flex items-baseline justify-between">
            <span class="text-2xl font-extrabold text-[#0F172A]">{{ dashboardData?.resumes_count > 0 ? 'Active' : 'None' }}</span>
            <span :class="['text-[11px] font-bold px-2 py-0.5 rounded-full', dashboardData?.resumes_count > 0 ? 'bg-green-50 text-[#10B981]' : 'bg-slate-100 text-slate-500']">
              {{ dashboardData?.resumes_count > 0 ? 'PDF Parsed' : 'Upload' }}
            </span>
          </div>
          <p class="text-[11px] text-slate-400 mt-1">Resume file & ATS summary</p>
        </router-link>
      </div>

      <!-- Main Two-Column Layout -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left 2 Columns: Profile Completion, Recommendations & Opportunities -->
        <div class="lg:col-span-2 space-y-6">
          
          <!-- Profile Completion Meter -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-base font-extrabold text-[#0F172A]">Profile Completion Percentage</h2>
                <p class="text-xs text-slate-500">Completing all sections maximizes recruiter visibility and job match accuracy</p>
              </div>
              <span class="text-2xl font-extrabold text-[#2563EB]">{{ dashboardData?.completion_percentage ?? 0 }}%</span>
            </div>

            <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
              <div 
                class="bg-gradient-to-r from-[#2563EB] via-[#8B5CF6] to-[#10B981] h-full rounded-full transition-all duration-1000"
                :style="{ width: (dashboardData?.completion_percentage ?? 0) + '%' }"
              ></div>
            </div>

            <div class="flex items-center justify-between text-xs font-semibold text-slate-600 pt-1">
              <span>Target Career Role: <strong class="text-[#2563EB]">{{ dashboardData?.career_preference?.preferred_role || 'Not Configured' }}</strong></span>
              <router-link to="/preferences" class="text-[#2563EB] hover:underline flex items-center">
                {{ dashboardData?.career_preference ? 'Edit Preferences' : 'Set Preferences' }} <ArrowRight class="w-3.5 h-3.5 ml-1" />
              </router-link>
            </div>
          </div>

          <!-- Opportunity Radar Widget -->

        </div>

        <!-- Right Column: AI Recommendations & Quick Module Navigation -->
        <div class="space-y-6">

          <!-- AI Career Recommendations -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50/50 rounded-2xl p-6 border border-blue-100 shadow-sm">
            <div class="flex items-center space-x-2 mb-3">
              <Sparkles class="w-5 h-5 text-[#2563EB]" />
              <h2 class="text-base font-extrabold text-[#0F172A]">AI Insights & Actions</h2>
            </div>
            <div class="space-y-2.5">
              <div 
                v-for="(rec, idx) in dashboardData?.ai_recommendations || []" 
                :key="idx"
                class="p-3 bg-white rounded-xl border border-blue-100 text-xs text-slate-700 font-medium leading-relaxed flex items-start space-x-2 shadow-2xs"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-[#2563EB] shrink-0 mt-1.5"></span>
                <span>{{ rec }}</span>
              </div>
            </div>
          </div>

          <!-- Student Module Quick Launch List -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-3">
            <h2 class="text-base font-extrabold text-[#0F172A] mb-2">Student Module Tools</h2>
            
            <router-link 
              to="/profile" 
              class="w-full p-3 bg-slate-50 hover:bg-blue-50 rounded-xl border border-slate-200 hover:border-blue-200 flex items-center justify-between transition-all group"
            >
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-blue-100 text-[#2563EB] flex items-center justify-center font-bold">
                  <User class="w-4 h-4" />
                </div>
                <div class="text-left">
                  <span class="text-xs font-bold text-[#0F172A] group-hover:text-[#2563EB] block">Edit Student Profile</span>
                  <span class="text-[10px] text-slate-500">Contact, bio & social links</span>
                </div>
              </div>
              <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-[#2563EB]" />
            </router-link>

            <router-link 
              to="/education" 
              class="w-full p-3 bg-slate-50 hover:bg-amber-50 rounded-xl border border-slate-200 hover:border-amber-200 flex items-center justify-between transition-all group"
            >
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-amber-100 text-[#F59E0B] flex items-center justify-center font-bold">
                  <GraduationCap class="w-4 h-4" />
                </div>
                <div class="text-left">
                  <span class="text-xs font-bold text-[#0F172A] group-hover:text-[#F59E0B] block">Education CRUD</span>
                  <span class="text-[10px] text-slate-500">Degrees, GPA & universities</span>
                </div>
              </div>
              <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-[#F59E0B]" />
            </router-link>

            <router-link 
              to="/skills" 
              class="w-full p-3 bg-slate-50 hover:bg-purple-50 rounded-xl border border-slate-200 hover:border-purple-200 flex items-center justify-between transition-all group"
            >
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-purple-100 text-[#8B5CF6] flex items-center justify-center font-bold">
                  <Zap class="w-4 h-4" />
                </div>
                <div class="text-left">
                  <span class="text-xs font-bold text-[#0F172A] group-hover:text-[#8B5CF6] block">Manage Tech Skills</span>
                  <span class="text-[10px] text-slate-500">Proficiency & verified badges</span>
                </div>
              </div>
              <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-[#8B5CF6]" />
            </router-link>

            <router-link 
              to="/resume" 
              class="w-full p-3 bg-slate-50 hover:bg-emerald-50 rounded-xl border border-slate-200 hover:border-emerald-200 flex items-center justify-between transition-all group"
            >
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-emerald-100 text-[#10B981] flex items-center justify-center font-bold">
                  <FileText class="w-4 h-4" />
                </div>
                <div class="text-left">
                  <span class="text-xs font-bold text-[#0F172A] group-hover:text-[#10B981] block">Resume & ATS Parser</span>
                  <span class="text-[10px] text-slate-500">Upload PDF & score analysis</span>
                </div>
              </div>
              <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-[#10B981]" />
            </router-link>

            <router-link 
              to="/skill-builder" 
              class="w-full p-3 bg-slate-50 hover:bg-indigo-50 rounded-xl border border-slate-200 hover:border-indigo-200 flex items-center justify-between transition-all group"
            >
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-indigo-100 text-[#6366F1] flex items-center justify-center font-bold">
                  <Target class="w-4 h-4" />
                </div>
                <div class="text-left">
                  <span class="text-xs font-bold text-[#0F172A] group-hover:text-[#6366F1] block">Skill Gap Analysis</span>
                  <span class="text-[10px] text-slate-500">Missing skills & learning links</span>
                </div>
              </div>
              <ChevronRight class="w-4 h-4 text-slate-400 group-hover:text-[#6366F1]" />
            </router-link>
          </div>

        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';
import { 
  Sparkles, 
  User, 
  Github, 
  Zap, 
  GraduationCap, 
  FileText, 
  Target, 
  ArrowRight, 
  ChevronRight,
  Loader2
} from 'lucide-vue-next';

const authStore = useAuthStore();
const dashboardData = ref(null);
const loading = ref(true);

const fetchDashboardData = async () => {
  loading.value = true;
  try {
    const response = await apiClient.get('/student/dashboard');
    dashboardData.value = response.data;
  } catch (err) {
    console.error('Failed to load student dashboard data:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchDashboardData();
});
</script>
