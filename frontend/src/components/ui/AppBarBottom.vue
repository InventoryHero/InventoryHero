<script setup lang="ts">


import {useRouter} from "vue-router";

const router = useRouter()

const active = defineModel();


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
      to="/storage/boxes"
      icon="mdi-package-variant"
      active-color="primary"
      variant="text"
  />
  <v-btn
      to="/storage/locations"
      icon="mdi-archive-marker"
      active-color="primary"
      variant="text"
  />
</v-bottom-navigation>
</template>

<style scoped lang="scss">


</style>