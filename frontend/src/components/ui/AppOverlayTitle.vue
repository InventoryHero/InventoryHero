<script setup lang="ts">

const {styling} = useAppStyling()
const text = defineModel<string>()

const {edit=false} = defineProps<{
  edit?: boolean
}>()
</script>

<template>
  <v-text-field
    v-if="edit"
    density="compact"
    hide-details="auto"
    v-model="text"
    v-bind="{
      ...styling,
      ...$attrs
    }"
  >

  </v-text-field>
  <template v-else>
    {{ text }}
  </template>
</template>

<style scoped lang="scss">

</style>