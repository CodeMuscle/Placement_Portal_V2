<!-- src/views/Register.vue -->
<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMessageStore } from '@/stores/message.js'

const router = useRouter()
const message_store = useMessageStore()

const selected_role = ref('')
const email = ref('')
const password = ref('')
const username = ref('')
const name = ref('')
const department = ref('')
const year_of_study = ref('')
const cgpa = ref('')
const company_name = ref('')
const description = ref('')
const hr_contact = ref('')
const website = ref('')

const isStudent = computed(() => selected_role.value === 'Student')
const isCompany = computed(() => selected_role.value === 'Company')

function resetForm() {
  email.value = ''
  password.value = ''
  username.value = ''
  name.value = ''
  department.value = ''
  year_of_study.value = ''
  cgpa.value = ''
  company_name.value = ''
  description.value = ''
  hr_contact.value = ''
  website.value = ''
}

async function register() {
  let url = ''
  let body = {}

  if (isStudent.value) {
    url = 'http://127.0.0.1:5000/api/auth/register/student'
    body = {
      email: email.value,
      password: password.value,
      username: username.value,
      name: name.value,
      department: department.value,
      year_of_study: parseInt(year_of_study.value),
      cgpa: parseFloat(cgpa.value)
    }
  } else if (isCompany.value) {
    url = 'http://127.0.0.1:5000/api/auth/register/company'
    body = {
      email: email.value,
      password: password.value,
      username: username.value,
      company_name: company_name.value,
      description: description.value,
      hr_contact: hr_contact.value,
      website: website.value
    }
  }

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })

  const data = await response.json()

  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    message_store.setMessage(data.message, 'success')
    resetForm()
    router.push('/login')
  }
}
</script>

<template>
  <div class="container-fluid">
    <div class="row justify-content-center mt-3">
      <div class="col-6 align-items-center">
        <h1>Register</h1>
        <form @submit.prevent="register">
          <div class="mb-3">
            <label for="roleSelect" class="form-label">Register as</label>
            <select class="form-select" id="roleSelect" v-model="selected_role" required>
              <option value="" disabled>Select role</option>
              <option value="Student">Student</option>
              <option value="Company">Company</option>
            </select>
          </div>
          <template v-if="selected_role">
            <div class="mb-3">
              <label for="regEmail" class="form-label">Email address</label>
              <input type="email" class="form-control" id="regEmail" v-model="email" required />
            </div>
            <div class="mb-3">
              <label for="regPassword" class="form-label">Password</label>
              <input type="password" class="form-control" id="regPassword" v-model="password" required />
            </div>
            <div class="mb-3">
              <label for="regUsername" class="form-label">Username</label>
              <input type="text" class="form-control" id="regUsername" v-model="username" required />
            </div>
          </template>
          <template v-if="isStudent">
            <div class="mb-3">
              <label for="regName" class="form-label">Full Name</label>
              <input type="text" class="form-control" id="regName" v-model="name" required />
            </div>
            <div class="mb-3">
              <label for="regDept" class="form-label">Department</label>
              <input type="text" class="form-control" id="regDept" v-model="department" required />
            </div>
            <div class="mb-3">
              <label for="regYear" class="form-label">Year of Study</label>
              <input type="number" class="form-control" id="regYear" v-model="year_of_study" min="1" max="5" required />
            </div>
            <div class="mb-3">
              <label for="regCgpa" class="form-label">CGPA</label>
              <input type="number" class="form-control" id="regCgpa" v-model="cgpa" min="0" max="10" step="0.01" required />
            </div>
          </template>
          <template v-if="isCompany">
            <div class="mb-3">
              <label for="regCompanyName" class="form-label">Company Name</label>
              <input type="text" class="form-control" id="regCompanyName" v-model="company_name" required />
            </div>
            <div class="mb-3">
              <label for="regDesc" class="form-label">Description</label>
              <textarea class="form-control" id="regDesc" v-model="description" rows="3"></textarea>
            </div>
            <div class="mb-3">
              <label for="regHr" class="form-label">HR Contact</label>
              <input type="text" class="form-control" id="regHr" v-model="hr_contact" />
            </div>
            <div class="mb-3">
              <label for="regWebsite" class="form-label">Website</label>
              <input type="url" class="form-control" id="regWebsite" v-model="website" />
            </div>
          </template>
          <button type="submit" class="btn btn-primary" :disabled="!selected_role">Register</button>
          <p class="mt-3">Already have an account? <RouterLink to="/login">Login here</RouterLink></p>
        </form>
      </div>
    </div>
  </div>
</template>