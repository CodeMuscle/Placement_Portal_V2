<!-- src/views/admin/AdminStudents.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const students = ref([])

async function fetchStudents() {
  const response = await fetch('http://127.0.0.1:5000/api/admin/students', {
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  })
  if (response.ok) students.value = await response.json()
}

async function updateStudent(student_id, action) {
  const response = await fetch(`http://127.0.0.1:5000/api/admin/students/${student_id}`, {
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
    fetchStudents()
  }
}

onMounted(() => { fetchStudents() })
</script>

<template>
  <div class="container mt-4">
    <h2>Manage Students</h2>
    <hr />
    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Year</th>
            <th>CGPA</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.student_id">
            <td>{{ student.student_id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.department }}</td>
            <td>{{ student.year_of_study }}</td>
            <td>{{ student.cgpa }}</td>
            <td>
              <span class="badge" :class="{
                'bg-success': student.status === 'Active',
                'bg-danger': student.status === 'Blocked',
                'bg-warning': student.status === 'Pending'
              }">{{ student.status }}</span>
            </td>
            <td>
              <button class="btn btn-sm btn-danger me-1" @click="updateStudent(student.student_id, 'block')" :disabled="student.status === 'Blocked'">Block</button>
              <button class="btn btn-sm btn-success" @click="updateStudent(student.student_id, 'unblock')" :disabled="student.status === 'Active'">Unblock</button>
            </td>
          </tr>
          <tr v-if="students.length === 0">
            <td colspan="8" class="text-center">No students found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>