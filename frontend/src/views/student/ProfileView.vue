<template>
  <div class="space-y-6">
    <!-- Top Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <UserIcon class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Profile & Account</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Student Profile</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Manage your personal details, contact information, academic background, and recruiter visibility.
        </p>
      </div>

      <div class="flex items-center space-x-3 shrink-0">
        <button 
          v-if="!isEditing"
          @click="startEditing" 
          class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center space-x-2"
        >
          <Edit3 class="w-4 h-4" />
          <span>Edit Profile Details</span>
        </button>
        <div v-else class="flex items-center space-x-2">
          <button 
            @click="cancelEditing" 
            class="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition-all"
          >
            Cancel
          </button>
          <button 
            @click="saveProfile" 
            :disabled="saving"
            class="px-4 py-2.5 bg-[#10B981] hover:bg-emerald-600 text-white font-bold text-xs rounded-xl transition-all shadow-sm flex items-center space-x-2 disabled:opacity-60"
          >
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <Save v-else class="w-4 h-4" />
            <span>Save Profile</span>
          </button>
        </div>
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
      <span class="text-sm font-semibold">Loading student profile...</span>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: Profile Card Preview -->
      <div class="space-y-6">
        <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm text-center">
          <!-- Profile Avatar with Hover Upload Overlay -->
          <div class="relative w-28 h-28 mx-auto mb-3 group">
            <img 
              :src="formattedProfilePicture" 
              alt="Student Avatar"
              class="w-28 h-28 rounded-full object-cover border-4 border-blue-50 shadow-md transition-all group-hover:brightness-90"
            />
            <button 
              @click="triggerFileInput"
              :disabled="uploadingAvatar"
              type="button"
              title="Click to change profile picture"
              class="absolute inset-0 flex flex-col items-center justify-center bg-black/40 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-[1px] cursor-pointer"
            >
              <Camera class="w-6 h-6 mb-0.5" />
              <span class="text-[10px] font-bold">Change</span>
            </button>
            <span class="absolute bottom-1 right-1 w-5 h-5 bg-[#10B981] border-2 border-white rounded-full shadow-sm"></span>
          </div>

          <!-- Upload Photo Button & Hidden File Input -->
          <div class="mb-4">
            <input 
              ref="fileInputRef" 
              type="file" 
              accept="image/jpeg,image/png,image/jpg,image/webp" 
              class="hidden" 
              @change="handleFileUpload" 
            />
            <button 
              @click="triggerFileInput" 
              :disabled="uploadingAvatar"
              type="button"
              class="inline-flex items-center space-x-1.5 px-3.5 py-1.5 bg-blue-50 hover:bg-blue-100 text-[#2563EB] text-xs font-bold rounded-xl transition-colors border border-blue-100 shadow-2xs disabled:opacity-60 cursor-pointer"
            >
              <Loader2 v-if="uploadingAvatar" class="w-3.5 h-3.5 animate-spin text-[#2563EB]" />
              <Camera v-else class="w-3.5 h-3.5 text-[#2563EB]" />
              <span>{{ uploadingAvatar ? 'Uploading Photo...' : 'Change Profile Picture' }}</span>
            </button>
            <p class="text-[10px] text-slate-400 mt-1">Supports JPG, JPEG, PNG, WEBP (Max 5MB)</p>
          </div>

          <h2 class="text-lg font-extrabold text-[#0F172A]">{{ authStore.studentName }}</h2>
          <p class="text-xs text-[#2563EB] font-bold mt-0.5">{{ profileForm.headline }}</p>
          <p class="text-xs text-slate-500 mt-1 font-medium">{{ profileForm.university }}</p>
          <p class="text-[11px] text-slate-400 font-medium">{{ profileForm.major }} • Class of {{ profileForm.graduation_year }}</p>

          <div class="mt-4 pt-4 border-t border-slate-100 flex justify-center space-x-3">
            <a v-if="profileForm.linkedin_url" :href="profileForm.linkedin_url" target="_blank" class="p-2 rounded-xl bg-blue-50 text-[#2563EB] hover:bg-blue-100 transition-colors">
              <Linkedin class="w-4 h-4" />
            </a>
            <a v-if="profileForm.github_url" :href="profileForm.github_url" target="_blank" class="p-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors">
              <Github class="w-4 h-4" />
            </a>
            <a v-if="profileForm.website" :href="profileForm.website" target="_blank" class="p-2 rounded-xl bg-purple-50 text-[#8B5CF6] hover:bg-purple-100 transition-colors">
              <Globe class="w-4 h-4" />
            </a>
          </div>
        </div>

        <!-- Career Readiness Metric Card -->
        <div class="bg-gradient-to-br from-[#0F172A] to-[#1E293B] rounded-2xl p-6 text-white shadow-md space-y-3">
          <div class="flex items-center justify-between text-xs text-blue-300 font-bold">
            <span class="flex items-center"><Sparkles class="w-4 h-4 mr-1.5 text-[#10B981]" /> Readiness Index</span>
            <span class="text-white text-sm font-extrabold">{{ profileData?.career_readiness_score ?? 0 }}%</span>
          </div>
          <div class="w-full bg-white/10 h-2.5 rounded-full overflow-hidden">
            <div class="bg-gradient-to-r from-[#2563EB] to-[#10B981] h-full rounded-full" :style="{ width: (profileData?.career_readiness_score ?? 0) + '%' }"></div>
          </div>
          <p class="text-[11px] text-slate-300 leading-relaxed">
            Your student profile score is automatically calculated based on skills, education, resume, and career preference completeness.
          </p>
        </div>
      </div>

      <!-- Right 2 Columns: Editable Details Form -->
      <div class="lg:col-span-2 bg-white rounded-2xl p-6 md:p-8 border border-[#E2E8F0] shadow-sm space-y-6">
        <div>
          <h3 class="text-base font-bold text-[#0F172A] mb-1">Personal & Contact Information</h3>
          <p class="text-xs text-slate-500">Keep your details up to date for campus recruiters and career advisors.</p>
        </div>

        <form @submit.prevent="saveProfile" class="space-y-5">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Full Name (Readonly from User Auth) -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input 
                :value="authStore.studentName" 
                disabled
                class="w-full px-3.5 py-2.5 bg-slate-100 border border-slate-200 rounded-xl text-xs text-slate-500 font-medium cursor-not-allowed"
              />
            </div>

            <!-- Email (Readonly from User Auth) -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
              <input 
                :value="authStore.studentEmail" 
                disabled
                class="w-full px-3.5 py-2.5 bg-slate-100 border border-slate-200 rounded-xl text-xs text-slate-500 font-medium cursor-not-allowed"
              />
            </div>

            <!-- Headline -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-slate-700 mb-1">Professional Headline</label>
              <input 
                v-model="profileForm.headline" 
                :disabled="!isEditing"
                type="text" 
                placeholder="e.g. Computer Science Student & Aspiring Software Engineer"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>

            <!-- Phone -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Phone Number</label>
              <input 
                v-model="profileForm.phone" 
                :disabled="!isEditing"
                type="text" 
                placeholder="+1 (555) 000-0000"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>

            <!-- Location -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Current Location</label>
              <input 
                v-model="profileForm.location" 
                :disabled="!isEditing"
                type="text" 
                placeholder="San Francisco, CA"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>

            <!-- University -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">University / Institution</label>
              <input 
                v-model="profileForm.university" 
                :disabled="!isEditing"
                type="text" 
                placeholder="National Institute of Technology"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>

            <!-- Major / Degree -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Major / Program</label>
              <input 
                v-model="profileForm.major" 
                :disabled="!isEditing"
                type="text" 
                placeholder="Master of Computer Applications (MCA)"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>

            <!-- Graduation Year -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Graduation Year</label>
              <input 
                v-model.number="profileForm.graduation_year" 
                :disabled="!isEditing"
                type="number" 
                placeholder="2026"
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>

            <!-- Profile Picture URL -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Profile Avatar Image URL</label>
              <input 
                v-model="profileForm.profile_picture" 
                :disabled="!isEditing"
                type="url" 
                placeholder="https://..."
                class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
              />
            </div>
          </div>

          <!-- Social / Portfolio URLs -->
          <div class="pt-4 border-t border-slate-100 space-y-4">
            <h4 class="text-xs font-bold text-slate-700 uppercase tracking-wider">Social Links & Portfolio</h4>
            
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs font-semibold text-slate-600 mb-1">LinkedIn Profile</label>
                <input 
                  v-model="profileForm.linkedin_url" 
                  :disabled="!isEditing"
                  type="text" 
                  placeholder="https://linkedin.com/in/..."
                  class="w-full px-3 py-2 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs disabled:bg-slate-50 disabled:text-slate-600"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-600 mb-1">GitHub Profile</label>
                <input 
                  v-model="profileForm.github_url" 
                  :disabled="!isEditing"
                  type="text" 
                  placeholder="https://github.com/..."
                  class="w-full px-3 py-2 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs disabled:bg-slate-50 disabled:text-slate-600"
                />
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-600 mb-1">Personal Portfolio / Blog</label>
                <input 
                  v-model="profileForm.website" 
                  :disabled="!isEditing"
                  type="text" 
                  placeholder="https://..."
                  class="w-full px-3 py-2 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs disabled:bg-slate-50 disabled:text-slate-600"
                />
              </div>
            </div>
          </div>

          <!-- Bio -->
          <div class="pt-4 border-t border-slate-100">
            <label class="block text-xs font-semibold text-slate-700 mb-1">Student Bio & Career Summary</label>
            <textarea 
              v-model="profileForm.bio" 
              :disabled="!isEditing"
              rows="4" 
              placeholder="Describe your technical background, interest areas, and target career goals..."
              class="w-full px-3.5 py-2.5 bg-[#F5F8FA] border border-[#E2E8F0] rounded-xl text-xs text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 disabled:bg-slate-50 disabled:text-slate-600"
            ></textarea>
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
  User as UserIcon, 
  Edit3, 
  Save, 
  Loader2, 
  Sparkles, 
  Linkedin, 
  Github, 
  Globe, 
  CheckCircle2, 
  AlertCircle,
  Camera
} from 'lucide-vue-next';

const authStore = useAuthStore();
const profileData = ref(null);
const loading = ref(true);
const isEditing = ref(false);
const saving = ref(false);
const uploadingAvatar = ref(false);
const fileInputRef = ref(null);
const successMsg = ref('');
const errorMsg = ref('');

const profileForm = ref({
  headline: '',
  phone: '',
  location: '',
  linkedin_url: '',
  github_url: '',
  website: '',
  university: '',
  major: '',
  graduation_year: 2026,
  bio: '',
  profile_picture: ''
});

// Helper to format image URL (supports relative /uploads paths and full URLs)
const formattedProfilePicture = computed(() => {
  const pic = profileForm.value.profile_picture || profileData.value?.profile_picture;
  if (!pic) {
    return 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=300';
  }
  if (pic.startsWith('http://') || pic.startsWith('https://') || pic.startsWith('data:')) {
    return pic;
  }
  return `http://127.0.0.1:8000${pic.startsWith('/') ? '' : '/'}${pic}`;
});

const loadProfile = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.get('/student/profile');
    profileData.value = res.data;
    profileForm.value = {
      headline: res.data.headline || '',
      phone: res.data.phone || '',
      location: res.data.location || '',
      linkedin_url: res.data.linkedin_url || '',
      github_url: res.data.github_url || '',
      website: res.data.website || '',
      university: res.data.university || '',
      major: res.data.major || '',
      graduation_year: res.data.graduation_year || 2026,
      bio: res.data.bio || '',
      profile_picture: res.data.profile_picture || ''
    };
  } catch (err) {
    console.error('Failed to load profile:', err);
    errorMsg.value = 'Failed to load profile details from backend database.';
  } finally {
    loading.value = false;
  }
};

const triggerFileInput = () => {
  if (fileInputRef.value) {
    fileInputRef.value.click();
  }
};

const handleFileUpload = async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;

  errorMsg.value = '';
  successMsg.value = '';

  // Validate allowed extensions and mime types
  const validExtensions = ['.jpg', '.jpeg', '.png', '.webp'];
  const fileNameLower = file.name.toLowerCase();
  const hasValidExt = validExtensions.some(ext => fileNameLower.endsWith(ext));
  
  if (!hasValidExt) {
    errorMsg.value = 'Invalid image file format. Please select a JPG, JPEG, PNG, or WEBP image.';
    if (fileInputRef.value) fileInputRef.value.value = '';
    return;
  }

  // Validate file size limit (5MB)
  const maxSize = 5 * 1024 * 1024;
  if (file.size > maxSize) {
    errorMsg.value = 'Selected image size exceeds the 5MB limit. Please choose a smaller image.';
    if (fileInputRef.value) fileInputRef.value.value = '';
    return;
  }

  uploadingAvatar.value = true;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await apiClient.post('/student/profile/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    profileData.value = res.data;
    profileForm.value.profile_picture = res.data.profile_picture;
    successMsg.value = 'Profile picture changed and saved successfully!';

    // Refresh auth store to update header avatar & local storage
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to upload profile picture:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to upload profile picture. Please try again.';
  } finally {
    uploadingAvatar.value = false;
    if (fileInputRef.value) {
      fileInputRef.value.value = '';
    }
  }
};

const startEditing = () => {
  isEditing.value = true;
  successMsg.value = '';
  errorMsg.value = '';
};

const cancelEditing = () => {
  isEditing.value = false;
  loadProfile();
};

const saveProfile = async () => {
  saving.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    const res = await apiClient.put('/student/profile', profileForm.value);
    profileData.value = res.data;
    isEditing.value = false;
    successMsg.value = 'Profile details updated successfully in the database!';
    // Refresh auth store current user profile data
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Failed to update profile:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to save changes.';
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadProfile();
});
</script>
