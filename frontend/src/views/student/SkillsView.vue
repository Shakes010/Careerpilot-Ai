<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Zap class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Technical & Soft Skills</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Skills & Competencies</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Add and manage your verified skills, proficiency levels, and tech stack tags stored in the database.
        </p>
      </div>

      <button 
        @click="openAddModal" 
        class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center space-x-2 shrink-0"
      >
        <Plus class="w-4 h-4" />
        <span>Add New Skill</span>
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
      <span class="text-sm font-semibold">Loading student skill records...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="skills.length === 0" class="bg-white rounded-2xl p-12 border border-[#E2E8F0] text-center space-y-4 shadow-sm">
      <div class="w-16 h-16 rounded-2xl bg-amber-50 text-[#F59E0B] flex items-center justify-center mx-auto">
        <Zap class="w-8 h-8" />
      </div>
      <div>
        <h3 class="text-base font-bold text-[#0F172A]">No Skills Added Yet</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Add skills like Python, Vue.js, FastAPI, SQL, or Docker to enable AI career matching and skill-gap analysis.
        </p>
      </div>
      <button 
        @click="openAddModal"
        class="px-4 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl hover:bg-blue-600 transition-all shadow-sm inline-flex items-center space-x-2"
      >
        <Plus class="w-4 h-4" />
        <span>Add Your First Skill</span>
      </button>
    </div>

    <!-- Skill Categories Layout -->
    <div v-else class="space-y-6">
      <div 
        v-for="(catSkills, category) in groupedSkills" 
        :key="category"
        class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4"
      >
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-[#2563EB]"></span>
            <h3 class="text-sm font-extrabold text-[#0F172A] uppercase tracking-wider">{{ category }}</h3>
            <span class="px-2 py-0.5 text-[11px] font-bold bg-slate-100 text-slate-600 rounded-full">
              {{ catSkills.length }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          <div 
            v-for="sk in catSkills" 
            :key="sk.id"
            class="p-4 rounded-xl border border-slate-100 bg-[#F5F8FA] hover:bg-white hover:border-blue-200 transition-all flex items-center justify-between group"
          >
            <div class="space-y-1">
              <div class="flex items-center space-x-1.5">
                <span class="font-extrabold text-sm text-[#0F172A]">{{ sk.skill_name }}</span>
                <ShieldCheck v-if="sk.is_verified" class="w-4 h-4 text-[#10B981]" title="Verified Skill" />
              </div>
              <span 
                :class="[
                  'inline-block px-2 py-0.5 text-[10px] font-bold rounded-md uppercase',
                  sk.proficiency === 'Expert' ? 'bg-purple-100 text-[#8B5CF6]' :
                  sk.proficiency === 'Advanced' ? 'bg-blue-100 text-[#2563EB]' :
                  sk.proficiency === 'Intermediate' ? 'bg-emerald-100 text-[#10B981]' : 'bg-slate-200 text-slate-700'
                ]"
              >
                {{ sk.proficiency }}
              </span>
            </div>

            <div class="flex items-center space-x-1 opacity-80 group-hover:opacity-100">
              <button 
                @click="openEditModal(sk)" 
                class="p-1.5 hover:bg-blue-50 text-slate-400 hover:text-[#2563EB] rounded-lg transition-colors"
                title="Edit Skill"
              >
                <Edit3 class="w-3.5 h-3.5" />
              </button>
              <button 
                @click="confirmDelete(sk.id)" 
                class="p-1.5 hover:bg-red-50 text-slate-400 hover:text-red-600 rounded-lg transition-colors"
                title="Delete Skill"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Form (Create / Edit) -->
    <div v-if="showModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl border border-[#E2E8F0] shadow-2xl max-w-md w-full p-6 space-y-5">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 class="text-base font-extrabold text-[#0F172A]">
            {{ isEditing ? 'Edit Skill' : 'Add New Skill' }}
          </h3>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="saveModal" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Skill Name *</label>
            <input 
              v-model="form.skill_name"
              type="text" 
              required
              placeholder="e.g. Python, Vue.js, PostgreSQL, Docker"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Category</label>
            <select 
              v-model="form.category"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            >
              <option value="Programming Languages">Programming Languages</option>
              <option value="Web Development">Web Development</option>
              <option value="AI / Data Science">AI / Data Science</option>
              <option value="Cloud & DevOps">Cloud & DevOps</option>
              <option value="Soft Skills">Soft Skills & Leadership</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Proficiency Level</label>
            <select 
              v-model="form.proficiency"
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20"
            >
              <option value="Beginner">Beginner (Learning phase)</option>
              <option value="Intermediate">Intermediate (Project experienced)</option>
              <option value="Advanced">Advanced (Proficient / Production ready)</option>
              <option value="Expert">Expert (Mastery / Architecture)</option>
            </select>
          </div>

          <div class="flex items-center space-x-2 pt-1">
            <input 
              v-model="form.is_verified"
              type="checkbox" 
              id="verified-check"
              class="w-4 h-4 rounded text-[#2563EB] focus:ring-0 cursor-pointer"
            />
            <label for="verified-check" class="text-xs font-semibold text-slate-700 cursor-pointer">
              Mark as Verified (Backed by coursework/project)
            </label>
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
              <span>{{ isEditing ? 'Update Skill' : 'Save Skill' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import apiClient from '@/services/api';
import { 
  Zap, 
  Plus, 
  Edit3, 
  Trash2, 
  Loader2, 
  ShieldCheck, 
  X, 
  CheckCircle2, 
  AlertCircle 
} from 'lucide-vue-next';

const authStore = useAuthStore();
const skills = ref([]);
const loading = ref(true);
const saving = ref(false);
const showModal = ref(false);
const isEditing = ref(false);
const currentId = ref(null);
const successMsg = ref('');
const errorMsg = ref('');

const form = ref({
  skill_name: '',
  category: 'Programming Languages',
  proficiency: 'Intermediate',
  is_verified: true
});

const groupedSkills = computed(() => {
  const groups = {};
  skills.value.forEach(s => {
    const cat = s.category || 'Other Skills';
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(s);
  });
  return groups;
});

const loadSkills = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.get('/student/skills');
    skills.value = res.data;
  } catch (err) {
    console.error('Failed to load skills:', err);
    errorMsg.value = 'Failed to load skills from database.';
  } finally {
    loading.value = false;
  }
};

const openAddModal = () => {
  isEditing.value = false;
  currentId.value = null;
  form.value = {
    skill_name: '',
    category: 'Programming Languages',
    proficiency: 'Intermediate',
    is_verified: true
  };
  showModal.value = true;
};

const openEditModal = (sk) => {
  isEditing.value = true;
  currentId.value = sk.id;
  form.value = {
    skill_name: sk.skill_name,
    category: sk.category,
    proficiency: sk.proficiency,
    is_verified: sk.is_verified
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
      await apiClient.put(`/student/skills/${currentId.value}`, form.value);
      successMsg.value = 'Skill updated successfully!';
    } else {
      await apiClient.post('/student/skills', form.value);
      successMsg.value = 'Skill added to database!';
    }
    showModal.value = false;
    await loadSkills();
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to save skill:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to save skill.';
  } finally {
    saving.value = false;
  }
};

const confirmDelete = async (id) => {
  if (!confirm('Remove this skill from your student profile?')) return;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    await apiClient.delete(`/student/skills/${id}`);
    successMsg.value = 'Skill removed.';
    await loadSkills();
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to delete skill:', err);
    errorMsg.value = 'Failed to remove skill.';
  }
};

onMounted(() => {
  loadSkills();
});
</script>
