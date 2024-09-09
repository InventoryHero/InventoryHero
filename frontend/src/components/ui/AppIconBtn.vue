<script setup lang="ts">


import {computed} from "vue";

defineOptions({
  inheritAttrs: false
})

const {color=""} = defineProps<{
  color?: string
}>()

const setColor = computed(() => {
  return color?? 'primary'
})

</script>

<template>
  <v-hover
      v-if="!$attrs['loading'] ?? true"
      v-slot="{ isHovering, props}"
  >
    <v-icon
        v-bind="{...$attrs, ...props}"
        :color="setColor"
        fixed-width
        class="app-font-awesome-btn"
        :class="{
          'hovering': isHovering && !$attrs['disabled'],
          'disabled': $attrs['disabled'],
        }"
    />
  </v-hover>
  <v-progress-circular
      v-if="$attrs['loading'] ?? false"
      :active="true"
      :indeterminate="true"
      size="25"
      width="3"
      :color="setColor"
  />
</template>

<style scoped lang="scss">
.disabled{
  &.v-theme--dark{
    color: rgba(255, 255, 255, 0.65) !important;
  }
  &.v-theme--light{
    color: rgba(255, 255, 255, 0.65) !important;
  }
}
.hovering{
  cursor: pointer;
  color: rgba(var(--v-theme-primary), 0.65);

}
</style>