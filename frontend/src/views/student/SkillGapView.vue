<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Target class="w-4 h-4 text-[#2563EB]" />
          <span>Student Module</span>
          <span>•</span>
          <span>Skill Gap & Growth</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Skill Gap & Learning Roadmaps</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Identify missing competencies required for your target role and access recommended learning modules.
        </p>
      </div>
    </div>

    <!-- Alert Messages -->
    <div v-if="errorMsg" class="p-4 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-semibold flex items-center space-x-2">
      <AlertCircle class="w-4 h-4 shrink-0 text-red-500" />
      <span>{{ errorMsg }}</span>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-16 text-center text-slate-500 flex justify-center items-center space-x-2">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Performing skill-gap analysis...</span>
    </div>

    <div v-else class="space-y-6">
      <!-- Target Role Skill Gap Card -->
      <div class="bg-white rounded-2xl p-6 md:p-8 border border-[#E2E8F0] shadow-sm space-y-6">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Target Role Analysis</span>
            <h2 class="text-xl font-extrabold text-[#0F172A] mt-0.5">{{ gapData?.target_role || 'Software Engineer' }}</h2>
          </div>

          <div class="flex items-center space-x-3 shrink-0">
            <div class="text-right">
              <span class="text-2xl font-extrabold text-[#2563EB]">{{ gapData?.match_percentage || 80 }}%</span>
              <span class="block text-[10px] font-bold text-slate-400 uppercase">Skill Match</span>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Existing Skills Box -->
          <div class="bg-green-50/60 rounded-xl p-5 border border-green-100 space-y-3">
            <div class="flex items-center space-x-2 text-xs font-extrabold text-[#10B981] uppercase tracking-wider">
              <CheckCircle2 class="w-4 h-4" />
              <span>Skills You Possess ({{ gapData?.existing_skills?.length || 0 }})</span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="sk in gapData?.existing_skills || []" 
                :key="sk"
                class="px-3 py-1 bg-white text-[#10B981] font-bold text-xs rounded-lg border border-green-200 shadow-2xs"
              >
                ✓ {{ sk }}
              </span>
            </div>
          </div>

          <!-- Missing Skills Box -->
          <div class="bg-amber-50/60 rounded-xl p-5 border border-amber-100 space-y-3">
            <div class="flex items-center space-x-2 text-xs font-extrabold text-[#F59E0B] uppercase tracking-wider">
              <AlertTriangle class="w-4 h-4" />
              <span>Identified Skill Gaps ({{ gapData?.missing_skills?.length || 0 }})</span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="sk in gapData?.missing_skills || []" 
                :key="sk"
                class="px-3 py-1 bg-white text-[#F59E0B] font-bold text-xs rounded-lg border border-amber-200 shadow-2xs"
              >
                ⚠ Need to learn: {{ sk }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Recommendations Section -->
      <div class="bg-white rounded-2xl p-6 md:p-8 border border-[#E2E8F0] shadow-sm space-y-4">
        <div>
          <h2 class="text-base font-extrabold text-[#0F172A] flex items-center">
            <BookOpen class="w-5 h-5 mr-2 text-[#2563EB]" />
            Recommended Learning Resources
          </h2>
          <p class="text-xs text-slate-500 mt-1">Curated courses and tutorials targeting your identified missing skills.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="res in learningResources" 
            :key="res.id"
            class="p-5 rounded-xl border border-slate-200 bg-[#F5F8FA] hover:bg-white hover:border-blue-200 transition-all flex flex-col justify-between space-y-3"
          >
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-0.5 text-[10px] font-extrabold bg-blue-100 text-[#2563EB] rounded-md uppercase">
                  Target Skill: {{ res.skill_name }}
                </span>
                <span class="text-[10px] font-bold text-slate-400 uppercase">{{ res.difficulty }}</span>
              </div>
              <h3 class="text-sm font-extrabold text-[#0F172A]">{{ res.title }}</h3>
              <p class="text-xs text-slate-500 font-medium">{{ res.provider }} • {{ res.topic }}</p>
            </div>

            <a 
              :href="res.url" 
              target="_blank" 
              class="w-full py-2 bg-white hover:bg-blue-50 text-[#2563EB] font-bold text-xs rounded-lg border border-blue-200 transition-colors flex items-center justify-center space-x-1.5"
            >
              <span>Access Learning Resource</span>
              <ExternalLink class="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api';
import { 
  Target, 
  CheckCircle2, 
  AlertTriangle, 
  BookOpen, 
  ExternalLink, 
  Loader2, 
  AlertCircle 
} from 'lucide-vue-next';

const gapData = ref(null);
const learningResources = ref([]);
const loading = ref(true);
const errorMsg = ref('');

const loadSkillGap = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const [gapRes, learnRes] = await Promise.all([
      apiClient.get('/student/skill-gap'),
      apiClient.get('/student/learning-recommendations')
    ]);
    gapData.value = gapRes.data;
    learningResources.value = learnRes.data;
  } catch (err) {
    console.error('Failed to load skill gap data:', err);
    errorMsg.value = 'Failed to load skill gap analysis.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadSkillGap();
});
</script>
