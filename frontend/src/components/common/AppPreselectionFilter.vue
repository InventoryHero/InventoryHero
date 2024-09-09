<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppPreselectionFilter",
  props: {
    title:{
      type: String,
      default: "PRELOAD FILTER"
    }
  }
})
</script>

<template>
  <v-chip
    :closable="true"
    variant="elevated"
    color="primary"
    class="chip"

  >
    <span class="text-wrap">
      {{title}}
    </span>
  </v-chip>
</template>

<style scoped lang="scss">

.chip{
  min-height: calc(var(--v-chip-height));
  height: fit-content;
}

</style>