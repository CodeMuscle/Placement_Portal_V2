<!-- src/views/company/CompanyApplications.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'
import { useRoute } from 'vue-router'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const route = useRoute()
const drive_id = route.params.drive_id
const applications = ref([])

async function fetchApplications() {
  const response = await fetch(`http://127.0.0.1:5000/api/company/drives/${drive_id}/applications`, {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) applications.value = await response.json()
}

async function updateStatus(application_id, status) {
  const response = await fetch(`http://127.0.0.1:5000/api/company/drives/${drive_id}/applications/${application_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': auth_store.getAuthToken()
    },
    body: JSON.stringify({ status })
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
    fetchApplications()
  }
}

onMounted(() => { fetchApplications() })
</script>

<template>
  <div class="container mt-4">
    <h2>Drive Applications</h2>
    <hr />
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Student Name</th>
            <th>Department</th>
            <th>Year</th>
            <th>CGPA</th>
            <th>Resume</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.student_name }}</td>
            <td>{{ app.department }}</td>
            <td>{{ app.year_of_study }}</td>
            <td>{{ app.cgpa }}</td>
            <td>
              <a v-if="app.resume_url" :href="`http://127.0.0.1:5000${app.resume_url}`" target="_blank" class="btn btn-sm btn-outline-secondary">View</a>
              <span v-else class="text-muted">N/A</span>
            </td>
            <td>
              <span class="badge" :class="{
                'bg-secondary': app.status === 'Applied',
                'bg-warning': app.status === 'Shortlisted',
                'bg-success': app.status === 'Selected',
                'bg-danger': app.status === 'Rejected'
              }">{{ app.status }}</span>
            </td>
            <td>
              <select class="form-select form-select-sm" @change="updateStatus(app.application_id, $event.target.value)" :value="app.status">
                <option value="Applied">Applied</option>
                <option value="Shortlisted">Shortlisted</option>
                <option value="Selected">Selected</option>
                <option value="Rejected">Rejected</option>
              </select>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="7" class="text-center">No applications yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>