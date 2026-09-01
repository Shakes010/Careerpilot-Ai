<template>
  <div class="empty-state">
    <div class="empty-icon">📂</div>
    <h4 class="empty-title">{{ title }}</h4>
    <p class="empty-description">{{ message }}</p>
    <div v-if="$slots.action" class="empty-action">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: 'No data available' },
  message: { type: String, default: 'No records were found matching your criteria.' }
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  text-align: center;
  background-color: var(--surface);
  border-radius: var(--radius-md);
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
  opacity: 0.8;
}

.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-heading);
}

.empty-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 0.375rem;
  max-width: 400px;
}

.empty-action {
  margin-top: 1.25rem;
}
</style>
