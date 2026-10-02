import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import PassportView from '../views/PassportView.vue'
import SkillsView from '../views/SkillsView.vue'
import AssessmentsView from '../views/AssessmentsView.vue'
import OpportunitiesView from '../views/OpportunitiesView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import ApplicationsView from '../views/ApplicationsView.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
import AdminView from '../views/AdminView.vue'
import RecruiterView from '../views/RecruiterView.vue'
import BillingView from '../views/BillingView.vue'
import { useAuthStore } from '../store'

const routes = [
  { path: '/', name: 'landing', component: LandingView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/passport', name: 'passport', component: PassportView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/skills', name: 'skills', component: SkillsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/assessments', name: 'assessments', component: AssessmentsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/assessments/skill/:skillId', name: 'assessments-by-skill', component: AssessmentsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/opportunities', name: 'opportunities', component: OpportunitiesView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/applications', name: 'applications', component: ApplicationsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/analytics', name: 'analytics', component: AnalyticsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/projects', name: 'projects', component: ProjectsView, meta: { requiresAuth: true, role: 'student' } },
  { path: '/admin', name: 'admin', component: AdminView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/recruiter', name: 'recruiter', component: RecruiterView, meta: { requiresAuth: true, role: 'recruiter' } },
  { path: '/billing', name: 'billing', component: BillingView, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.path === '/' && authStore.isAuthenticated) {
    if (authStore.role === 'admin') return next('/admin')
    if (authStore.role === 'recruiter') return next('/recruiter')
    return next('/dashboard')
  }

  if (to.path === '/login') {
    if (authStore.isAuthenticated) {
      if (authStore.role === 'admin') return next('/admin')
      if (authStore.role === 'recruiter') return next('/recruiter')
      return next('/dashboard')
    }
    return next()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.role && authStore.role !== to.meta.role) {
    // Redirect user to their own role's home view
    if (authStore.role === 'admin') return next('/admin')
    if (authStore.role === 'recruiter') return next('/recruiter')
    return next('/dashboard')
  }

  next()
})

export default router
