<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :temporary="mobile"
      :width="280"
      class="border-end"
    >
      <AppSidebar />
    </v-navigation-drawer>

    <v-app-bar
      app
      color="surface"
      elevation="1"
      class="border-bottom"
    >
      <v-app-bar-nav-icon
        class="me-2"
        @click.stop="drawer = !drawer"
      />
      <v-toolbar-title class="text-h6 font-weight-medium">
        <router-link
          to="/"
          class="text-decoration-none text-inherit"
        >
          <v-icon start>
            mdi-language-python
          </v-icon>
          Python Academy
        </router-link>
      </v-toolbar-title>

      <v-spacer />

      <v-btn
        variant="text"
        class="me-2"
        @click="themeStore.toggle"
      >
        <v-icon>{{ themeStore.isDark ? 'mdi-weather-night' : 'mdi-weather-sunny' }}</v-icon>
      </v-btn>

      <v-menu v-if="authStore.isAuthenticated">
        <template #activator="{ props }">
          <v-btn
            variant="text"
            v-bind="props"
            class="me-2"
          >
            <v-avatar size="32">
              <v-icon>mdi-account-circle</v-icon>
            </v-avatar>
            <span class="ms-1">{{ authStore.user?.display_name }}</span>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="goToDashboard">
            <v-list-item-title>Dashboard</v-list-item-title>
            <v-icon start>
              mdi-view-dashboard
            </v-icon>
          </v-list-item>
          <v-list-item @click="goToPipelines">
            <v-list-item-title>My Pipelines</v-list-item-title>
            <v-icon start>
              mdi-pipe
            </v-icon>
          </v-list-item>
          <v-divider />
          <v-list-item @click="logout">
            <v-list-item-title>Logout</v-list-item-title>
            <v-icon start>
              mdi-logout
            </v-icon>
          </v-list-item>
        </v-list>
      </v-menu>

      <template v-else>
        <v-btn
          variant="tonal"
          to="/login"
          class="me-2"
        >
          Login
        </v-btn>
        <v-btn
          color="primary"
          to="/register"
        >
          Register
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-container
        fluid
        class="pa-4"
      >
        <router-view v-slot="{ Component }">
          <transition
            name="fade"
            mode="out-in"
          >
            <component :is="Component" />
          </transition>
        </router-view>
      </v-container>
    </v-main>

    <v-footer
      class="py-4 px-6 border-top"
      app
    >
      <v-row
        align="center"
        justify="space-between"
      >
        <v-col
          cols="12"
          md="auto"
        >
          <span class="text-body-2 text-medium-emphasis">Python Academy &copy; 2026</span>
        </v-col>
        <v-col
          cols="12"
          md="auto"
        >
          <!-- About / Privacy links removed — no views exist -->
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDisplay, useTheme } from 'vuetify'
import AppSidebar from './components/AppSidebar.vue'
import { useAuthStore } from './stores/auth'
import { useThemeStore } from './stores/theme'

const router = useRouter()
const { mobile } = useDisplay()
const vuetifyTheme = useTheme()
const authStore = useAuthStore()
const themeStore = useThemeStore()

watch(
  () => themeStore.isDark,
  (isDark) => {
    vuetifyTheme.global.name.value = isDark ? 'dark' : 'light'
  },
  { immediate: true },
)

const drawer = ref(true)

function goToDashboard() {
  router.push('/dashboard')
  drawer.value = false
}

function goToPipelines() {
  router.push('/pipelines')
  drawer.value = false
}

function logout() {
  authStore.logout()
  router.push('/')
  drawer.value = false
}

onMounted(() => {
  authStore.init()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>