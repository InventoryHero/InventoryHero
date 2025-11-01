<template>
  <v-btn to="/administration/users">users</v-btn>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss"></style>

<route>
{
    "meta": {
        "requiresAuth": true,
        "requiresAdmin": true,
        "requiresHousehold": false, 
        "layout": "admin"
    }
}
</route>
