<template>
  <router-view />
</template>

<script setup lang="ts"></script>

<style scoped></style>

<route>
    {
        "meta": {
            "layout": "admin",
            "requiresAdmin": true,
            "requiresAuth": true
        }
    }
</route>
