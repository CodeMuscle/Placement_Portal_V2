<!-- src/views/admin/AdminCompanies.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const companies = ref([])
const status_filter = ref('')

async function fetchCompanies() {
  const query = status_filter.value ? `?status=${status_filter.value}` : ''
  const response = await fetch(`http://127.0.0.1:5000/api/admin/companies${query}`, {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) companies.value = await response.json()
}

async function updateCompany(company_id, action) {
  const response = await fetch(`http://127.0.0.1:5000/api/admin/companies/${company_id}`, {
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
    fetchCompanies()
  }
}

onMounted(() => { fetchCompanies() })
</script>

<template>
  <div class="container mt-4">
    <h2>Manage Companies</h2>
    <hr />
    <div class="row mb-3">
      <div class="col-md-4">
        <select class="form-select" v-model="status_filter" @change="fetchCompanies">
          <option value="">All</option>
          <option value="Pending">Pending</option>
          <option value="Approved">Approved</option>
          <option value="Blocked">Blocked</option>
        </select>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>HR Contact</th>
            <th>Website</th>
            <th>Status</th>
            <th>User Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in companies" :key="company.company_id">
            <td>{{ company.company_id }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.hr_contact }}</td>
            <td><a :href="company.website" target="_blank">{{ company.website }}</a></td>
            <td>
              <span class="badge" :class="{
                'bg-warning': company.approval_status === 'Pending',
                'bg-success': company.approval_status === 'Approved',
                'bg-danger': company.approval_status === 'Blocked'
              }">{{ company.approval_status }}</span>
            </td>
            <td>{{ company.user_status }}</td>
            <td>
              <button class="btn btn-sm btn-success me-1" @click="updateCompany(company.company_id, 'approve')" :disabled="company.approval_status === 'Approved'">Approve</button>
              <button class="btn btn-sm btn-danger" @click="updateCompany(company.company_id, 'block')" :disabled="company.approval_status === 'Blocked'">Block</button>
            </td>
          </tr>
          <tr v-if="companies.length === 0">
            <td colspan="7" class="text-center">No companies found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>