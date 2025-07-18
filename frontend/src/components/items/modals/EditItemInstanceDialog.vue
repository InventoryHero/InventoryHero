<script setup lang="ts">
import {
  CategoryReadSchema, ItemAttributesBaseSchema, ItemAttributesReadSchema, ItemAttributesUpdateSchema,
  ItemReadSchema,
  ItemStorageReadSchema, ItemStorageUpdateSchema,
  ItemSummarySchema,
  ItemUpdateSchema
} from "@/api/types/items.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
import {StorageResponseSchema} from "@/api/types/storage.ts";

const {t} = useI18n();
const {btnStyle, textFieldStyling, selectStyling, numberInputStyling, dateInputStyling} = useAppStyling()
const {items: itemEndpoint} = useAxios()

const active = defineModel<boolean>({
  required: true
})

const {
  itemId,
  itemInstance,
  itemAttributes
} = defineProps<{
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
const quantity = ref<number>(itemInstance.quantity)

const quantityRules = ref([
  (v: number | null | undefined) => v != null || t("create.item.form.quantity_required")
])


const emit = defineEmits<{
  (e: 'reload'): void
}>()

const close = () => {
  active.value = false
  editForm.value.reset()
}

const handleSave = async () => {
  // TODO TIMEZONES!!
  const {valid} = await editForm.value.validate()
  if(!valid){
    return
  }
  let payload = {
    stock: {
      quantity: quantity.value === itemInstance.quantity ? undefined : quantity.value,
    } as ItemStorageUpdateSchema,
    attributes: {
      expiration_date: expirationDate.value === itemAttributes.expiration_date ? undefined : expirationDate.value,
    } as ItemAttributesUpdateSchema
    
  }
  console.log(payload)
  console.log(quantity.value === itemInstance.quantity)
  console.log(itemInstance.quantity)
  itemEndpoint.updateItemInstance(itemId, itemInstance.id, payload)
  console.log(expirationDate.value)

  emit('reload')
}

onBeforeRouteLeave(() => {
  if(active.value) {
    return false
  }
})

</script>

<template>
  <v-dialog
      v-model="active"
      persistent
  >
    <v-card
      :title="t('items.item.instance.edit.title')"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="close"
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
              />
            </v-col>
            <v-col cols="12">
              <v-date-input
                  v-bind="dateInputStyling"
                  v-model="expirationDate"

              />
            </v-col>
            <v-col>

            </v-col>
          </v-row>

        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn
            v-bind="btnStyle"
            :text="t('items.item.instance.edit.cancel')"
            @click="close"
        />
        <v-spacer/>
        <v-btn
            v-bind="btnStyle"
            :text="t('items.item.instance.edit.save')"
            @click="handleSave"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>