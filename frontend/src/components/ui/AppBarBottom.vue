<script setup lang="ts">

const active = defineModel<boolean>();


</script>

<template>

<v-bottom-navigation
    :active="active"
    :grow="true"
>
  <v-btn
      to="/"
      icon="mdi-home"
      active-color="primary"
      variant="text"
  />
  <v-btn
      to="/products"
      icon="mdi-cart"
      active-color="primary"
      variant="text"
  />
  <v-btn
      to="/create"
      icon="mdi-plus-box"
      active-color="primary"
      variant="text"
  />
  <v-btn
      to="/boxes"
      icon="mdi-package-variant"
      active-color="primary"
      variant="text"
  />
  <v-btn
      to="/locations"
      icon="mdi-archive-marker"
      active-color="primary"
      variant="text"
  />
</v-bottom-navigation>
</template>

<style scoped lang="scss">


</style>