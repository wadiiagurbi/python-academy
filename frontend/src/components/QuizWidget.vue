<template>
  <v-card
    class="mt-6"
    elevation="0"
    variant="outlined"
  >
    <v-card-title class="text-h6">
      <v-icon start>
        mdi-quiz
      </v-icon>
      Mini Quiz
    </v-card-title>

    <v-card-text>
      <div
        v-if="!submitted"
        class="space-y-4"
      >
        <div
          v-for="(question, qIndex) in questions"
          :key="qIndex"
          class="quiz-question"
        >
          <p class="text-body-1 font-weight-medium mb-3">
            {{ qIndex + 1 }}. {{ question.question }}
          </p>
          <v-radio-group
            v-model="answers[qIndex]"
            mandatory
          >
            <v-radio
              v-for="(option, oIndex) in question.options"
              :key="oIndex"
              :label="option"
              :value="oIndex"
              class="d-block mb-2"
            />
          </v-radio-group>
        </div>

        <v-btn
          color="primary"
          class="mt-4"
          @click="submitQuiz"
        >
          Submit Quiz
        </v-btn>
      </div>

      <div
        v-else
        class="space-y-4"
      >
        <v-alert
          :type="scorePercentage === 100 ? 'success' : scorePercentage >= 70 ? 'info' : 'warning'"
          variant="tonal"
        >
          <strong>Score: {{ score }}/{{ questions.length }} ({{ scorePercentage }}%)</strong>
        </v-alert>

        <div
          v-for="(question, qIndex) in questions"
          :key="qIndex"
          class="quiz-result"
        >
          <div class="d-flex align-center mb-2">
            <v-icon
              :icon="results[qIndex].is_correct ? 'mdi-check-circle' : 'mdi-close-circle'"
              :color="results[qIndex].is_correct ? 'success' : 'error'"
              class="me-2"
            />
            <span class="font-weight-medium">{{ qIndex + 1 }}. {{ question.question }}</span>
          </div>
          <div class="ml-6 space-y-1">
            <div
              v-for="(option, oIndex) in question.options"
              :key="oIndex"
              class="text-body-2"
            >
              <span :class="getOptionClass(oIndex, qIndex)">
                {{ oIndex === results[qIndex].selected ? '→ ' : '  ' }}{{ option }}
              </span>
            </div>
            <div class="text-caption text-medium-emphasis mt-1 ml-6">
              {{ question.explanation || results[qIndex].explanation }}
            </div>
          </div>
          <v-divider
            v-if="qIndex < questions.length - 1"
            class="my-3"
          />
        </div>

        <v-btn
          variant="outlined"
          class="mt-4"
          @click="resetQuiz"
        >
          Try Again
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/client'

const props = defineProps({
  lessonSlug: { type: String, required: true },
  questions: { type: Array, required: true },
})

const route = useRoute()
const submitted = ref(false)
const answers = ref([])
const results = ref([])
const score = ref(0)

const scorePercentage = computed(() => Math.round((score.value / props.questions.length) * 100))

async function submitQuiz() {
  if (answers.value.some((a) => a === undefined)) {
    return
  }

  try {
    const response = await api.post(`/quizzes/${props.lessonSlug}/attempt`, {
      answers: answers.value,
    })
    results.value = response.data.results
    score.value = response.data.score
    submitted.value = true
  } catch (e) {
    console.error('Quiz submission failed:', e)
  }
}

function resetQuiz() {
  submitted.value = false
  answers.value = []
  results.value = []
  score.value = 0
}

function getOptionClass(optionIndex, questionIndex) {
  const result = results.value[questionIndex]
  if (!result) return ''

  if (optionIndex === result.correct) return 'text-success font-weight-medium'
  if (optionIndex === result.selected) return 'text-error'
  return ''
}
</script>

<style scoped>
.quiz-question {
  padding: 16px;
  background: var(--v-theme-surface-variant);
  border-radius: 8px;
  border: 1px solid var(--v-border-color);
}
.quiz-result {
  padding: 12px;
  background: var(--v-theme-surface-variant);
  border-radius: 8px;
}
.space-y-4 > * + * {
  margin-top: 1rem;
}
.space-y-1 > * + * {
  margin-top: 0.25rem;
}
</style>