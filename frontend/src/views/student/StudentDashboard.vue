<!-- src/views/student/StudentDashboard.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useRouter } from 'vue-router'

const auth_store = useAuthStore()
const router = useRouter()
const profile = ref(null)
const applications = ref([])

async function fetchProfile() {
  const response = await fetch('http://127.0.0.1:5000/api/student/profile', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) {
    profile.value = await response.json()
  }
}

async function fetchApplications() {
  const response = await fetch('http://127.0.0.1:5000/api/student/applications', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) {
    applications.value = await response.json()
  }
}

onMounted(() => {
  fetchProfile()
  fetchApplications()
})
</script>

<template>
  <div class="container mt-4">
    <h2>Student Dashboard</h2>
    <hr />
    <div v-if="profile" class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">{{ profile.name }}</h5>
        <p class="card-text"><strong>Email:</strong> {{ profile.email }}</p>
        <p class="card-text"><strong>Department:</strong> {{ profile.department }}</p>
        <p class="card-text"><strong>Year:</strong> {{ profile.year_of_study }}</p>
        <p class="card-text"><strong>CGPA:</strong> {{ profile.cgpa }}</p>
        <p class="card-text">
          <strong>Resume:</strong>
          <a v-if="profile.resume_url" :href="`http://127.0.0.1:5000${profile.resume_url}`" target="_blank" class="ms-2">View Resume</a>
          <span v-else class="text-muted ms-2">Not uploaded</span>
        </p>
      </div>
    </div>

    <div class="row mb-3">
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-primary w-100" @click="$router.push('/student/profile')">Edit Profile</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-success w-100" @click="$router.push('/student/drives')">Browse Drives</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-info w-100" @click="$router.push('/student/applications')">My Applications</button>
      </div>
    </div>

    <h5>Recent Applications</h5>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Company</th>
            <th>Drive</th>
            <th>Job Title</th>
            <th>Status</th>
            <th>Applied At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications.slice(0, 5)" :key="app.application_id">
            <td>{{ app.company_name }}</td>
            <td>{{ app.drive_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>
              <span class="badge" :class="{
                'bg-secondary': app.status === 'Applied',
                'bg-warning': app.status === 'Shortlisted',
                'bg-success': app.status === 'Selected',
                'bg-danger': app.status === 'Rejected'
              }">{{ app.status }}</span>
            </td>
            <td>{{ new Date(app.applied_at).toLocaleDateString() }}</td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="5" class="text-center">No applications yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>