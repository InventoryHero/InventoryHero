<script setup lang="ts">
const router = useRouter()
const {t} = useI18n()
</script>

<template>

  <v-card
      width="fit-content"
      class="sticky-btn mb-2 d-flex align-center pa-1 pe-2 text-primary"
      @click="router.back()"

      density="comfortable"
  >
    <v-icon
        icon="mdi-arrow-left"
        size="x-small"
        class="me-1"
    />
    <span
        class="text-caption text-subtitle-1"
    >
          {{ t('settings.back') }}
        </span>
  </v-card>
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
    "requiresAuth": false,
    "requiresHousehold": false,
    "title": 'titles.settings',
    "layout": "unauthorized",
  }
}
</route>