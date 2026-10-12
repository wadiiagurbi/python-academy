import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/courses',
    name: 'courses',
    component: () => import('../views/CoursesView.vue'),
  },
  {
    path: '/lessons/:slug',
    name: 'lesson',
    component: () => import('../views/LessonView.vue'),
    props: true,
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('../views/SearchView.vue'),
  },
  {
    path: '/pipelines',
    name: 'pipelines',
    component: () => import('../views/PipelinesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/pipelines/new',
    name: 'pipeline-new',
    component: () => import('../views/PipelineBuilderView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/pipelines/:id',
    name: 'pipeline-detail',
    component: () => import('../views/PipelineBuilderView.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/pipelines/:id/results',
    name: 'pipeline-results',
    component: () => import('../views/PipelineResultsView.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
  { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFoundView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.initialized) {
    await authStore.init()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router