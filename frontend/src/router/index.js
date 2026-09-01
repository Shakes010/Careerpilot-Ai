import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import RecruiterLogin from '@/views/recruiter/RecruiterLogin.vue'
import RecruiterRegister from '@/views/recruiter/RecruiterRegister.vue'
import RecruiterDashboard from '@/views/recruiter/RecruiterDashboard.vue'
import CompanyProfile from '@/views/recruiter/CompanyProfile.vue'
import Jobs from '@/views/recruiter/Jobs.vue'
import CreateJob from '@/views/recruiter/CreateJob.vue'
import EditJob from '@/views/recruiter/EditJob.vue'
import JobDetails from '@/views/recruiter/JobDetails.vue'

const routes = [
  {
    path: '/',
    redirect: '/recruiter/dashboard'
  },
  {
    path: '/recruiter/login',
    name: 'RecruiterLogin',
    component: RecruiterLogin,
    meta: { guestOnly: true }
  },
  {
    path: '/recruiter/register',
    name: 'RecruiterRegister',
    component: RecruiterRegister,
    meta: { guestOnly: true }
  },
  {
    path: '/recruiter/dashboard',
    name: 'RecruiterDashboard',
    component: RecruiterDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/recruiter/company',
    name: 'CompanyProfile',
    component: CompanyProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/recruiter/jobs',
    name: 'Jobs',
    component: Jobs,
    meta: { requiresAuth: true }
  },
  {
    path: '/recruiter/jobs/create',
    name: 'CreateJob',
    component: CreateJob,
    meta: { requiresAuth: true }
  },
  {
    path: '/recruiter/jobs/:id',
    name: 'JobDetails',
    component: JobDetails,
    meta: { requiresAuth: true }
  },
  {
    path: '/recruiter/jobs/:id/edit',
    name: 'EditJob',
    component: EditJob,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/recruiter/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/recruiter/login')
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/recruiter/dashboard')
  } else {
    next()
  }
})

export default router
