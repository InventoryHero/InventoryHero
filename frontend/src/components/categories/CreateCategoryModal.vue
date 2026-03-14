<script setup lang="ts">
import useAppStyling from '@/composables/useAppStyling.ts'
import categoryAddedEventBus from '@/services/categoryAddedEventBus.ts'

const { t } = useI18n()
const { textFieldStyling, btnStyle } = useAppStyling()

const { items } = useAxios()
const route = useRoute()

const active = defineModel<boolean>()
const { height, width } = defineProps<{
  height?: string | number | undefined
  width?: string | number | undefined
}>()

const name = ref<string | null>(null)
const loading = ref<boolean>(false)
const form = useTemplateRef('form')
const confirmLeaveDialogVisible = ref<boolean>(false)

const dirty = computed(() => {
  return !!name.value
})

const nameRules = ref([
  (value: string | null) =>
    !!value || t('create.category.form.rules.name_required')
])

const saveCategory = async () => {
  const { valid } = await form.value!.validate()
  if (!valid) {
    return
  }
  loading.value = true
  const { success, data } = await items.createNewCategory({
    name: name.value!
  })
  if (!success) {
    loading.value = false
    return false
  }
  if (route.path.startsWith('/items')) {
    categoryAddedEventBus.emit(data!)
  }

  loading.value = false
  return true
}

const saveAndClose = async () => {
  const success = await saveCategory()
  if (success) {
    forceClose()
  }
}

const save = async () => {
  const success = await saveCategory()
  if (success) {
    form.value!.reset()
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
      :disabeld="loading"
      :title="t('create.category.title')"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="close(false)"
        />
      </template>
      <v-card-text>
        <v-form
          @submit.prevent=""
          ref="form"
        >
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                :label="t('create.category.form.name')"
                v-model="name"
                :rules="nameRules"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn
          v-bind="btnStyle"
          :text="t('create.category.form.save')"
          @click="save"
          :disabled="loading"
        />
        <v-btn
          v-bind="btnStyle"
          :text="t('create.category.form.save_and_close')"
          @click="saveAndClose"
          :disabled="loading"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
  <confirm-leave-dialog
    v-model="confirmLeaveDialogVisible"
    @cancel="confirmLeaveDialogVisible = false"
    @confirm="forceClose"
  />
</template>

<style scoped lang="scss"></style>
