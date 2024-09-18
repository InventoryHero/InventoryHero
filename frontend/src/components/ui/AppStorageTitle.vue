<script setup lang="ts">
defineOptions({
  inheritAttrs: false
})

const {
  icon,
  title="",
} = defineProps<{
  icon?: string,
  title?: string
}>()
</script>

<template>
  <v-card
    density="compact"
    max-width="100%"
    width="fit-content"
    v-bind="$attrs"
    class="pa-0 ma-0"
  >
    <v-card-text
      class="pb-1 pt-1 d-flex align-center"
    >
      <v-icon
        :icon="icon"
        size="small"
      />
      <span
        v-if="title"
        class="ms-2 d-inline-block text-truncate"
      >
        {{ title }}
    </span>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">
</style>