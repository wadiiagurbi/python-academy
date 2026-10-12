<template>
  <v-container
    fluid
    class="pa-0"
  >
    <section class="text-center py-16">
      <v-icon
        size="120"
        color="primary"
        class="mb-6"
      >
        mdi-language-python
      </v-icon>
      <h1 class="display-1 font-weight-bold mb-4">
        Python Academy
      </h1>
      <p class="text-h5 text-medium-emphasis mb-8 max-w-xl mx-auto">
        Learn Python from scratch to advanced. Master fundamentals, web development, data science, and build real data pipelines.
      </p>
      <v-row
        justify="center"
        class="gap-4"
      >
        <v-col auto>
          <v-btn
            size="large"
            color="primary"
            to="/register"
            class="px-8"
          >
            <v-icon start>
              mdi-school
            </v-icon> Start Learning Free
          </v-btn>
        </v-col>
        <v-col auto>
          <v-btn
            size="large"
            variant="outlined"
            to="/courses"
            class="px-8"
          >
            Browse Courses
          </v-btn>
        </v-col>
      </v-row>
    </section>

    <v-divider class="my-12" />

    <section>
      <h2 class="text-h4 font-weight-bold mb-6 text-center">
        Learning Tracks
      </h2>
      <v-row dense>
        <v-col
          v-for="track in tracks"
          :key="track.key"
          cols="12"
          md="6"
          lg="3"
        >
          <v-card
            variant="outlined"
            class="h-100 fill-height"
            to="/courses"
          >
            <v-card-item>
              <v-card-title class="pb-2">
                <v-icon
                  :color="track.color"
                  size="large"
                  class="mb-2"
                >
                  {{ track.icon }}
                </v-icon>
                <div>{{ track.title }}</div>
              </v-card-title>
              <v-card-subtitle>{{ track.chapters }} chapters · {{ track.lessons }} lessons</v-card-subtitle>
              <v-card-text class="text-body-2 text-medium-emphasis">
                {{ track.description }}
              </v-card-text>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <v-divider class="my-12" />

    <section>
      <h2 class="text-h4 font-weight-bold mb-6 text-center">
        Final Project: Data Analysis Pipeline
      </h2>
      <v-row dense>
        <v-col
          cols="12"
          md="6"
        >
          <v-card
            variant="outlined"
            class="pa-6"
          >
            <v-icon
              size="large"
              color="secondary"
              class="mb-4"
            >
              mdi-pipe
            </v-icon>
            <h3 class="text-h6 mb-3">
              Build Real Data Pipelines
            </h3>
            <p class="text-body-1 text-medium-emphasis mb-4">
              Apply everything you've learned to build production-ready data analysis pipelines. Ingest, clean, transform, analyze, visualize, and export data — all with a visual drag-and-drop builder.
            </p>
            <ul class="space-y-2 text-body-2">
              <li
                v-for="feature in pipelineFeatures"
                :key="feature"
              >
                <v-icon
                  start
                  size="small"
                >
                  mdi-check
                </v-icon> {{ feature }}
              </li>
            </ul>
          </v-card>
        </v-col>
        <v-col
          cols="12"
          md="6"
        >
          <v-card
            variant="outlined"
            class="pa-6"
          >
            <v-icon
              size="large"
              color="accent"
              class="mb-4"
            >
              mdi-chart-line
            </v-icon>
            <h3 class="text-h6 mb-3">
              Interactive Visualizations
            </h3>
            <p class="text-body-1 text-medium-emphasis mb-4">
              Create stunning charts and dashboards from your pipeline results. Bar charts, line charts, scatter plots, heatmaps — all powered by Chart.js.
            </p>
            <ul class="space-y-2 text-body-2">
              <li
                v-for="feature in vizFeatures"
                :key="feature"
              >
                <v-icon
                  start
                  size="small"
                >
                  mdi-check
                </v-icon> {{ feature }}
              </li>
            </ul>
          </v-card>
        </v-col>
      </v-row>
    </section>
  </v-container>
</template>

<script setup>
const tracks = [
  {
    key: 'python-fundamentals',
    title: 'Python Fundamentals',
    chapters: 8,
    lessons: 42,
    color: 'blue',
    icon: 'mdi-alpha',
    description: 'Variables, types, control flow, functions, data structures, I/O, errors, modules',
  },
  {
    key: 'intermediate-python',
    title: 'Intermediate Python',
    chapters: 6,
    lessons: 30,
    color: 'purple',
    icon: 'mdi-cube-outline',
    description: 'OOP, decorators, generators, context managers, testing, packaging',
  },
  {
    key: 'advanced-python',
    title: 'Advanced Python',
    chapters: 5,
    lessons: 22,
    color: 'red',
    icon: 'mdi-rocket',
    description: 'Async/await, type hints, metaprogramming, performance, C extensions',
  },
  {
    key: 'web-development',
    title: 'Web Development (FastAPI)',
    chapters: 7,
    lessons: 28,
    color: 'green',
    icon: 'mdi-web',
    description: 'Routing, Pydantic, SQLAlchemy, Auth, WebSockets, Testing, Deployment',
  },
  {
    key: 'data-science',
    title: 'Data Science & ML',
    chapters: 8,
    lessons: 35,
    color: 'orange',
    icon: 'mdi-chart-line',
    description: 'NumPy, Pandas, Visualization, Scikit-learn, Pipelines, Model Deployment, Time Series',
  },
  {
    key: 'final-project',
    title: 'Final Project: Data Pipeline',
    chapters: 1,
    lessons: 10,
    color: 'teal',
    icon: 'mdi-trophy',
    description: 'End-to-end pipeline: ingest → clean → analyze → visualize → deploy as API',
  },
]

const pipelineFeatures = [
  'Visual drag-and-drop pipeline builder',
  '6 step types: Ingest, Clean, Transform, Analyze, Visualize, Export',
  'Real execution engine with step-by-step results',
  'Configurable per-step settings',
  'Save, version, and share pipelines',
]

const vizFeatures = [
  'Bar, line, scatter, pie, heatmap charts',
  'Interactive tooltips and zoom',
  'Export charts as PNG/SVG',
  'Dashboard-style results view',
  'Real-time execution feedback',
]
</script>