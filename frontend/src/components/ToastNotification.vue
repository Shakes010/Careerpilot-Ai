<template>
  <Teleport to="body">
    <div class="toast-container" role="alert" aria-live="polite">
      <TransitionGroup name="toast-anim">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast--${toast.type}`]"
        >
          <span class="toast__icon" aria-hidden="true">
            {{ toast.type === 'success' ? '✓' : toast.type === 'error' ? '✕' : 'ℹ' }}
          </span>
          {{ toast.message }}
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

function show(message, type = 'info', duration = 3500) {
  const id = ++nextId
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }, duration)
}

// Expose so parent can call $refs.toast.show(...)
defineExpose({ show })
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
}

.toast {
  padding: 0.75rem 1.25rem;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.06);
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 280px;
  max-width: 400px;
}

.toast--success { background: #dcfce7; color: #16a34a; }
.toast--error   { background: #fee2e2; color: #dc2626; }
.toast--info    { background: #dbeafe; color: #2563eb; }

.toast__icon { font-weight: 700; font-size: 1rem; }

/* TransitionGroup animations */
.toast-anim-enter-active { animation: slideIn 0.25s ease; }
.toast-anim-leave-active  { animation: slideOut 0.2s ease forwards; }

@keyframes slideIn {
  from { opacity: 0; transform: translateX(20px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideOut {
  from { opacity: 1; transform: translateX(0); }
  to   { opacity: 0; transform: translateX(20px); }
}
</style>
