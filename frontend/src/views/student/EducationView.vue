<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <GraduationCap class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Academic Background</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Education & Degrees</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Manage your academic qualifications, GPA/grades, coursework, and degree details stored in the database.
        </p>
      </div>

      <button 
        @click="openAddModal" 
        class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center space-x-2 shrink-0"
      >
        <Plus class="w-4 h-4" />
        <span>Add Education Entry</span>
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
      <span class="text-sm font-semibold">Loading student education records...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="educations.length === 0" class="bg-white rounded-2xl p-12 border border-[#E2E8F0] text-center space-y-4 shadow-sm">
      <div class="w-16 h-16 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto">
        <BookOpen class="w-8 h-8" />
      </div>
      <div>
        <h3 class="text-base font-bold text-[#0F172A]">No Education Entries Recorded</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Add your degree, university, GPA, and graduation year to boost your career readiness score.
        </p>
      </div>
      <button 
        @click="openAddModal"
        class="px-4 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl hover:bg-blue-600 transition-all shadow-sm inline-flex items-center space-x-2"
      >
        <Plus class="w-4 h-4" />
        <span>Add Your First Degree</span>
      </button>
    </div>

    <!-- Education Timeline List -->
    <div v-else class="space-y-4">
      <div 
        v-for="edu in educations" 
        :key="edu.id"
        class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm hover:border-blue-200 transition-all flex flex-col md:flex-row md:items-start justify-between gap-4"
      >
        <div class="flex items-start space-x-4">
          <div class="w-12 h-12 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0 mt-1">
            <GraduationCap class="w-6 h-6" />
          </div>
          <div class="space-y-1">
            <h3 class="text-base font-extrabold text-[#0F172A]">{{ edu.degree }}</h3>
            <p class="text-xs font-semibold text-slate-700">{{ edu.institution }}</p>
            <div class="flex flex-wrap items-center gap-2 text-xs text-slate-500">
              <span class="font-medium bg-slate-100 px-2.5 py-0.5 rounded-md text-slate-600">
                {{ edu.start_year }} - {{ edu.end_year ? edu.end_year : 'Present' }}
              </span>
              <span v-if="edu.grade" class="font-bold text-[#10B981] bg-green-50 px-2.5 py-0.5 rounded-md border border-green-100">
                GPA / Grade: {{ edu.grade }}
              </span>
            </div>
            <p v-if="edu.details" class="text-xs text-slate-600 mt-2 leading-relaxed font-medium">
              {{ edu.details }}
            </p>
          </div>
        </div>

        <div class="flex items-center space-x-2 self-end md:self-start shrink-0">
          <button 
            @click="openEditModal(edu)"
            class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl transition-all flex items-center space-x-1.5"
          >
            <Edit3 class="w-3.5 h-3.5" />
            <span>Edit</span>
          </button>
          <button 
            @click="confirmDelete(edu.id)"
            class="px-3 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 font-semibold text-xs rounded-xl transition-all flex items-center space-x-1.5"
          >
            <Trash2 class="w-3.5 h-3.5" />
            <span>Delete</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Form (Create / Edit) -->
    <div v-if="showModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl border border-[#E2E8F0] shadow-2xl max-w-lg w-full p-6 md:p-8 space-y-5">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 class="text-base font-extrabold text-[#0F172A]">
            {{ isEditing ? 'Edit Education Entry' : 'Add New Education Entry' }}
          </h3>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="saveModal" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Degree / Program Title *</label>
            <input 
              v-model="form.degree"
              type="text" 
              required
              placeholder="e.g. Master of Computer Applications (MCA) or B.Tech CS"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Institution / University *</label>
            <input 
              v-model="form.institution"
              type="text" 
              required
              placeholder="e.g. National Institute of Technology"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Start Year *</label>
              <input 
                v-model.number="form.start_year"
                type="number" 
                required
                placeholder="2024"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">End Year (or Expected)</label>
              <input 
                v-model.number="form.end_year"
                type="number" 
                placeholder="2026"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Grade / CGPA / Percentage</label>
            <input 
              v-model="form.grade"
              type="text" 
              placeholder="e.g. 3.9 / 4.0 GPA or 88%"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Relevant Details & Coursework</label>
            <textarea 
              v-model="form.details"
              rows="3" 
              placeholder="Specialization, honors, relevant coursework, thesis topic..."
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            ></textarea>
          </div>

          <div class="pt-3 flex justify-end space-x-3 border-t border-slate-100">
            <button 
              type="button"
              @click="closeModal" 
              class="px-4 py-2 bg-slate-100 text-slate-700 text-xs font-bold rounded-xl hover:bg-slate-200"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              :disabled="saving"
              class="px-4 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-xl hover:bg-blue-600 shadow-sm flex items-center space-x-1.5 disabled:opacity-60"
            >
              <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
              <span>{{ isEditing ? 'Update Entry' : 'Save Entry' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';
import { 
  GraduationCap, 
  Plus, 
  Edit3, 
  Trash2, 
  Loader2, 
  BookOpen, 
  X, 
  CheckCircle2, 
  AlertCircle 
} from 'lucide-vue-next';

const authStore = useAuthStore();
const educations = ref([]);
const loading = ref(true);
const saving = ref(false);
const showModal = ref(false);
const isEditing = ref(false);
const currentId = ref(null);
const successMsg = ref('');
const errorMsg = ref('');

const form = ref({
  degree: '',
  institution: '',
  start_year: 2024,
  end_year: 2026,
  grade: '',
  details: ''
});

const loadEducations = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.get('/student/education');
    educations.value = res.data;
  } catch (err) {
    console.error('Failed to load educations:', err);
    errorMsg.value = 'Failed to load education entries.';
  } finally {
    loading.value = false;
  }
};

const openAddModal = () => {
  isEditing.value = false;
  currentId.value = null;
  form.value = {
    degree: '',
    institution: '',
    start_year: 2024,
    end_year: 2026,
    grade: '',
    details: ''
  };
  showModal.value = true;
};

const openEditModal = (edu) => {
  isEditing.value = true;
  currentId.value = edu.id;
  form.value = {
    degree: edu.degree,
    institution: edu.institution,
    start_year: edu.start_year,
    end_year: edu.end_year,
    grade: edu.grade || '',
    details: edu.details || ''
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveModal = async () => {
  saving.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    if (isEditing.value) {
      await apiClient.put(`/student/education/${currentId.value}`, form.value);
      successMsg.value = 'Education entry updated successfully!';
    } else {
      await apiClient.post('/student/education', form.value);
      successMsg.value = 'New education entry added successfully!';
    }
    showModal.value = false;
    await loadEducations();
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to save education:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to save education entry.';
  } finally {
    saving.value = false;
  }
};

const confirmDelete = async (id) => {
  if (!confirm('Are you sure you want to delete this education entry?')) return;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    await apiClient.delete(`/student/education/${id}`);
    successMsg.value = 'Education entry deleted.';
    await loadEducations();
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to delete education:', err);
    errorMsg.value = 'Failed to delete entry.';
  }
};

onMounted(() => {
  loadEducations();
});
</script>
