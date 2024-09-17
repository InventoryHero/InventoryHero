<script setup lang="ts">

defineOptions({
  inheritAttrs: false
})

const {scrolledDown=false} = defineProps<{
  scrolledDown: boolean
}>()


</script>

<template>
  <v-fab
      :active="scrolledDown"
      icon="mdi-chevron-double-up"
      location="bottom right"
      variant="elevated"
      border="md"
      size="large"
      absolute
      v-bind="{
        density: 'comfortable',
        ...$attrs
      }"
  >
    <template v-slot:default>
      <v-icon
          color="primary"
          size="large"
      />
    </template>

  </v-fab>
</template>

<style scoped lang="scss">
.v-fab{
  bottom: 8px;
  right: 8px;
}
</style>