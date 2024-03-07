<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "NavItem",
  props:{
    route: {
      type: String,
      default: ""
    },
    exact: {
      type: Boolean,
      default: true
    },
    icon:{
      type: String,
      default: ""
    },
    title:{
      type: String,
      default: ""
    },
    size:{
      type: String,
      default: undefined
    }
  }
})
</script>

<template>
  <v-list-item
      :to="route"
      :exact="exact"

  >
    <template v-slot:prepend>

        <v-icon
            :icon="icon"
            :size="size"
        ></v-icon>

    </template>
    <v-list-item-title>
      <slot name="title">
        {{ title }}
      </slot>
    </v-list-item-title>
  </v-list-item>
</template>

<style scoped lang="scss">

</style>