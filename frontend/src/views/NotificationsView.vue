<template>
  <div>
    <!-- ================================================================
         Page header row
         ================================================================ -->
    <div class="page-header mb-6">
      <div>
        <h2 class="page-header__title">Notifications</h2>
        <p class="page-header__sub">Send and manage user notifications</p>
      </div>
      <button
        id="open-send-modal-btn"
        class="btn btn--primary"
        @click="showSendForm = !showSendForm"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        {{ showSendForm ? 'Close Form' : 'Send Notification' }}
      </button>
    </div>

    <!-- ================================================================
         Send Notification Form
         ================================================================ -->
    <Transition name="slide-down">
      <div v-if="showSendForm" class="card mb-6">
        <div class="card__header">
          <div>
            <div class="card__title">Send Notification</div>
            <div class="card__subtitle">Deliver a message to a specific user</div>
          </div>
        </div>
        <div class="card__body">
          <form id="send-notification-form" @submit.prevent="handleSend" novalidate>
            <div class="form-grid">
              <div class="form-group">
                <label for="user-id-input" class="form-label">User ID (UUID) *</label>
                <input
                  id="user-id-input"
                  v-model="form.user_id"
                  type="text"
                  class="form-input"
                  placeholder="e.g. 550e8400-e29b-41d4-a716-446655440000"
                  required
                  :disabled="sending"
                />
              </div>
              <div class="form-group">
                <label for="notif-title-input" class="form-label">Title *</label>
                <input
                  id="notif-title-input"
                  v-model="form.title"
                  type="text"
                  class="form-input"
                  placeholder="Notification title"
                  required
                  maxlength="255"
                  :disabled="sending"
                />
              </div>
            </div>
            <div class="form-group mt-4">
              <label for="notif-message-input" class="form-label">Message *</label>
              <textarea
                id="notif-message-input"
                v-model="form.message"
                class="form-textarea"
                placeholder="Write the notification message…"
                required
                :disabled="sending"
              />
            </div>
            <div class="form-actions mt-4">
              <button
                id="submit-notification-btn"
                type="submit"
                class="btn btn--primary"
                :disabled="sending || !isFormValid"
              >
                <span v-if="sending" class="spinner" aria-hidden="true" />
                {{ sending ? 'Sending…' : 'Send Notification' }}
              </button>
              <button
                type="button"
                class="btn btn--outline"
                :disabled="sending"
                @click="resetForm"
              >
                Clear
              </button>
            </div>
            <p v-if="sendError" class="form-error mt-4" role="alert">{{ sendError }}</p>
          </form>
        </div>
      </div>
    </Transition>

    <!-- ================================================================
         Fetch Notifications Panel
         ================================================================ -->
    <div class="card mb-6">
      <div class="card__header">
        <div>
          <div class="card__title">View User Notifications</div>
          <div class="card__subtitle">Enter a user UUID to load their notifications</div>
        </div>
      </div>
      <div class="card__body">
        <div class="fetch-row">
          <input
            id="fetch-user-id-input"
            v-model="fetchUserId"
            type="text"
            class="form-input"
            placeholder="User UUID…"
            @keyup.enter="loadNotifications"
          />
          <button
            id="fetch-notifications-btn"
            class="btn btn--primary"
            :disabled="loading || !fetchUserId.trim()"
            @click="loadNotifications"
          >
            <span v-if="loading" class="spinner" aria-hidden="true" />
            {{ loading ? 'Loading…' : 'Load' }}
          </button>
        </div>
        <p v-if="fetchError" class="form-error mt-4" role="alert">{{ fetchError }}</p>
      </div>
    </div>

    <!-- ================================================================
         Notifications List
         ================================================================ -->
    <div v-if="hasLoaded">
      <!-- Stats row -->
      <div class="stats-row mb-4" v-if="notifications.length">
        <div class="stat-chip stat-chip--total">
          {{ notifications.length }} total
        </div>
        <div class="stat-chip stat-chip--unread">
          {{ unreadCount }} unread
        </div>
        <div class="stat-chip stat-chip--read">
          {{ notifications.length - unreadCount }} read
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="!notifications.length" class="card">
        <div class="empty-state">
          <div class="empty-state__icon" aria-hidden="true">🔔</div>
          <div class="empty-state__text">No notifications found for this user.</div>
        </div>
      </div>

      <!-- Notification cards -->
      <TransitionGroup name="notif-list" tag="div" class="notif-list">
        <div
          v-for="notif in notifications"
          :key="notif.id"
          :class="['notif-card', notif.is_read ? 'notif-card--read' : 'notif-card--unread']"
        >
          <div class="notif-card__header">
            <div class="notif-card__title">{{ notif.title }}</div>
            <div class="notif-card__actions">
              <span
                v-if="!notif.is_read"
                class="badge badge--blue"
              >
                Unread
              </span>
              <span v-else class="badge badge--gray">Read</span>
              <button
                v-if="!notif.is_read"
                :id="`mark-read-btn-${notif.id}`"
                class="btn btn--outline btn--sm"
                :disabled="markingId === notif.id"
                @click="markAsRead(notif)"
              >
                <span v-if="markingId === notif.id" class="spinner" style="width:12px;height:12px;" aria-hidden="true"/>
                {{ markingId === notif.id ? '…' : 'Mark read' }}
              </button>
            </div>
          </div>
          <p class="notif-card__message">{{ notif.message }}</p>
          <div class="notif-card__meta">
            <span>{{ formatDate(notif.created_at) }}</span>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- Toast -->
    <ToastNotification ref="toast" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { notificationApi } from '@/api/index.js'
import ToastNotification from '@/components/ToastNotification.vue'

const emit = defineEmits(['unread-count-change'])

// ---- Send form state ----
const showSendForm = ref(false)
const sending = ref(false)
const sendError = ref('')
const form = ref({ user_id: '', title: '', message: '' })
const isFormValid = computed(() =>
  form.value.user_id.trim() && form.value.title.trim() && form.value.message.trim()
)

// ---- Fetch state ----
const fetchUserId = ref('')
const loading = ref(false)
const fetchError = ref('')
const hasLoaded = ref(false)

// ---- Notifications data ----
const notifications = ref([])
const markingId = ref(null)

const unreadCount = computed(() => notifications.value.filter((n) => !n.is_read).length)

// Keep parent's bell badge in sync
watch(unreadCount, (val) => emit('unread-count-change', val))

const toast = ref(null)

// ---- Helpers ----
function formatDate(isoString) {
  if (!isoString) return ''
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(isoString))
}

function resetForm() {
  form.value = { user_id: '', title: '', message: '' }
  sendError.value = ''
}

// ---- Send notification ----
async function handleSend() {
  if (!isFormValid.value) return
  sending.value = true
  sendError.value = ''
  try {
    const { data } = await notificationApi.send({
      user_id: form.value.user_id.trim(),
      title: form.value.title.trim(),
      message: form.value.message.trim(),
    })
    toast.value?.show('Notification sent successfully!', 'success')
    resetForm()
    showSendForm.value = false
    // If we're currently viewing that user's notifications, prepend new one
    if (fetchUserId.value.trim() === data.user_id) {
      notifications.value.unshift(data)
    }
  } catch (err) {
    sendError.value = err.message
    toast.value?.show(err.message, 'error')
  } finally {
    sending.value = false
  }
}

// ---- Load notifications for a user ----
async function loadNotifications() {
  const userId = fetchUserId.value.trim()
  if (!userId) return
  loading.value = true
  fetchError.value = ''
  hasLoaded.value = false
  try {
    const { data } = await notificationApi.listByUser(userId)
    notifications.value = data
    hasLoaded.value = true
  } catch (err) {
    fetchError.value = err.message
    toast.value?.show(err.message, 'error')
  } finally {
    loading.value = false
  }
}

// ---- Mark notification as read ----
async function markAsRead(notif) {
  markingId.value = notif.id
  try {
    const { data } = await notificationApi.markRead(notif.id)
    const idx = notifications.value.findIndex((n) => n.id === notif.id)
    if (idx !== -1) notifications.value[idx] = data
    toast.value?.show('Marked as read', 'success')
  } catch (err) {
    toast.value?.show(err.message, 'error')
  } finally {
    markingId.value = null
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}
.page-header__title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  line-height: 1.2;
}
.page-header__sub {
  font-size: 0.875rem;
  color: var(--color-gray-500);
  margin-top: 0.25rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
@media (max-width: 640px) {
  .form-grid { grid-template-columns: 1fr; }
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.form-error {
  font-size: 0.875rem;
  color: var(--color-danger);
}

.fetch-row {
  display: flex;
  gap: 0.75rem;
}
.fetch-row .form-input {
  flex: 1;
}

/* Stats chips */
.stats-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.stat-chip {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--color-gray-100);
  color: var(--color-gray-600);
}
.stat-chip--unread { background: var(--color-primary-s); color: var(--color-primary); }
.stat-chip--read   { background: var(--color-gray-100); color: var(--color-gray-500); }
.stat-chip--total  { background: var(--color-gray-200); color: var(--color-gray-700); }

/* Notification card actions */
.notif-card__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

/* Notification list */
.notif-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Transitions */
.slide-down-enter-active { transition: all 0.25s ease; }
.slide-down-leave-active { transition: all 0.2s ease; }
.slide-down-enter-from,
.slide-down-leave-to    { opacity: 0; transform: translateY(-12px); }

.notif-list-enter-active { transition: all 0.3s ease; }
.notif-list-leave-active { transition: all 0.2s ease; }
.notif-list-enter-from   { opacity: 0; transform: translateY(8px); }
.notif-list-leave-to     { opacity: 0; transform: translateX(-8px); }
</style>
