<script setup lang="ts">
import {
  ItemAttributesBaseSchema,
  ItemStorageReadSchema
} from '@/api/types/items.ts'
import useAppStyling from '@/composables/useAppStyling.ts'
const { numberInputStyling } = useAppStyling()
const { t, d } = useI18n()
const { items: itemEndpoint } = useAxios()
const { openModal } = useGlobalModal()
const {
  itemName,
  storageName,
  itemId,
  instance,
  attributes,
  loading = false
} = defineProps<{
  itemName: string
  storageName: string
  itemId: string
  instance: ItemStorageReadSchema
  attributes: ItemAttributesBaseSchema
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'consume'): void
  (e: 'add'): void
  (e: 'reload'): void
}>()

const quantityLoading = ref<boolean>(false)
const deleting = ref<boolean>(false)

const formatExpirationDate = (expirationDate: string | null | undefined) => {
  if (!expirationDate) {
    return ''
  }
  const date = new Date(expirationDate)
  if (isNaN(date.getTime())) {
    return t('items.attributes.invalid_expiration_set')
  }
  return d(date, 'short')
}

const addInstance = async () => {
  quantityLoading.value = true
  const { success, data, error } = await itemEndpoint.addItemInstance(
    itemId,
    instance.id
  )
  if (!success) {
    quantityLoading.value = false
    return
  }
  emit('add')
  quantityLoading.value = false
}

const consumeInstance = async () => {
  quantityLoading.value = true
  const { success } = await itemEndpoint.consumeItemInstance(
    itemId,
    instance.id
  )
  if (!success) {
    quantityLoading.value = false
    return
  }
  emit('consume')
  quantityLoading.value = false
}

const changeAmount = (newAmount: number) => {
  if (instance.quantity > newAmount) {
    consumeInstance()
  } else {
    addInstance()
  }
}

const edit = () => {
  openModal('editItemInstanceModal', {
    itemName: itemName,
    storageName: storageName,
    itemInstance: instance,
    itemAttributes: attributes,
    itemId: itemId,
    onReload: () => emit('reload')
  })
}
const deleteAllInstances = async () => {
  deleting.value = true
  const { success, data, error } = await itemEndpoint.deleteInstances(
    itemId,
    instance.id
  )
  if (!success) {
    deleting.value = false
    return
  }
  emit('reload')
  deleting.value = false
}
</script>

<template>
  <v-card
    height="fit-content"
    max-height="400"
    variant="outlined"
    class="mt-1 mb-1 overflow-y-scroll"
    :loading="loading || deleting"
    :disabled="loading || deleting"
  >
    <v-card-text>
      <v-list>
        <v-list-item
          :disabled="quantityLoading"
          :loading="quantityLoading"
        >
          <v-list-item-title class="text-wrap">
            {{ t('items.attributes.quantity') }}
          </v-list-item-title>
          <v-list-item-subtitle class="mt-1">
            <v-number-input
              v-bind="numberInputStyling"
              :model-value="instance.quantity"
              @update:model-value="changeAmount"
              density="compact"
              :disabled="quantityLoading"
              :loading="quantityLoading"
              :min="0"
            />
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item
          v-if="attributes.expiration_date"
          :title="t('items.attributes.expiry_date')"
          :subtitle="formatExpirationDate(attributes.expiration_date)"
        />
        <v-list-item
          v-if="attributes.serial_number"
          :title="t('items.attributes.serial_number')"
          :subtitle="attributes.serial_number"
        />
        <v-list-item
          v-if="attributes.batch_code"
          :title="t('items.attributes.batch')"
          :subtitle="attributes.batch_code"
        />
        <v-list-item
          v-if="attributes.notes"
          :title="t('items.attributes.notes')"
          :subtitle="attributes.notes"
        />
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <!-- TODO confirmation for delete -->
      <v-btn
        prepend-icon="mdi-trash-can"
        :text="t('items.attributes.delete')"
        class="text-none"
        density="compact"
        color="error"
        @click="deleteAllInstances"
      />
      <v-btn
        density="compact"
        prepend-icon="mdi-pencil"
        :text="t('items.attributes.edit.button')"
        class="text-none"
        color="primary"
        @click="edit"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss"></style>
