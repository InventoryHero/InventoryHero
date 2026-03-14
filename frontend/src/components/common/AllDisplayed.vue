<script setup lang="ts">
  const {
    title,
    icon = 'mdi-check-circle-outline',
    color = 'success'
  } = defineProps<{
    title?: string
    icon?: string
    color?: string
  }>()
</script>

<template>
  <v-sheet
    color="transparent"
    class="text-center pa-4"
  >
    <v-icon
      :icon="icon"
      :color="color"
      size="x-large"
      class="mb-2"
    />
    <p class="text-medium-emphasis">
      {{ title }}
    </p>
  </v-sheet>
</template>

<style scoped lang="scss"></style>
