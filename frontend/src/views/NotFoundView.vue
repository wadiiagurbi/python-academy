<template>
  <v-container class="pa-0 text-center py-16">
    <v-row justify="center">
      <v-col
        cols="12"
        md="6"
      >
        <v-icon
          size="120"
          color="error"
          class="mb-6"
        >
          mdi-alert-circle-outline
        </v-icon>
        <h1 class="display-1 font-weight-bold mb-4">
          404
        </h1>
        <h2 class="text-h4 mb-4">
          Page Not Found
        </h2>
        <p class="text-body-1 text-medium-emphasis mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <v-btn
          color="primary"
          to="/"
          size="large"
        >
          <v-icon start>
            mdi-home
          </v-icon> Go Home
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>