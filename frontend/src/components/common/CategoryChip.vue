<script setup lang="ts">
import {CategoryReadSchema} from "@/api/types/items.ts";

const {
  category
} = defineProps<{
  category: CategoryReadSchema
}>()
</script>

<template>
  <v-chip
      density="compact"
      size="small"
      :text="category.name"
      variant="tonal"
      color="primary"
  />
</template>

<style scoped lang="scss">

</style>