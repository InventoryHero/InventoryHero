<template>
  <v-dialog
    v-model="active"
    :max-height="height"
    :max-width="width"
    persistent
    no-click-animation
  >
    <v-card
      :loading="loading"
      :disabled="loading"
    >
      <template v-slot:title>
        <i18n-t keypath="households.transfer.title">
          <template #user>
            <span class="text-primary">{{ username }}</span>
          </template>
        </i18n-t>
      </template>
      <v-card-text>
        {{ t('households.transfer.text', { user: username }) }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          v-bind="btnStyle"
          variant="elevated"
          :text="t('households.transfer.cancel')"
          @click="active = false"
        />
        <v-btn
          v-bind="btnStyle"
          color="error"
          :text="t('households.transfer.confirm')"
          @click="emit('transfer')"
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
const { loading, username } = defineProps<{
  loading: boolean
  username: string
}>()
const emit = defineEmits<{
  (e: 'transfer'): void
}>()
</script>

<style scoped></style>
