import { defineStore } from 'pinia'
import api from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken && !!state.user,
  },

  actions: {
    async init() {
      if (this.initialized) return

      const token = localStorage.getItem('access_token')
      const refresh = localStorage.getItem('refresh_token')

      if (token && refresh) {
        this.accessToken = token
        this.refreshToken = refresh
        try {
          await this.fetchUser()
        } catch {
          this.logout()
        }
      }

      this.initialized = true
    },

    async fetchUser() {
      const response = await api.get('/auth/me')
      this.user = response.data
    },

    async login(email, password) {
      const response = await api.post('/auth/login', { email, password })
      this.setTokens(response.data.access_token, response.data.refresh_token)
      await this.fetchUser()
    },

    async register(data) {
      const response = await api.post('/auth/register', data)
      this.setTokens(response.data.access_token, response.data.refresh_token)
      await this.fetchUser()
    },

    setTokens(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
    },

    logout() {
      this.user = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
  },
})