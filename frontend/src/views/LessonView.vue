<template>
  <div
    v-if="loading"
    class="text-center py-16"
  >
    <v-progress-circular
      indeterminate
      color="primary"
      size="80"
    />
  </div>

  <v-container
    v-else
    fluid
    class="pa-0"
  >
    <v-row
      class="mb-4"
      dense
    >
      <v-col cols="12">
        <v-breadcrumbs
          :items="breadcrumbs"
          divider="mdi-chevron-right"
          class="mb-2"
        />
        <h1 class="text-h4 font-weight-bold mb-1">
          {{ lesson?.title }}
        </h1>
        <div class="d-flex flex-wrap gap-3 text-caption text-medium-emphasis">
          <v-chip
            size="x-small"
            variant="tonal"
            :color="difficultyColor"
          >
            {{ difficultyLabel }}
          </v-chip>
          <v-chip
            size="x-small"
            variant="tonal"
          >
            {{ lesson?.estimated_minutes }} min
          </v-chip>
          <v-chip
            size="x-small"
            variant="tonal"
          >
            {{ lesson?.chapter_title }}
          </v-chip>
        </div>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col
        cols="12"
        lg="9"
      >
        <v-card
          variant="outlined"
          class="pa-6"
        >
          <div class="d-flex justify-space-between mb-4">
            <div>
              <v-btn
                variant="text"
                :disabled="completed"
                @click="markComplete"
              >
                <v-icon start>
                  {{ completed ? 'mdi-check-circle' : 'mdi-check' }}
                </v-icon>
                {{ completed ? 'Completed' : 'Mark Complete' }}
              </v-btn>
            </div>
            <div class="d-flex gap-2">
              <v-btn
                variant="text"
                :to="prevLesson"
                :disabled="!prevLesson"
                size="small"
              >
                <v-icon start>
                  mdi-chevron-left
                </v-icon> Previous
              </v-btn>
              <v-btn
                variant="text"
                :to="nextLesson"
                :disabled="!nextLesson"
                size="small"
              >
                Next <v-icon end>
                  mdi-chevron-right
                </v-icon>
              </v-btn>
            </div>
          </div>

          <MarkdownContent :content="lesson?.sections?.learning_objective" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.explanation" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.why_it_matters" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.example" />
          <v-divider class="my-4" />
          <CodeBlock
            :code="lesson?.sections?.code"
            :language="lesson?.sections?.code_language"
          />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.code_explanation" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.common_mistakes" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.best_practices" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.exercise" />
          <v-divider class="my-4" />
          <MarkdownContent :content="lesson?.sections?.solution" />

          <QuizWidget
            v-if="lesson?.quiz?.length"
            :lesson-slug="slug"
            :questions="lesson.quiz"
          />
        </v-card>
      </v-col>

      <v-col
        cols="12"
        lg="3"
      >
        <AppSidebar />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCoursesStore } from '../stores/courses'
import { useProgressStore } from '../stores/progress'
import { useAuthStore } from '../stores/auth'
import MarkdownContent from '../components/MarkdownContent.vue'
import CodeBlock from '../components/CodeBlock.vue'
import QuizWidget from '../components/QuizWidget.vue'
import AppSidebar from '../components/AppSidebar.vue'

const route = useRoute()
const router = useRouter()
const coursesStore = useCoursesStore()
const progressStore = useProgressStore()
const authStore = useAuthStore()

const slug = computed(() => route.params.slug)
const loading = ref(true)
const lesson = ref(null)
const completed = ref(false)

const breadcrumbs = computed(() => [
  { title: 'Courses', to: '/courses' },
  { title: lesson.value?.track_title, to: `/courses?track=${lesson.value?.track}` },
  { title: lesson.value?.chapter_title, disabled: true },
  { title: lesson.value?.title, disabled: true },
])

const prevLesson = computed(() => {
  if (!lesson.value?.navigation?.previous) return null
  return { name: 'lesson', params: { slug: lesson.value.navigation.previous.slug } }
})

const nextLesson = computed(() => {
  if (!lesson.value?.navigation?.next) return null
  return { name: 'lesson', params: { slug: lesson.value.navigation.next.slug } }
})

const difficultyColor = computed(() => {
  const colors = { beginner: 'success', intermediate: 'warning', advanced: 'error' }
  return colors[lesson.value?.difficulty] || 'primary'
})

const difficultyLabel = computed(() => {
  const labels = { beginner: 'Beginner', intermediate: 'Intermediate', advanced: 'Advanced' }
  return labels[lesson.value?.difficulty] || lesson.value?.difficulty
})

async function loadLesson() {
  loading.value = true
  try {
    lesson.value = await coursesStore.fetchLesson(slug.value)
    if (authStore.isAuthenticated) {
      completed.value = lesson.value.sections?.completed || false
    }
  } catch (e) {
    console.error('Lesson load failed:', e)
    router.push({ name: 'not-found' })
  } finally {
    loading.value = false
  }
}

async function markComplete() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  try {
    await progressStore.markComplete(slug.value)
    completed.value = true
    coursesStore.setCompleted(slug.value)
  } catch (e) {
    console.error('Mark complete failed:', e)
  }
}

onMounted(loadLesson)

watch(() => route.params.slug, (newSlug) => {
  if (newSlug) loadLesson()
})
</script>