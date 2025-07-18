<script setup lang="ts">

import {Notifications} from "@kyvg/vue3-notification";
</script>

<template>
  <notifications
      position="top right"
      classes="vue-notification mt-2 me-8"
      :max="2"
  />
  <v-main>
    <v-container>
      <slot />
    </v-container>
  </v-main>
</template>

<style scoped lang="scss">

</style>