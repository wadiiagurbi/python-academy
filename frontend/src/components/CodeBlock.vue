<template>
  <div class="code-block-wrapper">
    <div class="code-block-header">
      <span class="code-language">{{ language }}</span>
      <button
        class="copy-btn"
        :title="copied ? 'Copied!' : 'Copy to clipboard'"
        @click="copyCode"
      >
        <svg
          v-if="!copied"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <rect
            x="9"
            y="9"
            width="13"
            height="13"
            rx="2"
            ry="2"
          />
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
        </svg>
        <svg
          v-else
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="20 6 9 17 4 12" />
        </svg>
      </button>
    </div>
    <pre class="hljs"><code
:class="'language-' + language"
                            v-html="highlightedCode"
    /></pre>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import hljs from 'highlight.js'

const props = defineProps({
  code: { type: String, required: true },
  language: { type: String, default: 'python' },
})

const copied = ref(false)
const highlightedCode = computed(() => {
  if (props.language && hljs.getLanguage(props.language)) {
    try {
      return hljs.highlight(props.code, { language: props.language }).value
    } catch {
      return hljs.highlightAuto(props.code).value
    }
  }
  return hljs.highlightAuto(props.code).value
})

async function copyCode() {
  await navigator.clipboard.writeText(props.code)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}

onMounted(() => {
  hljs.highlightAll()
})
</script>

<style scoped>
.code-block-wrapper {
  border-radius: 8px;
  overflow: hidden;
  margin: 16px 0;
  background: var(--v-theme-surface);
  border: 1px solid var(--v-border-color);
}
.code-block-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--v-theme-surface-variant);
  border-bottom: 1px solid var(--v-border-color);
}
.code-language {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--v-text-medium-emphasis);
}
.copy-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--v-text-medium-emphasis);
  border-radius: 4px;
  transition: all 0.2s;
}
.copy-btn:hover {
  background: var(--v-theme-surface-container);
  color: var(--v-text-high-emphasis);
}
pre.hljs {
  margin: 0;
  padding: 16px;
  border-radius: 0;
  overflow-x: auto;
}
</style>