<!-- src/views/company/CompanyProfile.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const profile = ref({ description: '', hr_contact: '', website: '' })

async function fetchProfile() {
  const response = await fetch('http://127.0.0.1:5000/api/company/profile', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) profile.value = await response.json()
}

async function updateProfile() {
  const response = await fetch('http://127.0.0.1:5000/api/company/profile', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authentication-Token': auth_store.getAuthToken()
    },
    body: JSON.stringify({
      description: profile.value.description,
      hr_contact: profile.value.hr_contact,
      website: profile.value.website
    })
  })
  const data = await response.json()
  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
  }
}

onMounted(() => { fetchProfile() })
</script>

<template>
  <div class="container mt-4">
    <h2>Company Profile</h2>
    <hr />
    <div class="row justify-content-center">
      <div class="col-md-6">
        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label class="form-label">Company Name</label>
            <input type="text" class="form-control" :value="profile.name" disabled />
          </div>
          <div class="mb-3">
            <label class="form-label">Description</label>
            <textarea class="form-control" v-model="profile.description" rows="3"></textarea>
          </div>
          <div class="mb-3">
            <label class="form-label">HR Contact</label>
            <input type="text" class="form-control" v-model="profile.hr_contact" />
          </div>
          <div class="mb-3">
            <label class="form-label">Website</label>
            <input type="url" class="form-control" v-model="profile.website" />
          </div>
          <button type="submit" class="btn btn-primary">Update Profile</button>
        </form>
      </div>
    </div>
  </div>
</template>