<template>
  <v-dialog
    v-model="active"
    :max-height="height"
    :max-width="width"
  >
    <v-card
      :title="t('households.delete.title')"
      :loading="loading"
      :disabled="loading"
    >
      <v-card-text>
        {{ t('households.delete.text') }}
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn
          v-bind="btnStyle"
          prepend-icon="mdi-cancel"
          :text="t('households.delete.abort')"
          @click="active = false"
        />
        <v-btn
          v-bind="btnStyle"
          prepend-icon="mdi-delete"
          color="error"
          :text="t('households.delete.confirm')"
          @click="emit('delete')"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
const { width, height } = useDialogSize()
const { btnStyle } = useAppStyling()
const { t } = useI18n()

const active = defineModel<boolean>('active', {
  required: true
})
const { loading } = defineProps<{
  loading: boolean
}>()
const emit = defineEmits<{
  (e: 'delete'): void
}>()
</script>

<style scoped></style>
