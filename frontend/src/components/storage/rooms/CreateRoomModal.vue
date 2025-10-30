<script setup lang="ts">
import useAppStyling from '@/composables/useAppStyling.ts'
import { useTemplateRef } from 'vue'
import { VForm } from 'vuetify/components'

import roomAddedEventBus from '@/services/roomAddedEventBus.ts'
import ConfirmLeaveDialog from '@/components/common/modals/ConfirmLeaveDialog.vue'

const { t } = useI18n()
const { textFieldStyling, btnStyle } = useAppStyling()
const { storage: storageEndpoint } = useAxios()
const route = useRoute()

const active = defineModel<boolean>()

const { height, width } = defineProps<{
  height?: string | number | undefined
  width?: string | number | undefined
}>()

const nameRules = ref([
  (v: string | null) => !!v || t('create.room.form.name_required')
])

const name = ref<string | null>()
const form = useTemplateRef('form')
const loading = ref<boolean>(false)
const confirmLeaveDialogVisible = ref<boolean>(false)

const dirty = computed(() => {
  return !!name.value
})

const saveRoom = async () => {
  //@ts-expect-error
  const { valid } = await form.value.validate()
  if (!valid) {
    return false
  }

  loading.value = true
  const { success, data, error } = await storageEndpoint.createStorage({
    name: name.value!,
    storage_type: 'room'
  })
  if (!success) {
    return false
  }
  loading.value = false

  if (route.name === '/storage/rooms/room.[id]') {
    roomAddedEventBus.emit()
  }
  name.value = null
  return true
}

const saveAndClose = async () => {
  const success = await saveRoom()
  if (success) {
    forceClose()
  }
}

const save = async () => {
  const success = await saveRoom()
  if (success) {
    form.value.reset()
  }
}

const forceClose = () => {
  close(true)
}
const close = (force: boolean = false) => {
  if (force) {
    active.value = false
  } else if (dirty.value) {
    confirmLeaveDialogVisible.value = true
    return
  } else {
    active.value = false
  }
  form.value.reset()
}

onBeforeRouteLeave(() => {
  if (dirty.value) {
    confirmLeaveDialogVisible.value = true
    return false
  }
  if (active.value) {
    active.value = false
    return false
  }
  return true
})
</script>

<template>
  <v-dialog
    v-model="active"
    scrollable
    :height="height"
    :width="width"
  >
    <v-card
      :loading="loading"
      :disabled="loading"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="close(false)"
        />
      </template>
      <template v-slot:title>
        {{ t('create.room.title') }}
      </template>

      <v-card-text>
        <v-form
          @submit.prevent=""
          ref="form"
        >
          <v-text-field
            v-bind="textFieldStyling"
            v-model="name"
            :label="t('create.room.form.name')"
            :rules="nameRules"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-btn
          v-bind="btnStyle"
          :text="t('create.room.form.save')"
          @click="save"
        />
        <v-btn
          v-bind="btnStyle"
          :text="t('create.room.form.save_and_close')"
          @click="saveAndClose"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
  <confirm-leave-dialog
    v-model="confirmLeaveDialogVisible"
    @cancel="confirmLeaveDialogVisible = false"
    @confirm="forceClose()"
  />
</template>

<style scoped lang="scss"></style>
