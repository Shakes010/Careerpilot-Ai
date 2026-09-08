import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Universal Auth Views
import UniversalLogin from '@/views/auth/UniversalLogin.vue'
import RecruiterRegister from '@/views/recruiter/RecruiterRegister.vue'

// Recruiter Views
import RecruiterDashboard from '@/views/recruiter/RecruiterDashboard.vue'
import CompanyProfile from '@/views/recruiter/CompanyProfile.vue'
import Jobs from '@/views/recruiter/Jobs.vue'
import CreateJob from '@/views/recruiter/CreateJob.vue'
import EditJob from '@/views/recruiter/EditJob.vue'
import JobDetails from '@/views/recruiter/JobDetails.vue'

// Admin Views
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import RecruiterVerification from '@/views/admin/RecruiterVerification.vue'
import JobModeration from '@/views/admin/JobModeration.vue'
import SkillLibrary from '@/views/admin/SkillLibrary.vue'
import PlatformAnalytics from '@/views/admin/PlatformAnalytics.vue'
import FlaggedQueue from '@/views/admin/FlaggedQueue.vue'

// Student Phase 2A Views
import StudentProjectsList from '@/views/student/ProjectsList.vue'
import StudentCreateProject from '@/views/student/CreateProject.vue'
import StudentProjectDetails from '@/views/student/ProjectDetails.vue'
import CareerSandbox from '@/views/student/CareerSandbox.vue'
import SandboxChallengeDetails from '@/views/student/SandboxChallengeDetails.vue'
import SandboxAttempt from '@/views/student/SandboxAttempt.vue'

const routes = [
  { path: '/', redirect: '/login' },

  // Unified Universal Auth Routes
  { path: '/login', name: 'Login', component: UniversalLogin, meta: { guestOnly: true } },
  { path: '/recruiter/login', redirect: '/login' },
  { path: '/admin/login', redirect: '/login' },
  { path: '/recruiter/register', name: 'RecruiterRegister', component: RecruiterRegister, meta: { guestOnly: true } },

  // Recruiter Routes
  { path: '/recruiter/dashboard', name: 'RecruiterDashboard', component: RecruiterDashboard, meta: { requiresAuth: true } },
  { path: '/recruiter/company', name: 'CompanyProfile', component: CompanyProfile, meta: { requiresAuth: true } },
  { path: '/recruiter/jobs', name: 'Jobs', component: Jobs, meta: { requiresAuth: true } },
  { path: '/recruiter/jobs/create', name: 'CreateJob', component: CreateJob, meta: { requiresAuth: true } },
  { path: '/recruiter/jobs/:id', name: 'JobDetails', component: JobDetails, meta: { requiresAuth: true } },
  { path: '/recruiter/jobs/:id/edit', name: 'EditJob', component: EditJob, meta: { requiresAuth: true } },

  // Admin Routes
  { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAdmin: true } },
  { path: '/admin/users', name: 'UserManagement', component: UserManagement, meta: { requiresAdmin: true } },
  { path: '/admin/verifications', name: 'RecruiterVerification', component: RecruiterVerification, meta: { requiresAdmin: true } },
  { path: '/admin/job-moderation', name: 'JobModeration', component: JobModeration, meta: { requiresAdmin: true } },
  { path: '/admin/skills', name: 'SkillLibrary', component: SkillLibrary, meta: { requiresAdmin: true } },
  { path: '/admin/analytics', name: 'PlatformAnalytics', component: PlatformAnalytics, meta: { requiresAdmin: true } },
  { path: '/admin/flagged-queue', name: 'FlaggedQueue', component: FlaggedQueue, meta: { requiresAdmin: true } },

  // Student Phase 2A Routes
  { path: '/student/projects', name: 'StudentProjectsList', component: StudentProjectsList, meta: { requiresAuth: true } },
  { path: '/student/projects/create', name: 'StudentCreateProject', component: StudentCreateProject, meta: { requiresAuth: true } },
  { path: '/student/projects/:id', name: 'StudentProjectDetails', component: StudentProjectDetails, meta: { requiresAuth: true } },
  { path: '/student/career-sandbox', name: 'CareerSandbox', component: CareerSandbox, meta: { requiresAuth: true } },
  { path: '/student/career-sandbox/:id', name: 'SandboxChallengeDetails', component: SandboxChallengeDetails, meta: { requiresAuth: true } },
  { path: '/student/career-sandbox/attempt/:id', name: 'SandboxAttempt', component: SandboxAttempt, meta: { requiresAuth: true } },

  // Legacy fallback routes
  { path: '/projects', redirect: '/student/projects' },
  { path: '/projects/create', redirect: '/student/projects/create' },
  { path: '/projects/:id', redirect: to => `/student/projects/${to.params.id}` },

  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && (!authStore.isAuthenticated || authStore.user?.role !== 'ADMIN')) {
    if (!authStore.isAuthenticated) {
      next('/login')
    } else if (authStore.user?.role === 'RECRUITER') {
      next('/recruiter/dashboard')
    } else if (authStore.user?.role === 'STUDENT') {
      next('/student/projects')
    } else {
      next('/login')
    }
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    if (authStore.user?.role === 'ADMIN') {
      next('/admin/dashboard')
    } else if (authStore.user?.role === 'STUDENT') {
      next('/student/projects')
    } else {
      next('/recruiter/dashboard')
    }
  } else {
    next()
  }
})

export default router
