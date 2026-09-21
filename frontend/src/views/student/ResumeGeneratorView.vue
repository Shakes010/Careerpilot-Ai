<template>
  <div class="space-y-6">
    <!-- Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Sparkles class="w-4 h-4 text-amber-500" />
          <span>Student Module</span>
          <span>•</span>
          <span>Free AI Tools</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">AI Resume Generator (Non-Paid)</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Automatically synthesize your verified profile data, education, skills, certificates, and GitHub projects into a professional ATS-friendly resume.
        </p>
      </div>

      <div class="flex items-center space-x-3 shrink-0">
        <button 
          @click="generateResume" 
          :disabled="generating"
          class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl shadow-sm transition-all flex items-center space-x-2"
        >
          <Loader2 v-if="generating" class="w-4 h-4 animate-spin" />
          <Sparkles v-else class="w-4 h-4 text-amber-300" />
          <span>{{ generatedData ? 'Re-Generate Resume' : 'Generate Resume' }}</span>
        </button>

        <button 
          v-if="generatedData" 
          @click="saveAsVersion" 
          :disabled="saving"
          class="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-sm transition-all flex items-center space-x-2"
        >
          <Save v-if="!saving" class="w-4 h-4" />
          <Loader2 v-else class="w-4 h-4 animate-spin" />
          <span>Save as Resume Version</span>
        </button>
      </div>
    </div>

    <!-- Notifications -->
    <div v-if="successMsg" class="p-4 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-semibold flex items-center space-x-2">
      <CheckCircle2 class="w-4 h-4 shrink-0 text-[#10B981]" />
      <span>{{ successMsg }}</span>
    </div>
    <div v-if="errorMsg" class="p-4 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-semibold flex items-center space-x-2">
      <AlertCircle class="w-4 h-4 shrink-0 text-red-500" />
      <span>{{ errorMsg }}</span>
    </div>

    <!-- Initial Prompt State (Before Generation) -->
    <div v-if="!generatedData && !generating" class="bg-white rounded-2xl p-12 border border-[#E2E8F0] text-center space-y-4 shadow-sm max-w-xl mx-auto">
      <div class="w-16 h-16 rounded-2xl bg-amber-50 text-amber-500 flex items-center justify-center mx-auto">
        <Wand2 class="w-8 h-8" />
      </div>
      <div>
        <h3 class="text-lg font-bold text-[#0F172A]">Generate Professional ATS Resume</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Our AI engine will assemble your stored profile details, academic records, verified skills, and GitHub projects into a structured, high-scoring ATS resume layout.
        </p>
      </div>
      <button 
        @click="generateResume" 
        class="px-5 py-2.5 bg-[#2563EB] text-white text-xs font-bold rounded-xl hover:bg-blue-600 inline-flex items-center space-x-2 shadow-sm"
      >
        <Sparkles class="w-4 h-4 text-amber-300" />
        <span>Generate Resume Now</span>
      </button>
    </div>

    <!-- Generating Loader -->
    <div v-if="generating" class="bg-white rounded-2xl p-16 border border-[#E2E8F0] text-center space-y-3 shadow-sm">
      <Loader2 class="w-10 h-10 animate-spin text-[#2563EB] mx-auto" />
      <h3 class="text-base font-bold text-[#0F172A]">Synthesizing Resume Data...</h3>
      <p class="text-xs text-slate-500">Retrieving education, skills, certificates, and GitHub projects from PostgreSQL database.</p>
    </div>

    <!-- Generated Resume Preview -->
    <div v-if="generatedData && !generating" class="bg-white rounded-2xl p-8 border border-[#E2E8F0] shadow-md max-w-3xl mx-auto space-y-6 text-[#0F172A]">
      <!-- Header Section -->
      <div class="border-b border-slate-200 pb-4 text-center space-y-1">
        <h2 class="text-2xl font-black tracking-tight uppercase text-[#0F172A]">{{ generatedData.full_name }}</h2>
        <div class="flex flex-wrap justify-center items-center gap-x-3 gap-y-1 text-xs text-slate-600">
          <span>{{ generatedData.email }}</span>
          <span v-if="generatedData.phone">• {{ generatedData.phone }}</span>
          <span v-if="generatedData.location">• {{ generatedData.location }}</span>
        </div>
        <div class="flex flex-wrap justify-center items-center gap-x-3 text-xs text-[#2563EB]">
          <a v-if="generatedData.linkedin_url" :href="generatedData.linkedin_url" target="_blank" class="hover:underline">LinkedIn</a>
          <a v-if="generatedData.github_url" :href="generatedData.github_url" target="_blank" class="hover:underline">GitHub</a>
        </div>
      </div>

      <!-- Professional Summary -->
      <div>
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-[#2563EB] border-b border-blue-100 pb-1 mb-2">Professional Summary</h3>
        <p class="text-xs text-slate-700 leading-relaxed">{{ generatedData.professional_summary }}</p>
      </div>

      <!-- Technical Skills -->
      <div v-if="generatedData.skills_grouped && generatedData.skills_grouped.length > 0">
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-[#2563EB] border-b border-blue-100 pb-1 mb-2">Technical Skills</h3>
        <div class="space-y-1 text-xs">
          <div v-for="sg in generatedData.skills_grouped" :key="sg.category" class="flex">
            <span class="font-bold text-slate-800 w-36 shrink-0">{{ sg.category }}:</span>
            <span class="text-slate-600">{{ sg.skills.join(', ') }}</span>
          </div>
        </div>
      </div>

      <!-- Education -->
      <div v-if="generatedData.education && generatedData.education.length > 0">
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-[#2563EB] border-b border-blue-100 pb-1 mb-2">Education</h3>
        <div class="space-y-3">
          <div v-for="edu in generatedData.education" :key="edu.id" class="text-xs">
            <div class="flex justify-between font-bold text-slate-800">
              <span>{{ edu.degree }}</span>
              <span>{{ edu.start_year }} - {{ edu.end_year || 'Present' }}</span>
            </div>
            <div class="flex justify-between text-slate-600">
              <span>{{ edu.institution }}</span>
              <span v-if="edu.grade">GPA/Grade: {{ edu.grade }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Projects (from GitHub) -->
      <div v-if="generatedData.projects && generatedData.projects.length > 0">
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-[#2563EB] border-b border-blue-100 pb-1 mb-2">Projects & Open Source</h3>
        <div class="space-y-3">
          <div v-for="p in generatedData.projects" :key="p.id" class="text-xs">
            <div class="flex justify-between font-bold text-slate-800">
              <a :href="p.html_url" target="_blank" class="hover:text-blue-600 flex items-center space-x-1">
                <span>{{ p.name }}</span>
                <ExternalLink class="w-3 h-3 text-slate-400" />
              </a>
              <span v-if="p.language" class="text-slate-500 text-[11px] font-normal">{{ p.language }}</span>
            </div>
            <p class="text-slate-600 mt-0.5">{{ p.description }}</p>
          </div>
        </div>
      </div>

      <!-- Certifications -->
      <div v-if="generatedData.certifications && generatedData.certifications.length > 0">
        <h3 class="text-xs font-extrabold uppercase tracking-wider text-[#2563EB] border-b border-blue-100 pb-1 mb-2">Certifications</h3>
        <div class="space-y-2">
          <div v-for="c in generatedData.certifications" :key="c.id" class="text-xs flex justify-between">
            <div>
              <span class="font-bold text-slate-800">{{ c.title }}</span>
              <span class="text-slate-500"> — {{ c.issuing_organization }}</span>
            </div>
            <span class="text-slate-500 text-[11px]">{{ c.issue_date }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/services/api';
import { 
  Sparkles, 
  Wand2, 
  Save, 
  Loader2, 
  CheckCircle2, 
  AlertCircle, 
  ExternalLink 
} from 'lucide-vue-next';

const router = useRouter();
const generatedData = ref(null);
const generating = ref(false);
const saving = ref(false);
const successMsg = ref('');
const errorMsg = ref('');

const generateResume = async () => {
  generating.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.post('/student/resume/generate');
    generatedData.value = res.data;
    successMsg.value = 'Resume generated successfully from database profile records!';
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to generate resume.';
  } finally {
    generating.value = false;
  }
};

const saveAsVersion = async () => {
  if (!generatedData.value) return;
  saving.value = true;
  try {
    const title = `AI Resume - ${generatedData.value.target_role || 'Software Engineer'} (${new Date().toLocaleDateString()})`;
    await apiClient.post('/student/resume/save-generated', {
      title: title,
      resume_data: generatedData.value,
      set_active: true
    });
    successMsg.value = 'Saved as active resume version in Smart Resume Manager!';
    setTimeout(() => {
      router.push('/resume-versions');
    }, 1500);
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to save generated resume version.';
  } finally {
    saving.value = false;
  }
};
</script>
