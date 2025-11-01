<script setup lang="ts"></script>

<template>
  <general-settings />
  <ui-settings />
</template>

<style scoped lang="scss">
.sticky-btn {
  position: sticky;
  top: 16px;
  z-index: 10; /* Ensure it's above other elements */
}
</style>

<route>
{
  "meta": {
    "requiresAdmin": false,
    "requiresAuth": false,
    "requiresHousehold": false,
    "title": 'titles.settings',
    "layout": "default"
  }
}
</route>
