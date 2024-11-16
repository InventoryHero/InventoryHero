<script setup lang="ts">

const {fromAdmin=false, smtpEnabled=false} = defineProps<{
  fromAdmin?: boolean,
  smtpEnabled?: boolean
}>()
</script>

<template>
  <v-sheet
      class="pa-4 mb-2 d-flex text-justify d-inline-block"
      color="accent"
      rounded="lg"
      style="hyphens:auto;"
      v-if="fromAdmin"
  >
    <span
        v-if="!smtpEnabled"
    >
      {{  $t("reset_password.email_disabled") }}
    </span>

    <span
        v-else
    >
      {{  $t("reset_password.email_or_direct") }}
    </span>
  </v-sheet>
</template>

<style scoped lang="scss">

</style>