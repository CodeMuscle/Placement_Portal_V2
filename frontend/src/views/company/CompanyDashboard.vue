<!-- src/views/company/CompanyDashboard.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useRouter } from 'vue-router'

const auth_store = useAuthStore()
const router = useRouter()
const profile = ref(null)
const drives = ref([])

async function fetchProfile() {
  const response = await fetch('http://127.0.0.1:5000/api/company/profile', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) {
    profile.value = await response.json()
  }
}

async function fetchDrives() {
  const response = await fetch('http://127.0.0.1:5000/api/company/drives', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) {
    drives.value = await response.json()
  }
}

onMounted(() => {
  fetchProfile()
  fetchDrives()
})
</script>

<template>
  <div class="container mt-4">
    <h2>Company Dashboard</h2>
    <hr />
    <div v-if="profile" class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">{{ profile.name }}</h5>
        <p class="card-text text-muted">{{ profile.description }}</p>
        <p><strong>HR Contact:</strong> {{ profile.hr_contact }}</p>
        <p><strong>Website:</strong> <a :href="profile.website" target="_blank">{{ profile.website }}</a></p>
        <span class="badge" :class="{
          'bg-warning': profile.approval_status === 'Pending',
          'bg-success': profile.approval_status === 'Approved',
          'bg-danger': profile.approval_status === 'Blocked'
        }">{{ profile.approval_status }}</span>
      </div>
    </div>

    <div class="row mb-3">
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-primary w-100" @click="$router.push('/company/profile')">Edit Profile</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-success w-100" @click="$router.push('/company/drives')">Manage Drives</button>
      </div>
      <div class="col-md-3 mb-2">
        <button class="btn btn-outline-info w-100" @click="$router.push('/company/applications')">View Applications</button>
      </div>
    </div>

    <h5>My Drives</h5>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Drive Name</th>
            <th>Job Title</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Applicants</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.drive_id">
            <td>{{ drive.drive_name }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
            <td>
              <span class="badge" :class="{
                'bg-warning': drive.status === 'Pending',
                'bg-success': drive.status === 'Approved',
                'bg-secondary': drive.status === 'Closed',
                'bg-info': drive.status === 'Completed'
              }">{{ drive.status }}</span>
            </td>
            <td>{{ drive.applicant_count }}</td>
          </tr>
          <tr v-if="drives.length === 0">
            <td colspan="5" class="text-center">No drives created yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>