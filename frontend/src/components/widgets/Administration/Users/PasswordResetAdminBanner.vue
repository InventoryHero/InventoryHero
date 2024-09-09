<script setup lang="ts">

const {fromAdmin=false, smtpEnabled=false} = defineProps<{
  fromAdmin?: boolean,
  smtpEnabled?: boolean
}>()
</script>

<template>
  <v-sheet
      class="pa-4 mb-2"
      color="accent"
      rounded="lg"
      v-if="fromAdmin"
  >
    <span
        v-if="!smtpEnabled"
    >
      {{  $t("administration.users.password_reset.email_disabled") }}
    </span>

    <span
        v-else
    >
      {{  $t("administration.users.password_reset.email_or_direct") }}
    </span>
  </v-sheet>
</template>

<style scoped lang="scss">

</style>