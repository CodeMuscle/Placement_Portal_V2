<!-- src/views/admin/AdminDashboard.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useRouter } from 'vue-router'

const auth_store = useAuthStore()
const router = useRouter()

const stats = ref(null)

async function fetchDashboard() {
  const response = await fetch('http://127.0.0.1:5000/api/admin/dashboard', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (!response.ok) {
    alert('Failed to load dashboard.')
  } else {
    stats.value = await response.json()
  }
}

onMounted(() => { fetchDashboard() })
</script>

<template>
  <div class="container mt-4">
    <h2>Admin Dashboard</h2>
    <hr />
    <div v-if="stats" class="row mt-3">
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h5 class="card-title">Total Students</h5>
            <p class="card-text fs-3">{{ stats.total_students }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h5 class="card-title">Total Companies</h5>
            <p class="card-text fs-3">{{ stats.total_companies }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-info">
          <div class="card-body">
            <h5 class="card-title">Total Drives</h5>
            <p class="card-text fs-3">{{ stats.total_drives }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-warning">
          <div class="card-body">
            <h5 class="card-title">Total Applications</h5>
            <p class="card-text fs-3">{{ stats.total_applications }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-danger">
          <div class="card-body">
            <h5 class="card-title">Pending Companies</h5>
            <p class="card-text fs-3">{{ stats.pending_companies }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card text-white bg-secondary">
          <div class="card-body">
            <h5 class="card-title">Pending Drives</h5>
            <p class="card-text fs-3">{{ stats.pending_drives }}</p>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading dashboard...</p>
    </div>
    <hr />
    <div class="row mt-2">
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-primary w-100" @click="$router.push('/admin/companies')">Manage Companies</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-success w-100" @click="$router.push('/admin/drives')">Manage Drives</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-info w-100" @click="$router.push('/admin/students')">Manage Students</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-secondary w-100" @click="$router.push('/admin/search')">Search</button>
      </div>
    </div>
  </div>
</template>