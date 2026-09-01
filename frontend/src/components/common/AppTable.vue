<template>
  <div class="app-table-container">
    <table class="app-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="columns.length" class="text-center py-4">
            <AppLoader message="Loading data..." />
          </td>
        </tr>
        <tr v-else-if="!data || data.length === 0">
          <td :colspan="columns.length" class="text-center py-4">
            <AppEmptyState :message="emptyMessage" />
          </td>
        </tr>
        <tr v-else v-for="(row, idx) in data" :key="row.id || idx">
          <td v-for="col in columns" :key="col.key">
            <slot :name="col.key" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import AppLoader from './AppLoader.vue'
import AppEmptyState from './AppEmptyState.vue'

defineProps({
  columns: { type: Array, required: true }, // [{ label: 'Title', key: 'title' }]
  data: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  emptyMessage: { type: String, default: 'No records found.' }
})
</script>

<style scoped>
.text-center { text-align: center; }
.py-4 { padding-top: 1.5rem; padding-bottom: 1.5rem; }
</style>
