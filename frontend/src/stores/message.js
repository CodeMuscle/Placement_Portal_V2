// src/stores/message.js
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMessageStore = defineStore('messageStore', () => {
  const message = ref('')
  const type = ref('success')

  function setMessage(msg, msg_type = 'success') {
    message.value = msg
    type.value = msg_type
    setTimeout(() => {
      message.value = ''
      type.value = 'success'
    }, 4000)
  }

  function clearMessage() {
    message.value = ''
    type.value = 'success'
  }

  return { message, type, setMessage, clearMessage }
})