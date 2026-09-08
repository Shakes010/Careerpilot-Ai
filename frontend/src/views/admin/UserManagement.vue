<template>
  <AdminLayout>
    <div class="user-management-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">User Account Management 👤</h1>
          <p class="page-subtitle">Inspect user accounts, manage active statuses, and update administrative roles.</p>
        </div>
      </div>

      <!-- Filters Card -->
      <AppCard class="filter-card">
        <div class="filter-row">
          <AppInput
            v-model="search"
            placeholder="Search users by name, email or phone..."
            @keyup.enter="handleFilter"
          />
          <AppSelect
            v-model="roleFilter"
            :options="roleOptions"
            placeholder="All Roles"
            @change="handleFilter"
          />
          <AppSelect
            v-model="statusFilter"
            :options="statusOptions"
            placeholder="All Statuses"
            @change="handleFilter"
          />
        </div>
      </AppCard>

      <!-- Users Table -->
      <div class="users-table-container">
        <AppTable
          :columns="columns"
          :data="adminStore.users"
          :loading="adminStore.loading"
          empty-message="No user accounts match current filter criteria."
        >
          <template #user_info="{ row }">
            <div class="font-semibold">{{ row.full_name }}</div>
            <div class="text-xs text-muted">{{ row.email }} • {{ row.phone || 'No phone' }}</div>
          </template>

          <template #role="{ row }">
            <AppSelect
              :model-value="row.role"
              :options="roleChoices"
              size="sm"
              @update:model-value="val => changeRole(row, val)"
            />
          </template>

          <template #is_active="{ row }">
            <span :class="`status-chip ${row.is_active ? 'chip-active' : 'chip-suspended'}`">
              {{ row.is_active ? 'ACTIVE' : 'SUSPENDED' }}
            </span>
          </template>

          <template #actions="{ row }">
            <div class="table-actions">
              <button
                v-if="row.is_active"
                class="btn btn-danger btn-sm"
                @click="toggleUserStatus(row, false)"
              >
                Suspend
              </button>
              <button
                v-else
                class="btn btn-primary btn-sm"
                @click="toggleUserStatus(row, true)"
              >
                Activate
              </button>
            </div>
          </template>
        </AppTable>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppTable from '@/components/common/AppTable.vue'
import { useAdminStore } from '@/stores/admin'
import { useToast } from '@/components/common/AppToast.vue'

const adminStore = useAdminStore()
const toast = useToast()

const search = ref('')
const roleFilter = ref('')
const statusFilter = ref('')

const columns = [
  { label: 'User Details', key: 'user_info' },
  { label: 'Role', key: 'role' },
  { label: 'Status', key: 'is_active' },
  { label: 'Actions', key: 'actions' }
]

const roleChoices = [
  { label: 'Student', value: 'STUDENT' },
  { label: 'Recruiter', value: 'RECRUITER' },
  { label: 'Admin', value: 'ADMIN' }
]

const roleOptions = [
  { label: 'All Roles', value: '' },
  ...roleChoices
]

const statusOptions = [
  { label: 'All Statuses', value: '' },
  { label: 'Active', value: 'true' },
  { label: 'Suspended', value: 'false' }
]

const handleFilter = () => {
  let activeBool = undefined
  if (statusFilter.value === 'true') activeBool = true
  if (statusFilter.value === 'false') activeBool = false

  adminStore.fetchUsers({
    search: search.value || undefined,
    role: roleFilter.value || undefined,
    is_active: activeBool
  })
}

const toggleUserStatus = async (user, newStatus) => {
  try {
    await adminStore.updateUserStatus(user.id, newStatus, newStatus ? 'Re-activated by admin' : 'Suspended by admin')
    toast.show(`✓ Account '${user.email}' ${newStatus ? 'activated' : 'suspended'}`)
  } catch (err) {
    toast.show('Failed to update user status.', 'error')
  }
}

const changeRole = async (user, newRole) => {
  try {
    await adminStore.updateUserRole(user.id, newRole)
    toast.show(`✓ User '${user.email}' role updated to ${newRole}`)
  } catch (err) {
    toast.show('Failed to update user role.', 'error')
  }
}

onMounted(() => {
  adminStore.fetchUsers()
})
</script>

<style scoped>
.user-management-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.filter-row { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 1rem; }

.status-chip { font-size: 0.6875rem; font-weight: 700; padding: 0.125rem 0.5rem; border-radius: 4px; }
.chip-active { background-color: #dcfce7; color: #166534; }
.chip-suspended { background-color: #fee2e2; color: #991b1b; }

.font-semibold { font-weight: 600; }
.text-xs { font-size: 0.75rem; }
.text-muted { color: var(--text-muted); }
.table-actions { display: flex; gap: 0.375rem; }

@media (max-width: 768px) { .filter-row { grid-template-columns: 1fr; } }
</style>
