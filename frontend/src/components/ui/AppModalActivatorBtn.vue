<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppModalActivatorBtn",
  emits:{
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    'update:model-value'(value: boolean){
      return true
    }
  },
  computed: {
    model: {
      get(): boolean {
        return this.modelValue
      },
      set(value: boolean){
        this.$emit('update:model-value', value)
      }
    }
  },
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: ""
    },
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: ""
    }
  }
})
</script>

<template>
  <v-btn
      :prepend-icon="icon"
      :loading="loading"
      class="position-relative"
      @click="model=!model"
  >
    <template #loader>
      <v-overlay
          :model-value="loading"
          :contained="true"
          class="justify-center align-center rounded"
      ><v-progress-circular color="primary" :indeterminate="true"/>
      </v-overlay>
    </template>
    <slot >
      {{ title }}
    </slot>
  </v-btn>
</template>

<style scoped lang="scss">
:deep(.v-btn--loading .v-btn__content){
  opacity: 0.25 !important;
}
</style>