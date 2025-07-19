<script setup lang="ts">
const {t} = useI18n();
</script>

<template>
  <v-app>
    <v-app-bar
        density="compact"
    >
      <v-app-bar-title>
        <v-card
            hover
            width="fit-content"
            to="/"
        >
          {{ t('app.title') }}
        </v-card>
      </v-app-bar-title>
    </v-app-bar>
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