<template>
  <AdminLayout>
    <div class="skills-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Skill Library Management 📚</h1>
          <p class="page-subtitle">Centralized taxonomy repository for candidate verification and recruiter job tags.</p>
        </div>
        <AppButton variant="primary" @click="openAddModal">
          + Add New Skill
        </AppButton>
      </div>

      <!-- Search & Category Filters -->
      <AppCard class="filter-card">
        <div class="filter-row">
          <AppInput
            v-model="search"
            placeholder="Search skills by name, description or category..."
            @keyup.enter="handleFilter"
          />
          <AppSelect
            v-model="selectedCategory"
            :options="categoryOptions"
            placeholder="All Categories"
            @change="handleFilter"
          />
        </div>
      </AppCard>

      <!-- Skills Table -->
      <div class="skills-table-container">
        <AppTable
          :columns="columns"
          :data="adminStore.skills"
          :loading="adminStore.loading"
          empty-message="No skills found in taxonomy."
        >
          <template #name="{ row }">
            <div class="skill-name-cell">{{ row.name }}</div>
          </template>

          <template #category="{ row }">
            <span class="category-chip">{{ row.category }}</span>
          </template>

          <template #description="{ row }">
            <span class="text-desc">{{ row.description || 'No description provided.' }}</span>
          </template>

          <template #actions="{ row }">
            <div class="table-actions">
              <button class="btn btn-secondary btn-sm" @click="openEditModal(row)">
                Edit
              </button>
              <button class="btn btn-danger btn-sm" @click="deleteSkill(row)">
                Delete
              </button>
            </div>
          </template>
        </AppTable>
      </div>

      <!-- Add/Edit Skill Modal -->
      <AppModal
        :show="skillModal.show"
        :title="skillModal.isEdit ? 'Edit Skill Entry' : 'Add New Skill to Library'"
        @close="skillModal.show = false"
      >
        <form @submit.prevent="saveSkill">
          <AppInput
            v-model="skillModal.form.name"
            label="Skill Name *"
            placeholder="e.g. FastAPI"
            required
            :error="skillModal.error"
          />

          <AppSelect
            v-model="skillModal.form.category"
            label="Skill Category *"
            :options="categoryChoices"
            required
          />

          <div class="form-group">
            <label class="form-label">Description / Summary</label>
            <textarea
              v-model="skillModal.form.description"
              rows="3"
              class="form-textarea"
              placeholder="Brief description of the skill and usage domain..."
            ></textarea>
          </div>
        </form>

        <template #footer>
          <AppButton variant="secondary" @click="skillModal.show = false">Cancel</AppButton>
          <AppButton variant="primary" :loading="skillModal.saving" @click="saveSkill">
            {{ skillModal.isEdit ? 'Save Changes' : 'Add Skill' }}
          </AppButton>
        </template>
      </AppModal>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppTable from '@/components/common/AppTable.vue'
import AppModal from '@/components/common/AppModal.vue'
import { useAdminStore } from '@/stores/admin'
import { useToast } from '@/components/common/AppToast.vue'

const adminStore = useAdminStore()
const toast = useToast()

const search = ref('')
const selectedCategory = ref('')

const columns = [
  { label: 'Skill Name', key: 'name' },
  { label: 'Category', key: 'category' },
  { label: 'Description', key: 'description' },
  { label: 'Actions', key: 'actions' }
]

const categoryChoices = [
  'Backend Engineering',
  'Frontend Engineering',
  'Databases & Storage',
  'DevOps & Cloud',
  'Data Science',
  'Design & Product',
  'Mobile Engineering',
  'General'
]

const categoryOptions = [
  { label: 'All Categories', value: '' },
  ...categoryChoices.map(c => ({ label: c, value: c }))
]

const skillModal = reactive({
  show: false,
  isEdit: false,
  skillId: null,
  form: { name: '', category: 'Backend Engineering', description: '' },
  error: '',
  saving: false
})

const handleFilter = () => {
  adminStore.fetchSkills({
    search: search.value || undefined,
    category: selectedCategory.value || undefined
  })
}

const openAddModal = () => {
  skillModal.isEdit = false
  skillModal.skillId = null
  skillModal.form.name = ''
  skillModal.form.category = 'Backend Engineering'
  skillModal.form.description = ''
  skillModal.error = ''
  skillModal.show = true
}

const openEditModal = (skill) => {
  skillModal.isEdit = true
  skillModal.skillId = skill.id
  skillModal.form.name = skill.name
  skillModal.form.category = skill.category
  skillModal.form.description = skill.description || ''
  skillModal.error = ''
  skillModal.show = true
}

const saveSkill = async () => {
  if (!skillModal.form.name.trim()) {
    skillModal.error = 'Skill name is required.'
    return
  }

  skillModal.saving = true
  try {
    if (skillModal.isEdit) {
      await adminStore.updateSkill(skillModal.skillId, skillModal.form)
      toast.show(`✓ Skill '${skillModal.form.name}' updated`)
    } else {
      await adminStore.createSkill(skillModal.form)
      toast.show(`✓ Skill '${skillModal.form.name}' added to library`)
    }
    skillModal.show = false
  } catch (err) {
    skillModal.error = err.response?.data?.detail || 'Failed to save skill.'
  } finally {
    skillModal.saving = false
  }
}

const deleteSkill = async (skill) => {
  if (confirm(`Delete skill '${skill.name}' from taxonomy library?`)) {
    try {
      await adminStore.deleteSkill(skill.id)
      toast.show(`✓ Skill '${skill.name}' deleted`)
    } catch (err) {
      toast.show('Failed to delete skill.', 'error')
    }
  }
}

onMounted(() => {
  adminStore.fetchSkills()
})
</script>

<style scoped>
.skills-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }
.filter-row { display: grid; grid-template-columns: 3fr 1fr; gap: 1rem; }
.skill-name-cell { font-weight: 700; color: var(--text-heading); font-size: 0.9375rem; }
.category-chip { background-color: var(--primary-light); color: var(--primary); padding: 0.25rem 0.625rem; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 600; }
.text-desc { font-size: 0.8125rem; color: var(--text-secondary); }
.table-actions { display: flex; gap: 0.375rem; }
</style>
