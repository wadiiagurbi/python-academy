<template>
  <v-container
    fluid
    class="pa-0"
  >
    <v-row
      class="mb-6"
      dense
    >
      <v-col
        cols="12"
        md="8"
      >
        <h1 class="text-h4 font-weight-bold mb-2">
          My Data Pipelines
        </h1>
        <p class="text-medium-emphasis">
          Build, manage, and execute data analysis pipelines
        </p>
      </v-col>
      <v-col
        cols="12"
        md="4"
        class="d-flex align-end"
      >
        <v-btn
          color="primary"
          to="/pipelines/new"
          class="w-100"
          size="large"
        >
          <v-icon start>
            mdi-plus-circle
          </v-icon> New Pipeline
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
      v-else-if="pipelines.length"
      dense
    >
      <v-col
        v-for="pipeline in pipelines"
        :key="pipeline.id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card
          variant="outlined"
          class="h-100"
        >
          <v-card-item>
            <v-card-title class="d-flex justify-space-between">
              <div>
                <div class="text-h6">
                  {{ pipeline.name }}
                </div>
                <v-chip
                  :color="getStatusColor(pipeline.status)"
                  size="x-small"
                >
                  {{ pipeline.status }}
                </v-chip>
              </div>
            </v-card-title>
            <v-card-subtitle>{{ pipeline.steps_count }} steps · {{ formatDate(pipeline.updated_at) }}</v-card-subtitle>
            <v-card-text
              v-if="pipeline.description"
              class="text-body-2 text-medium-emphasis"
            >
              {{ pipeline.description }}
            </v-card-text>
            <v-card-actions>
              <v-btn
                variant="text"
                :to="{ name: 'pipeline-detail', params: { id: pipeline.id } }"
              >
                Edit
              </v-btn>
              <v-btn
                v-if="pipeline.last_result"
                variant="text"
                :to="{ name: 'pipeline-results', params: { id: pipeline.id } }"
              >
                View Results
              </v-btn>
              <v-spacer />
              <v-menu>
                <template #activator="{ props }">
                  <v-btn
                    variant="text"
                    v-bind="props"
                    icon="mdi-dots-vertical"
                  />
                </template>
                <v-list>
                  <v-list-item @click="executePipeline(pipeline.id)">
                    <v-list-item-title>
                      <v-icon start>
                        mdi-play-circle
                      </v-icon> Execute
                    </v-list-item-title>
                  </v-list-item>
                  <v-list-item @click="duplicatePipeline(pipeline)">
                    <v-list-item-title>
                      <v-icon start>
                        mdi-content-copy
                      </v-icon> Duplicate
                    </v-list-item-title>
                  </v-list-item>
                  <v-divider />
                  <v-list-item
                    color="error"
                    @click="confirmDelete(pipeline.id)"
                  >
                    <v-list-item-title>
                      <v-icon start>
                        mdi-delete
                      </v-icon> Delete
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-card-actions>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-else
      dense
    >
      <v-col
        cols="12"
        class="text-center py-16"
      >
        <v-icon
          size="80"
          class="mb-4 text-medium-emphasis"
        >
          mdi-pipe
        </v-icon>
        <h3 class="text-h6 mb-2">
          No Pipelines Yet
        </h3>
        <p class="text-medium-emphasis mb-6">
          Create your first data analysis pipeline
        </p>
        <v-btn
          color="primary"
          to="/pipelines/new"
          size="large"
        >
          <v-icon start>
            mdi-plus-circle
          </v-icon> Create Pipeline
        </v-btn>
      </v-col>
    </v-row>

    <v-dialog
      v-model="showDeleteDialog"
      max-width="400"
    >
      <v-card>
        <v-card-title>Delete Pipeline</v-card-title>
        <v-card-text>Are you sure you want to delete this pipeline? This action cannot be undone.</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showDeleteDialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="error"
            :loading="deleting"
            @click="deletePipeline"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePipelineStore } from '../stores/pipeline'

const router = useRouter()
const pipelineStore = usePipelineStore()

const pipelines = computed(() => pipelineStore.pipelines)
const loading = ref(false)
const showDeleteDialog = ref(false)
const deleting = ref(false)
const pipelineToDelete = ref(null)

function getStatusColor(status) {
  const colors = { draft: 'warning', running: 'info', completed: 'success', failed: 'error' }
  return colors[status] || 'default'
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString()
}

async function loadPipelines() {
  loading.value = true
  try {
    await pipelineStore.fetchPipelines()
  } catch (e) {
    console.error('Load pipelines failed:', e)
  } finally {
    loading.value = false
  }
}

async function executePipeline(id) {
  try {
    await pipelineStore.executePipeline(id)
    router.push({ name: 'pipeline-results', params: { id } })
  } catch (e) {
    console.error('Execute failed:', e)
  }
}

async function duplicatePipeline(pipeline) {
  try {
    await pipelineStore.createPipeline({
      name: `${pipeline.name} (Copy)`,
      description: pipeline.description,
      config: pipeline.config,
    })
  } catch (e) {
    console.error('Duplicate failed:', e)
  }
}

function confirmDelete(id) {
  pipelineToDelete.value = id
  showDeleteDialog.value = true
}

async function deletePipeline() {
  if (!pipelineToDelete.value) return
  deleting.value = true
  try {
    await pipelineStore.deletePipeline(pipelineToDelete.value)
    showDeleteDialog.value = false
  } catch (e) {
    console.error('Delete failed:', e)
  } finally {
    deleting.value = false
    pipelineToDelete.value = null
  }
}

onMounted(loadPipelines)
</script>