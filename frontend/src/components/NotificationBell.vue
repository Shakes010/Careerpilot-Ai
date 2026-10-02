<template>
  <div class="bell-wrap" ref="bellRef">
    <!-- Bell Button -->
    <button class="cp-bell-btn" @click="togglePanel" :aria-label="unreadCount + ' notifications'">
      <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>
      <span v-if="unreadCount > 0" class="cp-bell-dot"></span>
    </button>

    <!-- Notification Dropdown -->
    <transition name="notif-fade">
      <div v-if="isOpen" class="cp-notif-panel">

        <!-- Header -->
        <div class="cp-notif-header">
          <h4>Notifications</h4>
          <div class="notif-header-actions">
            <span v-if="unreadCount > 0" class="notif-unread-badge">{{ unreadCount }} new</span>
            <button v-if="notifications.length" class="notif-clear-btn" @click="markAllRead">
              Mark all read
            </button>
          </div>
        </div>

        <!-- Items -->
        <div class="notif-scroll">
          <div v-if="!notifications.length" class="notif-empty">
            <span>🔔</span>
            <p>No notifications yet</p>
          </div>

          <div
            v-for="n in notifications"
            :key="n.id"
            class="cp-notif-item"
            :class="{ 'cp-notif-unread': !n.read }"
            @click="handleClick(n)"
          >
            <span class="notif-type-icon">{{ typeIcon(n.type) }}</span>
            <div style="flex:1; min-width:0;">
              <div class="cp-notif-title">{{ n.title }}</div>
              <div class="cp-notif-body">{{ n.body }}</div>
              <div class="cp-notif-time">{{ formatTime(n.created_at) }}</div>
            </div>
            <span v-if="!n.read" class="cp-notif-dot-unread"></span>
          </div>
        </div>

        <!-- Footer -->
        <div v-if="notifications.length" class="notif-footer">
          <button class="notif-view-all" @click="isOpen = false">View all activity →</button>
        </div>

      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  notifications: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['mark-all-read', 'notification-click'])

const isOpen = ref(false)
const bellRef = ref(null)

const unreadCount = computed(() => props.notifications.filter(n => !n.read).length)

const togglePanel = () => { isOpen.value = !isOpen.value }

const markAllRead = () => {
  emit('mark-all-read')
}

const handleClick = (n) => {
  emit('notification-click', n)
  isOpen.value = false
}

const typeIcon = (type) => {
  const icons = {
    success: '✅',
    warning: '⚠️',
    info: 'ℹ️',
    error: '❌',
    badge: '🏅',
    job: '💼',
    assessment: '☑️',
    skill: '🎖️'
  }
  return icons[type] || '🔔'
}

const formatTime = (ts) => {
  if (!ts) return ''
  const d = new Date(ts)
  const now = new Date()
  const diff = Math.floor((now - d) / 1000)
  if (diff < 60) return 'Just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return d.toLocaleDateString()
}

// Close on outside click
const handleOutside = (e) => {
  if (bellRef.value && !bellRef.value.contains(e.target)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleOutside, true))
onUnmounted(() => document.removeEventListener('click', handleOutside, true))
</script>

<style scoped>
.bell-wrap {
  position: relative;
  display: inline-flex;
}

/* Transition */
.notif-fade-enter-active,
.notif-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.notif-fade-enter-from,
.notif-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* Header extras */
.notif-header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.notif-unread-badge {
  background: var(--color-error-bg);
  color: var(--color-error);
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-error-border);
}

.notif-clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-primary);
  padding: 0;
}

.notif-clear-btn:hover {
  text-decoration: underline;
}

/* Scroll area */
.notif-scroll {
  max-height: 340px;
  overflow-y: auto;
}

/* Empty state */
.notif-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 36px 16px;
  gap: 8px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.notif-empty span {
  font-size: 28px;
}

/* Type icon */
.notif-type-icon {
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 1px;
}

/* Footer */
.notif-footer {
  padding: 10px 16px;
  border-top: 1px solid var(--color-border);
  text-align: center;
}

.notif-view-all {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-primary);
}

.notif-view-all:hover {
  text-decoration: underline;
}
</style>
