import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Views
const LoginView = () => import('@/views/auth/LoginView.vue');
const RegisterView = () => import('@/views/auth/RegisterView.vue');
const DashboardView = () => import('@/views/student/DashboardView.vue');
const ProfileView = () => import('@/views/student/ProfileView.vue');
const EducationView = () => import('@/views/student/EducationView.vue');
const SkillsView = () => import('@/views/student/SkillsView.vue');
const ResumeView = () => import('@/views/student/ResumeView.vue');
const CareerPreferencesView = () => import('@/views/student/CareerPreferencesView.vue');
const SkillGapView = () => import('@/views/student/SkillGapView.vue');
const ResumeVersionsView = () => import('@/views/student/ResumeVersionsView.vue');
const CertificatesView = () => import('@/views/student/CertificatesView.vue');
const PassportView = () => import('@/views/student/PassportView.vue');
const GithubView = () => import('@/views/student/GithubView.vue');
const TimelineView = () => import('@/views/student/TimelineView.vue');
const ResumeGeneratorView = () => import('@/views/student/ResumeGeneratorView.vue');

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true, title: 'Student Dashboard' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true, title: 'Student Profile' }
  },
  {
    path: '/passport',
    name: 'Passport',
    component: PassportView,
    meta: { requiresAuth: true, title: 'Career Passport' }
  },
  {
    path: '/education',
    name: 'Education',
    component: EducationView,
    meta: { requiresAuth: true, title: 'Academic Education' }
  },
  {
    path: '/skills',
    name: 'Skills',
    component: SkillsView,
    meta: { requiresAuth: true, title: 'Skills & Competencies' }
  },
  {
    path: '/certificates',
    name: 'Certificates',
    component: CertificatesView,
    meta: { requiresAuth: true, title: 'Certificate Management' }
  },
  {
    path: '/github',
    name: 'Github',
    component: GithubView,
    meta: { requiresAuth: true, title: 'GitHub Integration' }
  },

  {
    path: '/resume',
    name: 'Resume',
    component: ResumeView,
    meta: { requiresAuth: true, title: 'Resume & ATS Parser' }
  },
  {
    path: '/resume-versions',
    name: 'ResumeVersions',
    component: ResumeVersionsView,
    meta: { requiresAuth: true, title: 'Smart Resume Version Manager' }
  },
  {
    path: '/resume-generator',
    name: 'ResumeGenerator',
    component: ResumeGeneratorView,
    meta: { requiresAuth: true, title: 'AI Resume Generator' }
  },
  {
    path: '/timeline',
    name: 'Timeline',
    component: TimelineView,
    meta: { requiresAuth: true, title: 'Career Timeline' }
  },
  {
    path: '/preferences',
    name: 'Preferences',
    component: CareerPreferencesView,
    meta: { requiresAuth: true, title: 'Career Preferences' }
  },

  {
    path: '/skill-builder',
    name: 'SkillBuilder',
    component: SkillGapView,
    meta: { requiresAuth: true, title: 'Skill Gap & Learning Roadmaps' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
];


const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  }
});

// Auth Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
