<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppScrollToTopBtn",
  props: {
    modelValue: {
      type: Boolean,
      required: true
    }
  }
})
</script>

<template>
  <v-fade-transition>
    <v-btn
        icon="mdi-chevron-double-up"
        variant="elevated"
        :elevation="10"
        v-if="modelValue"
        class="caret-up"
        size="x-small"
    >
      <v-icon size="x-large" color="primary" />
    </v-btn>
  </v-fade-transition>
</template>

<style scoped lang="scss">
.caret-up{
  position: absolute;
  right: 10px;
  z-index: 10;
  bottom: 10px;
  border: 1px solid rgba(var(--v-theme-primary), 0.5)
}
</style>