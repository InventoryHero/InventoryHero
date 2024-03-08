<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "AppSettingsCard",
  props: {
    title: {
      type: String,
      default: ''
    }
  }
})
</script>

<template>
  <div
    class="text-subtitle-2 ms-4 pb-2"
  >

    {{ title }}
  </div>
  <v-card
      :elevation="5"
      density="compact"
      class="mb-4"
  >
    <slot />
  </v-card>

</template>

<style scoped lang="scss">

</style>