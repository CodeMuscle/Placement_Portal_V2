<!-- src/views/student/StudentDrives.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const drives = ref([])
const search = ref('')

async function fetchDrives() {
  const query = search.value ? `?search=${search.value}` : ''
  const response = await fetch(`http://127.0.0.1:5000/api/student/drives${query}`, {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) drives.value = await response.json()
}

async function applyDrive(drive_id) {
  const response = await fetch(`http://127.0.0.1:5000/api/student/apply/${drive_id}`, {
    method: 'POST',
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
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
    <h2>Browse Placement Drives</h2>
    <hr />
    <div class="row mb-3">
      <div class="col-md-6">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="Search by job title or drive name..." v-model="search" @keyup.enter="fetchDrives" />
          <button class="btn btn-primary" @click="fetchDrives">Search</button>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 mb-3" v-for="drive in drives" :key="drive.drive_id">
        <div class="card h-100" :class="{ 'border-success': drive.is_eligible, 'border-danger': !drive.is_eligible }">
          <div class="card-body">
            <h5 class="card-title">{{ drive.job_title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ drive.company_name }}</h6>
            <p class="card-text">{{ drive.job_description }}</p>
            <p><strong>Location:</strong> {{ drive.location || 'N/A' }}</p>
            <p><strong>Salary:</strong> {{ drive.salary ? drive.salary + ' LPA' : 'N/A' }}</p>
            <p><strong>Min CGPA:</strong> {{ drive.min_cgpa }}</p>
            <p><strong>Departments:</strong> {{ drive.eligible_departments.join(', ') || 'All' }}</p>
            <p><strong>Deadline:</strong> {{ new Date(drive.deadline).toLocaleDateString() }}</p>
            <span class="badge mb-2" :class="drive.is_eligible ? 'bg-success' : 'bg-danger'">
              {{ drive.is_eligible ? 'Eligible' : 'Not Eligible' }}
            </span>
          </div>
          <div class="card-footer">
            <button class="btn btn-primary w-100" @click="applyDrive(drive.drive_id)" :disabled="!drive.is_eligible">Apply</button>
          </div>
        </div>
      </div>
      <div class="col-12" v-if="drives.length === 0">
        <p class="text-center text-muted">No drives available.</p>
      </div>
    </div>
  </div>
</template>