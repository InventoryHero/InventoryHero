<template>
  <v-dialog
    v-model="active"
    :max-height="height"
    :max-width="width"
  >
    <v-card
      :title="t('account.profile_picture.upload.title')"
      :loading="loading"
      :disabled="loading"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="active = false"
        />
      </template>
      <v-card-text>
        <v-file-upload
          v-model="selectedFile"
          show-size
          @rejected="rejected"
          :filter-by-type="allowedFileTypes"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          prepend-icon="mdi-upload"
          :text="t('account.profile_picture.upload.upload')"
          @click="upload"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useNotification } from '@kyvg/vue3-notification'

const { t } = useI18n()
const { notify } = useNotification()
const { height, width } = useDialogSize()
const { userEndpoint } = useAxios()

const active = defineModel<boolean>('active', {
  required: true
})
const emit = defineEmits<{
  (e: 'updated:profilePicture'): void
}>()

const selectedFile = ref<File>()
const loading = ref<boolean>(false)

const allowedFileTypes = computed(() => {
  return 'image/jpeg,image/png,image/webp,image/bmp,image/tiff'
})

const upload = async () => {
  loading.value = true
  if (selectedFile.value) {
    await userEndpoint.uploadProfilePicture(selectedFile.value)
    active.value = false
    emit('updated:profilePicture')
    loading.value = false
    return
  }
  loading.value = false
}
const rejected = async (_: File[]) => {
  notify({
    title: t('account.profile_picture.upload.invalid_file_type'),
    text: t('account.profile_picture.upload.accepted_file_types'),
    type: 'warn'
  })
}
</script>

<style scoped></style>
