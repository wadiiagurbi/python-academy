<template>
  <v-card
    class="d-flex flex-column"
    elevation="0"
    variant="outlined"
    :class="step.color"
  >
    <v-card-title class="pb-1 d-flex justify-space-between align-center">
      <div class="d-flex align-center">
        <v-icon
          :color="step.color"
          class="me-1"
        >
          {{ step.icon }}
        </v-icon>
        <span class="font-weight-medium">{{ step.name }}</span>
      </div>
      <div class="d-flex gap-1">
        <v-btn
          icon
          size="x-small"
          :disabled="isFirst"
          :title="'Move Up'"
          @click="$emit('move-up')"
        >
          <v-icon>mdi-chevron-up</v-icon>
        </v-btn>
        <v-btn
          icon
          size="x-small"
          :disabled="isLast"
          :title="'Move Down'"
          @click="$emit('move-down')"
        >
          <v-icon>mdi-chevron-down</v-icon>
        </v-btn>
        <v-btn
          icon
          size="x-small"
          :title="'Configure'"
          @click="$emit('configure')"
        >
          <v-icon>mdi-cog</v-icon>
        </v-btn>
        <v-btn
          icon
          size="x-small"
          color="error"
          :title="'Remove'"
          @click="$emit('remove')"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </div>
    </v-card-title>
    <v-card-text class="pt-0 pb-2">
      <v-chip
        :color="step.color"
        size="x-small"
        variant="tonal"
      >
        {{ step.type }}
      </v-chip>
      <div class="mt-2 text-caption text-medium-emphasis">
        {{ getConfigSummary(step.config) }}
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
defineProps({
  step: { type: Object, required: true },
  index: { type: Number, required: true },
  isFirst: { type: Boolean, default: false },
  isLast: { type: Boolean, default: false },
})

defineEmits(['remove', 'move-up', 'move-down', 'configure'])

function getConfigSummary(config) {
  if (!config) return 'No configuration'
  const keys = Object.keys(config).filter((k) => config[k] !== '' && config[k] !== null)
  if (keys.length === 0) return 'Default settings'
  return keys.slice(0, 3).map((k) => `${k}: ${config[k]}`).join(', ') + (keys.length > 3 ? '...' : '')
}
</script>