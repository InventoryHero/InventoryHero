<script setup lang="ts">
defineOptions({
  inheritAttrs: false
})

</script>

<template>
  <v-btn
      v-bind="{...$attrs}"
      variant="plain"
      density="compact"
      :ripple="false"
  />
</template>

<style scoped lang="scss">

</style>