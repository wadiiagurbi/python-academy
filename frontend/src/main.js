import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useThemeStore } from './stores/theme'
import './assets/main.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#2563EB',
          secondary: '#0891B2',
          accent: '#F59E0B',
          error: '#DC2626',
          info: '#0EA5E9',
          success: '#16A34A',
          warning: '#F59E0B',
          background: '#F8FAFC',
          surface: '#FFFFFF',
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-surface': '#0F172A',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#3B82F6',
          secondary: '#06B6D4',
          accent: '#FBBF24',
          error: '#EF4444',
          info: '#38BDF8',
          success: '#22C55E',
          warning: '#FBBF24',
          background: '#0F172A',
          surface: '#1E293B',
          'on-primary': '#FFFFFF',
          'on-secondary': '#FFFFFF',
          'on-surface': '#F8FAFC',
        },
      },
    },
  },
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(vuetify)
app.use(router)

const themeStore = useThemeStore()
themeStore.init()

app.mount('#app')