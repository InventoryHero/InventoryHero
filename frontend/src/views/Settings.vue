<script setup lang="ts">
import {useAuthStore} from "@/store";

const authStore = useAuthStore()
const authorized = computed(() => authStore.authorized)
const router = useRouter()

const {t} = useI18n()
</script>

<template>

  <v-row
    class="fill-height"
    dense
    justify="center"
  >
    <v-col
      cols="12"
      lg="8"
    >
      <v-card
          v-if="!authorized"
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
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.sticky-btn {
  position: sticky;
  top: 16px;
  z-index: 10; /* Ensure it's above other elements */
}
</style>
