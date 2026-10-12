<template>
  <v-container class="pa-0">
    <v-row justify="center">
      <v-col
        cols="12"
        md="6"
        lg="4"
      >
        <v-card
          variant="outlined"
          class="pa-8"
        >
          <v-icon
            size="80"
            color="primary"
            class="mb-4 d-block text-center"
          >
            mdi-language-python
          </v-icon>
          <h2 class="text-h4 text-center mb-2">
            Create Account
          </h2>
          <p class="text-center text-medium-emphasis mb-6">
            Start your Python learning journey
          </p>

          <form @submit.prevent="register">
            <v-text-field
              v-model="form.display_name"
              label="Display Name"
              prepend-icon="mdi-account"
              density="comfortable"
              class="mb-3"
              :error-messages="errors.display_name"
              required
            />
            <v-text-field
              v-model="form.email"
              label="Email"
              type="email"
              prepend-icon="mdi-email"
              density="comfortable"
              class="mb-3"
              :error-messages="errors.email"
              required
            />
            <v-text-field
              v-model="form.password"
              label="Password"
              type="password"
              prepend-icon="mdi-lock"
              density="comfortable"
              class="mb-3"
              :error-messages="errors.password"
              required
              counter="128"
            />
            <v-text-field
              v-model="form.confirm_password"
              label="Confirm Password"
              type="password"
              prepend-icon="mdi-lock-outline"
              density="comfortable"
              class="mb-4"
              :error-messages="errors.confirm_password"
              required
            />
            <v-btn
              type="submit"
              color="primary"
              class="w-100"
              size="large"
              :loading="loading"
            >
              Create Account
            </v-btn>
          </form>

          <div class="text-center mt-6">
            <p class="text-medium-emphasis">
              Already have an account?
              <router-link
                to="/login"
                class="text-primary ml-1"
              >
                Sign in
              </router-link>
            </p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const form = reactive({ display_name: '', email: '', password: '', confirm_password: '' })
const errors = reactive({ display_name: [], email: [], password: [], confirm_password: [] })

async function register() {
  errors.display_name = []
  errors.email = []
  errors.password = []
  errors.confirm_password = []

  if (form.password !== form.confirm_password) {
    errors.confirm_password = ['Passwords do not match']
    return
  }

  if (form.password.length < 8) {
    errors.password = ['Password must be at least 8 characters']
    return
  }

  loading.value = true

  try {
    await authStore.register(form)
    router.push('/dashboard')
  } catch (e) {
    if (e.response?.status === 400) {
      errors.email = ['Email already registered']
    } else {
      errors.email = ['Registration failed. Please try again.']
    }
  } finally {
    loading.value = false
  }
}
</script>