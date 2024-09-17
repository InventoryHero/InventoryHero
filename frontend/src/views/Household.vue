<script setup lang="ts">



</script>

<template>


  <v-row
    class="fill-height fill-width"
    justify="center"
    no-gutters
  >
    <v-col
      cols="12"
      lg="8"
      class="d-flex flex-column position-relative fill-height"
    >
      <router-view v-slot="{Component, route }">
        <component :is="Component"  :key="route" />
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
</style>