<template>
  <div class="login-page">
    <div class="login-form">
      <h2>Login</h2>
      <div v-if="error" class="error">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="Enter your email"
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <p class="register-link">
        Don't have an account?
        <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL
const router = useRouter()

const email = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.post(`${API_URL}/users/login`, {
      email: email.value
    })
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      router.push('/')
    } else {
      error.value = 'Invalid response from server'
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to login'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  background: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  margin-bottom: 1.5rem;
  text-align: left;
  color: #1a1a1a;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #1a1a1a;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #1a1a1a;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #333;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  color: #e74c3c;
  margin-bottom: 1rem;
  text-align: left;
}

.register-link {
  margin-top: 1rem;
  text-align: center;
  color: #666;
}

.register-link a {
  color: #1a1a1a;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style> 