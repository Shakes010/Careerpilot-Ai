<template>
  <!-- Notification Bell Icon with unread badge -->
  <button
    id="notification-bell-btn"
    class="bell-btn"
    :aria-label="`Notifications${unreadCount > 0 ? `, ${unreadCount} unread` : ''}`"
    @click="$emit('click')"
  >
    <!-- Bell SVG -->
    <svg
      class="bell-icon"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
      <path d="M13.73 21a2 2 0 0 1-3.46 0" />
    </svg>

    <!-- Unread badge -->
    <span
      v-if="unreadCount > 0"
      id="notification-badge"
      class="bell-badge"
      aria-live="polite"
    >
      {{ unreadCount > 99 ? '99+' : unreadCount }}
    </span>
  </button>
</template>

<script setup>
defineProps({
  unreadCount: {
    type: Number,
    default: 0,
  },
})

defineEmits(['click'])
</script>

<style scoped>
.bell-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--color-gray-500);
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.bell-btn:hover {
  background-color: var(--color-gray-100);
  color: var(--color-gray-900);
}

.bell-icon {
  width: 22px;
  height: 22px;
}

.bell-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  background-color: var(--color-primary);
  color: white;
  font-size: 10px;
  font-weight: 700;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  border: 2px solid white;
  animation: pulse-badge 2s ease infinite;
}

@keyframes pulse-badge {
  0%, 100% { transform: scale(1); }
  50%       { transform: scale(1.15); }
}
</style>
