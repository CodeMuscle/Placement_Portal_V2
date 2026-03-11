<!-- src/views/Home.vue -->
<script setup>
import { useAuthStore } from '@/stores/auth.js'
import { useRouter } from 'vue-router'

const auth_store = useAuthStore()
const router = useRouter()

function goToDashboard() {
  const role = auth_store.getRole()
  if (role === 'Admin') router.push('/admin/dashboard')
  else if (role === 'Company') router.push('/company/dashboard')
  else if (role === 'Student') router.push('/student/dashboard')
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center text-center">
      <div class="col-md-8">
        <h1 class="display-4 mb-3">Placement Portal Application</h1>
        <p class="lead text-muted mb-4">A unified platform for students, companies, and the institute placement cell to manage campus recruitment seamlessly.</p>
        <hr />
        <div v-if="!auth_store.isAuthenticated" class="mt-4">
          <RouterLink to="/login" class="btn btn-primary btn-lg me-3">Login</RouterLink>
          <RouterLink to="/register" class="btn btn-outline-secondary btn-lg">Register</RouterLink>
        </div>
        <div v-else class="mt-4">
          <button class="btn btn-primary btn-lg" @click="goToDashboard">Go to Dashboard</button>
        </div>
        <div class="row mt-5 text-start">
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Students</h5>
                <p class="card-text text-muted">Browse approved placement drives, apply based on eligibility, and track your application history.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Companies</h5>
                <p class="card-text text-muted">Register your company, create placement drives, and manage student applications and selections.</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Institute Admin</h5>
                <p class="card-text text-muted">Approve companies and drives, manage students, and view complete placement statistics.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>