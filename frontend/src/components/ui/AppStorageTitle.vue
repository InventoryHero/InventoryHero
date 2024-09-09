<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppStorageTitle",
  props:{
    icon: {
      type: String,
      default: ""
    },
    title: {
      type: String,
      default: ""
    },
    color:{
      type: String,
      default: ""
    },
    variant: {
      type: String,
      default: "tonal"
    },
    disabled:{
      type: Boolean,
      default: false
    }
  },
  computed:{
    btnDisabled(){
      return this.color === "" || this.disabled
    },
    btnVariant(){
      if(this.btnDisabled)
      {
        return 'elevated'
      }
      return this.variant
    }
  }

})
</script>

<template>
  <v-btn
    density="compact"
    :prepend-icon="icon"
    :color="color"
    :variant="btnVariant"
    class="mb-1 text-truncate"
    :disabled="btnDisabled"
  >
    {{ title }}
  </v-btn>

</template>

<style scoped lang="scss">
.hovering{
  color: rgba(var(--v-theme-primary), 0.65) !important;
  cursor: pointer;
}
</style>