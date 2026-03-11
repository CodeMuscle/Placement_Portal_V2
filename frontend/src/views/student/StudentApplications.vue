<!-- src/views/student/StudentApplications.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const applications = ref([])

async function fetchApplications() {
  const response = await fetch('http://127.0.0.1:5000/api/student/applications', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) applications.value = await response.json()
}

async function exportCSV() {
  const response = await fetch('http://127.0.0.1:5000/api/student/export', {
    method: 'POST',
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
  }
}

onMounted(() => { fetchApplications() })
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <h2>My Applications</h2>
      <button class="btn btn-outline-secondary" @click="exportCSV">Export CSV</button>
    </div>
    <hr />
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Company</th>
            <th>Drive</th>
            <th>Job Title</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Applied At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
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
            <td>{{ app.remarks || '—' }}</td>
            <td>{{ new Date(app.applied_at).toLocaleDateString() }}</td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="6" class="text-center">No applications yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>