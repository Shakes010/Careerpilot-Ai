<template>
  <AdminLayout>
    <div class="notifications-page">
      <div class="page-header">
        <div>
          <h1 class="page-title">Notification Management 🔔</h1>
          <p class="page-subtitle">Send targeted notifications to users and inspect system notification logs.</p>
        </div>
        <AppButton variant="primary" @click="showSendForm = !showSendForm">
          {{ showSendForm ? 'Close Form' : '+ Send Notification' }}
        </AppButton>
      </div>

      <!-- Send Notification Form Card -->
      <AppCard v-if="showSendForm" title="📤 Send Notification">
        <form @submit.prevent="handleSend">
          <div class="form-grid">
            <AppInput
              v-model="sendForm.user_id"
              label="Target User ID *"
              placeholder="e.g. paste user UUID here..."
              required
            />
            <AppInput
              v-model="sendForm.title"
              label="Notification Title *"
              placeholder="e.g. Account Verification Update"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Notification Body Message *</label>
            <textarea
              v-model="sendForm.message"
              rows="3"
              class="form-textarea"
              placeholder="Type your notification message content..."
              required
            ></textarea>
          </div>

          <div class="card-footer">
            <AppButton variant="secondary" @click="showSendForm = false">Cancel</AppButton>
            <AppButton type="submit" variant="primary" :loading="sending">
              Send Notification
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- Search / Lookup Notifications Card -->
      <AppCard title="🔍 Lookup Notifications by User">
        <div class="fetch-row">
          <AppInput
            v-model="lookupUserId"
            placeholder="Enter User ID to load notifications..."
            @keyup.enter="loadUserNotifications"
          />
          <AppButton variant="secondary" :loading="loading" @click="loadUserNotifications">
            Load Notifications
          </AppButton>
        </div>
      </AppCard>

      <!-- Notifications List -->
      <AppCard title="System Notifications List">
        <AppEmptyState
          v-if="notifications.length === 0"
          title="No notifications loaded."
          message="Enter a User ID above or send a notification to view logs."
        />

        <div v-else class="notifications-list">
          <div
            v-for="n in notifications"
            :key="n.id"
            :class="['notif-card', n.is_read ? 'read' : 'unread']"
          >
            <div class="notif-header">
              <div>
                <h4 class="notif-title">{{ n.title }}</h4>
                <span class="notif-date">{{ formatDate(n.created_at) }}</span>
              </div>
              <div class="notif-actions">
                <span :class="`badge ${n.is_read ? 'badge-read' : 'badge-unread'}`">
                  {{ n.is_read ? 'READ' : 'UNREAD' }}
                </span>
                <button
                  v-if="!n.is_read"
                  class="btn btn-secondary btn-sm"
                  @click="markRead(n.id)"
                >
                  Mark Read
                </button>
              </div>
            </div>
            <p class="notif-body">{{ n.message }}</p>
          </div>
        </div>
      </AppCard>
    </div>
  </AdminLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import AdminLayout from '@/components/layout/AdminLayout.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'
import AppEmptyState from '@/components/common/AppEmptyState.vue'
import notificationApi from '@/services/notificationApi'
import { useToast } from '@/components/common/AppToast.vue'

const toast = useToast()

const showSendForm = ref(false)
const sending = ref(false)
const loading = ref(false)

const lookupUserId = ref('')
const notifications = ref([])

const sendForm = reactive({
  user_id: '',
  title: '',
  message: ''
})

const formatDate = (d) => d ? new Date(d).toLocaleString('en-IN') : ''

const handleSend = async () => {
  if (!sendForm.user_id.trim() || !sendForm.title.trim() || !sendForm.message.trim()) return

  sending.value = true
  try {
    const res = await notificationApi.send(sendForm)
    toast.show('✓ Notification sent successfully!')
    showSendForm.value = false
    lookupUserId.value = sendForm.user_id
    sendForm.user_id = ''
    sendForm.title = ''
    sendForm.message = ''
    await loadUserNotifications()
  } catch (err) {
    toast.show(err.response?.data?.detail || 'Failed to send notification.', 'error')
  } finally {
    sending.value = false
  }
}

const loadUserNotifications = async () => {
  if (!lookupUserId.value.trim()) return

  loading.value = true
  try {
    const res = await notificationApi.listByUser(lookupUserId.value.trim())
    notifications.value = res.data.data
    toast.show(`Loaded ${notifications.value.length} notifications.`)
  } catch (err) {
    toast.show(err.response?.data?.detail || 'User notifications not found.', 'error')
  } finally {
    loading.value = false
  }
}

const markRead = async (notifId) => {
  try {
    await notificationApi.markRead(notifId)
    const idx = notifications.value.findIndex(n => n.id === notifId)
    if (idx !== -1) {
      notifications.value[idx].is_read = true
    }
    toast.show('✓ Notification marked as read.')
  } catch (err) {
    toast.show('Failed to update notification.', 'error')
  }
}
</script>

<style scoped>
.notifications-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; }
.page-title { font-size: 1.5rem; font-weight: 700; }
.page-subtitle { font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.25rem; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.fetch-row { display: grid; grid-template-columns: 3fr 1fr; gap: 1rem; align-items: center; }

.notifications-list { display: flex; flex-direction: column; gap: 0.875rem; margin-top: 0.75rem; }
.notif-card { padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--border); background: var(--background); display: flex; flex-direction: column; gap: 0.5rem; }
.notif-card.unread { border-left: 4px solid var(--primary); background: #f0f9ff; }

.notif-header { display: flex; justify-content: space-between; align-items: flex-start; }
.notif-title { font-weight: 700; font-size: 1rem; }
.notif-date { font-size: 0.75rem; color: var(--text-muted); }

.notif-actions { display: flex; align-items: center; gap: 0.5rem; }
.badge { font-size: 0.6875rem; font-weight: 700; padding: 0.125rem 0.5rem; border-radius: 4px; }
.badge-unread { background-color: #dbeafe; color: #1e40af; }
.badge-read { background-color: #e2e8f0; color: #64748b; }

.notif-body { font-size: 0.875rem; color: var(--text-primary); line-height: 1.45; }
.card-footer { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1rem; padding-top: 0.875rem; border-top: 1px solid var(--border); }

@media (max-width: 640px) { .form-grid, .fetch-row { grid-template-columns: 1fr; } }
</style>
