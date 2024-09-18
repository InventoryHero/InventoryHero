<script setup lang="ts">

const search = defineModel<string>("search")
onBeforeUnmount(() => {
  console.log("DU FICKER")
})
</script>

<template>
  <div
    class="d-flex align-center"
  >
    <text-filter
        class="flex-1-1"
        v-model:filter="search"
    />

    <app-storage-qr-code-btn
    />
  </div>
</template>

<style scoped lang="scss">

</style>