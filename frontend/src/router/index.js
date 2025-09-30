import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '../views/RegisterView.vue'
import VerifyView from '../views/VerifyView.vue'
import AdminPanel from '../views/AdminPanel.vue'
import AdminLoginView from '../views/AdminLoginView.vue'

const routes = [
  { path: '/', name: 'register', component: RegisterView },
  { path: '/verify-email/:token', name: 'verify', component: VerifyView },
  { path: '/admin/login', name: 'admin-login', component: AdminLoginView },
  { path: '/admin', name: 'admin', component: AdminPanel, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
