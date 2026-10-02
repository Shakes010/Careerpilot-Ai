<template>
  <!-- Toast Container — renders to a portal-like fixed position -->
  <teleport to="body">
    <div class="cp-toast-container">
      <transition-group name="toast-slide" tag="div" class="toast-list">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="cp-toast"
          :class="`cp-toast-${toast.type}`"
        >
          <span class="cp-toast-icon">{{ typeIcon(toast.type) }}</span>
          <div class="cp-toast-content">
            <div v-if="toast.title" class="cp-toast-title">{{ toast.title }}</div>
            <div class="cp-toast-msg">{{ toast.message }}</div>
          </div>
          <button class="cp-toast-close" @click="remove(toast.id)">✕</button>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

/**
 * Usage (in any component):
 *
 *   import { useToast } from '@/components/ToastNotification.vue'
 *   const toast = useToast()
 *   toast.success('Saved!', 'Your changes have been saved.')
 *   toast.error('Failed', 'Something went wrong.')
 *   toast.info('Info', 'Here is some info.')
 *   toast.warning('Warning', 'Be careful.')
 */

const toasts = ref([])
let nextId = 0
const timers = new Map()

const add = (type, title, message, duration = 4000) => {
  const id = ++nextId
  toasts.value.push({ id, type, title, message })

  if (duration > 0) {
    const timer = setTimeout(() => remove(id), duration)
    timers.set(id, timer)
  }

  return id
}

const remove = (id) => {
  const idx = toasts.value.findIndex(t => t.id === id)
  if (idx !== -1) toasts.value.splice(idx, 1)
  if (timers.has(id)) {
    clearTimeout(timers.get(id))
    timers.delete(id)
  }
}

onUnmounted(() => {
  timers.forEach(t => clearTimeout(t))
})

const typeIcon = (type) => {
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' }
  return icons[type] || '🔔'
}

// Expose composable-style API so parent can call directly
const api = {
  success: (title, msg, d) => add('success', title, msg, d),
  error:   (title, msg, d) => add('error',   title, msg, d),
  info:    (title, msg, d) => add('info',     title, msg, d),
  warning: (title, msg, d) => add('warning',  title, msg, d),
  dismiss: remove
}

defineExpose(api)

// Global singleton composable (optional convenience import)
export const useToast = () => api
</script>

<style scoped>
.toast-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Slide-up animation */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.22s ease;
}
.toast-slide-enter-from {
  opacity: 0;
  transform: translateY(12px) scale(0.96);
}
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(20px) scale(0.96);
}
</style>
