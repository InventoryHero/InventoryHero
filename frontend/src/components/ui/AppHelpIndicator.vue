<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "AppHelpIndicator",
  emits: {
    'click:outside'(){
      return true
    },
    click(){
      return true
    }
  },
  methods: {
    handleOutside(){
      this.$emit('click:outside')
    },
    handleClick(){
      this.$emit('click')
    },
    include () {
      return [document.querySelector('.included')]
    },
  }
})
</script>

<template>
  <v-icon
      color="primary"
      icon="mdi-help-circle-outline"
      ref="btn"
      class="included"
      @click="handleClick()"
      v-click-outside="{
        handler: handleOutside,
        include
      }"
  >
  </v-icon>
</template>

<style scoped lang="scss">

</style>