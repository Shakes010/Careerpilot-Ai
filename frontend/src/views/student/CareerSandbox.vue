<template>
  <StudentLayout>
    <div class="sandbox-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Career Sandbox 🧪</h1>
          <p class="page-subtitle">Practice real-world industry scenarios and test your coding skills in simulated environments.</p>
        </div>
      </div>

      <!-- Search & Category Filters -->
      <AppCard class="filter-card">
        <div class="filter-row">
          <AppInput
            v-model="search"
            placeholder="Search challenges by title, skills or description..."
            @keyup.enter="handleSearch"
          />
          <AppSelect
            v-model="difficulty"
            :options="difficultyOptions"
            placeholder="All Difficulties"
            @change="handleSearch"
          />
        </div>
      </AppCard>

      <!-- Loading State -->
      <AppLoader v-if="sandboxStore.loading && sandboxStore.challenges.length === 0" message="Loading sandbox challenges..." />

      <!-- Empty State -->
      <AppEmptyState
        v-else-if="sandboxStore.challenges.length === 0"
        title="No Career Sandbox challenges available."
        message="Check back soon for new practice challenges released by platform administrators."
      />

      <!-- Challenges Grid -->
      <div v-else class="challenges-grid">
        <AppCard
          v-for="challenge in sandboxStore.challenges"
          :key="challenge.id"
          class="challenge-card"
          hoverable
        >
          <div class="challenge-header">
            <h3 class="challenge-title">{{ challenge.title }}</h3>
            <span :class="`difficulty-chip diff-${challenge.difficulty.toLowerCase()}`">
              {{ challenge.difficulty }}
            </span>
          </div>

          <p class="challenge-desc">{{ truncateText(challenge.description, 140) }}</p>

          <div v-if="challenge.skills" class="skills-tags">
            <span v-for="skill in parseSkills(challenge.skills)" :key="skill" class="skill-tag">
              {{ skill }}
            </span>
          </div>

          <div class="challenge-footer">
            <div class="time-limit font-medium text-xs text-muted">
              ⏱️ Time Limit: {{ challenge.time_limit ? `${challenge.time_limit} mins` : 'Untimed' }}
            </div>
            <router-link :to="`/student/career-sandbox/${challenge.id}`" class="btn btn-secondary btn-sm">
              View Challenge →
            </router-link>
          </div>
        </AppCard>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StudentLayout from '@/components/layout/StudentLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppEmptyState from '@/components/common/AppEmptyState.vue'
import { useSandboxStore } from '@/stores/sandbox'

const sandboxStore = useSandboxStore()

const search = ref('')
const difficulty = ref('')

const difficultyOptions = [
  { label: 'All Difficulties', value: '' },
  { label: 'Beginner', value: 'BEGINNER' },
  { label: 'Intermediate', value: 'INTERMEDIATE' },
  { label: 'Advanced', value: 'ADVANCED' }
]

const parseSkills = (str) => str ? str.split(',').map(s => s.trim()).filter(Boolean) : []
const truncateText = (str, len) => str && str.length > len ? str.substring(0, len) + '...' : str

const handleSearch = () => {
  sandboxStore.fetchChallenges({
    search: search.value || undefined,
    difficulty: difficulty.value || undefined
  })
}

onMounted(() => {
  sandboxStore.fetchChallenges()
})
</script>

<style scoped>
.sandbox-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.filter-row { display: grid; grid-template-columns: 3fr 1fr; gap: 1rem; }

.challenges-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem; }
.challenge-card { display: flex; flex-direction: column; gap: 0.75rem; }
.challenge-header { display: flex; justify-content: space-between; align-items: flex-start; }
.challenge-title { font-size: 1.125rem; font-weight: 700; color: var(--text-heading); }

.difficulty-chip { font-size: 0.6875rem; font-weight: 700; padding: 0.125rem 0.5rem; border-radius: 4px; text-transform: uppercase; }
.diff-beginner { background-color: #dcfce7; color: #166534; }
.diff-intermediate { background-color: #fef3c7; color: #92400e; }
.diff-advanced { background-color: #fee2e2; color: #991b1b; }

.challenge-desc { font-size: 0.875rem; color: var(--text-primary); line-height: 1.45; }

.skills-tags { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.skill-tag { font-size: 0.75rem; background-color: var(--primary-light); color: var(--primary); padding: 0.125rem 0.5rem; border-radius: var(--radius-sm); font-weight: 600; }

.challenge-footer { margin-top: auto; padding-top: 0.75rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.text-muted { color: var(--text-muted); }
.text-xs { font-size: 0.75rem; }
.font-medium { font-weight: 500; }

@media (max-width: 640px) { .filter-row { grid-template-columns: 1fr; } }
</style>
