<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { useMessageStore } from '@/stores/message.js'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const auth_store = useAuthStore()
const message_store = useMessageStore()
const router = useRouter()

const username = computed(() => auth_store.getUsername())
const role = computed(() => auth_store.getRole())

function goToDashboard() {
  if (role.value === 'Admin') router.push('/admin/dashboard')
  else if (role.value === 'Company') router.push('/company/dashboard')
  else if (role.value === 'Student') router.push('/student/dashboard')
}

function logout() {
  fetch('http://127.0.0.1:5000/api/auth/logout', {
    method: 'POST',
    headers: { 'Authentication-Token': auth_store.getAuthToken() }
  }).then(() => {
    auth_store.clearAuthToken()
    message_store.setMessage('You have been logged out successfully.', 'success')
    router.push('/')
  })
}
</script>

<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Placement Portal Application</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarScroll" aria-controls="navbarScroll" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarScroll">
          <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/">Home</RouterLink>
            </li>
            <li class="nav-item" v-if="auth_store.isAuthenticated">
              <a class="nav-link" style="cursor:pointer" @click="goToDashboard">Dashboard</a>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto my-2 my-lg-0">
            <template v-if="!auth_store.isAuthenticated">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/login">Login</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/register">Register</RouterLink>
              </li>
            </template>
            <template v-else>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  {{ username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li><span class="dropdown-item-text text-muted">{{ role }}</span></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" style="cursor:pointer" @click="logout">Logout</a></li>
                </ul>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid px-4 mt-2" v-if="message_store.message">
      <div class="alert mt-2" :class="{
        'alert-success': message_store.type === 'success',
        'alert-danger': message_store.type === 'error',
        'alert-warning': message_store.type === 'warning'
      }" role="alert">
        {{ message_store.message }}
      </div>
    </div>

    <RouterView />
  </div>
</template>