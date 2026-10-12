<template>
  <v-card
    class="h-100"
    elevation="0"
    variant="outlined"
  >
    <v-card-title class="pb-2">
      {{ chartData?.type || 'Chart' }}
    </v-card-title>
    <v-card-text class="pa-2">
      <div
        class="chart-container"
        :style="{ height: `${height}px` }"
      >
        <canvas ref="canvasRef" />
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  chartData: { type: Object, required: true },
  height: { type: Number, default: 300 },
})

const canvasRef = ref(null)
const chartInstance = ref(null)

function createChart() {
  if (!canvasRef.value || !props.chartData) return

  const ctx = canvasRef.value.getContext('2d')
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  const data = props.chartData.data || {}
  const chartType = props.chartData.type || 'bar'

  chartInstance.value = new Chart(ctx, {
    type: chartType,
    data: {
      labels: data.labels || [],
      datasets: data.datasets || [
        {
          label: 'Data',
          data: data.values || [],
          backgroundColor: 'rgba(37, 99, 235, 0.6)',
          borderColor: 'rgb(37, 99, 235)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: chartType !== 'bar' },
      },
      scales: chartType !== 'pie' && chartType !== 'doughnut' ? {
        y: { beginAtZero: true },
      } : {},
    },
  })
}

onMounted(() => {
  nextTick(createChart)
})

watch(() => props.chartData, createChart, { deep: true })

onUnmounted(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
    chartInstance.value = null
  }
})
</script>