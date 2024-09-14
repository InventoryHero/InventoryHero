<script setup lang="ts">
const hintShown = ref(false)
const {t} = useI18n()

function toggleHint(){
  hintShown.value = !hintShown.value
}

</script>

<template>
<v-card
  class="d-flex flex-column fill-height"
>
  <v-card
      class="pt-2 pb-2  flex-0-0 fill-width"
      elevation="0"
  >
    <div
      class="d-flex justify-center"
    >
      <app-qr-code
      />
    </div>
    <div
        class="position-relative pt-1 ps-4 pe-4 d-flex justify-start align-center"
    >
      <app-icon-btn
        icon="mdi-help-circle-outline"
        class="me-2"
        @click="toggleHint"
      />
      <v-expand-transition>
        <p
            v-if="hintShown"
            class="mb-0 mt-0 text-caption text-wrap"
        >
          {{ t('print.qr_code_settings.constrained') }}
        </p>
      </v-expand-transition>
    </div>
  </v-card>
  <v-container class="flex-1-1 overflow-auto">

    <label-settings />
    <div class="mt-4" />
    <page-settings />

  </v-container>
</v-card>
</template>

<style scoped lang="scss">

</style>