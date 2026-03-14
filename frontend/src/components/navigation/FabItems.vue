<script setup lang="ts">
const fabOpen = defineModel<boolean>({
  required: true
})

const emit = defineEmits<{
  (e: 'openCreateItemModal'): void,
  (e: 'openCreateBoxModal'): void,
  (e: 'openCreateRoomModal'): void,
  (e: 'openCreateCategoryModal'): void,
}>()

</script>

<template>
  <v-speed-dial
      location="top center"
      transition="slide-x-transition"
      v-model="fabOpen"
      activator="parent"
  >
    <v-btn
      key="1"
      color="secondary"
      icon="mdi-invoice-text-plus"
      @click="emit('openCreateItemModal')"
    />
    <v-btn
        key="2"
        color="secondary"
        icon="mdi-package-variant-plus"
        @click="emit('openCreateBoxModal')"
    />
    <v-btn
        key="3"
        color="secondary"
        icon="mdi-map-marker-plus"
        @click="emit('openCreateRoomModal')"
    />
    <v-btn
        key="4"
        color="secondary"
        icon="mdi-shape-plus"
        @click="emit('openCreateCategoryModal')"
    />

  </v-speed-dial>
</template>

<style scoped lang="scss">

</style>