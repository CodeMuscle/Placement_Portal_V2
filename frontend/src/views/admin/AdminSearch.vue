<!-- src/views/admin/AdminSearch.vue -->
<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth.js'

const auth_store = useAuthStore()
const query = ref('')
const students = ref([])
const companies = ref([])
const searched = ref(false)

async function search() {
  if (!query.value.trim()) return
  const response = await fetch(`http://127.0.0.1:5000/api/admin/search?q=${query.value}`, {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) {
    const data = await response.json()
    students.value = data.students
    companies.value = data.companies
    searched.value = true
  }
}
</script>

<template>
  <div class="container mt-4">
    <h2>Search</h2>
    <hr />
    <div class="row mb-4">
      <div class="col-md-8">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="Search students or companies..." v-model="query" @keyup.enter="search" />
          <button class="btn btn-primary" @click="search">Search</button>
        </div>
      </div>
    </div>

    <div v-if="searched">
      <h5>Students <span class="badge bg-primary">{{ students.length }}</span></h5>
      <div class="table-responsive mb-4">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
              <th>CGPA</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.student_id">
              <td>{{ s.student_id }}</td>
              <td>{{ s.name }}</td>
              <td>{{ s.email }}</td>
              <td>{{ s.department }}</td>
              <td>{{ s.cgpa }}</td>
              <td><span class="badge" :class="{ 'bg-success': s.status === 'Active', 'bg-danger': s.status === 'Blocked' }">{{ s.status }}</span></td>
            </tr>
            <tr v-if="students.length === 0">
              <td colspan="6" class="text-center">No students found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h5>Companies <span class="badge bg-success">{{ companies.length }}</span></h5>
      <div class="table-responsive">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Approval Status</th>
              <th>User Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in companies" :key="c.company_id">
              <td>{{ c.company_id }}</td>
              <td>{{ c.name }}</td>
              <td>{{ c.email }}</td>
              <td><span class="badge" :class="{ 'bg-success': c.approval_status === 'Approved', 'bg-warning': c.approval_status === 'Pending', 'bg-danger': c.approval_status === 'Blocked' }">{{ c.approval_status }}</span></td>
              <td>{{ c.status }}</td>
            </tr>
            <tr v-if="companies.length === 0">
              <td colspan="5" class="text-center">No companies found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>