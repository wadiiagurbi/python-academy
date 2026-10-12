import { defineStore } from 'pinia'
import api from '../api/client'

export const useCoursesStore = defineStore('courses', {
  state: () => ({
    tracks: [],
    currentLesson: null,
    searchResults: [],
    loading: false,
    error: null,
  }),

  getters: {
    allLessons: (state) => {
      const lessons = []
      for (const track of state.tracks) {
        for (const chapter of track.chapters) {
          lessons.push(...chapter.lessons)
        }
      }
      return lessons
    },

    getLessonBySlug: (state) => (slug) => {
      return state.allLessons.find((l) => l.slug === slug)
    },

    nextLesson: (state) => (slug) => {
      const lessons = state.allLessons
      const index = lessons.findIndex((l) => l.slug === slug)
      return index >= 0 && index < lessons.length - 1 ? lessons[index + 1] : null
    },

    prevLesson: (state) => (slug) => {
      const lessons = state.allLessons
      const index = lessons.findIndex((l) => l.slug === slug)
      return index > 0 ? lessons[index - 1] : null
    },
  },

  actions: {
    async fetchCourses() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/courses')
        this.tracks = response.data
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },

    async fetchLesson(slug) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get(`/courses/lessons/${slug}`)
        this.currentLesson = response.data
        return response.data
      } catch (e) {
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    },

    async search(query) {
      if (!query.trim()) {
        this.searchResults = []
        return this.searchResults
      }
      this.loading = true
      try {
        const response = await api.get('/courses/search', { params: { q: query } })
        this.searchResults = response.data
        return response.data
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },

    setCompleted(slug) {
      for (const track of this.tracks) {
        for (const chapter of track.chapters) {
          const lesson = chapter.lessons.find((l) => l.slug === slug)
          if (lesson) {
            lesson.completed = true
            // Recompute chapter.completed
            chapter.completed = chapter.lessons.every((l) => l.completed)
            return
          }
        }
      }
    },

    setIncomplete(slug) {
      for (const track of this.tracks) {
        for (const chapter of track.chapters) {
          const lesson = chapter.lessons.find((l) => l.slug === slug)
          if (lesson) {
            lesson.completed = false
            return
          }
        }
      }
    },
  },
})