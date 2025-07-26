<script setup lang="ts">

</script>

<template>
  <v-list
      density="compact"
      nav
  >
    <v-list-item
        to="/administration"
        prepend-icon="mdi-view-dashboard"
        :title="$t('nav.admin.overview')"
        color="primary"
        :exact="true"
    />
    <v-list-item
        to="/administration/users"
        prepend-icon="mdi-account-group"
        :title="$t('nav.admin.users')"
        color="primary"
        :exact="true"
    />
  </v-list>
</template>

<style scoped lang="scss">

</style>