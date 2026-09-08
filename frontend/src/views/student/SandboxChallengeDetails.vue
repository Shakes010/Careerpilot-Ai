<template>
  <StudentLayout>
    <div class="challenge-details-page">
      <div class="page-header">
        <router-link to="/student/career-sandbox" class="back-link">
          ← Back to Sandbox Challenges
        </router-link>
      </div>

      <AppLoader v-if="sandboxStore.loading && !challenge" message="Loading challenge details..." />

      <div v-else-if="challenge" class="challenge-card-container">
        <AppCard>
          <div class="challenge-top-row">
            <div>
              <h1 class="title">{{ challenge.title }}</h1>
              <p class="category">Category: {{ challenge.category }}</p>
            </div>
            <span :class="`difficulty-chip diff-${challenge.difficulty.toLowerCase()}`">
              {{ challenge.difficulty }}
            </span>
          </div>

          <div class="divider"></div>

          <div class="section">
            <h3>Challenge Description</h3>
            <p class="desc">{{ challenge.description }}</p>
          </div>

          <div class="section">
            <h3>Instructions & Deliverables</h3>
            <div class="instructions-box">{{ challenge.instructions }}</div>
          </div>

          <div class="section" v-if="challenge.skills">
            <h3>Target Skills Tested</h3>
            <div class="skills-wrap">
              <span v-for="skill in parseSkills(challenge.skills)" :key="skill" class="skill-chip">
                {{ skill }}
              </span>
            </div>
          </div>

          <div class="footer-bar">
            <div class="time-box">
              ⏱️ <strong>Time Limit:</strong> {{ challenge.time_limit ? `${challenge.time_limit} minutes` : 'Untimed' }}
            </div>
            <AppButton
              variant="primary"
              :loading="sandboxStore.loading"
              @click="handleStartChallenge"
            >
              🚀 Start Challenge
            </AppButton>
          </div>
        </AppCard>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import StudentLayout from '@/components/layout/StudentLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import { useSandboxStore } from '@/stores/sandbox'
import { useToast } from '@/components/common/AppToast.vue'

const route = useRoute()
const router = useRouter()
const sandboxStore = useSandboxStore()
const toast = useToast()

const challengeId = route.params.id
const challenge = computed(() => sandboxStore.currentChallenge)

const parseSkills = (str) => str ? str.split(',').map(s => s.trim()).filter(Boolean) : []

const handleStartChallenge = async () => {
  try {
    const res = await sandboxStore.startAttempt(challengeId)
    toast.show('✓ Challenge attempt started!')
    router.push(`/student/career-sandbox/attempt/${res.data.id}`)
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to start challenge attempt.', 'error')
  }
}

onMounted(() => {
  sandboxStore.fetchChallengeDetails(challengeId)
})
</script>

<style scoped>
.challenge-details-page { display: flex; flex-direction: column; gap: 1.5rem; }
.back-link { font-size: 0.875rem; font-weight: 600; color: var(--primary); }
.challenge-top-row { display: flex; justify-content: space-between; align-items: flex-start; }
.title { font-size: 1.625rem; font-weight: 700; color: var(--text-heading); }
.category { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.difficulty-chip { font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.625rem; border-radius: 4px; text-transform: uppercase; }
.diff-beginner { background-color: #dcfce7; color: #166534; }
.diff-intermediate { background-color: #fef3c7; color: #92400e; }
.diff-advanced { background-color: #fee2e2; color: #991b1b; }

.divider { height: 1px; background-color: var(--border); margin: 1.25rem 0; }
.section { margin-bottom: 1.25rem; }
.section h3 { font-size: 1rem; margin-bottom: 0.5rem; }
.desc { font-size: 0.9375rem; color: var(--text-primary); line-height: 1.5; }
.instructions-box { background-color: var(--background); padding: 1rem; border-radius: var(--radius-sm); font-size: 0.875rem; line-height: 1.6; white-space: pre-wrap; font-family: monospace; border: 1px solid var(--border); }

.skills-wrap { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.skill-chip { background-color: var(--primary-light); color: var(--primary); padding: 0.25rem 0.625rem; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600; }

.footer-bar { margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.time-box { font-size: 0.875rem; color: var(--text-secondary); }
</style>
