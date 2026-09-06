import { createRouter, createWebHistory } from 'vue-router'
import NotificationsView from '../views/NotificationsView.vue'
import UsersView from '../views/UsersView.vue'

const routes = [
  {
    path: '/',
    redirect: '/notifications',
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: NotificationsView,
    meta: { title: 'Notifications' },
  },
  {
    path: '/users',
    name: 'Users',
    component: UsersView,
    meta: { title: 'User Management' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// Update document title on navigation
router.afterEach((to) => {
  document.title = to.meta.title
    ? `${to.meta.title} — CareerPilot-AI`
    : 'CareerPilot-AI'
})

export default router
