import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDark: false,
  }),

  actions: {
    init() {
      const saved = localStorage.getItem('theme')
      if (saved) {
        this.isDark = saved === 'dark'
      } else if (typeof window !== 'undefined' && window.matchMedia) {
        this.isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      this.applyDom()
    },

    toggle() {
      this.isDark = !this.isDark
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light')
      this.applyDom()
    },

    applyDom() {
      if (typeof document !== 'undefined') {
        document.documentElement.classList.toggle('dark', this.isDark)
      }
    },
  },
})