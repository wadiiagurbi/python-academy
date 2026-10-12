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
        <v-text-field
          v-model="pipelineName"
          label="Pipeline Name"
          placeholder="e.g., Customer Churn Analysis"
          prepend-icon="mdi-pipe"
          class="mb-2"
        />
        <v-textarea
          v-model="pipelineDescription"
          label="Description"
          placeholder="Describe what this pipeline does..."
          rows="2"
        />
      </v-col>
      <v-col
        cols="12"
        md="4"
        class="d-flex align-end"
      >
        <v-btn
          color="primary"
          :loading="saving"
          class="w-100"
          @click="savePipeline"
        >
          <v-icon start>
            mdi-content-save
          </v-icon> Save Pipeline
        </v-btn>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col
        cols="12"
        lg="4"
      >
        <v-card
          class="h-100"
          elevation="0"
          variant="outlined"
        >
          <v-card-title class="pb-2">
            <v-icon start>
              mdi-folder-multiple
            </v-icon>
            Pipeline Steps
          </v-card-title>
          <v-card-text class="pa-2">
            <v-list
              lines="two"
              density="compact"
            >
              <v-list-item
                v-for="(step, index) in availableSteps"
                :key="step.type"
                draggable
                class="cursor-move pa-2 hover:bg-surface-variant rounded"
                @dragstart="onDragStart($event, step, index)"
              >
                <v-icon
                  :color="step.color"
                  class="me-2"
                >
                  {{ step.icon }}
                </v-icon>
                <div>
                  <v-list-item-title>{{ step.label }}</v-list-item-title>
                  <v-list-item-subtitle>{{ step.description }}</v-list-item-subtitle>
                </div>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col
        cols="12"
        lg="8"
      >
        <v-card
          class="h-100"
          elevation="0"
          variant="outlined"
          @dragover.prevent
          @drop="onDrop"
        >
          <v-card-title class="pb-2 d-flex justify-space-between">
            <span>
              <v-icon start>mdi-account-tree</v-icon>
              Pipeline Flow
            </span>
            <v-chip
              v-if="pipelineSteps.length"
              size="small"
              color="primary"
            >
              {{ pipelineSteps.length }} steps
            </v-chip>
          </v-card-title>
          <v-card-text class="pa-2 min-h-[400px]">
            <div
              v-if="pipelineSteps.length === 0"
              class="text-center pa-12 text-medium-emphasis"
            >
              <v-icon
                size="x-large"
                class="mb-2"
              >
                mdi-pipe-disconnected
              </v-icon>
              <p>Drag steps here to build your pipeline</p>
            </div>

            <v-row
              v-else
              dense
              class="gx-2 gy-2"
            >
              <v-col
                v-for="(step, index) in pipelineSteps"
                :key="`step-${index}`"
                cols="12"
                md="6"
                lg="4"
              >
                <PipelineStepCard
                  :step="step"
                  :index="index"
                  :is-first="index === 0"
                  :is-last="index === pipelineSteps.length - 1"
                  @remove="removeStep"
                  @move-up="moveStepUp"
                  @move-down="moveStepDown"
                  @configure="configureStep"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog
      v-model="showConfigDialog"
      max-width="600"
    >
      <v-card>
        <v-card-title>Configure Step: {{ configStep?.label }}</v-card-title>
        <v-card-text>
          <component
            :is="resolvedConfigComponent"
            v-model="configStep.config"
            :available-columns="configStep.availableColumns"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showConfigDialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="saveStepConfig"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="showExecuteDialog"
      max-width="500"
    >
      <v-card>
        <v-card-title>Execute Pipeline</v-card-title>
        <v-card-text>
          <p class="text-body-2">
            Run the pipeline with current configuration.
          </p>
          <v-switch
            v-model="executeConfigOverride"
            label="Override with test data"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showExecuteDialog = false">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="executing"
            @click="executePipeline"
          >
            <v-icon start>
              mdi-play-circle
            </v-icon> Execute
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePipelineStore } from '../stores/pipeline'
import PipelineStepCard from './PipelineStepCard.vue'

const route = useRoute()
const router = useRouter()
const pipelineStore = usePipelineStore()

const pipelineName = ref('')
const pipelineDescription = ref('')
const pipelineSteps = ref([])
const saving = ref(false)
const executing = ref(false)
const showConfigDialog = ref(false)
const showExecuteDialog = ref(false)
const executeConfigOverride = ref(false)
const configStep = ref(null)

// Fallback component for config dialogs not yet implemented
const PlaceholderConfig = {
  props: ['modelValue', 'availableColumns'],
  setup() {
    return () => h('div', { class: 'text-medium-emphasis pa-4' }, 'Configuration panel coming soon.')
  },
}

const resolvedConfigComponent = computed(() => {
  if (!configStep.value?.configComponent) return PlaceholderConfig
  const name = configStep.value.configComponent
  // If it's already a component object, use it; otherwise fall back
  return typeof name === 'string' ? PlaceholderConfig : name
})

const availableSteps = [
  {
    type: 'ingest',
    label: 'Ingest Data',
    description: 'Load data from CSV, JSON, API, or database',
    icon: 'mdi-database-import',
    color: 'blue',
    configComponent: 'IngestConfig',
  },
  {
    type: 'clean',
    label: 'Clean Data',
    description: 'Handle missing values, outliers, type conversion',
    icon: 'mdi-broom',
    color: 'orange',
    configComponent: 'CleanConfig',
  },
  {
    type: 'transform',
    label: 'Transform',
    description: 'Feature engineering, encoding, scaling, aggregation',
    icon: 'mdi-swap-horizontal',
    color: 'purple',
    configComponent: 'TransformConfig',
  },
  {
    type: 'analyze',
    label: 'Analyze',
    description: 'Statistics, correlations, ML model training',
    icon: 'mdi-chart-line',
    color: 'green',
    configComponent: 'AnalyzeConfig',
  },
  {
    type: 'visualize',
    label: 'Visualize',
    description: 'Charts, plots, dashboards',
    icon: 'mdi-chart-bar',
    color: 'red',
    configComponent: 'VisualizeConfig',
  },
  {
    type: 'export',
    label: 'Export',
    description: 'Save results as CSV, JSON, or API endpoint',
    icon: 'mdi-export',
    color: 'teal',
    configComponent: 'ExportConfig',
  },
]

async function loadPipeline() {
  if (route.params.id) {
    const pipeline = await pipelineStore.fetchPipeline(route.params.id)
    pipelineName.value = pipeline.name
    pipelineDescription.value = pipeline.description || ''
    pipelineSteps.value = pipeline.config.steps || []
  }
}

function onDragStart(event, step, index) {
  event.dataTransfer.setData('stepType', step.type)
  event.dataTransfer.setData('stepIndex', index)
}

function onDrop(event) {
  event.preventDefault()
  const stepType = event.dataTransfer.getData('stepType')
  if (!stepType) return

  const stepDef = availableSteps.find((s) => s.type === stepType)
  if (!stepDef) return

  const newStep = {
    ...stepDef,
    id: Date.now(),
    name: stepDef.label,
    config: getDefaultConfig(stepType),
  }
  pipelineSteps.value.push(newStep)
}

function getDefaultConfig(type) {
  const defaults = {
    ingest: { source: 'sample', path: '' },
    clean: { handle_missing: 'drop', handle_outliers: false },
    transform: { operations: [] },
    analyze: { method: 'statistics', target: '' },
    visualize: { chart_type: 'bar', x: '', y: '' },
    export: { format: 'json', path: '' },
  }
  return defaults[type] || {}
}

function removeStep(index) {
  pipelineSteps.value.splice(index, 1)
}

function moveStepUp(index) {
  if (index > 0) {
    ;[pipelineSteps.value[index], pipelineSteps.value[index - 1]] = [
      pipelineSteps.value[index - 1],
      pipelineSteps.value[index],
    ]
  }
}

function moveStepDown(index) {
  if (index < pipelineSteps.value.length - 1) {
    ;[pipelineSteps.value[index], pipelineSteps.value[index + 1]] = [
      pipelineSteps.value[index + 1],
      pipelineSteps.value[index],
    ]
  }
}

function configureStep(step) {
  configStep.value = { ...step, config: { ...step.config } }
  showConfigDialog.value = true
}

function saveStepConfig() {
  const index = pipelineSteps.value.findIndex((s) => s.id === configStep.value?.id)
  if (index >= 0) {
    pipelineSteps.value[index].config = configStep.value.config
    pipelineSteps.value[index].name = configStep.value.name
  }
  showConfigDialog.value = false
}

async function savePipeline() {
  if (!pipelineName.value.trim()) return

  saving.value = true
  try {
    const config = { steps: pipelineSteps.value.map((s) => ({
      type: s.type,
      name: s.name,
      config: s.config,
    })) }

    if (route.params.id) {
      await pipelineStore.updatePipeline(route.params.id, {
        name: pipelineName.value,
        description: pipelineDescription.value,
        config,
      })
    } else {
      await pipelineStore.createPipeline({
        name: pipelineName.value,
        description: pipelineDescription.value,
        config,
      })
    }
    router.push('/pipelines')
  } catch (e) {
    console.error('Save failed:', e)
  } finally {
    saving.value = false
  }
}

async function executePipeline() {
  if (!route.params.id) {
    await savePipeline()
    if (!route.params.id) return
  }

  executing.value = true
  showExecuteDialog.value = false
  try {
    const result = await pipelineStore.executePipeline(route.params.id)
    router.push({ name: 'pipeline-results', params: { id: route.params.id } })
  } catch (e) {
    console.error('Execution failed:', e)
  } finally {
    executing.value = false
  }
}

onMounted(loadPipeline)
</script>

<style scoped>
.cursor-move { cursor: grab; }
.cursor-move:active { cursor: grabbing; }
.min-h-\[400px\] { min-height: 400px; }
</style>