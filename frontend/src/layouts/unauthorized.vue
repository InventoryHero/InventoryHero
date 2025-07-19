<script setup lang="ts">

import {Notifications} from "@kyvg/vue3-notification";
</script>

<template>
  <v-app>
    <notifications
        position="top right"
        classes="vue-notification mt-2 me-8"
        :max="2"
    />
    <router-view v-slot="{Component, route}" >
      <v-main :key="route.fullPath">
        <v-container>
          <component :is="Component"  />
        </v-container>
      </v-main>
    </router-view>
  </v-app>
</template>

<style scoped lang="scss">

</style>