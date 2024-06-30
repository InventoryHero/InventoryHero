<script lang="ts">
import {defineComponent} from 'vue'
import {useConfigStore} from "@/store";

export default defineComponent({
  name: "AppProgressCircular",
  setup(){
    const configStore = useConfigStore();
    return {
      configStore
    }
  },
  props: {
    message: {
      type: String,
      default: ""
    },
    size: {
      type: Number,
      default: 100
    },
    width: {
      type: Number,
      default: 20
    },
    indeterminate: {
      type: Boolean,
      default: true
    },
    color: {
      type: String,
      default: undefined
    }
  },
  computed: {
    spinnerColor(){
      if(this.color === undefined){
        return this.configStore.color
      }
      return this.color
    }
  }
})
</script>

<template>
  <v-progress-circular
      v-bind="$attrs"
      :size="size"
      :width="width"
      :color="spinnerColor"
      :indeterminate="indeterminate"
  >

  </v-progress-circular>
  <p
      class="test text-wrap"
  >
    <slot >
      {{ message }}
    </slot>
  </p>
</template>

<style scoped lang="scss">
.test{
  word-break: break-all;
}
</style>