<script lang="ts">
import {defineComponent} from 'vue'


export default defineComponent({
  name: "AppOverlayTitle",
  emits:{
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    'update:modelValue'(_: string){
      return true
    }
  },
  computed: {
    value: {
      get() {
        return this.modelValue
      },
      set(value: string) {
        this.$emit('update:modelValue', value)
      }
    }
  },
  props:{
    modelValue:{
      type: String
    },
    label: {
      type: String,
      default: ""
    },
    edit: {
      type: Boolean,
      default: false
    },
  }
})
</script>

<template>
  <v-text-field
      density="compact"
      v-if="edit"
      hide-details="auto"
      :label="label"
      v-model="value"
      v-bind="$attrs"
  >

  </v-text-field>
  <template v-else>
    {{ value }}
  </template>
</template>

<style scoped lang="scss">

</style>