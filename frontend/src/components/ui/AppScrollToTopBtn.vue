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
      density="comfortable"
      location="bottom end"
      variant="elevated"
      border="md"
      size="large"
      absolute
      v-bind="$attrs"
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
  margin-top: -5px;
  margin-right: 5px;
}
</style>