<template>
  <v-container
    fluid
    class="pa-0"
  >
    <v-row
      v-if="authStore.isAuthenticated"
      class="mb-6"
    >
      <v-col
        v-for="stat in stats"
        :key="stat.label"
        cols="12"
        md="3"
      >
        <v-card
          variant="tonal"
          class="pa-4 text-center"
        >
          <v-icon
            :color="stat.color"
            size="x-large"
            class="mb-2"
          >
            {{ stat.icon }}
          </v-icon>
          <div class="text-h4 font-weight-bold">
            {{ stat.value }}
          </div>
          <div class="text-caption text-medium-emphasis">
            {{ stat.label }}
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-if="authStore.isAuthenticated"
      dense
      class="mb-6"
    >
      <v-col
        cols="12"
        md="8"
      >
        <v-card variant="outlined">
          <v-card-title class="d-flex justify-space-between">
            <span>Continue Learning</span>
            <v-btn
              variant="text"
              to="/courses"
            >
              View All
            </v-btn>
          </v-card-title>
          <v-card-text class="pt-0">
            <v-list
              v-if="nextLessons.length"
              lines="two"
              density="compact"
            >
              <v-list-item
                v-for="lesson in nextLessons"
                :key="lesson.slug"
                :to="{ name: 'lesson', params: { slug: lesson.slug } }"
              >
                <v-icon
                  :color="lesson.completed ? 'success' : 'primary'"
                  class="me-3"
                >
                  {{ lesson.completed ? 'mdi-check-circle' : 'mdi-play-circle' }}
                </v-icon>
                <div>
                  <v-list-item-title>{{ lesson.title }}</v-list-item-title>
                  <v-list-item-subtitle>{{ lesson.chapter_title }} · {{ lesson.estimated_minutes }} min</v-list-item-subtitle>
                </div>
              </v-list-item>
            </v-list>
            <div
              v-else
              class="text-center py-8 text-medium-emphasis"
            >
              <v-icon
                size="large"
                class="mb-2"
              >
                mdi-school
              </v-icon>
              <p>
                No lessons started yet. <router-link
                  to="/courses"
                  class="text-primary"
                >
                  Browse courses
                </router-link>
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col
        cols="12"
        md="4"
      >
        <v-card
          variant="outlined"
          class="h-100"
        >
          <v-card-title class="d-flex justify-space-between">
            <span>Quiz Stats</span>
            <v-btn
              variant="text"
              size="small"
            >
              View All
            </v-btn>
          </v-card-title>
          <v-card-text class="pt-0">
            <v-list
              lines="one"
              density="compact"
            >
              <v-list-item>
                <v-list-item-title>Total Attempts</v-list-item-title>
                <v-list-item-subtitle>{{ quizStats.total_attempts || 0 }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Average Score</v-list-item-title>
                <v-list-item-subtitle>{{ (quizStats.average_score || 0).toFixed(1) }}%</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Best Score</v-list-item-title>
                <v-list-item-subtitle>{{ quizStats.best_score || 0 }}%</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-if="authStore.isAuthenticated"
      dense
    >
      <v-col
        cols="12"
        md="6"
      >
        <v-card variant="outlined">
          <v-card-title class="d-flex justify-space-between">
            <span>My Pipelines</span>
            <v-btn
              variant="text"
              size="small"
              to="/pipelines/new"
            >
              <v-icon start>
                mdi-plus
              </v-icon> New
            </v-btn>
          </v-card-title>
          <v-card-text class="pt-0">
            <v-list
              v-if="recentPipelines.length"
              lines="two"
              density="compact"
            >
              <v-list-item
                v-for="pipeline in recentPipelines"
                :key="pipeline.id"
                :to="{ name: 'pipeline-detail', params: { id: pipeline.id } }"
              >
                <v-icon
                  :color="getStatusColor(pipeline.status)"
                  class="me-3"
                >
                  {{ getStatusIcon(pipeline.status) }}
                </v-icon>
                <div>
                  <v-list-item-title>{{ pipeline.name }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ pipeline.status }} · Updated {{ formatDate(pipeline.updated_at) }}
                  </v-list-item-subtitle>
                </div>
              </v-list-item>
            </v-list>
            <div
              v-else
              class="text-center py-6 text-medium-emphasis"
            >
              <v-icon
                size="large"
                class="mb-2"
              >
                mdi-pipe
              </v-icon>
              <p>
                No pipelines yet. <router-link
                  to="/pipelines/new"
                  class="text-primary"
                >
                  Create one
                </router-link>
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col
        cols="12"
        md="6"
      >
        <v-card variant="outlined">
          <v-card-title>Progress Overview</v-card-title>
          <v-card-text class="pt-0">
            <div v-if="progress.completion_percentage > 0">
              <v-progress-linear
                :model-value="progress.completion_percentage"
                color="primary"
                height="8"
                class="mb-4"
              />
              <div class="d-flex justify-space-between text-caption">
                <span>{{ progress.completion_percentage.toFixed(1) }}% Complete</span>
                <span>{{ progress.completed_lessons.length }}/{{ progress.total_lessons }} lessons</span>
              </div>
            </div>
            <div
              v-else
              class="text-center py-8 text-medium-emphasis"
            >
              <v-icon
                size="large"
                class="mb-2"
              >
                mdi-chart-donut
              </v-icon>
              <p>Start learning to see progress!</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <div
      v-else
      class="text-center py-16"
    >
      <v-icon
        size="80"
        color="primary"
        class="mb-4"
      >
        mdi-language-python
      </v-icon>
      <h2 class="text-h4 mb-3">
        Welcome to Python Academy
      </h2>
      <p class="text-body-1 text-medium-emphasis mb-6 max-w-md mx-auto">
        Create an account to track your progress, take quizzes, and build data pipelines.
      </p>
      <v-row
        justify="center"
        class="gap-4"
      >
        <v-col auto>
          <v-btn
            size="large"
            color="primary"
            to="/register"
          >
            <v-icon start>
              mdi-account-plus
            </v-icon> Sign Up Free
          </v-btn>
        </v-col>
        <v-col auto>
          <v-btn
            size="large"
            variant="outlined"
            to="/login"
          >
            <v-icon start>
              mdi-login
            </v-icon> Login
          </v-btn>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCoursesStore } from '../stores/courses'
import { usePipelineStore } from '../stores/pipeline'
import { useProgressStore } from '../stores/progress'

const authStore = useAuthStore()
const coursesStore = useCoursesStore()
const pipelineStore = usePipelineStore()
const progressStore = useProgressStore()

const progress = ref({ completion_percentage: 0, completed_lessons: [], total_lessons: 0 })
const nextLessons = ref([])
const quizStats = ref({})
const recentPipelines = ref([])

const stats = computed(() => [
  { label: 'Lessons Completed', value: progress.value.completed_lessons.length, icon: 'mdi-book-check', color: 'primary' },
  { label: 'Completion', value: `${progress.value.completion_percentage.toFixed(1)}%`, icon: 'mdi-chart-donut', color: 'success' },
  { label: 'Quiz Attempts', value: quizStats.value.total_attempts || 0, icon: 'mdi-quiz', color: 'warning' },
  { label: 'Pipelines', value: recentPipelines.value.length, icon: 'mdi-pipe', color: 'secondary' },
])

async function loadDashboard() {
  if (!authStore.isAuthenticated) return

  try {
    await Promise.all([
      progressStore.fetchProgress().catch(() => {}),
      coursesStore.tracks.length ? Promise.resolve() : coursesStore.fetchCourses().catch(() => {}),
      pipelineStore.fetchPipelines().catch(() => {}),
    ])
    progress.value = progressStore.progress
    quizStats.value = progressStore.progress.quiz_stats || {}
    recentPipelines.value = pipelineStore.pipelines.slice(0, 5)
    const all = coursesStore.allLessons || []
    const completed = new Set(progress.value.completed_lessons || [])
    const upcoming = all.filter((l) => !completed.has(l.slug)).slice(0, 5)
    nextLessons.value = upcoming.length ? upcoming : all.slice(0, 5)
  } catch (e) {
    console.error('Dashboard load failed:', e)
  }
}

function getStatusColor(status) {
  const colors = { draft: 'warning', running: 'info', completed: 'success', failed: 'error' }
  return colors[status] || 'default'
}

function getStatusIcon(status) {
  const icons = { draft: 'mdi-file-outline', running: 'mdi-play-circle', completed: 'mdi-check-circle', failed: 'mdi-close-circle' }
  return icons[status] || 'mdi-help-circle'
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString()
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await loadDashboard()
  }
})
</script>