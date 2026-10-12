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
            Welcome Back
          </h2>
          <p class="text-center text-medium-emphasis mb-6">
            Sign in to continue learning
          </p>

          <form @submit.prevent="login">
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
              class="mb-4"
              :error-messages="errors.password"
              required
            />
            <v-btn
              type="submit"
              color="primary"
              class="w-100"
              size="large"
              :loading="loading"
            >
              Sign In
            </v-btn>
          </form>

          <div class="text-center mt-6">
            <p class="text-medium-emphasis">
              Don't have an account?
              <router-link
                to="/register"
                class="text-primary ml-1"
              >
                Sign up
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
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loading = ref(false)
const form = reactive({ email: '', password: '' })
const errors = reactive({ email: [], password: [] })

async function login() {
  errors.email = []
  errors.password = []
  loading.value = true

  try {
    await authStore.login(form.email, form.password)
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (e) {
    if (e.response?.status === 401) {
      errors.password = ['Invalid email or password']
    } else {
      errors.email = ['Login failed. Please try again.']
    }
  } finally {
    loading.value = false
  }
}
</script>