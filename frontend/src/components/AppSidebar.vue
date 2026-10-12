<template>
  <v-sheet
    elevation="0"
    class="pa-3 h-full d-flex flex-column"
  >
    <v-text-field
      v-model="searchQuery"
      placeholder="Search lessons..."
      density="compact"
      variant="solo"
      prepend-icon="mdi-magnify"
      class="mb-4"
      @keydown.enter="onSearch"
    />

    <v-divider class="mb-3" />

    <v-list
      nav
      density="compact"
      lines="two"
      class="flex-grow-1 overflow-auto"
    >
      <v-list-item
        v-for="track in coursesStore.tracks"
        :key="track.key"
        :to="{ name: 'courses', params: { track: track.key } }"
        exact
      >
        <v-list-item-title class="text-h6 font-weight-bold text-primary">
          {{ track.title }}
        </v-list-item-title>
        <v-list-item-subtitle>{{ track.chapters.length }} chapters</v-list-item-subtitle>
      </v-list-item>

      <v-divider
        v-if="coursesStore.tracks.length"
        class="my-2"
      />

      <template
        v-for="track in coursesStore.tracks"
        :key="`track-${track.key}`"
      >
        <template
          v-for="chapter in track.chapters"
          :key="`chapter-${track.key}-${chapter.key}`"
        >
          <v-expansion-panels
            v-model="openChapters"
            :multiple="true"
            class="mb-2"
          >
            <v-expansion-panel :value="`chapter-${track.key}-${chapter.key}`">
              <v-expansion-panel-title>
                <v-icon start>
                  {{ chapterIcon(chapter) }}
                </v-icon>
                {{ chapter.title }}
                <v-chip
                  v-if="getCompletedCount(chapter) > 0"
                  size="x-small"
                  color="success"
                  class="ms-auto"
                >
                  {{ getCompletedCount(chapter) }}/{{ chapter.lessons.length }}
                </v-chip>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="pb-0">
                <v-list
                  lines="one"
                  density="compact"
                  nav
                >
                  <v-list-item
                    v-for="lesson in chapter.lessons"
                    :key="lesson.slug"
                    :to="{ name: 'lesson', params: { slug: lesson.slug } }"
                    :class="[
                      'px-2',
                      { 'bg-primary-lighten-5': isCurrentLesson(lesson.slug) },
                      { 'text-primary': isCurrentLesson(lesson.slug) },
                    ]"
                    exact
                  >
                    <v-icon
                      :icon="getLessonIcon(lesson)"
                      :class="[
                        'me-2',
                        { 'text-success': lesson.completed, 'text-primary': isCurrentLesson(lesson.slug) },
                      ]"
                    />
                    <v-list-item-title class="text-truncate">
                      {{ lesson.title }}
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </template>
      </template>
    </v-list>

    <v-divider
      v-if="authStore.isAuthenticated"
      class="my-3"
    />

    <v-list
      v-if="authStore.isAuthenticated"
      nav
      density="compact"
      lines="one"
    >
      <v-list-item
        to="/pipelines"
        exact
      >
        <v-icon start>
          mdi-pipe
        </v-icon>
        <v-list-item-title>Data Pipelines</v-list-item-title>
      </v-list-item>
      <v-list-item
        to="/pipelines/new"
        exact
      >
        <v-icon start>
          mdi-plus-circle
        </v-icon>
        <v-list-item-title>Create Pipeline</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-sheet>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesStore } from '../stores/courses'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()
const authStore = useAuthStore()

const searchQuery = ref('')
const openChapters = ref([])

function onSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'search', query: { q: searchQuery.value } })
  }
}

function isCurrentLesson(slug) {
  return route.params.slug === slug
}

function chapterIcon(chapter) {
  const icons = {
    'getting-started': 'mdi-rocket-launch',
    'variables-and-types': 'mdi-alpha',
    'control-flow': 'mdi-sitemap',
    'functions': 'mdi-function',
    'data-structures': 'mdi-array',
    'oop': 'mdi-cube-outline',
    'modules-packages': 'mdi-package-variant',
    'file-io': 'mdi-file-document',
    'error-handling': 'mdi-alert-circle-outline',
    'testing': 'mdi-check-circle-outline',
    'async': 'mdi-clock-fast',
    'decorators': 'mdi-star-outline',
    'generators': 'mdi-sync',
    'context-managers': 'mdi-bracket-curly',
    'type-hints': 'mdi-tag-outline',
    'metaprogramming': 'mdi-code-braces',
    'performance': 'mdi-speedometer',
    'web-basics': 'mdi-web',
    'routing': 'mdi-map-marker-path',
    'pydantic': 'mdi-shield-check',
    'database': 'mdi-database',
    'auth': 'mdi-lock',
    'websockets': 'mdi-websocket',
    'testing-web': 'mdi-test-tube',
    'deployment': 'mdi-rocket',
    'numpy': 'mdi-calculator',
    'pandas': 'mdi-table',
    'visualization': 'mdi-chart-bar',
    'sklearn': 'mdi-brain',
    'pipelines': 'mdi-pipe',
    'model-deployment': 'mdi-server',
    'time-series': 'mdi-chart-timeline',
    'final-project': 'mdi-trophy',
  }
  return icons[chapter.key] || 'mdi-book-open-page-variant'
}

function getLessonIcon(lesson) {
  if (lesson.completed) return 'mdi-check-circle'
  return 'mdi-circle-outline'
}

function getCompletedCount(chapter) {
  return chapter.lessons.filter((l) => l.completed).length
}
</script>

<style scoped>
.code-block-wrapper {
  border-radius: 8px;
  overflow: hidden;
  margin: 16px 0;
}
.code-block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
.dark .code-block-header {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.code-language {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--v-text-medium-emphasis);
}
.copy-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--v-text-medium-emphasis);
  border-radius: 4px;
  transition: background 0.2s;
}
.copy-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}
.dark .copy-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}
pre.hljs {
  margin: 0;
  padding: 16px;
  border-radius: 0;
}
</style>