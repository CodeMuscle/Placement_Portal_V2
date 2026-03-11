<!-- src/views/student/StudentProfile.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const profile = ref({ name: '', department: '', year_of_study: '', cgpa: '' })
const resume_file = ref(null)

async function fetchProfile() {
  const response = await fetch('http://127.0.0.1:5000/api/student/profile', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) profile.value = await response.json()
}

async function updateProfile() {
  const response = await fetch('http://127.0.0.1:5000/api/student/profile', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': auth_store.getAuthToken()
    },
    body: JSON.stringify({
      name: profile.value.name,
      department: profile.value.department,
      year_of_study: profile.value.year_of_study,
      cgpa: profile.value.cgpa
    })
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
  }
}

async function uploadResume() {
  if (!resume_file.value) {
    message_store.setMessage('Please select a PDF file.', 'error')
    return
  }
  const form_data = new FormData()
  form_data.append('resume', resume_file.value)
  const response = await fetch('http://127.0.0.1:5000/api/student/resume', {
    method: 'POST',
    headers: { 'Authentication-Token': auth_store.getAuthToken() },
    body: form_data
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
    fetchProfile()
  }
}

function handleFileChange(event) {
  resume_file.value = event.target.files[0]
}

onMounted(() => { fetchProfile() })
</script>

<template>
  <div class="container mt-4">
    <h2>My Profile</h2>
    <hr />
    <div class="row justify-content-center">
      <div class="col-md-6">
        <form @submit.prevent="updateProfile" class="mb-4">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" class="form-control" v-model="profile.name" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Department</label>
            <input type="text" class="form-control" v-model="profile.department" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Year of Study</label>
            <input type="number" class="form-control" v-model="profile.year_of_study" min="1" max="5" required />
          </div>
          <div class="mb-3">
            <label class="form-label">CGPA</label>
            <input type="number" class="form-control" v-model="profile.cgpa" min="0" max="10" step="0.01" required />
          </div>
          <button type="submit" class="btn btn-primary">Update Profile</button>
        </form>
        <hr />
        <h5>Upload Resume</h5>
        <div class="mb-3">
          <input type="file" class="form-control" accept=".pdf" @change="handleFileChange" />
        </div>
        <div v-if="profile.resume_url" class="mb-2">
          <a :href="`http://127.0.0.1:5000${profile.resume_url}`" target="_blank">View current resume</a>
        </div>
        <button class="btn btn-secondary" @click="uploadResume">Upload Resume</button>
      </div>
    </div>
  </div>
</template>