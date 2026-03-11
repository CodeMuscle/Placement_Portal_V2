<!-- src/views/admin/AdminApplications.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'

const auth_store = useAuthStore()
const applications = ref([])

async function fetchApplications() {
  const response = await fetch('http://127.0.0.1:5000/api/admin/applications', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) {
    applications.value = await response.json()
  }
}

onMounted(() => { fetchApplications() })
</script>

<template>
  <div class="container mt-4">
    <h2>All Applications</h2>
    <hr />
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Student</th>
            <th>Company</th>
            <th>Drive</th>
            <th>Job Title</th>
            <th>Status</th>
            <th>Applied At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.application_id }}</td>
            <td>{{ app.student_name }}</td>
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
            <td colspan="7" class="text-center">No applications found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>