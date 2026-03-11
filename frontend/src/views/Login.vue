<!-- src/views/Login.vue -->
<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'
import { useRouter } from 'vue-router'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const router = useRouter()

const email = ref('')
const password = ref('')

async function login() {
  const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value, password: password.value })
  })

  const data = await response.json()

  if (!response.ok) {
    message_store.setMessage(data.message, 'error')
  } else {
    auth_store.setUserCred(data.user_details.auth_token, {
      email: data.user_details.email,
      username: data.user_details.username,
      role: data.user_details.role,
      roles: data.user_details.roles
    })
    message_store.setMessage(data.message, 'success')
    if (data.user_details.role === 'Admin') router.push('/admin/dashboard')
    else if (data.user_details.role === 'Company') router.push('/company/dashboard')
    else if (data.user_details.role === 'Student') router.push('/student/dashboard')
  }
}
</script>

<template>
  <div class="container-fluid">
    <div class="row justify-content-center mt-3">
      <div class="col-6 align-items-center">
        <h1>Login</h1>
        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="loginEmail" class="form-label">Email address</label>
            <input type="email" class="form-control" id="loginEmail" v-model="email" required />
          </div>
          <div class="mb-3">
            <label for="loginPassword" class="form-label">Password</label>
            <input type="password" class="form-control" id="loginPassword" v-model="password" required />
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
          <p class="mt-3">Don't have an account? <RouterLink to="/register">Register here</RouterLink></p>
        </form>
      </div>
    </div>
  </div>
</template>