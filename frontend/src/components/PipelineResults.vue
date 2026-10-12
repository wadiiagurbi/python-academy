<template>
  <v-container
    fluid
    class="pa-0"
  >
    <v-row class="mb-4">
      <v-col
        cols="12"
        md="8"
      >
        <v-card
          class="pa-3"
          elevation="0"
          variant="outlined"
        >
          <v-icon
            :color="executionResult?.success ? 'success' : 'error'"
            size="x-large"
            class="mb-2"
          >
            {{ executionResult?.success ? 'mdi-check-circle' : 'mdi-close-circle' }}
          </v-icon>
          <h2 class="mb-1">
            {{ pipeline?.name || 'Pipeline Results' }}
          </h2>
          <p class="text-medium-emphasis">
            {{ pipeline?.description }}
          </p>
          <v-chip
            :color="executionResult?.success ? 'success' : 'error'"
            size="small"
          >
            {{ executionResult?.success ? 'Completed' : 'Failed' }}
          </v-chip>
          <v-chip
            color="primary"
            size="small"
            class="ms-2"
          >
            {{ formatDuration(executionResult?.execution_time_ms) }}
          </v-chip>
        </v-card>
      </v-col>
      <v-col
        cols="12"
        md="4"
        class="d-flex align-end"
      >
        <v-btn
          variant="outlined"
          to="/pipelines"
        >
          <v-icon start>
            mdi-arrow-left
          </v-icon> Back to Pipelines
        </v-btn>
      </v-col>
    </v-row>

    <v-row
      v-if="executionResult?.error"
      dense
      class="mb-4"
    >
      <v-col cols="12">
        <v-alert
          type="error"
          variant="tonal"
          title="Execution Error"
        >
          {{ executionResult.error }}
        </v-alert>
      </v-col>
    </v-row>

    <v-row
      v-if="executionResult?.steps_executed?.length"
      dense
      class="mb-4"
    >
      <v-col cols="12">
        <v-card
          elevation="0"
          variant="outlined"
        >
          <v-card-title>Execution Steps</v-card-title>
          <v-card-text class="pa-0">
            <v-data-table
              :items="executionResult.steps_executed"
              :headers="stepHeaders"
              density="compact"
              hide-default-footer
            >
              <template #[`item.output_shape`]="{ item }">
                <pre class="ma-0 text-caption">{{ JSON.stringify(item.output_shape, null, 2) }}</pre>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-if="executionResult?.output?.charts?.length"
      dense
      class="mb-4"
    >
      <v-col cols="12">
        <v-card
          elevation="0"
          variant="outlined"
        >
          <v-card-title>Visualizations</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col
                v-for="(chart, index) in executionResult.output.charts"
                :key="index"
                cols="12"
                md="6"
                lg="4"
              >
                <ChartWidget
                  :chart-data="chart"
                  :height="300"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-if="executionResult?.output?.result"
      dense
      class="mb-4"
    >
      <v-col cols="12">
        <v-card
          elevation="0"
          variant="outlined"
        >
          <v-card-title>Output Data</v-card-title>
          <v-card-text>
            <pre class="bg-surface-variant p-4 rounded overflow-auto max-h-96 text-caption">
              {{ JSON.stringify(executionResult.output.result, null, 2) }}
            </pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row
      v-if="executionResult?.output?.statistics"
      dense
      class="mb-4"
    >
      <v-col cols="12">
        <v-card
          elevation="0"
          variant="outlined"
        >
          <v-card-title>Statistics</v-card-title>
          <v-card-text>
            <v-row dense>
              <v-col
                v-for="(value, key) in executionResult.output.statistics"
                :key="key"
                cols="12"
                md="6"
                lg="3"
              >
                <v-chip
                  color="primary"
                  variant="tonal"
                  size="small"
                >
                  {{ key }}: {{ value }}
                </v-chip>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { usePipelineStore } from '../stores/pipeline'
import ChartWidget from './ChartWidget.vue'

const route = useRoute()
const pipelineStore = usePipelineStore()

const pipeline = ref(null)
const executionResult = ref(null)

const stepHeaders = [
  { title: 'Step', key: 'name' },
  { title: 'Type', key: 'type' },
  { title: 'Status', key: 'success', align: 'center' },
  { title: 'Time (ms)', key: 'execution_time_ms', align: 'center' },
  { title: 'Output Shape', key: 'output_shape' },
]

function formatDuration(ms) {
  if (!ms) return 'N/A'
  if (ms < 1000) return `${ms}ms`
  return `${(ms / 1000).toFixed(2)}s`
}

async function loadData() {
  const id = route.params.id
  if (!id) return

  pipeline.value = await pipelineStore.fetchPipeline(id)
  executionResult.value = pipelineStore.executionResult
}

onMounted(loadData)

watch(() => route.params.id, (newId) => {
  if (newId) loadData()
})
</script>