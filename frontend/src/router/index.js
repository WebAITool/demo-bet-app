import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/auth/login' },
  { path: '/events', name: 'EventsList', component: () => import('../pages/EventsListPage.vue') },
  { path: '/events/:id', name: 'EventDetails', component: () => import('../pages/EventDetailsPage.vue') },
  { path: '/auth/login', name: 'Login', component: () => import('../pages/LoginPage.vue') },
  { path: '/auth/register', name: 'Register', component: () => import('../pages/RegisterPage.vue') },
  { path: '/account', name: 'Account', component: () => import('../pages/AccountPage.vue') },
  { path: '/account/info', name: 'AccountInfo', component: () => import('../pages/AccountInfoPage.vue') },
  { path: '/my-events', name: 'MyEvents', component: () => import('../pages/MyEventsPage.vue') },
  { path: '/my-events/create', name: 'CreateEvent', component: () => import('../pages/CreateEventPage.vue') },
  { path: '/my-events/:id/edit', name: 'EditEvent', component: () => import('../pages/EditEventPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
