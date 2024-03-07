<script lang="ts">
import {defineComponent, defineModel} from 'vue'

type Rule = (value: string) => string


export default defineComponent({
  name: "AppOverlayTitle",
  emits:{
    'update:modelValue'(_: string){
      return true
    }
  },
  computed: {
    value: {
      get() {
        return this.modelValue
      },
      set(value) {
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
    rules: {
      type: Array<Rule>,
      default: []
    }
  }
})
</script>

<template>
  <v-text-field
      density="compact"
      v-if="edit"
      hide-details="auto"
      :label="label"
      :rules="rules"
      v-model="value"
  >

  </v-text-field>
  <template v-else>
    {{ value }}
  </template>
</template>

<style scoped lang="scss">

</style>