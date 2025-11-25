import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', redirect: '/auth/login' },
  { path: '/events', name: 'EventsList', meta: { requiresAuth: true }, component: () => import('../pages/EventsListPage.vue') },
  { path: '/events/:id', name: 'EventDetails', meta: { requiresAuth: true }, component: () => import('../pages/EventDetailsPage.vue') },
  { path: '/auth/login', name: 'Login', component: () => import('../pages/LoginPage.vue') },
  { path: '/auth/register', name: 'Register', component: () => import('../pages/RegisterPage.vue') },
  { path: '/account', name: 'Account', meta: { requiresAuth: true }, component: () => import('../pages/AccountPage.vue') },
  { path: '/account/info', name: 'AccountInfo', meta: { requiresAuth: true }, component: () => import('../pages/AccountInfoPage.vue') },
  { path: '/my-events', name: 'MyEvents', meta: { requiresAuth: true }, component: () => import('../pages/MyEventsPage.vue') },
  { path: '/my-events/create', name: 'CreateEvent', meta: { requiresAuth: true }, component: () => import('../pages/CreateEventPage.vue') },
  { path: '/my-events/:id/edit', name: 'EditEvent', meta: { requiresAuth: true }, component: () => import('../pages/EditEventPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta?.requiresAuth && !auth.isAuth) {
    const next = encodeURIComponent(to.fullPath)
    return { path: '/auth/login', query: { next } }
  }
  return true
})

export default router
