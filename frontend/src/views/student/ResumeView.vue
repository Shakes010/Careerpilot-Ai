<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <FileText class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Document Management</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Resume & ATS Optimizer</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Upload, manage, and analyze your resume for ATS formatting and recruiter matches.
        </p>
      </div>

      <label 
        class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center space-x-2 shrink-0 cursor-pointer"
      >
        <Upload class="w-4 h-4" />
        <span>{{ resume ? 'Upload New Version' : 'Upload Resume PDF' }}</span>
        <input type="file" accept=".pdf,.docx,.doc" class="hidden" @change="handleFileUpload" />
      </label>
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
      <span class="text-sm font-semibold">Analyzing student resume...</span>
    </div>

    <!-- Empty Upload Dropzone State -->
    <div v-else-if="!resume" class="bg-white rounded-2xl p-12 border-2 border-dashed border-[#E2E8F0] hover:border-blue-300 text-center space-y-4 shadow-sm transition-colors">
      <div class="w-16 h-16 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto">
        <UploadCloud class="w-8 h-8" />
      </div>
      <div class="max-w-md mx-auto space-y-1">
        <h3 class="text-base font-bold text-[#0F172A]">No Resume Uploaded</h3>
        <p class="text-xs text-slate-500">
          Upload your PDF or Word resume (.pdf, .docx, max 10MB) to enable ATS keyword analysis and job application attachment.
        </p>
      </div>
      <label class="px-5 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl hover:bg-blue-600 transition-all shadow-sm inline-flex items-center space-x-2 cursor-pointer">
        <Upload class="w-4 h-4" />
        <span>Browse Resume File</span>
        <input type="file" accept=".pdf,.docx,.doc" class="hidden" @change="handleFileUpload" />
      </label>
    </div>

    <!-- Active Resume Display & ATS Analysis Card -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: Document File Card -->
      <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-5">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Document</span>
          <span class="px-2.5 py-0.5 text-[10px] font-extrabold bg-green-50 text-[#10B981] border border-green-200 rounded-full">
            Verified PDF
          </span>
        </div>

        <div class="p-4 rounded-xl bg-[#F5F8FA] border border-slate-200 flex items-center space-x-4">
          <div class="w-12 h-12 rounded-xl bg-red-50 text-red-600 flex items-center justify-center shrink-0">
            <FileText class="w-6 h-6" />
          </div>
          <div class="min-w-0 flex-1">
            <h3 class="text-xs font-extrabold text-[#0F172A] truncate" :title="resume.filename">{{ resume.filename }}</h3>
            <p class="text-[11px] text-slate-500 mt-0.5">{{ formatBytes(resume.file_size) }} • {{ formatDate(resume.uploaded_at) }}</p>
          </div>
        </div>

        <div class="space-y-2 pt-2 border-t border-slate-100">
          <label class="w-full py-2.5 px-4 bg-blue-50 hover:bg-blue-100 text-[#2563EB] font-bold text-xs rounded-xl transition-colors flex items-center justify-center space-x-2 cursor-pointer">
            <RefreshCw class="w-3.5 h-3.5" />
            <span>Replace Resume</span>
            <input type="file" accept=".pdf,.docx,.doc" class="hidden" @change="handleFileUpload" />
          </label>

          <button 
            @click="deleteResume" 
            class="w-full py-2.5 px-4 bg-red-50 hover:bg-red-100 text-red-600 font-bold text-xs rounded-xl transition-colors flex items-center justify-center space-x-2"
          >
            <Trash2 class="w-3.5 h-3.5" />
            <span>Delete Resume</span>
          </button>
        </div>
      </div>

      <!-- Right 2 Columns: ATS Analysis & Parsed Keywords -->
      <div class="lg:col-span-2 space-y-6">
        <!-- ATS Score Overview -->
        <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-base font-extrabold text-[#0F172A]">ATS Resume Compatibility</h2>
              <p class="text-xs text-slate-500">Evaluated by CareerPilot AI parser against technical job requirements.</p>
            </div>
            <span class="text-3xl font-extrabold text-[#2563EB]">{{ resume.ats_score }}%</span>
          </div>

          <div class="w-full bg-slate-100 h-3 rounded-full overflow-hidden">
            <div 
              class="bg-gradient-to-r from-[#2563EB] via-[#8B5CF6] to-[#10B981] h-full rounded-full transition-all duration-700" 
              :style="{ width: resume.ats_score + '%' }"
            ></div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
            <div class="p-3 rounded-xl bg-green-50 border border-green-100">
              <span class="font-bold text-[#10B981] block">Format & Layout</span>
              <span class="text-[11px] text-slate-600">Standard single-column PDF</span>
            </div>
            <div class="p-3 rounded-xl bg-blue-50 border border-blue-100">
              <span class="font-bold text-[#2563EB] block">Keyword Match</span>
              <span class="text-[11px] text-slate-600">High alignment with MCA skills</span>
            </div>
            <div class="p-3 rounded-xl bg-purple-50 border border-purple-100">
              <span class="font-bold text-[#8B5CF6] block">Section Headings</span>
              <span class="text-[11px] text-slate-600">Education, Experience, Skills</span>
            </div>
          </div>
        </div>

        <!-- Parsed Summary & Recommendations -->
        <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-3">
          <h3 class="text-xs font-bold text-[#0F172A] uppercase tracking-wider flex items-center">
            <Sparkles class="w-4 h-4 mr-1.5 text-[#2563EB]" />
            Parsed Executive Summary
          </h3>
          <p class="text-xs text-slate-700 leading-relaxed font-medium bg-[#F5F8FA] p-4 rounded-xl border border-slate-200">
            {{ resume.summary }}
          </p>

          <div class="pt-2">
            <h4 class="text-xs font-bold text-slate-700 mb-2">ATS Optimization Tips</h4>
            <ul class="space-y-1.5 text-xs text-slate-600">
              <li class="flex items-start space-x-2">
                <CheckCircle2 class="w-3.5 h-3.5 text-[#10B981] shrink-0 mt-0.5" />
                <span>Include quantifiable project metrics (e.g. "Improved API response speed by 40%").</span>
              </li>
              <li class="flex items-start space-x-2">
                <CheckCircle2 class="w-3.5 h-3.5 text-[#10B981] shrink-0 mt-0.5" />
                <span>Ensure tech stack keywords like FastAPI, Vue.js, and PostgreSQL appear in project bullet points.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';
import { 
  FileText, 
  Upload, 
  UploadCloud, 
  RefreshCw, 
  Trash2, 
  Loader2, 
  Sparkles, 
  CheckCircle2, 
  AlertCircle 
} from 'lucide-vue-next';

const authStore = useAuthStore();
const resume = ref(null);
const loading = ref(true);
const successMsg = ref('');
const errorMsg = ref('');

const loadResume = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.get('/student/resume');
    resume.value = res.data;
  } catch (err) {
    console.error('Failed to load resume:', err);
    errorMsg.value = 'Failed to load resume information from database.';
  } finally {
    loading.value = false;
  }
};

const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Client-side file validation
  if (!file.name.match(/\.(pdf|docx|doc)$/i)) {
    errorMsg.value = 'Invalid file format. Please upload a PDF or Word document (.pdf, .docx).';
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  loading.value = true;
  successMsg.value = '';
  errorMsg.value = '';

  try {
    const res = await apiClient.post('/student/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    resume.value = res.data;
    successMsg.value = 'Resume uploaded and analyzed successfully!';
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to upload resume:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to upload resume file.';
  } finally {
    loading.value = false;
  }
};

const deleteResume = async () => {
  if (!resume.value) return;
  if (!confirm('Are you sure you want to delete your uploaded resume?')) return;

  loading.value = true;
  successMsg.value = '';
  errorMsg.value = '';

  try {
    await apiClient.delete(`/student/resume/${resume.value.id}`);
    resume.value = null;
    successMsg.value = 'Resume deleted from database.';
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to delete resume:', err);
    errorMsg.value = 'Failed to delete resume.';
  } finally {
    loading.value = false;
  }
};

const formatBytes = (bytes) => {
  if (!bytes) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

onMounted(() => {
  loadResume();
});
</script>
