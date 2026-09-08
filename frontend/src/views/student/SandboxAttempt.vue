<template>
  <StudentLayout>
    <div class="attempt-page">
      <div class="page-header">
        <router-link to="/student/career-sandbox" class="back-link">
          ← Back to Sandbox Challenges
        </router-link>
      </div>

      <AppLoader v-if="sandboxStore.loading && !attempt" message="Loading sandbox workspace..." />

      <div v-else-if="attempt" class="attempt-container">
        <AppCard>
          <div class="attempt-header">
            <div>
              <h1 class="title">{{ attempt.challenge_title || 'Sandbox Attempt' }}</h1>
              <p class="meta">Started: {{ formatDate(attempt.started_at) }}</p>
            </div>
            <AppBadge :status="attempt.status" size="lg" />
          </div>

          <div class="divider"></div>

          <!-- Submission Feedback Result Box -->
          <div v-if="attempt.status === 'SUBMITTED' || attempt.status === 'EVALUATED'" class="submitted-alert">
            <span class="icon">✅</span>
            <div>
              <h4>Submission Received</h4>
              <p>{{ attempt.feedback || 'Your submission has been received. Evaluation will be connected to the assessment system.' }}</p>
            </div>
          </div>

          <!-- Solution Input Workspace -->
          <div class="workspace-section">
            <label class="form-label">Solution Submission Area *</label>
            <textarea
              v-model="submissionText"
              rows="12"
              class="code-textarea"
              placeholder="Write your code solution or answer submission here..."
              :disabled="attempt.status !== 'STARTED'"
            ></textarea>
          </div>

          <div class="footer-bar">
            <AppButton
              v-if="attempt.status === 'STARTED'"
              variant="primary"
              :loading="sandboxStore.loading"
              @click="handleSubmit"
            >
              Submit Challenge
            </AppButton>
            <router-link v-else to="/student/career-sandbox" class="btn btn-secondary">
              Back to Career Sandbox
            </router-link>
          </div>
        </AppCard>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import StudentLayout from '@/components/layout/StudentLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppBadge from '@/components/common/AppBadge.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import { useSandboxStore } from '@/stores/sandbox'
import { useToast } from '@/components/common/AppToast.vue'

const route = useRoute()
const sandboxStore = useSandboxStore()
const toast = useToast()

const attemptId = route.params.id
const attempt = computed(() => sandboxStore.currentAttempt)
const submissionText = ref('')

const formatDate = (d) => d ? new Date(d).toLocaleString('en-IN') : ''

const handleSubmit = async () => {
  if (!submissionText.value.trim()) {
    toast.show('Please enter your solution before submitting.', 'error')
    return
  }

  try {
    await sandboxStore.submitAttempt(attemptId, submissionText.value)
    toast.show('✓ Challenge submitted successfully')
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Unable to submit challenge.', 'error')
  }
}

onMounted(async () => {
  const res = await sandboxStore.fetchAttemptDetails(attemptId)
  if (res.data && res.data.submission) {
    submissionText.value = res.data.submission
  }
})
</script>

<style scoped>
.attempt-page { display: flex; flex-direction: column; gap: 1.5rem; }
.back-link { font-size: 0.875rem; font-weight: 600; color: var(--primary); }
.attempt-header { display: flex; justify-content: space-between; align-items: flex-start; }
.title { font-size: 1.5rem; font-weight: 700; color: var(--text-heading); }
.meta { font-size: 0.8125rem; color: var(--text-secondary); margin-top: 0.25rem; }

.divider { height: 1px; background-color: var(--border); margin: 1.25rem 0; }

.submitted-alert { display: flex; gap: 1rem; align-items: flex-start; background-color: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 1rem; border-radius: var(--radius-sm); margin-bottom: 1.5rem; }
.submitted-alert .icon { font-size: 1.5rem; }
.submitted-alert h4 { font-size: 1rem; font-weight: 700; margin-bottom: 0.25rem; }
.submitted-alert p { font-size: 0.875rem; }

.workspace-section { display: flex; flex-direction: column; gap: 0.5rem; }
.code-textarea { font-family: 'Fira Code', 'Consolas', monospace; font-size: 0.875rem; background-color: #0f172a; color: #f8fafc; padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--border); line-height: 1.5; resize: vertical; }

.footer-bar { margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; }
</style>
