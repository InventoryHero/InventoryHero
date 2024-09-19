<script setup lang="ts">

const {
  text
} = defineProps<{
  text?: string
}>()

</script>

<template>
  <v-row
      dense
      class="pb-4 pt-2 ps-2 pe-2 text-center"
      justify="center"

  >
    <slot>
      {{ text }}
    </slot>
  </v-row>
</template>

<style scoped lang="scss">

</style>