<template>
  <span :class="['badge', `badge-${computedVariant}`]">
    <span class="badge-dot" v-if="showDot"></span>
    <slot>{{ text }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  text: { type: String, default: '' },
  status: { type: String, default: '' },
  variant: { type: String, default: '' }, // success, warning, danger, info, default
  showDot: { type: Boolean, default: true }
})

const computedVariant = computed(() => {
  if (props.variant) return props.variant
  const val = (props.status || props.text).toUpperCase()
  if (['VERIFIED', 'PUBLISHED', 'ACTIVE'].includes(val)) return 'success'
  if (['PENDING', 'DRAFT', 'PAUSED'].includes(val)) return 'warning'
  if (['REJECTED', 'CLOSED', 'EXPIRED'].includes(val)) return 'danger'
  return 'default'
})
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.625rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}

.badge-success {
  background-color: var(--success-bg);
  color: #047857;
  border: 1px solid var(--success-border);
}

.badge-warning {
  background-color: var(--warning-bg);
  color: #b45309;
  border: 1px solid var(--warning-border);
}

.badge-danger {
  background-color: var(--danger-bg);
  color: #b91c1c;
  border: 1px solid var(--danger-border);
}

.badge-default {
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
}
</style>
