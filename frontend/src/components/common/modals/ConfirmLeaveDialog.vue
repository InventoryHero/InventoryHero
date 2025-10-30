<script setup lang="ts">
const { t } = useI18n()
const isAwaitingConfirmation = defineModel<boolean>({
  required: true
})

const emit = defineEmits<{
  (e: 'cancel'): void
  (e: 'confirm'): void
}>()
</script>

<template>
  <v-dialog
    v-model="isAwaitingConfirmation"
    persistent
    width="auto"
  >
    <v-card class="pa-4">
      <v-card-text>
        {{ t('leave_confirmation.text') }}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          @click="emit('cancel')"
          :text="t('leave_confirmation.stay')"
        />
        <v-btn
          color="error"
          variant="tonal"
          @click="emit('confirm')"
          :text="t('leave_confirmation.discard')"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss"></style>
