<script lang="ts">
import {defineComponent} from "vue";
export default defineComponent({
  name: "AppBarBottom"
})

</script>

<template>

<v-bottom-navigation
    class="dock"
    density="compact"
    :grow="true"
>

  <v-row
    :no-gutters="true"
    class="fill-height align-center justify-space-evenly"
  >
    <nav-list
        :is-dock="true"
    />

  </v-row>

</v-bottom-navigation>
</template>

<style scoped lang="scss">
  :deep(.v-list-item__prepend) {
    display: flex !important;
    justify-content: center;
    align-items: center;
  }
  :deep(.v-list-item__spacer)
  {
    width: 0 !important;;
  }

</style>