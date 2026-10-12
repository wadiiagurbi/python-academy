import { defineStore } from 'pinia'
import api from '../api/client'

export const usePipelineStore = defineStore('pipeline', {
  state: () => ({
    pipelines: [],
    currentPipeline: null,
    executionResult: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchPipelines() {
      this.loading = true
      try {
        const response = await api.get('/pipelines')
        this.pipelines = response.data
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },

    async fetchPipeline(id) {
      this.loading = true
      try {
        const response = await api.get(`/pipelines/${id}`)
        this.currentPipeline = response.data
        return response.data
      } catch (e) {
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    },

    async createPipeline(data) {
      const response = await api.post('/pipelines', data)
      this.pipelines.unshift(response.data)
      return response.data
    },

    async updatePipeline(id, data) {
      const response = await api.put(`/pipelines/${id}`, data)
      const index = this.pipelines.findIndex((p) => p.id === id)
      if (index >= 0) this.pipelines[index] = response.data
      if (this.currentPipeline?.id === id) this.currentPipeline = response.data
      return response.data
    },

    async deletePipeline(id) {
      await api.delete(`/pipelines/${id}`)
      this.pipelines = this.pipelines.filter((p) => p.id !== id)
      if (this.currentPipeline?.id === id) this.currentPipeline = null
    },

    async executePipeline(id, configOverride = null) {
      this.loading = true
      try {
        const response = await api.post(`/pipelines/${id}/execute`, { config_override: configOverride })
        this.executionResult = response.data
        return response.data
      } catch (e) {
        this.error = e.message
        throw e
      } finally {
        this.loading = false
      }
    },

    setCurrentPipeline(pipeline) {
      this.currentPipeline = pipeline
    },

    clearExecutionResult() {
      this.executionResult = null
    },
  },
})