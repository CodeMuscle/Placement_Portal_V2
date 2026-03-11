<!-- src/views/company/CompanyDrives.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const drives = ref([])
const show_form = ref(false)

const form = ref({
  drive_name: '', job_title: '', job_description: '',
  eligible_departments: '', min_cgpa: 0, eligible_years: '',
  salary: '', location: '', deadline: ''
})

async function fetchDrives() {
  const response = await fetch('http://127.0.0.1:5000/api/company/drives', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) drives.value = await response.json()
}

async function createDrive() {
  const response = await fetch('http://127.0.0.1:5000/api/company/drives', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': auth_store.getAuthToken()
    },
    body: JSON.stringify(form.value)
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
    show_form.value = false
    form.value = { drive_name: '', job_title: '', job_description: '', eligible_departments: '', min_cgpa: 0, eligible_years: '', salary: '', location: '', deadline: '' }
    fetchDrives()
  }
}

onMounted(() => { fetchDrives() })
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <h2>Placement Drives</h2>
      <button class="btn btn-success" @click="show_form = !show_form">{{ show_form ? 'Cancel' : '+ New Drive' }}</button>
    </div>
    <hr />
    <div v-if="show_form" class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Create New Drive</h5>
        <form @submit.prevent="createDrive">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Drive Name</label>
              <input type="text" class="form-control" v-model="form.drive_name" required />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Job Title</label>
              <input type="text" class="form-control" v-model="form.job_title" required />
            </div>
            <div class="col-12 mb-3">
              <label class="form-label">Job Description</label>
              <textarea class="form-control" v-model="form.job_description" rows="3" required></textarea>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Departments (comma separated)</label>
              <input type="text" class="form-control" v-model="form.eligible_departments" placeholder="CSE, ECE, IT" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Years (comma separated)</label>
              <input type="text" class="form-control" v-model="form.eligible_years" placeholder="3, 4" />
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Min CGPA</label>
              <input type="number" class="form-control" v-model="form.min_cgpa" min="0" max="10" step="0.1" />
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Salary (LPA)</label>
              <input type="number" class="form-control" v-model="form.salary" />
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Location</label>
              <input type="text" class="form-control" v-model="form.location" />
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Application Deadline</label>
              <input type="datetime-local" class="form-control" v-model="form.deadline" required />
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Submit Drive</button>
        </form>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Drive Name</th>
            <th>Job Title</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Applicants</th>
            <th>Actions</th>
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
            <td>
              <button class="btn btn-sm btn-outline-info" @click="$router.push(`/company/applications/${drive.drive_id}`)">View Applicants</button>
            </td>
          </tr>
          <tr v-if="drives.length === 0">
            <td colspan="6" class="text-center">No drives found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>