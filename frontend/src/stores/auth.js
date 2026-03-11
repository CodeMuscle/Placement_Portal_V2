// src/stores/auth.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('authStore', () => {
  const auth_token = ref(localStorage.getItem('auth_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)

  const isAuthenticated = computed(() => auth_token.value !== null)

  function setUserCred(token, user_data) {
    localStorage.setItem('auth_token', token)
    localStorage.setItem('user', JSON.stringify(user_data))
    auth_token.value = token
    user.value = user_data
  }

  function clearAuthToken() {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    auth_token.value = null
    user.value = null
  }

  function getAuthToken() {
    return auth_token.value
  }

  function getUsername() {
    return user.value ? user.value.username : null
  }

  function getEmail() {
    return user.value ? user.value.email : null
  }

  function getRole() {
    return user.value ? user.value.role : null
  }

  function getRoles() {
    return user.value ? user.value.roles : []
  }

  return {
    isAuthenticated,
    setUserCred,
    clearAuthToken,
    getAuthToken,
    getUsername,
    getEmail,
    getRole,
    getRoles
  }
})