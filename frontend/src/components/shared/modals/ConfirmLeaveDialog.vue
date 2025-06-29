<script setup lang="ts">
import {useModal} from "@/composables-new/useModal.ts";

const isAwaitingConfirmation = defineModel<boolean>({
  required: true
})

const emit = defineEmits<{
  (e: 'cancel'): void,
  (e: 'confirm'): void,
}>()

</script>

<template>

  <v-dialog
      v-model="isAwaitingConfirmation"
      persistent
      width="auto"
  >
    <v-card class="pa-4" >
      <v-card-title class="text-h6">Unsaved Changes</v-card-title>
      <v-card-text>
        Are you sure you want to leave? Your changes will be lost.
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="emit('cancel')">Stay</v-btn>
        <v-btn color="error" variant="tonal" @click="emit('confirm')">Discard Changes</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>