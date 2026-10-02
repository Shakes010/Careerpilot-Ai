<template>
  <div class="space-y-6">

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toast" class="fixed top-6 right-6 z-50 flex items-center gap-3 px-5 py-3 rounded-2xl shadow-xl border text-xs font-bold backdrop-blur-md" :class="toast.type === 'error' ? 'bg-red-50/95 border-red-200 text-red-700' : 'bg-emerald-50/95 border-emerald-200 text-emerald-800'">
        <span>{{ toast.type === 'error' ? '⚠️' : '✅' }}</span>
        <span>{{ toast.message }}</span>
      </div>
    </transition>

    <!-- ─── Header ──────────────────────────────────────────────────────── -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-extrabold text-[#0F172A]">Verification Assessment Terminal</h1>
        <p class="text-xs text-[#6B7280] mt-1">
          Sequential checkpoint enforcement · Multi-language code execution · Behavioral integrity monitoring
        </p>
      </div>
    </div>

    <!-- ─── Loading spinner ──────────────────────────────────────────────── -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="w-10 h-10 border-4 border-[#2563EB] border-t-transparent rounded-full animate-spin"></div>
      <span class="ml-3 text-sm text-[#6B7280]">{{ loadingMsg }}</span>
    </div>

    <!-- ─── Assessment List (generic /assessments route) ─────────────────── -->
    <div v-else-if="!activeAssessment && !loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

      <!-- Empty state -->
      <div v-if="!assessments.length" class="col-span-3 cp-card text-center py-12 space-y-3">
        <div class="text-3xl">🎯</div>
        <h3 class="font-bold text-[#0F172A]">No Assessments Available</h3>
        <p class="text-xs text-[#6B7280]">Check back later or declare a skill to unlock verifications.</p>
      </div>

      <div v-for="ass in assessments" :key="ass.id" class="cp-card flex flex-col justify-between space-y-4">
        <div>
          <div class="flex items-center justify-between mb-2">
            <span class="cp-badge-verified text-xs capitalize">{{ ass.assessment_type }}</span>
            <span class="text-xs font-semibold text-[#6B7280]">{{ ass.total_checkpoints }} Checkpoints</span>
          </div>
          <h3 class="font-bold text-[#0F172A] text-base mb-1">{{ ass.assessment_name }}</h3>
          <p class="text-xs text-[#6B7280]">Target Skill: {{ ass.skill_name }}</p>

          <!-- Status badge if flagged or retake -->
          <div v-if="ass.status === 'flagged_pending'" class="mt-2.5 p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs space-y-1">
            <div class="font-bold flex items-center gap-1.5 text-amber-800">
              <span>⏳</span> Waiting for Admin Response
            </div>
            <p class="text-[11px] text-amber-700 leading-relaxed">
              {{ ass.status_desc || 'Your previous attempt was flagged for copy/paste anomaly. Admin is reviewing your explanation.' }}
            </p>
          </div>
          <div v-else-if="ass.status === 'flagged_rejected'" class="mt-2.5 p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-900 text-xs space-y-1">
            <div class="font-bold flex items-center gap-1.5 text-red-800">
              <span>⚠️</span> Admin Rejected Previous Attempt
            </div>
            <p class="text-[11px] text-red-700 leading-relaxed">
              {{ ass.status_desc || 'Retake required. Please complete this same assessment honestly to earn your verified badge.' }}
            </p>
          </div>
          <div v-else class="mt-1 flex items-center gap-1.5">
            <span
              v-if="!ass.is_language_flexible"
              class="inline-flex items-center gap-1 text-[10px] font-semibold bg-[#EFF6FF] text-[#2563EB] px-2 py-0.5 rounded-full"
            >
              🔒 {{ getSkillLangLabel(ass) }} Only
            </span>
            <span
              v-else
              class="inline-flex items-center gap-1 text-[10px] font-semibold bg-[#F0FDF4] text-[#16A34A] px-2 py-0.5 rounded-full"
            >
              🌐 Multi-Language (Python, JS, Java, C++)
            </span>
          </div>
        </div>

        <div>
          <!-- If flagged pending: Disabled button -->
          <button
            v-if="ass.status === 'flagged_pending'"
            disabled
            class="cp-btn-secondary text-xs w-full opacity-60 cursor-not-allowed bg-amber-50 text-amber-800 border-amber-300 font-semibold"
          >
            ⏳ Waiting for Admin Response
          </button>
          <!-- If rejected: Retake same assessment -->
          <button
            v-else-if="ass.status === 'flagged_rejected'"
            @click="initiateAssessment(ass)"
            class="cp-btn-primary text-xs w-full bg-amber-600 hover:bg-amber-700 border-amber-600"
          >
            🔄 Retake Same Assessment
          </button>
          <!-- Available: Start verification test -->
          <button
            v-else
            @click="initiateAssessment(ass)"
            class="cp-btn-primary text-xs w-full"
          >
            Start Verification Test →
          </button>
        </div>
      </div>
    </div>

    <!-- ─── Language Selection Screen ────────────────────────────────────── -->
    <div v-else-if="activeAssessment && !languageConfirmed" class="max-w-lg mx-auto space-y-5">
      <div class="cp-card space-y-5">
        <div>
          <h2 class="text-lg font-bold text-[#0F172A]">{{ activeAssessment.assessment_name }}</h2>
          <p class="text-xs text-[#6B7280] mt-1">{{ checkpoints.length }} checkpoints · {{ activeAssessment.skill_name }}</p>
        </div>

        <div class="p-4 bg-[#F8FAFC] border border-[#E5E7EB] rounded-xl space-y-2 text-xs">
          <div class="font-bold text-[#0F172A]">📋 Before You Begin</div>
          <ul class="text-[#475569] space-y-1 list-disc list-inside">
            <li>Checkpoints must be completed in sequence — each one unlocks the next.</li>
            <li>Your code is executed against automated test cases.</li>
            <li>Paste events and timing are logged for integrity monitoring.</li>
            <li>Once you confirm your language, it is <strong>locked for this attempt</strong>.</li>
          </ul>
        </div>

        <!-- Locked language badge for skill-specific assessments -->
        <div v-if="!activeAssessment.is_language_flexible" class="space-y-2">
          <label class="block text-xs font-semibold text-[#0F172A]">Execution Language</label>
          <div class="flex items-center gap-3 p-3 bg-[#EFF6FF] border border-[#BFDBFE] rounded-xl">
            <span class="text-xl">🔒</span>
            <div>
              <div class="font-bold text-[#1D4ED8] text-sm">{{ getSkillLangLabel(activeAssessment) }}</div>
              <div class="text-[10px] text-[#3B82F6]">Fixed — this assessment targets {{ activeAssessment.skill_name }}</div>
            </div>
            <span class="ml-auto text-xs bg-[#DBEAFE] text-[#1D4ED8] px-2 py-0.5 rounded-full font-semibold">🔒 Fixed</span>
          </div>
        </div>

        <!-- Multi-language selector for general/aptitude assessments -->
        <div v-else class="space-y-2">
          <label class="block text-xs font-semibold text-[#0F172A]">Choose Your Language</label>
          <p class="text-[11px] text-[#6B7280]">Your choice is locked once you start. Pick what you know best.</p>
          <div class="grid grid-cols-2 gap-2">
            <button
              v-for="lang in AVAILABLE_LANGUAGES"
              :key="lang.key"
              @click="selectedLanguageKey = lang.key"
              :class="[
                'flex items-center gap-2 p-3 rounded-xl border-2 text-xs font-semibold transition-all',
                selectedLanguageKey === lang.key
                  ? 'border-[#2563EB] bg-[#EFF6FF] text-[#1D4ED8]'
                  : 'border-[#E5E7EB] bg-white text-[#374151] hover:border-[#93C5FD]'
              ]"
            >
              <span class="text-lg">{{ lang.emoji }}</span>
              <div class="text-left">
                <div>{{ lang.label }}</div>
                <div class="text-[10px] font-normal text-[#6B7280]">{{ lang.version }}</div>
              </div>
            </button>
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button @click="cancelAssessment" class="cp-btn-secondary text-xs flex-1">Cancel</button>
          <button @click="confirmLanguageAndStart" class="cp-btn-primary text-xs flex-1">
            Begin Assessment →
          </button>
        </div>
      </div>
    </div>

    <!-- ─── Active Assessment Workspace ──────────────────────────────────── -->
    <div v-else-if="activeAssessment && languageConfirmed" class="space-y-6">

      <!-- Top bar -->
      <div class="cp-card flex items-center justify-between">
        <div>
          <h2 class="text-lg font-bold text-[#0F172A]">{{ activeAssessment.assessment_name }}</h2>
          <div class="flex items-center gap-2 mt-0.5">
            <p class="text-xs text-[#6B7280]">Sequential Checkpoint Sequence</p>
            <span class="inline-flex items-center gap-1 text-[10px] font-semibold bg-[#EFF6FF] text-[#2563EB] px-2 py-0.5 rounded-full">
              {{ resolvedLangLabel }}
            </span>
          </div>
        </div>
        <button @click="cancelAssessment" class="cp-btn-secondary text-xs">Exit Test</button>
      </div>

      <!-- Progress track -->
      <div class="cp-card py-6 relative overflow-hidden">
        <!-- Connecting line -->
        <div class="absolute top-1/2 left-[10%] right-[10%] h-0.5 bg-[#E5E7EB] -translate-y-4 z-0"></div>
        <div class="flex items-start justify-around relative z-10">
          <div v-for="(cp, idx) in checkpoints" :key="cp.id" class="flex flex-col items-center gap-2 w-32">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-300 shadow-sm"
              :class="[
                completedCheckpointIds.includes(cp.id)
                  ? 'bg-[#2563EB] text-white shadow-blue-200 shadow-md'
                  : idx === currentCheckpointIndex
                    ? 'bg-white text-[#2563EB] border-2 border-[#2563EB] ring-4 ring-blue-100'
                    : 'bg-[#F1F5F9] text-[#94A3B8] border border-[#E5E7EB]'
              ]"
            >
              <span v-if="completedCheckpointIds.includes(cp.id)">✓</span>
              <span v-else>{{ cp.sequence_order }}</span>
            </div>
            <span
              class="text-xs font-semibold text-center leading-tight"
              :class="idx === currentCheckpointIndex ? 'text-[#2563EB]' : completedCheckpointIds.includes(cp.id) ? 'text-[#6B7280]' : 'text-[#94A3B8]'"
            >{{ cp.title }}</span>
            <span v-if="idx > currentCheckpointIndex && !completedCheckpointIds.includes(cp.id)" class="text-[10px] text-[#94A3B8]">🔒 Locked</span>
          </div>
        </div>
      </div>

      <!-- Checkpoint Workspace -->
      <div v-if="currentCP" class="cp-card space-y-4">

        <!-- Checkpoint header -->
        <div class="flex items-center justify-between border-b border-[#E5E7EB] pb-3">
          <h3 class="font-bold text-[#0F172A] text-base">
            Checkpoint {{ currentCP.sequence_order }}: {{ currentCP.title }}
          </h3>
          <div class="flex items-center gap-3 text-xs">
            <span class="text-[#6B7280]">⏱ <strong class="text-[#0F172A]">{{ timeSpentSeconds }}s</strong></span>
            <span class="text-[#6B7280]">📋 Pastes: <strong class="text-amber-600">{{ pasteEventCount }}</strong> ({{ pasteCharCount }} chars)</span>
          </div>
        </div>

        <!-- Instructions -->
        <div class="p-4 bg-[#F8FAFC] border border-[#E5E7EB] rounded-xl text-xs space-y-2">
          <div class="font-bold text-[#0F172A]">Instructions & Requirements:</div>
          <p class="text-[#475569] leading-relaxed whitespace-pre-line">{{ currentCP.instructions }}</p>
        </div>

        <!-- Code editor -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs font-semibold">
            <span class="text-[#0F172A]">Your Solution Code</span>
            <span class="text-[10px] bg-[#0F172A] text-[#4ADE80] px-2 py-0.5 rounded font-mono">
              {{ resolvedLangLabel }}
            </span>
          </div>
          <textarea
            v-model="submittedCode"
            @paste="handlePaste"
            :rows="14"
            class="cp-input font-mono text-xs bg-[#0F172A] text-green-400 p-4 leading-relaxed w-full rounded-xl"
            :placeholder="editorPlaceholder"
          ></textarea>
        </div>

        <!-- ─── Test Case Results Panel ──────────────────────────────────── -->
        <div v-if="testResults.length" class="space-y-2">
          <div class="flex items-center justify-between text-xs font-semibold text-[#0F172A]">
            <span>Test Case Results</span>
            <span :class="allTestsPassed ? 'text-green-600' : 'text-red-500'">
              {{ passedCount }}/{{ testResults.length }} passed
            </span>
          </div>
          <div class="rounded-xl border border-[#E5E7EB] overflow-hidden divide-y divide-[#F1F5F9]">
            <div
              v-for="r in testResults"
              :key="r.index"
              class="flex items-start gap-3 px-4 py-3 text-xs"
              :class="r.passed ? 'bg-[#F0FDF4]' : 'bg-[#FFF7F7]'"
            >
              <span class="text-base leading-none mt-0.5">{{ r.passed ? '✅' : '❌' }}</span>
              <div class="flex-1 min-w-0">
                <div class="font-semibold" :class="r.passed ? 'text-green-700' : 'text-red-600'">
                  Test Case {{ r.index }} — {{ r.passed ? 'Passed' : 'Failed' }}
                </div>
                <div v-if="!r.passed && r.error" class="mt-1 font-mono text-[11px] text-red-500 bg-red-50 rounded px-2 py-1 break-all">
                  {{ r.error }}
                </div>
                <div v-else-if="!r.passed" class="mt-1 text-[11px] text-red-400">
                  Output did not match expected result.
                </div>
              </div>
            </div>
          </div>

          <!-- Summary message after failed run -->
          <div v-if="!allTestsPassed" class="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800">
            💡 <strong>{{ passedCount }}/{{ testResults.length }} test cases passed.</strong>
            Review the errors above, fix your code, and resubmit.
            The expected output is not shown — debug using the input hints in the instructions.
          </div>
          <div v-else class="p-3 bg-green-50 border border-green-200 rounded-xl text-xs text-green-800">
            🎉 All test cases passed! Checkpoint saved — moving to next.
          </div>
        </div>

        <!-- ─── Flagging / Explanation Panel ─────────────────────────────── -->
        <div v-if="flagMsg" class="p-4 bg-amber-50 border border-amber-300 rounded-xl text-xs text-amber-800 space-y-3">
          <div class="font-bold text-amber-900">⚠️ Flagged for Human Admin Review:</div>
          <p>{{ flagMsg }}</p>
          <div>
            <label class="block font-semibold mb-1">Please provide your written explanation:</label>
            <textarea v-model="flagExplanation" rows="3" class="cp-input text-xs" placeholder="Explain your approach or logic behind the code..."></textarea>
          </div>
          <button @click="submitExplanation" class="cp-btn-primary text-xs">Submit Explanation</button>
        </div>

        <!-- ─── Submit button ─────────────────────────────────────────────── -->
        <div v-else-if="!allTestsPassed || testResults.length === 0" class="flex justify-end gap-3 pt-2">
          <button
            @click="submitCurrentCP"
            :disabled="submitting || !submittedCode.trim()"
            class="cp-btn-primary text-xs px-6 py-2.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span v-if="submitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ submitting ? 'Running tests…' : `Submit Checkpoint ${currentCP.sequence_order} →` }}</span>
          </button>
        </div>
      </div>

      <!-- All done notification -->
      <div v-if="assessmentPassed" class="cp-card p-6 text-center space-y-3 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200">
        <div class="text-4xl">🏆</div>
        <h3 class="text-lg font-bold text-green-800">Assessment Passed!</h3>
        <button @click="handleAssessmentPassedDone" class="cp-btn-primary text-xs mx-auto">
          Back to Assessments (Next Assessment Ready) →
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch } from '../services/api'

// ─── Constants ───────────────────────────────────────────────────────────────

const AVAILABLE_LANGUAGES = [
  { key: 'python',     label: 'Python 3',    version: 'Python 3.8.1',   emoji: '🐍', id: 71 },
  { key: 'javascript', label: 'JavaScript',  version: 'Node.js 12.14',  emoji: '🟨', id: 63 },
  { key: 'java',       label: 'Java',        version: 'OpenJDK 13',     emoji: '☕', id: 62 },
  { key: 'cpp',        label: 'C++',         version: 'GCC 9.2.0',      emoji: '⚙️', id: 54 },
]

// ─── State ───────────────────────────────────────────────────────────────────

const route = useRoute()

const loading       = ref(false)
const loadingMsg    = ref('Loading…')
const assessments   = ref([])

const activeAssessment        = ref(null)
const checkpoints             = ref([])
const currentCheckpointIndex  = ref(0)
const completedCheckpointIds  = ref([])
const activeAttemptId         = ref(null)

const languageConfirmed       = ref(false)
const selectedLanguageKey     = ref('python')

const submittedCode   = ref('')
const pasteEventCount = ref(0)
const pasteCharCount  = ref(0)
const timeSpentSeconds = ref(0)
const submitting      = ref(false)

const testResults   = ref([])   // [{index, passed, error}]
const passedCount   = ref(0)

const flagMsg         = ref('')
const flagExplanation = ref('')
const assessmentPassed = ref(false)
const toast = ref(null)

let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { message, type }
  toastTimer = setTimeout(() => {
    toast.value = null
  }, 4000)
}

let timerInterval = null

// ─── Computed ────────────────────────────────────────────────────────────────

const currentCP     = computed(() => checkpoints.value[currentCheckpointIndex.value])
const allTestsPassed = computed(() => testResults.value.length > 0 && testResults.value.every(r => r.passed))

const resolvedLangLabel = computed(() => {
  if (!activeAssessment.value) return 'Python'
  if (!activeAssessment.value.is_language_flexible) {
    return getSkillLangLabel(activeAssessment.value)
  }
  return AVAILABLE_LANGUAGES.find(l => l.key === selectedLanguageKey.value)?.label ?? 'Python'
})

const editorPlaceholder = computed(() => {
  const langLabel = resolvedLangLabel.value.toLowerCase()
  if (langLabel.includes('python')) return '# Write your Python solution here…'
  if (langLabel.includes('javascript') || langLabel.includes('js')) return '// Write your JavaScript solution here…'
  if (langLabel.includes('java')) return '// Write your Java solution here…\npublic class Main {\n  public static void main(String[] args) {\n  }\n}'
  if (langLabel.includes('c++') || langLabel.includes('cpp')) return '// Write your C++ solution here…\n#include <iostream>\nusing namespace std;'
  if (langLabel.includes('sql')) return '-- Write your SQL query here…'
  return '// Write your solution here…'
})

// ─── Helpers ─────────────────────────────────────────────────────────────────

function getSkillLangKey(skillName) {
  const s = (skillName || '').toLowerCase()
  if (s.includes('sql')) return 'sql'
  if (s.includes('vue') || s.includes('js') || s.includes('javascript')) return 'javascript'
  return 'python'
}

function getSkillLangLabel(ass) {
  if (ass?.is_language_flexible) return 'Multi-Language'
  const key = getSkillLangKey(ass?.skill_name)
  if (key === 'sql') return 'SQL'
  if (key === 'javascript') return 'JavaScript'
  return 'Python'
}

// ─── Lifecycle ───────────────────────────────────────────────────────────────

onMounted(async () => {
  const skillId = route.query.skill_id || route.params.skillId
  if (skillId) {
    await loadRandomAssessmentForSkill(skillId)
  } else {
    await loadAllAssessments()
  }
})

onUnmounted(() => {
  if (timerInterval) clearInterval(timerInterval)
})

// Watch for route param / query changes (e.g., navigating between skill links)
watch(() => route.query.skill_id || route.params.skillId, async (newSkillId) => {
  cancelAssessment()
  if (newSkillId) {
    await loadRandomAssessmentForSkill(newSkillId)
  } else {
    await loadAllAssessments()
  }
})

// ─── Data loading ────────────────────────────────────────────────────────────

async function loadAllAssessments() {
  loading.value = true
  loadingMsg.value = 'Loading assessments…'
  try {
    const list = await apiFetch('/assessments')
    assessments.value = list
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function loadRandomAssessmentForSkill(skillId) {
  loading.value = true
  loadingMsg.value = 'Selecting a randomised assessment for this skill…'
  try {
    const ass = await apiFetch(`/assessments/by-skill/${skillId}`)
    loading.value = false
    await initiateAssessment(ass)
  } catch (err) {
    loading.value = false
    console.error('No assessment found for this skill — showing list instead.', err)
    await loadAllAssessments()
  }
}

// ─── Assessment flow ─────────────────────────────────────────────────────────

async function initiateAssessment(ass) {
  loading.value = true
  loadingMsg.value = 'Loading assessment details…'
  resetState()
  try {
    const details = await apiFetch(`/assessments/${ass.id}`)
    activeAssessment.value = { ...ass, ...details }
    checkpoints.value = details.checkpoints || []
    languageConfirmed.value = false
    selectedLanguageKey.value = 'python'
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function confirmLanguageAndStart() {
  if (!activeAssessment.value) return
  loading.value = true
  loadingMsg.value = 'Starting attempt…'
  try {
    const langKey = activeAssessment.value.is_language_flexible
      ? selectedLanguageKey.value
      : getSkillLangKey(activeAssessment.value.skill_name)

    const startRes = await apiFetch(`/assessments/${activeAssessment.value.id}/start`, {
      method: 'POST',
      body: JSON.stringify({ chosen_language: langKey })
    })
    activeAttemptId.value = startRes.attempt_id
    languageConfirmed.value = true
    currentCheckpointIndex.value = 0
    completedCheckpointIds.value = []
    assessmentPassed.value = false
    resetMetrics()
    startTimer()
  } catch (err) {
    showToast(err.message, 'error')
  } finally {
    loading.value = false
  }
}

function cancelAssessment() {
  if (timerInterval) clearInterval(timerInterval)
  activeAssessment.value = null
  checkpoints.value = []
  languageConfirmed.value = false
  assessmentPassed.value = false
  resetState()
}

function resetState() {
  currentCheckpointIndex.value = 0
  completedCheckpointIds.value = []
  activeAttemptId.value = null
  testResults.value = []
  passedCount.value = 0
  flagMsg.value = ''
  flagExplanation.value = ''
  if (timerInterval) clearInterval(timerInterval)
  resetMetrics()
}

function resetMetrics() {
  submittedCode.value = ''
  pasteEventCount.value = 0
  pasteCharCount.value = 0
  timeSpentSeconds.value = 0
  testResults.value = []
  passedCount.value = 0
}

function startTimer() {
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = setInterval(() => { timeSpentSeconds.value++ }, 1000)
}

function handlePaste(e) {
  pasteEventCount.value++
  const text = (e.clipboardData || window.clipboardData).getData('text')
  if (text) pasteCharCount.value += text.length
}

// ─── Checkpoint submission ────────────────────────────────────────────────────

async function submitCurrentCP() {
  if (!currentCP.value || submitting.value) return
  submitting.value = true
  testResults.value = []
  passedCount.value = 0

  const langKey = activeAssessment.value?.is_language_flexible
    ? selectedLanguageKey.value
    : getSkillLangKey(activeAssessment.value?.skill_name)

  try {
    const res = await apiFetch(
      `/assessments/attempts/${activeAttemptId.value}/checkpoints/${currentCP.value.id}/submit`,
      {
        method: 'POST',
        body: JSON.stringify({
          submitted_code:    submittedCode.value,
          language:          langKey,
          paste_event_count: pasteEventCount.value,
          paste_char_count:  pasteCharCount.value,
          time_spent_seconds: timeSpentSeconds.value,
        }),
      }
    )

    if (res.status === 'test_failed') {
      testResults.value = res.results || []
      passedCount.value = res.passed_count ?? 0
      return
    }

    if (res.is_flagged) {
      flagMsg.value = res.message
      return
    }

    // Success — show green results momentarily then advance
    if (res.results?.length) {
      testResults.value = res.results
      passedCount.value = res.passed_count ?? res.results.length
    } else {
      testResults.value = [{ index: 1, passed: true }]
      passedCount.value = 1
    }

    completedCheckpointIds.value.push(currentCP.value.id)

    if (res.status === 'passed') {
      assessmentPassed.value = true
      if (timerInterval) clearInterval(timerInterval)
      return
    }

    if (currentCheckpointIndex.value < checkpoints.value.length - 1) {
      setTimeout(() => {
        currentCheckpointIndex.value++
        resetMetrics()
      }, 1400)
    }

  } catch (err) {
    showToast(err.message ?? 'Submission failed. Try again.', 'error')
  } finally {
    submitting.value = false
  }
}

// ─── Flag explanation ─────────────────────────────────────────────────────────

async function handleAssessmentPassedDone() {
  cancelAssessment()
  await loadAllAssessments()
}

async function submitExplanation() {
  try {
    await apiFetch(`/assessments/attempts/${activeAttemptId.value}/explain`, {
      method: 'POST',
      body: JSON.stringify({ explanation: flagExplanation.value }),
    })
    showToast('Explanation submitted to Admin Review Queue. Status: Under Review.')
    cancelAssessment()
    await loadAllAssessments()
  } catch (err) {
    showToast(err.message, 'error')
  }
}
</script>
