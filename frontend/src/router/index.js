import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '../views/RegisterView.vue'
import VerifyView from '../views/VerifyView.vue'
import AdminPanel from '../views/AdminPanel.vue'

const routes = [
  { path: '/', name: 'register', component: RegisterView },
  { path: '/verify-email/:token', name: 'verify', component: VerifyView },
  { path: '/admin', name: 'admin', component: AdminPanel } // protect this in prod with auth
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router