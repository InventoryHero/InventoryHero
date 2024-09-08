<script setup lang="ts">

const active = defineModel()

function handleClickOutside(){
  active.value = false
}

function include () {
  return [document.querySelector('.included')]
}
</script>

<template>
  <v-icon
      v-bind="$attrs"
      color="primary"
      icon="mdi-help-circle-outline"
      ref="btn"
      class="included"
      v-click-outside="{
        handler: handleClickOutside,
        include
      }"
      @click="active=true"
  >
  </v-icon>
</template>

<style scoped lang="scss">

</style>