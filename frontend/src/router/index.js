// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import AdminCompanies from '@/views/admin/AdminCompanies.vue'
import AdminDrives from '@/views/admin/AdminDrives.vue'
import AdminStudents from '@/views/admin/AdminStudents.vue'
import AdminApplications from '@/views/admin/AdminApplications.vue'
import AdminSearch from '@/views/admin/AdminSearch.vue'

import CompanyDashboard from '@/views/company/CompanyDashboard.vue'
import CompanyProfile from '@/views/company/CompanyProfile.vue'
import CompanyDrives from '@/views/company/CompanyDrives.vue'
import CompanyApplications from '@/views/company/CompanyApplications.vue'

import StudentDashboard from '@/views/student/StudentDashboard.vue'
import StudentProfile from '@/views/student/StudentProfile.vue'
import StudentDrives from '@/views/student/StudentDrives.vue'
import StudentApplications from '@/views/student/StudentApplications.vue'

const routes = [
  { path: '/',        component: Home },
  { path: '/login',   component: Login,    meta: { guest_only: true } },
  { path: '/register',component: Register, meta: { guest_only: true } },

  { path: '/admin/dashboard',    component: AdminDashboard,    meta: { required_role: 'Admin' } },
  { path: '/admin/companies',    component: AdminCompanies,    meta: { required_role: 'Admin' } },
  { path: '/admin/drives',       component: AdminDrives,       meta: { required_role: 'Admin' } },
  { path: '/admin/students',     component: AdminStudents,     meta: { required_role: 'Admin' } },
  { path: '/admin/applications', component: AdminApplications, meta: { required_role: 'Admin' } },
  { path: '/admin/search',       component: AdminSearch,       meta: { required_role: 'Admin' } },

  { path: '/company/dashboard',                      component: CompanyDashboard,    meta: { required_role: 'Company' } },
  { path: '/company/profile',                        component: CompanyProfile,      meta: { required_role: 'Company' } },
  { path: '/company/drives',                         component: CompanyDrives,       meta: { required_role: 'Company' } },
  { path: '/company/applications/:drive_id',         component: CompanyApplications, meta: { required_role: 'Company' } },

  { path: '/student/dashboard',    component: StudentDashboard,    meta: { required_role: 'Student' } },
  { path: '/student/profile',      component: StudentProfile,      meta: { required_role: 'Student' } },
  { path: '/student/drives',       component: StudentDrives,       meta: { required_role: 'Student' } },
  { path: '/student/applications', component: StudentApplications, meta: { required_role: 'Student' } },

  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth_store = useAuthStore()

  if (to.meta.guest_only && auth_store.isAuthenticated) {
    const role = auth_store.getRole()
    if (role === 'Admin') return next('/admin/dashboard')
    if (role === 'Company') return next('/company/dashboard')
    if (role === 'Student') return next('/student/dashboard')
  }

  if (to.meta.required_role) {
    if (!auth_store.isAuthenticated) return next('/login')
    if (auth_store.getRole() !== to.meta.required_role) return next('/')
  }

  next()
})

export default router