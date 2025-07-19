<script setup lang="ts">
/*
  this file is needed as otherwise vite-plugin-layouts-next will stack views. E.g. confirmation/confirm/:code will then
  render the tokenized layout inside the default layout
 */
</script>

<template>
  <RouterView />
</template>

<route >
{
  "meta": {
    "layout": false
  }
}
</route>