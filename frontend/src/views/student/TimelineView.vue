<template>
  <div class="space-y-6">
    <!-- Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <History class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Career Journey</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Career Timeline</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Chronological milestone history tracking education additions, skills added, certificate achievements, resume uploads, and GitHub activity.
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="py-16 text-center text-slate-500 flex justify-center items-center space-x-2">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Loading timeline events...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="events.length === 0" class="bg-white rounded-2xl p-12 border border-[#E2E8F0] text-center space-y-4 shadow-sm">
      <div class="w-16 h-16 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto">
        <Clock class="w-8 h-8" />
      </div>
      <div>
        <h3 class="text-base font-bold text-[#0F172A]">No Timeline Milestones Logged Yet</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Add an education degree, skill, certificate, or connect GitHub to populate your career timeline.
        </p>
      </div>
    </div>

    <!-- Chronological Vertical Timeline -->
    <div v-else class="bg-white rounded-2xl p-6 md:p-8 border border-[#E2E8F0] shadow-sm">
      <div class="relative border-l-2 border-slate-200 ml-4 md:ml-6 space-y-8 pb-4">
        <div 
          v-for="(evt, idx) in events" 
          :key="evt.id" 
          class="relative pl-6 md:pl-8 group"
        >
          <!-- Category Dot Indicator -->
          <div 
            :class="[
              'absolute -left-[17px] top-1.5 w-8 h-8 rounded-full border-4 border-white flex items-center justify-center text-white shadow-sm transition-transform group-hover:scale-110',
              getCategoryBg(evt.category)
            ]"
          >
            <component :is="getCategoryIcon(evt.category)" class="w-3.5 h-3.5" />
          </div>

          <!-- Event Content Card -->
          <div class="bg-slate-50/80 hover:bg-slate-50 p-4 md:p-5 rounded-2xl border border-slate-200/80 transition-all">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-2">
              <div class="flex items-center space-x-2">
                <span 
                  :class="[
                    'text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded-md',
                    getCategoryBadgeClass(evt.category)
                  ]"
                >
                  {{ evt.category }}
                </span>
                <h3 class="font-bold text-sm md:text-base text-[#0F172A]">{{ evt.title }}</h3>
              </div>

              <span class="text-xs font-semibold text-slate-400">
                {{ formatDate(evt.event_date) }}
              </span>
            </div>

            <p class="text-xs text-slate-600 leading-relaxed">{{ evt.description }}</p>
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
  History, 
  Clock, 
  Loader2, 
  GraduationCap, 
  Zap, 
  Award, 
  FileText, 
  Github, 
  Sliders, 
  Sparkles 
} from 'lucide-vue-next';

const events = ref([]);
const loading = ref(true);

const fetchTimeline = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get('/student/timeline');
    events.value = res.data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const getCategoryBg = (cat) => {
  switch (cat) {
    case 'Education': return 'bg-blue-600';
    case 'Skill': return 'bg-emerald-500';
    case 'Certificate': return 'bg-purple-600';
    case 'Resume': return 'bg-indigo-600';
    case 'GitHub': return 'bg-slate-800';
    case 'Preference': return 'bg-amber-500';
    default: return 'bg-blue-500';
  }
};

const getCategoryBadgeClass = (cat) => {
  switch (cat) {
    case 'Education': return 'bg-blue-100 text-blue-700';
    case 'Skill': return 'bg-emerald-100 text-emerald-700';
    case 'Certificate': return 'bg-purple-100 text-purple-700';
    case 'Resume': return 'bg-indigo-100 text-indigo-700';
    case 'GitHub': return 'bg-slate-200 text-slate-800';
    case 'Preference': return 'bg-amber-100 text-amber-800';
    default: return 'bg-blue-100 text-blue-700';
  }
};

const getCategoryIcon = (cat) => {
  switch (cat) {
    case 'Education': return GraduationCap;
    case 'Skill': return Zap;
    case 'Certificate': return Award;
    case 'Resume': return FileText;
    case 'GitHub': return Github;
    case 'Preference': return Sliders;
    default: return Sparkles;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

onMounted(fetchTimeline);
</script>
