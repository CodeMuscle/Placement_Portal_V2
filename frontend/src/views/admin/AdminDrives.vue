<!-- src/views/admin/AdminDrives.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const drives = ref([])
const status_filter = ref('')

async function fetchDrives() {
  const query = status_filter.value ? `?status=${status_filter.value}` : ''
  const response = await fetch(`http://127.0.0.1:5000/api/admin/drives${query}`, {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) drives.value = await response.json()
}

async function updateDrive(drive_id, action) {
  const response = await fetch(`http://127.0.0.1:5000/api/admin/drives/${drive_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': auth_store.getAuthToken()
    },
    body: JSON.stringify({ action })
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
    fetchDrives()
  }
}

onMounted(() => { fetchDrives() })
</script>

<template>
  <div class="container mt-4">
    <h2>Manage Drives</h2>
    <hr />
    <div class="row mb-3">
      <div class="col-md-4">
        <select class="form-select" v-model="status_filter" @change="fetchDrives">
          <option value="">All</option>
          <option value="Pending">Pending</option>
          <option value="Approved">Approved</option>
          <option value="Closed">Closed</option>
          <option value="Completed">Completed</option>
        </select>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Drive Name</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.drive_id">
            <td>{{ drive.drive_id }}</td>
            <td>{{ drive.drive_name }}</td>
            <td>{{ drive.company_name }}</td>
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
            <td>
              <button class="btn btn-sm btn-success me-1" @click="updateDrive(drive.drive_id, 'approve')" :disabled="drive.status === 'Approved'">Approve</button>
              <button class="btn btn-sm btn-secondary" @click="updateDrive(drive.drive_id, 'close')" :disabled="drive.status === 'Closed'">Close</button>
            </td>
          </tr>
          <tr v-if="drives.length === 0">
            <td colspan="7" class="text-center">No drives found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>