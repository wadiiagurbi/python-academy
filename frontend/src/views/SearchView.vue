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
          Search Lessons
        </h1>
        <p class="text-medium-emphasis">
          Find lessons by keyword across all tracks
        </p>
      </v-col>
    </v-row>

    <v-row
      class="mb-6"
      dense
    >
      <v-col
        cols="12"
        md="8"
      >
        <v-text-field
          v-model="query"
          placeholder="Search for topics, concepts, or keywords..."
          prepend-icon="mdi-magnify"
          density="comfortable"
          variant="solo"
          class="w-100"
          @keydown.enter="search"
        />
      </v-col>
      <v-col
        cols="12"
        md="4"
      >
        <v-btn
          color="primary"
          class="w-100"
          :loading="loading"
          @click="search"
        >
          <v-icon start>
            mdi-magnify
          </v-icon> Search
        </v-btn>
      </v-col>
    </v-row>

    <v-row
      v-if="loading"
      dense
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
      v-else-if="results.length"
      dense
    >
      <v-col
        v-for="result in results"
        :key="result.lesson.slug"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card variant="outlined">
          <v-card-item>
            <v-card-title class="pb-2">
              <router-link
                :to="{ name: 'lesson', params: { slug: result.lesson.slug } }"
                class="text-decoration-none text-inherit"
              >
                {{ result.lesson.title }}
              </router-link>
            </v-card-title>
            <v-card-subtitle>{{ result.lesson.track_title }} / {{ result.lesson.chapter_title }}</v-card-subtitle>
            <v-card-text class="text-body-2 text-medium-emphasis">
              {{ result.excerpt }}
            </v-card-text>
            <v-card-actions>
              <v-btn
                variant="text"
                :to="{ name: 'lesson', params: { slug: result.lesson.slug } }"
              >
                View Lesson
              </v-btn>
            </v-card-actions>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-else-if="query.trim()"
      dense
    >
      <v-col
        cols="12"
        class="text-center py-12"
      >
        <v-icon
          size="80"
          class="mb-4 text-medium-emphasis"
        >
          mdi-magnify-off
        </v-icon>
        <p class="text-h6">
          No results found
        </p>
        <p class="text-medium-emphasis">
          Try different keywords or check spelling
        </p>
      </v-col>
    </v-row>

    <v-row
      v-else
      dense
    >
      <v-col
        cols="12"
        class="text-center py-12"
      >
        <v-icon
          size="80"
          class="mb-4 text-medium-emphasis"
        >
          mdi-magnify
        </v-icon>
        <p class="text-h6">
          Search Lessons
        </p>
        <p class="text-medium-emphasis">
          Enter a keyword to search across all course content
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCoursesStore } from '../stores/courses'

const coursesStore = useCoursesStore()

const query = ref('')
const loading = ref(false)

const results = computed(() => coursesStore.searchResults || [])

async function search() {
  if (!query.value.trim()) return
  loading.value = true
  try {
    await coursesStore.search(query.value)
  } catch (e) {
    console.error('Search failed:', e)
  } finally {
    loading.value = false
  }
}
</script>