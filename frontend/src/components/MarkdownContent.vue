<template>
  <div
    ref="container"
    class="markdown-content"
    v-html="renderedHtml"
  />
</template>

<script setup>
import { nextTick, ref, watch, onMounted } from 'vue'
import { renderMarkdown, initCodeCopyButtons } from '../utils/markdown'

const props = defineProps({
  content: { type: String, required: true },
})

const renderedHtml = ref('')
const container = ref(null)

function render() {
  renderedHtml.value = renderMarkdown(props.content)
  nextTick(() => {
    if (container.value) {
      initCodeCopyButtons(container.value)
    }
  })
}

watch(() => props.content, render, { immediate: true })

onMounted(() => {
  render()
})
</script>

<style scoped>
.markdown-content {
  line-height: 1.7;
}
.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
  line-height: 1.3;
}
.markdown-content h1 { font-size: 2rem; }
.markdown-content h2 { font-size: 1.5rem; border-bottom: 1px solid var(--v-border-color); padding-bottom: 0.3em; }
.markdown-content h3 { font-size: 1.25rem; }
.markdown-content p { margin-bottom: 1em; }
.markdown-content ul, .markdown-content ol { margin-bottom: 1em; padding-left: 1.5em; }
.markdown-content li { margin-bottom: 0.25em; }
.markdown-content a { color: var(--v-theme-primary); text-decoration: none; }
.markdown-content a:hover { text-decoration: underline; }
.markdown-content blockquote {
  border-left: 4px solid var(--v-theme-primary);
  padding-left: 1em;
  margin: 1em 0;
  color: var(--v-text-medium-emphasis);
  font-style: italic;
}
.markdown-content code:not(pre code) {
  background: var(--v-theme-surface-variant);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}
.markdown-content pre { margin: 1em 0; }
.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}
.markdown-content th, .markdown-content td {
  border: 1px solid var(--v-border-color);
  padding: 0.5em 1em;
  text-align: left;
}
.markdown-content th { background: var(--v-theme-surface-variant); }
.markdown-content img { max-width: 100%; height: auto; border-radius: 8px; }
.markdown-content hr { border: none; border-top: 1px solid var(--v-border-color); margin: 2em 0; }
</style>