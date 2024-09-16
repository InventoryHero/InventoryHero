<script setup lang="ts">
defineOptions({
  inheritAttrs: false
})

</script>

<template>
  <v-btn
      v-bind="{
        variant: 'plain',
        density: 'compact',
        ...$attrs
      }"
      :ripple="false"
  />
</template>

<style scoped lang="scss">

</style>