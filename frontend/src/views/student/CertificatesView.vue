<template>
  <div class="space-y-6">
    <!-- Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Award class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Credentials & Certifications</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">Certificate Management</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Store, verify, and highlight your earned professional certificates and credentials.
        </p>
      </div>

      <button 
        @click="openAddModal" 
        class="px-4 py-2.5 bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs rounded-xl shadow-sm transition-all flex items-center space-x-2 shrink-0"
      >
        <Plus class="w-4 h-4" />
        <span>Add Certificate</span>
      </button>
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

    <!-- Loading State -->
    <div v-if="loading" class="py-16 text-center text-slate-500 flex justify-center items-center space-x-2">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Loading certificates...</span>
    </div>

    <!-- Empty State -->
    <div v-else-if="certificates.length === 0" class="bg-white rounded-2xl p-12 border border-[#E2E8F0] text-center space-y-4 shadow-sm">
      <div class="w-16 h-16 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto">
        <Award class="w-8 h-8" />
      </div>
      <div>
        <h3 class="text-base font-bold text-[#0F172A]">No Certificates Added Yet</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Add certificates from AWS, Coursera, NPTEL, Udemy, or your university to showcase verified achievements.
        </p>
      </div>
      <button 
        @click="openAddModal" 
        class="px-4 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-xl hover:bg-blue-600 inline-flex items-center space-x-2"
      >
        <Plus class="w-4 h-4" />
        <span>Add Your First Certificate</span>
      </button>
    </div>

    <!-- Certificate List -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-5">
      <div 
        v-for="cert in certificates" 
        :key="cert.id"
        class="bg-white rounded-2xl border border-[#E2E8F0] p-6 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
      >
        <div>
          <div class="flex items-start justify-between mb-2">
            <div>
              <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">
                {{ cert.issuing_organization }}
              </span>
              <h3 class="font-bold text-lg text-[#0F172A] mt-2">{{ cert.title }}</h3>
            </div>
            <div class="flex space-x-1">
              <button @click="deleteCert(cert.id)" class="p-1.5 text-slate-400 hover:text-red-600 rounded-lg hover:bg-red-50" title="Delete">
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>

          <p v-if="cert.description" class="text-xs text-slate-600 mb-3">{{ cert.description }}</p>

          <div class="grid grid-cols-2 gap-2 text-xs text-slate-600 bg-slate-50 p-3 rounded-xl border border-slate-100 mb-3">
            <div>
              <span class="text-slate-400 block text-[10px]">Issued:</span>
              <span class="font-medium">{{ cert.issue_date }}</span>
            </div>
            <div v-if="cert.expiry_date">
              <span class="text-slate-400 block text-[10px]">Expires:</span>
              <span class="font-medium">{{ cert.expiry_date }}</span>
            </div>
            <div v-if="cert.credential_id" class="col-span-2">
              <span class="text-slate-400 block text-[10px]">Credential ID:</span>
              <span class="font-mono text-slate-700 truncate block">{{ cert.credential_id }}</span>
            </div>
          </div>

          <div v-if="cert.skills_tags" class="flex flex-wrap gap-1 mb-3">
            <span 
              v-for="s in cert.skills_tags.split(',')" 
              :key="s" 
              class="text-[10px] bg-slate-100 text-slate-600 font-semibold px-2 py-0.5 rounded-md"
            >
              {{ s.trim() }}
            </span>
          </div>
        </div>

        <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
          <a 
            v-if="cert.credential_url" 
            :href="cert.credential_url" 
            target="_blank" 
            class="text-[#2563EB] hover:underline font-bold flex items-center space-x-1"
          >
            <span>View Credential</span>
            <ExternalLink class="w-3.5 h-3.5" />
          </a>
          <span v-else class="text-slate-400 italic">No external URL</span>

          <button 
            v-if="cert.filename" 
            @click="viewCertFile(cert)"
            :disabled="viewingId === cert.id"
            class="text-[#2563EB] hover:text-blue-700 hover:underline font-bold flex items-center space-x-1 transition-colors group cursor-pointer text-left"
            :title="`Click to open ${cert.filename}`"
          >
            <Loader2 v-if="viewingId === cert.id" class="w-3.5 h-3.5 animate-spin text-[#2563EB]" />
            <FileText v-else class="w-3.5 h-3.5 text-[#2563EB] group-hover:scale-110 transition-transform" />
            <span class="truncate max-w-[140px]">{{ cert.filename }}</span>
          </button>
          <span v-else class="text-slate-400 italic text-[11px]">No certificate file</span>
        </div>
      </div>
    </div>

    <!-- Add Certificate Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-lg shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
        <h3 class="text-lg font-bold text-[#0F172A]">Add Certificate</h3>

        <form @submit.prevent="submitCert" class="space-y-3">
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Certificate Title *</label>
            <input v-model="form.title" type="text" required placeholder="e.g., AWS Certified Solutions Architect" class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1">Issuing Organization *</label>
              <input v-model="form.issuing_organization" type="text" required placeholder="e.g., Amazon Web Services" class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1">Issue Date *</label>
              <input v-model="form.issue_date" type="text" required placeholder="e.g., May 2025" class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1">Expiry Date (Optional)</label>
              <input v-model="form.expiry_date" type="text" placeholder="e.g., May 2028" class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 mb-1">Credential ID (Optional)</label>
              <input v-model="form.credential_id" type="text" placeholder="e.g., AWS-123456" class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Credential URL (Optional)</label>
            <input v-model="form.credential_url" type="url" placeholder="https://www.credly.com/badges/..." class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Relevant Skills / Tags</label>
            <input v-model="form.skills_tags" type="text" placeholder="e.g. AWS, Cloud Computing, Docker" class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none" />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Upload Certificate File (PDF / Image / DOCX)</label>
            <input @change="handleFile" type="file" accept=".pdf,.png,.jpg,.jpeg,.webp,.docx" class="w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-[#2563EB] hover:file:bg-blue-100" />
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">Description (Optional)</label>
            <textarea v-model="form.description" rows="2" placeholder="Brief details about skills mastered..." class="w-full px-3.5 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none"></textarea>
          </div>

          <div class="flex justify-end space-x-3 pt-2">
            <button type="button" @click="showModal = false" class="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl">
              Cancel
            </button>
            <button type="submit" :disabled="submitting" class="px-4 py-2 text-xs font-bold bg-[#2563EB] text-white rounded-xl hover:bg-blue-600 flex items-center space-x-2">
              <Loader2 v-if="submitting" class="w-3.5 h-3.5 animate-spin" />
              <span>Save Certificate</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import apiClient from '@/services/api';
import { 
  Award, 
  Plus, 
  CheckCircle2, 
  AlertCircle, 
  Loader2, 
  Trash2, 
  ExternalLink, 
  FileText 
} from 'lucide-vue-next';

const certificates = ref([]);
const loading = ref(true);
const submitting = ref(false);
const showModal = ref(false);
const successMsg = ref('');
const errorMsg = ref('');
const certFile = ref(null);
const viewingId = ref(null);

const viewCertFile = async (cert) => {
  if (!cert || !cert.id || !cert.filename) return;

  errorMsg.value = '';
  viewingId.value = cert.id;

  const ext = cert.filename.slice(cert.filename.lastIndexOf('.')).toLowerCase();
  const isViewable = ['.pdf', '.png', '.jpg', '.jpeg', '.webp'].includes(ext);

  // Synchronously open blank tab inside click handler to bypass browser popup blockers
  let newTab = null;
  if (isViewable) {
    newTab = window.open('about:blank', '_blank');
  }

  try {
    const res = await apiClient.get(`/student/certificates/${cert.id}/file`, {
      responseType: 'blob'
    });

    const contentType = res.headers['content-type'] || 'application/octet-stream';
    const blob = new Blob([res.data], { type: contentType });
    const blobUrl = URL.createObjectURL(blob);

    if (isViewable) {
      if (newTab) {
        newTab.location.href = blobUrl;
      } else {
        window.open(blobUrl, '_blank');
      }
    } else {
      const link = document.createElement('a');
      link.href = blobUrl;
      link.setAttribute('download', cert.filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      if (newTab) {
        newTab.close();
      }
    }

    // Revoke Blob URL after 60s once loaded
    setTimeout(() => {
      URL.revokeObjectURL(blobUrl);
    }, 60000);

  } catch (err) {
    if (newTab) {
      newTab.close(); // Cleanly close tab on error so no empty window remains
    }
    console.error('Failed to view certificate file:', err);
    errorMsg.value = err.response?.data?.detail || 'Failed to open certificate file: File not found or inaccessible.';
  } finally {
    viewingId.value = null;
  }
};

const form = reactive({
  title: '',
  issuing_organization: '',
  issue_date: '',
  expiry_date: '',
  credential_id: '',
  credential_url: '',
  skills_tags: '',
  description: ''
});

const fetchCerts = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get('/student/certificates');
    certificates.value = res.data;
  } catch (err) {
    errorMsg.value = 'Failed to load certificates.';
  } finally {
    loading.value = false;
  }
};

const openAddModal = () => {
  form.title = '';
  form.issuing_organization = '';
  form.issue_date = '';
  form.expiry_date = '';
  form.credential_id = '';
  form.credential_url = '';
  form.skills_tags = '';
  form.description = '';
  certFile.value = null;
  showModal.value = true;
};

const handleFile = (e) => {
  if (e.target.files && e.target.files[0]) {
    certFile.value = e.target.files[0];
  }
};

const submitCert = async () => {
  submitting.value = true;
  try {
    const formData = new FormData();
    formData.append('title', form.title);
    formData.append('issuing_organization', form.issuing_organization);
    formData.append('issue_date', form.issue_date);
    if (form.expiry_date) formData.append('expiry_date', form.expiry_date);
    if (form.credential_id) formData.append('credential_id', form.credential_id);
    if (form.credential_url) formData.append('credential_url', form.credential_url);
    if (form.skills_tags) formData.append('skills_tags', form.skills_tags);
    if (form.description) formData.append('description', form.description);
    if (certFile.value) formData.append('file', certFile.value);

    await apiClient.post('/student/certificates', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    showModal.value = false;
    successMsg.value = 'Certificate added successfully!';
    fetchCerts();
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to add certificate.';
  } finally {
    submitting.value = false;
  }
};

const deleteCert = async (id) => {
  if (!confirm('Delete this certificate?')) return;
  try {
    await apiClient.delete(`/student/certificates/${id}`);
    successMsg.value = 'Certificate deleted.';
    fetchCerts();
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = 'Failed to delete certificate.';
  }
};

onMounted(fetchCerts);
</script>
