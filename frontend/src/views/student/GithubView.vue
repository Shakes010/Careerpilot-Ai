<template>
  <div class="space-y-6">
    <!-- Header Banner -->
    <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center space-x-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider mb-1">
          <Github class="w-4 h-4" />
          <span>Student Module</span>
          <span>•</span>
          <span>Open Source Profile</span>
        </div>
        <h1 class="text-2xl font-extrabold text-[#0F172A] tracking-tight">GitHub Integration</h1>
        <p class="text-xs md:text-sm text-slate-500 mt-1">
          Connect your public GitHub username to import public repositories, stargazers, primary coding languages, and open-source contributions.
        </p>
      </div>

      <div v-if="githubProfile" class="flex items-center space-x-3 shrink-0">
        <button 
          @click="syncGithub" 
          :disabled="syncing"
          class="px-4 py-2.5 bg-blue-50 text-[#2563EB] hover:bg-blue-100 font-bold text-xs rounded-xl transition-all flex items-center space-x-2 shrink-0"
        >
          <RefreshCw :class="['w-4 h-4', syncing ? 'animate-spin' : '']" />
          <span>Sync Now</span>
        </button>
        <button 
          @click="disconnectGithub" 
          class="px-4 py-2.5 bg-red-50 text-red-600 hover:bg-red-100 font-bold text-xs rounded-xl transition-all shrink-0"
        >
          Disconnect
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

    <!-- Loading State -->
    <div v-if="loading" class="py-16 text-center text-slate-500 flex justify-center items-center space-x-2">
      <Loader2 class="w-6 h-6 animate-spin text-[#2563EB]" />
      <span class="text-sm font-semibold">Loading GitHub profile details...</span>
    </div>

    <!-- Connect GitHub Form (If not connected) -->
    <div v-else-if="!githubProfile" class="bg-white rounded-2xl p-8 border border-[#E2E8F0] shadow-sm max-w-xl mx-auto text-center space-y-5">
      <div class="w-16 h-16 rounded-2xl bg-slate-900 text-white flex items-center justify-center mx-auto">
        <Github class="w-8 h-8" />
      </div>

      <div>
        <h3 class="text-lg font-bold text-[#0F172A]">Connect Your Public GitHub Profile</h3>
        <p class="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          Enter your GitHub username to automatically fetch public projects, stars, and programming languages for your Career Passport and AI Resume.
        </p>
      </div>

      <form @submit.prevent="connectGithub" class="flex flex-col sm:flex-row items-center gap-3">
        <div class="relative flex-1 w-full">
          <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center text-slate-400 text-xs font-semibold">
            github.com/
          </span>
          <input 
            v-model="usernameInput" 
            type="text" 
            required 
            :placeholder="usernameInput || 'octocat'" 
            class="w-full pl-24 pr-4 py-2.5 text-xs font-semibold border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#2563EB] outline-none"
          />
        </div>
        <button 
          type="submit" 
          :disabled="connecting"
          class="w-full sm:w-auto px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl shadow-sm transition-all flex items-center justify-center space-x-2 shrink-0"
        >
          <Loader2 v-if="connecting" class="w-4 h-4 animate-spin" />
          <span>Fetch Profile</span>
        </button>
      </form>
    </div>

    <!-- Connected GitHub Profile Display -->
    <div v-else class="space-y-6">
      <!-- Profile Card -->
      <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-6">
        <img 
          :src="githubProfile.avatar_url" 
          :alt="githubProfile.username" 
          class="w-20 h-20 rounded-2xl border-2 border-slate-100 object-cover shadow-sm shrink-0" 
        />
        
        <div class="flex-1 text-center sm:text-left space-y-2">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h2 class="text-xl font-bold text-[#0F172A]">{{ githubProfile.name || githubProfile.username }}</h2>
              <a :href="githubProfile.html_url" target="_blank" class="text-xs font-semibold text-[#2563EB] hover:underline inline-flex items-center space-x-1">
                <span>@{{ githubProfile.username }}</span>
                <ExternalLink class="w-3 h-3" />
              </a>
            </div>

            <div class="text-[11px] text-slate-400 font-medium">
              Last synced: {{ formatDate(githubProfile.last_synced_at) }}
            </div>
          </div>

          <p v-if="githubProfile.bio" class="text-xs text-slate-600 max-w-2xl">{{ githubProfile.bio }}</p>

          <div class="flex flex-wrap items-center justify-center sm:justify-start gap-4 pt-2 text-xs">
            <div class="bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-100">
              <span class="text-slate-400 block text-[10px]">Public Repos</span>
              <span class="font-extrabold text-[#0F172A] text-sm">{{ githubProfile.public_repos }}</span>
            </div>
            <div class="bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-100">
              <span class="text-slate-400 block text-[10px]">Followers</span>
              <span class="font-extrabold text-[#0F172A] text-sm">{{ githubProfile.followers }}</span>
            </div>
            <div class="bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-100">
              <span class="text-slate-400 block text-[10px]">Following</span>
              <span class="font-extrabold text-[#0F172A] text-sm">{{ githubProfile.following }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Repositories List -->
      <div class="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
        <h3 class="text-base font-bold text-[#0F172A] flex items-center space-x-2">
          <Code2 class="w-5 h-5 text-[#2563EB]" />
          <span>Public Repositories ({{ githubProfile.repositories?.length || 0 }})</span>
        </h3>

        <div v-if="!githubProfile.repositories || githubProfile.repositories.length === 0" class="text-xs text-slate-500 py-6 text-center">
          No public repositories found.
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="repo in githubProfile.repositories" 
            :key="repo.id"
            class="p-4 rounded-xl border border-slate-200/80 bg-slate-50/50 hover:bg-white hover:shadow-sm transition-all flex flex-col justify-between"
          >
            <div>
              <div class="flex items-center justify-between mb-1">
                <a :href="repo.html_url" target="_blank" class="font-bold text-sm text-[#0F172A] hover:text-[#2563EB] truncate max-w-[220px]">
                  {{ repo.name }}
                </a>
                <span v-if="repo.is_fork" class="text-[9px] font-bold uppercase bg-slate-200 text-slate-600 px-2 py-0.5 rounded-md">
                  Fork
                </span>
              </div>
              <p class="text-xs text-slate-500 line-clamp-2 mb-3">{{ repo.description || 'No description provided.' }}</p>
            </div>

            <div class="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100">
              <span v-if="repo.language" class="font-bold text-[#2563EB] flex items-center space-x-1">
                <span class="w-2 h-2 rounded-full bg-[#2563EB] inline-block"></span>
                <span>{{ repo.language }}</span>
              </span>
              <span v-else class="text-slate-400">Text</span>

              <div class="flex items-center space-x-3">
                <span class="flex items-center space-x-1">
                  <Star class="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                  <span>{{ repo.stargazers_count }}</span>
                </span>
                <span class="flex items-center space-x-1">
                  <GitFork class="w-3.5 h-3.5 text-slate-400" />
                  <span>{{ repo.forks_count }}</span>
                </span>
              </div>
            </div>
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
  Github, 
  RefreshCw, 
  CheckCircle2, 
  AlertCircle, 
  Loader2, 
  ExternalLink, 
  Code2, 
  Star, 
  GitFork 
} from 'lucide-vue-next';

const githubProfile = ref(null);
const loading = ref(true);
const connecting = ref(false);
const syncing = ref(false);
const usernameInput = ref('');
const successMsg = ref('');
const errorMsg = ref('');

const extractGithubUsername = (rawInput) => {
  if (!rawInput) return '';
  let s = String(rawInput).trim();
  s = s.split('?')[0].split('#')[0].trim();
  
  if (s.toLowerCase().startsWith('https://')) s = s.slice(8);
  else if (s.toLowerCase().startsWith('http://')) s = s.slice(7);
  
  if (s.toLowerCase().startsWith('www.')) s = s.slice(4);
  if (s.toLowerCase().startsWith('github.com/')) s = s.slice(11);
  
  s = s.replace(/^@+/, '').replace(/\/+$/, '').trim();
  const parts = s.split('/').filter(p => p.trim());
  return parts.length > 0 ? parts[0] : '';
};

const fetchGithub = async () => {
  loading.value = true;
  errorMsg.value = '';
  try {
    const [ghRes, profileRes] = await Promise.allSettled([
      apiClient.get('/student/github'),
      apiClient.get('/student/profile')
    ]);

    if (ghRes.status === 'fulfilled') {
      githubProfile.value = ghRes.value.data;
    }

    if (profileRes.status === 'fulfilled' && profileRes.value.data?.github_url) {
      const extracted = extractGithubUsername(profileRes.value.data.github_url);
      if (extracted) {
        usernameInput.value = extracted;
      }
    }
  } catch (err) {
    console.error('Failed to load GitHub profile:', err);
    errorMsg.value = 'Failed to load GitHub profile.';
  } finally {
    loading.value = false;
  }
};

const connectGithub = async () => {
  const usernameOnly = extractGithubUsername(usernameInput.value);
  if (!usernameOnly) {
    errorMsg.value = 'Invalid GitHub profile URL.';
    return;
  }
  usernameInput.value = usernameOnly;
  connecting.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.post('/student/github/connect', {
      username: usernameOnly
    });
    githubProfile.value = res.data;
    successMsg.value = `Successfully connected GitHub profile @${res.data.username}!`;
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to connect GitHub profile.';
  } finally {
    connecting.value = false;
  }
};

const syncGithub = async () => {
  syncing.value = true;
  errorMsg.value = '';
  try {
    const res = await apiClient.post('/student/github/sync');
    githubProfile.value = res.data;
    successMsg.value = 'GitHub repositories synced!';
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = 'Failed to sync GitHub repositories.';
  } finally {
    syncing.value = false;
  }
};

const disconnectGithub = async () => {
  if (!confirm('Disconnect your GitHub integration?')) return;
  try {
    await apiClient.delete('/student/github');
    githubProfile.value = null;
    usernameInput.value = '';
    successMsg.value = 'GitHub profile disconnected.';
    setTimeout(() => successMsg.value = '', 4000);
  } catch (err) {
    errorMsg.value = 'Failed to disconnect GitHub.';
  }
};

const formatDate = (d) => {
  if (!d) return '';
  return new Date(d).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

onMounted(fetchGithub);
</script>
