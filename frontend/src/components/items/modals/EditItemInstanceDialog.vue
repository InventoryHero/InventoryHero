<script setup lang="ts">
import {
  ItemAttributesBaseSchema, ItemAttributesUpdateSchema,
  ItemStorageReadSchema, ItemStorageUpdateSchema,
} from "@/api/types/items.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
import {toISODateString} from "@/utils/date.ts";


const {t} = useI18n();
const {btnStyle, textFieldStyling, textAreaStyle, numberInputStyling, dateInputStyling} = useAppStyling()
const {items: itemEndpoint} = useAxios()
const {close, onBeforeRouteLeaveHandler} = useGlobalModal()

const active = defineModel<boolean>({
  required: true
})

const {
  height,
  width,
  itemName,
  storageName,
  itemId,
  itemInstance,
  itemAttributes
} = defineProps<{
  height: string,
  width: string,
  itemName: string,
  storageName: string,
  itemId: string,
  itemInstance: ItemStorageReadSchema,
  itemAttributes: ItemAttributesBaseSchema
}>()

const editForm = useTemplateRef("editForm")
const expirationDate = ref<Date|null>(
    itemAttributes.expiration_date ?
        new Date(itemAttributes.expiration_date) :
        null
)
const serialNumber = ref<string|null>(itemAttributes.serial_number ?? null)
const batchCode = ref<string|null>(itemAttributes.batch_code ?? null)
const notes = ref<string|null>(itemAttributes.notes ?? null)
const quantity = ref<number>(itemInstance.quantity)

const quantityRules = ref([
  (v: number | null | undefined) => v != null || t("create.item.form.quantity_required")
])

const loading = ref<boolean>(false);

const emit = defineEmits<{
  (e: 'reload'): void
}>()

const reset = () => {
  quantity.value = itemInstance.quantity
  expirationDate.value = itemAttributes.expiration_date ? new Date(itemAttributes.expiration_date) : null
  serialNumber.value = itemAttributes.serial_number ?? null
  batchCode.value = itemAttributes.batch_code ?? null
  notes.value = itemAttributes.notes ?? null
  if(editForm.value){
    editForm.value.resetValidation()
  }
}

const handleSave = async () => {
  const {valid} = await editForm.value.validate()
  if(!valid){
    return
  }
  let payload = {
    stock: {
      quantity: quantity.value === itemInstance.quantity ? undefined : quantity.value,
    } as ItemStorageUpdateSchema,
    attributes: {
      expiration_date: expirationDate.value === itemAttributes.expiration_date ? undefined : toISODateString(expirationDate.value),
      serial_number: serialNumber.value === itemAttributes.serial_number ? undefined : serialNumber.value,
      batch_code: batchCode.value === itemAttributes.batch_code ? undefined : batchCode.value,
      notes: notes.value === itemAttributes.notes ? undefined : notes.value
    } as ItemAttributesUpdateSchema
    
  }
  loading.value = true
  await itemEndpoint.updateItemInstance(itemId, itemInstance.id, payload)
  emit('reload')
  close()

}

watch(active, () => {
  loading.value = false
  reset()
})

onBeforeRouteLeave(() => {
  return onBeforeRouteLeaveHandler()
})

</script>

<template>
  <v-dialog
      v-model="active"
      persistent
      :height="height"
      :width="width"
  >
    <v-card
      v-if="active"
      :loading="loading"
      :disabled="loading"
      :title="t('items.attributes.edit.title', {item: itemName, storage: storageName})"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="close()"
        />
      </template>
      <v-card-text>
        <v-form
          ref="editForm"
          @submit.prevent=""
        >
          <v-row>
            <v-col cols="12">
              <v-number-input
                v-bind="numberInputStyling"
                v-model="quantity"
                :min="0"
                :rules="quantityRules"
                :label="t('items.attributes.edit.quantity')"
              />
            </v-col>
            <v-col cols="12">
              <v-date-input
                  v-bind="dateInputStyling"
                  v-model="expirationDate"
                  :label="t('items.attributes.edit.expiry_date')"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="serialNumber"
                clearable
                :label="t('items.attributes.edit.serial_number')"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                  v-bind="textFieldStyling"
                  v-model="batchCode"
                  clearable
                  :label="t('items.attributes.edit.batch')"
              />
            </v-col>
            <v-col cols="12">
              <v-textarea
                  v-bind="textAreaStyle"
                  v-model="notes"
                  clearable
                  :label="t('items.attributes.edit.notes')"
              />
            </v-col>
          </v-row>

        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn
            v-bind="btnStyle"
            :text="t('items.attributes.edit.cancel')"
            @click="close"
        />
        <v-btn
            v-bind="btnStyle"
            :text="t('items.attributes.edit.save')"
            @click="handleSave"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>