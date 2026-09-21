<template>
  <div class="space-y-6">
    <!-- Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <BookOpen class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Verified Identity</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Career Passport</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Consolidated professional identity aggregating profile, education, verified skills, active resume, certificates, and GitHub contributions.
        </p>
      </div>

      <button 
        @click="printPassport" 
        class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl shadow-sm transition-all flex items-center space-x-2 shrink-0"
      >
        <Printer class="w-4 h-4" />
        <span>Export Passport</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-16 text-center text-slate-500 flex justify-center items-center space-x-2">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Loading Career Passport data...</span>
    </div>

    <!-- Passport Document Content -->
    <div v-else-if="passport" id="passport-document" class="space-y-6">
      <!-- Top Passport Badge Card -->
      <div class="bg-gradient-to-br from-[#0F172A] via-[#1E293B] to-[#334155] rounded-3xl p-6 md:p-8 text-white shadow-xl relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 opacity-10 text-white select-none">
          <BookOpen class="w-64 h-64" />
        </div>

        <div class="relative z-10 flex flex-col md:flex-row items-center md:items-start justify-between gap-6">
          <div class="flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-6 text-center sm:text-left">
            <div class="w-24 h-24 rounded-2xl border-2 border-white/20 bg-white/10 overflow-hidden shrink-0 flex items-center justify-center text-3xl font-extrabold text-white shadow-inner">
              <img 
                v-if="formattedProfilePicture && !imageError" 
                :src="formattedProfilePicture" 
                @error="handleImageError"
                alt="Student Avatar" 
                class="w-full h-full object-cover" 
              />
              <span v-else>{{ getInitials(passport.user?.full_name) }}</span>
            </div>

            <div class="space-y-1">
              <span class="text-[10px] font-bold tracking-widest text-blue-400 uppercase">OFFICIAL CAREER PASSPORT</span>
              <h2 class="text-2xl font-black text-white tracking-tight">{{ passport.user?.full_name }}</h2>
              <p class="text-xs text-slate-300 font-medium">{{ passport.profile?.headline || passport.career_preference?.preferred_role || 'Software Engineering Student' }}</p>
              
              <div class="flex flex-wrap items-center justify-center sm:justify-start gap-x-4 gap-y-1 text-xs text-slate-400 pt-2">
                <span v-if="passport.profile?.university" class="flex items-center space-x-1">
                  <GraduationCap class="w-3.5 h-3.5 text-blue-400" />
                  <span>{{ passport.profile.university }}</span>
                </span>
                <span v-if="passport.profile?.location" class="flex items-center space-x-1">
                  <MapPin class="w-3.5 h-3.5 text-blue-400" />
                  <span>{{ passport.profile.location }}</span>
                </span>
              </div>
            </div>
          </div>

          <!-- Metrics Badges -->
          <div class="grid grid-cols-2 gap-3 w-full md:w-auto shrink-0">
            <div class="bg-white/10 backdrop-blur-md p-3 rounded-2xl border border-white/10 text-center">
              <span class="text-[10px] font-bold text-slate-300 block uppercase">Readiness Index</span>
              <span class="text-xl font-black text-emerald-400">{{ passport.profile?.career_readiness_score ?? 0 }}%</span>
            </div>
            <div class="bg-white/10 backdrop-blur-md p-3 rounded-2xl border border-white/10 text-center">
              <span class="text-[10px] font-bold text-slate-300 block uppercase">Skill Trust</span>
              <span class="text-xl font-black text-blue-400">{{ passport.profile?.skill_trust_meter ?? 0 }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Passport Grid Sections -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left 2-Column Details -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Academic Education -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
            <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
              <GraduationCap class="w-5 h-5 text-[#2563EB]" />
              <span>Academic Qualifications</span>
            </h3>

            <div v-if="!passport.educations || passport.educations.length === 0" class="text-xs text-slate-400 py-3 italic">
              No education entries recorded in database.
            </div>

            <div v-else class="space-y-3">
              <div 
                v-for="edu in passport.educations" 
                :key="edu.id" 
                class="p-4 rounded-xl bg-slate-50 border border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
              >
                <div>
                  <h4 class="font-bold text-sm text-[#0F172A]">{{ edu.degree }}</h4>
                  <p class="text-xs text-slate-500 font-medium">{{ edu.institution }}</p>
                </div>
                <div class="text-right text-xs">
                  <span class="font-bold text-[#2563EB] bg-blue-50 px-2.5 py-1 rounded-md">{{ edu.start_year }} - {{ edu.end_year || 'Present' }}</span>
                  <span v-if="edu.grade" class="block text-slate-500 text-[11px] font-semibold mt-1">Grade: {{ edu.grade }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Skills & Tech Stack -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
            <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
              <Zap class="w-5 h-5 text-amber-500" />
              <span>Skills & Competencies ({{ passport.skills?.length || 0 }})</span>
            </h3>

            <div v-if="!passport.skills || passport.skills.length === 0" class="text-xs text-slate-400 py-3 italic">
              No skills added yet.
            </div>

            <div v-else class="flex flex-wrap gap-2">
              <div 
                v-for="s in passport.skills" 
                :key="s.id"
                class="px-3 py-1.5 rounded-xl border border-slate-200 bg-slate-50 text-xs font-semibold flex items-center space-x-2"
              >
                <span class="text-slate-800">{{ s.skill_name }}</span>
                <span class="text-[10px] text-slate-400 bg-white px-1.5 py-0.5 rounded-md border border-slate-100">{{ s.proficiency }}</span>
                <CheckCircle2 v-if="s.is_verified" class="w-3.5 h-3.5 text-emerald-500" title="Verified Skill" />
              </div>
            </div>
          </div>

          <!-- Certificates -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
            <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
              <Award class="w-5 h-5 text-purple-600" />
              <span>Certificates & Credentials</span>
            </h3>

            <div v-if="!passport.certificates || passport.certificates.length === 0" class="text-xs text-slate-400 py-3 italic">
              No certificates recorded.
            </div>

            <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div 
                v-for="c in passport.certificates" 
                :key="c.id" 
                class="p-3.5 rounded-xl bg-slate-50 border border-slate-100 space-y-1"
              >
                <span class="text-[10px] font-bold text-purple-600 uppercase">{{ c.issuing_organization }}</span>
                <h4 class="font-bold text-xs text-[#0F172A] line-clamp-1">{{ c.title }}</h4>
                <span class="text-[11px] text-slate-400 block">Issued: {{ c.issue_date }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column Details -->
        <div class="space-y-6">
          <!-- Active Resume Info -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-3">
            <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
              <FileText class="w-5 h-5 text-[#2563EB]" />
              <span>Active Resume</span>
            </h3>

            <div v-if="passport.active_resume" class="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-[#0F172A] truncate max-w-[150px]">{{ passport.active_resume.title }}</span>
                <span class="text-xs font-extrabold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">ATS {{ passport.active_resume.ats_score }}%</span>
              </div>
              <p class="text-xs text-slate-500 line-clamp-3">{{ passport.active_resume.summary }}</p>
            </div>
            <div v-else class="text-xs text-slate-400 italic py-2">
              No active resume selected.
            </div>
          </div>

          <!-- GitHub Profile -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-3">
            <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
              <Github class="w-5 h-5 text-slate-800" />
              <span>GitHub Activity</span>
            </h3>

            <div v-if="passport.github_profile" class="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-2">
              <div class="flex items-center space-x-3">
                <img :src="passport.github_profile.avatar_url" class="w-10 h-10 rounded-xl object-cover" />
                <div>
                  <h4 class="text-xs font-bold text-[#0F172A]">{{ passport.github_profile.name || passport.github_profile.username }}</h4>
                  <a :href="passport.github_profile.html_url" target="_blank" class="text-[11px] text-[#2563EB] hover:underline">@{{ passport.github_profile.username }}</a>
                </div>
              </div>
              <div class="flex justify-between text-xs text-slate-600 pt-2 border-t border-slate-200/60">
                <span>Public Repos: <strong class="text-slate-800">{{ passport.github_profile.public_repos }}</strong></span>
                <span>Followers: <strong class="text-slate-800">{{ passport.github_profile.followers }}</strong></span>
              </div>
            </div>
            <div v-else class="text-xs text-slate-400 italic py-2">
              GitHub not connected.
            </div>
          </div>



          <!-- Career Preferences -->
          <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-3">
            <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
              <Sliders class="w-5 h-5 text-blue-600" />
              <span>Career Focus</span>
            </h3>

            <div v-if="passport.career_preference" class="space-y-2 text-xs">
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-400">Target Role:</span>
                <span class="font-bold text-[#0F172A]">{{ passport.career_preference.preferred_role }}</span>
              </div>
              <div class="flex justify-between py-1.5 border-b border-slate-100">
                <span class="text-slate-400">Industry:</span>
                <span class="font-semibold text-slate-700">{{ passport.career_preference.preferred_industry }}</span>
              </div>
              <div class="flex justify-between py-1.5">
                <span class="text-slate-400">Work Mode:</span>
                <span class="font-semibold text-slate-700">{{ passport.career_preference.work_mode }} ({{ passport.career_preference.employment_type }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import apiClient from '@/services/api';
import { 
  BookOpen, 
  Printer, 
  Loader2, 
  GraduationCap, 
  MapPin, 
  Zap, 
  CheckCircle2, 
  Award, 
  FileText, 
  Github, 
  Sliders 
} from 'lucide-vue-next';

const passport = ref(null);
const loading = ref(true);
const imageError = ref(false);

const formattedProfilePicture = computed(() => {
  const pic = passport.value?.profile?.profile_picture;
  if (!pic) return null;
  if (pic.startsWith('http://') || pic.startsWith('https://') || pic.startsWith('data:')) {
    return pic;
  }
  return `http://127.0.0.1:8000${pic.startsWith('/') ? '' : '/'}${pic}`;
});

const handleImageError = () => {
  imageError.value = true;
};

const fetchPassport = async () => {
  loading.value = true;
  imageError.value = false;
  try {
    const res = await apiClient.get('/student/passport');
    passport.value = res.data;
  } catch (err) {
    console.error('Failed to load Career Passport', err);
  } finally {
    loading.value = false;
  }
};

const getInitials = (name) => {
  if (!name) return 'CP';
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
};

const printPassport = () => {
  window.print();
};

const formatDate = (d) => {
  if (!d) return '';
  return new Date(d).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

onMounted(fetchPassport);
</script>
