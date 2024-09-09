<script setup lang="ts">
defineOptions({
  inheritAttrs: false
})

const {visible=false, disabled=false, text=''} = defineProps<{
  visible?: boolean,
  disabled?: boolean,
  text?: string
}>()


</script>

<template>
  <v-fade-transition>
    <v-btn
        v-if="visible"
        :disabled="disabled"
        class="me-4"
        density="compact"
        prepend-icon="mdi-lock-reset"
        variant="tonal"
        v-bind="$attrs"
    >
      {{ text }}
    </v-btn>
  </v-fade-transition>
</template>

<style scoped lang="scss">

</style>