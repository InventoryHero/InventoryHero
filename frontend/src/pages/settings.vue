<template>
  <general-settings />
  <ui-settings />
</template>

<script setup lang="ts">
definePage({
  meta: {
    requiresAdmin: false,
    requiresAuth: false,
    requiresHousehold: false,
    title: 'titles.settings',
    layout: 'default'
  }
})
</script>

<style scoped lang="scss"></style>
