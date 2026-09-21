<template>
  <div class="space-y-6">
    <!-- Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Layers class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Smart Resume Manager</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Resume Version Manager</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Maintain and switch between multiple resume versions tailored for different roles without overwriting past versions.
        </p>
      </div>

      <div class="flex items-center space-x-3 shrink-0">
        <router-link
          to="/resume-generator"
          class="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm transition-all flex items-center space-x-2"
        >
          <Sparkles class="w-4 h-4 text-amber-300" />
          <span>Generate with AI</span>
        </router-link>
        <router-link
          to="/resume"
          class="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition-all flex items-center space-x-2"
        >
          <Upload class="w-4 h-4 text-slate-500" />
          <span>Upload File</span>
        </router-link>
      </div>
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
      <span class="text-sm font-semibold">Loading resume versions...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="versions.length === 0" class="bg-white rounded-2xl p-12 border border-[#E2E8F0] text-center space-y-4 shadow-sm">
      <div class="w-16 h-16 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto">
        <Layers class="w-8 h-8" />
      </div>
      <div>
        <h3 class="text-base font-bold text-[#0F172A]">No Resume Versions Created</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Upload a resume or use the AI Resume Generator to create your first resume version.
        </p>
      </div>
      <div class="flex justify-center space-x-3 pt-2">
        <router-link to="/resume" class="px-4 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-xl hover:bg-blue-600">
          Upload Resume
        </router-link>
        <router-link to="/resume-generator" class="px-4 py-2 bg-slate-100 text-slate-700 text-xs font-bold rounded-xl hover:bg-slate-200">
          Generate with AI
        </router-link>
      </div>
    </div>

    <!-- Resume Version Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <div 
        v-for="v in versions" 
        :key="v.id"
        :class="[
          'bg-white rounded-2xl border p-5 transition-all duration-200 flex flex-col justify-between relative shadow-sm',
          v.is_active ? 'border-[#2563EB] ring-2 ring-blue-500/10' : 'border-[#E2E8F0] hover:border-slate-300'
        ]"
      >
        <!-- Top Badge Info -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <span 
              :class="[
                'text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-1 rounded-full',
                v.is_active ? 'bg-blue-100 text-[#2563EB]' : 'bg-slate-100 text-slate-500'
              ]"
            >
              {{ v.is_active ? 'Primary Active' : v.status }}
            </span>
            <span class="text-[11px] font-bold text-slate-400">
              ATS: <span class="text-slate-700">{{ v.ats_score }}%</span>
            </span>
          </div>

          <h3 class="font-bold text-base text-[#0F172A] line-clamp-1 mb-1">{{ v.title }}</h3>
          <p class="text-xs text-slate-500 line-clamp-2 mb-4">{{ v.summary || 'No summary provided.' }}</p>

          <div class="space-y-1.5 text-xs text-slate-600 bg-slate-50 p-3 rounded-xl mb-4 border border-slate-100">
            <div class="flex justify-between">
              <span class="text-slate-400">Filename:</span>
              <span class="font-medium truncate max-w-[150px]">{{ v.filename }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Source:</span>
              <span class="font-semibold text-blue-600">{{ v.source }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Created:</span>
              <span>{{ formatDate(v.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Action Footer -->
        <div class="flex items-center justify-between pt-3 border-t border-slate-100">
          <button 
            v-if="!v.is_active"
            @click="setActive(v.id)" 
            class="px-3 py-1.5 bg-blue-50 text-[#2563EB] hover:bg-blue-100 text-xs font-bold rounded-lg transition-colors flex items-center space-x-1"
          >
            <CheckCircle2 class="w-3.5 h-3.5" />
            <span>Set Active</span>
          </button>
          <span v-else class="text-xs font-bold text-[#10B981] flex items-center space-x-1">
            <CheckCircle2 class="w-4 h-4 text-[#10B981]" />
            <span>Active Resume</span>
          </span>

          <div class="flex items-center space-x-2">
            <button 
              @click="openRename(v)" 
              class="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg"
              title="Rename"
            >
              <Edit3 class="w-4 h-4" />
            </button>
            <button 
              @click="deleteVersion(v.id)" 
              class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg"
              title="Delete"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Rename Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl space-y-4">
        <h3 class="text-lg font-bold text-[#0F172A]">Rename Resume Version</h3>
        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">Version Title</label>
          <input 
            v-model="editTitle" 
            type="text" 
            class="w-full px-3.5 py-2.5 text-sm border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
          />
        </div>
        <div class="flex justify-end space-x-3 pt-2">
          <button @click="showModal = false" class="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl">
            Cancel
          </button>
          <button @click="saveRename" class="px-4 py-2 text-xs font-bold bg-[#2563EB] text-white rounded-xl hover:bg-blue-600">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/services/api';
import { 
  Layers, 
  Sparkles, 
  Upload, 
  CheckCircle2, 
  AlertCircle, 
  Loader2, 
  Edit3, 
  Trash2 
} from 'lucide-vue-next';

const versions = ref([]);
const loading = ref(true);
const successMsg = ref('');
const errorMsg = ref('');
const showModal = ref(false);
const selectedVersion = ref(null);
const editTitle = ref('');

const fetchVersions = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get('/student/resume-versions');
    versions.value = res.data;
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to load resume versions';
  } finally {
    loading.value = false;
  }
};

const setActive = async (id) => {
  try {
    await apiClient.post(`/student/resume-versions/${id}/set-active`);
    successMsg.value = 'Active resume version updated successfully.';
    fetchVersions();
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = 'Failed to set active version.';
  }
};

const openRename = (v) => {
  selectedVersion.value = v;
  editTitle.value = v.title;
  showModal.value = true;
};

const saveRename = async () => {
  if (!selectedVersion.value || !editTitle.value.trim()) return;
  try {
    await apiClient.put(`/student/resume-versions/${selectedVersion.value.id}`, {
      title: editTitle.value.trim()
    });
    showModal.value = false;
    successMsg.value = 'Resume version title updated.';
    fetchVersions();
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = 'Failed to rename version.';
  }
};

const deleteVersion = async (id) => {
  if (!confirm('Are you sure you want to delete this resume version?')) return;
  try {
    await apiClient.delete(`/student/resume-versions/${id}`);
    successMsg.value = 'Resume version deleted.';
    fetchVersions();
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = 'Failed to delete version.';
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

onMounted(fetchVersions);
</script>
