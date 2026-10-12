<template>
  <v-container
    fluid
    class="pa-0"
  >
    <v-row
      class="mb-6"
      dense
    >
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">
          All Courses
        </h1>
        <p class="text-medium-emphasis">
          Explore {{ totalLessons }} lessons across {{ coursesStore.tracks.length }} learning tracks
        </p>
      </v-col>
    </v-row>

    <v-row
      v-if="coursesStore.loading"
      dense
      class="justify-center"
    >
      <v-col
        cols="12"
        class="text-center py-12"
      >
        <v-progress-circular
          indeterminate
          color="primary"
          size="60"
        />
      </v-col>
    </v-row>

    <v-row
      v-else
      dense
    >
      <v-col
        v-for="track in coursesStore.tracks"
        :key="track.key"
        cols="12"
        lg="6"
        xl="4"
      >
        <v-card
          variant="outlined"
          class="h-100"
        >
          <v-card-item>
            <v-card-title class="pb-2 d-flex justify-space-between">
              <div>
                <v-chip
                  :color="trackColor(track.key)"
                  size="x-small"
                  class="mb-2"
                >
                  {{ track.title }}
                </v-chip>
                <div class="text-h6">
                  {{ track.title }}
                </div>
              </div>
              <v-icon
                :color="trackColor(track.key)"
                size="large"
              >
                {{ trackIcon(track.key) }}
              </v-icon>
            </v-card-title>
            <v-card-subtitle>{{ track.chapters.length }} chapters · {{ totalTrackLessons(track) }} lessons</v-card-subtitle>
            <v-card-text class="pt-2">
              <v-list
                lines="one"
                density="compact"
                class="pa-0"
              >
                <v-list-item
                  v-for="chapter in track.chapters"
                  :key="chapter.key"
                >
                  <v-icon
                    :color="chapter.completed === chapter.lessons.length ? 'success' : 'primary'"
                    class="me-2"
                  >
                    {{ chapter.completed === chapter.lessons.length ? 'mdi-check-circle' : 'mdi-chevron-right' }}
                  </v-icon>
                  <v-list-item-title class="text-truncate">
                    {{ chapter.title }}
                  </v-list-item-title>
                  <v-chip
                    size="x-small"
                    variant="tonal"
                    class="ms-auto"
                  >
                    {{ chapter.lessons.length }} lessons
                  </v-chip>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-btn
                variant="text"
                :to="{ name: 'courses', params: { track: track.key } }"
              >
                View Track
              </v-btn>
              <v-spacer />
              <v-chip
                v-if="getTrackProgress(track) > 0"
                color="success"
                size="small"
              >
                {{ getTrackProgress(track) }}% complete
              </v-chip>
            </v-card-actions>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useCoursesStore } from '../stores/courses'

const coursesStore = useCoursesStore()

const totalLessons = computed(() => {
  return coursesStore.tracks.reduce((sum, track) =>
    sum + track.chapters.reduce((s, ch) => s + ch.lessons.length, 0), 0)
})

function totalTrackLessons(track) {
  return track.chapters.reduce((sum, ch) => sum + ch.lessons.length, 0)
}

function getTrackProgress(track) {
  let completed = 0
  let total = 0
  for (const chapter of track.chapters) {
    for (const lesson of chapter.lessons) {
      total++
      if (lesson.completed) completed++
    }
  }
  return total > 0 ? Math.round((completed / total) * 100) : 0
}

function trackColor(key) {
  const colors = {
    'python-fundamentals': 'blue',
    'intermediate-python': 'purple',
    'advanced-python': 'red',
    'web-development': 'green',
    'data-science': 'orange',
    'final-project': 'teal',
  }
  return colors[key] || 'primary'
}

function trackIcon(key) {
  const icons = {
    'python-fundamentals': 'mdi-alpha',
    'intermediate-python': 'mdi-cube-outline',
    'advanced-python': 'mdi-rocket',
    'web-development': 'mdi-web',
    'data-science': 'mdi-chart-line',
    'final-project': 'mdi-trophy',
  }
  return icons[key] || 'mdi-book'
}

onMounted(async () => {
  if (!coursesStore.tracks.length) {
    await coursesStore.fetchCourses()
  }
})
</script>