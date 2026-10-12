import { defineStore } from 'pinia'
import api from '../api/client'

export const useProgressStore = defineStore('progress', {
  state: () => ({
    progress: {
      completed_lessons: [],
      total_lessons: 0,
      completion_percentage: 0,
      last_lesson_slug: null,
      quiz_stats: {},
    },
    loading: false,
  }),

  actions: {
    async fetchProgress() {
      this.loading = true
      try {
        const response = await api.get('/progress')
        this.progress = response.data
      } catch (e) {
        console.error('Fetch progress failed:', e)
      } finally {
        this.loading = false
      }
    },

    async markComplete(slug) {
      await api.post(`/progress/lessons/${slug}/complete`)
      if (!this.progress.completed_lessons.includes(slug)) {
        this.progress.completed_lessons.push(slug)
        this.progress.completion_percentage =
          (this.progress.completed_lessons.length / this.progress.total_lessons) * 100
      }
      this.progress.last_lesson_slug = slug
    },

    async markIncomplete(slug) {
      await api.delete(`/progress/lessons/${slug}/complete`)
      this.progress.completed_lessons = this.progress.completed_lessons.filter((s) => s !== slug)
      this.progress.completion_percentage =
        (this.progress.completed_lessons.length / this.progress.total_lessons) * 100
    },
  },
})