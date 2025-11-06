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
        <i18n-t keypath="households.kick.title">
          <template #user>
            <span class="text-primary">{{ username }}</span>
          </template>
        </i18n-t>
      </template>
      <v-card-text>
        {{ t('households.kick.text', { user: username }) }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          :text="t('households.kick.cancel')"
          @click="active = false"
        />
        <v-btn
          :text="t('households.transfer.confirm')"
          @click="emit('kick')"
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
  (e: 'kick'): void
}>()
</script>

<style scoped></style>
