<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";
import {useTemplateRef} from "vue";
import {VForm} from "vuetify/components";
import {useModal} from "@/composables-new/useModal.ts";
import {StorageResponseSchema} from "@/api/types/storage.ts";
import {
  CategoryReadSchema,
  ItemAttributesBaseSchema,
  ItemCreateSchema, ItemInstanceCreate,
  ItemStorageBaseSchema,
  ItemSummarySchema
} from "@/api/types/items.ts";
import itemAddedEventBus from "@/services/itemAddedEventBus.ts";
import {toISODateString} from "@/utils/date.ts";


const {t} = useI18n()
const {textFieldStyling, btnStyle, selectStyling, numberInputStyling, dateInputStyling, textAreaStyle} = useAppStyling()
const {getStorageIcon} = useStorageHelper()
const {items: itemEndpoint, storage: storageEndpoint} = useAxios()
const {forceNavigation} = useModal()
const route = useRoute()
const nameRules = ref([
  (v: string|null|ItemSummarySchema) => {
    if (!v) {
      return t('create.item.form.name_required')
    }
    if (typeof v === 'object') {
      return !!(v as ItemSummarySchema).name?.trim() || t('create.item.form.name_required')
    }
    return !!String(v).trim() || t('create.item.form.name_required')
  }
])
const quantityRules = ref([
  (v: number | null | undefined) => v != null || t("create.item.form.quantity_required")
])
const notesRules = ref([
  (v: string|null) => (v ?? '').length < 1024 || t('create.item.form.notes_too_long')
])
const descriptionRules = ref([
  (v: string|null) => (v ?? '').length < 1024 || t('create.item.form.description_too_long')
])
const parentRules = ref([
  (v: StorageResponseSchema|null) => !!v || t('create.item.form.parent_needed')
])

const form = useTemplateRef("form")

const item = ref<string|null|ItemSummarySchema>()
const parent = ref<StorageResponseSchema|null>(null)
const quantity = ref<number>(0)
const loading = ref<boolean>(false)
const loadingParents = ref<boolean>(false)
const loadingCategories = ref<boolean>(false)
const parents = ref<StorageResponseSchema[]>([])
const items = ref<ItemSummarySchema[]>([])
const expiryDate = ref<Date|null>()
const serialNumber = ref<string|null>()
const batch = ref<string|null>()
const notes = ref<string|null>()
const selectedCategories = ref<string[]>([])
const categories = ref<CategoryReadSchema[]>([])
const description = ref<string|null>()


const itemFieldsDisabled = computed(() => {
  return !(typeof item.value == 'string' || !item.value)
})


const emit = defineEmits<{
  (e: 'close'): void
}>()


const checkIfNewItem = () => {
  if( typeof item.value == 'string' || !item.value){
    selectedCategories.value = []
    description.value = null
    return
  }
  let currItem = item.value as ItemSummarySchema
  selectedCategories.value = (currItem.categories ?? []).map(cat => cat.id)
  description.value = currItem.description
}

const handleCreateNewItem = async () => {
  let newItem: ItemCreateSchema = {
    name: item.value as string,
    description: description.value,
    categories: selectedCategories.value,
    attributes: {
      expiration_date: toISODateString(expiryDate.value ?? null),
      serial_number: serialNumber.value,
      batch_code: batch.value,
      notes: notes.value
    } as ItemAttributesBaseSchema,
    storage: {
      storage_id: parent.value!.id,
      quantity: quantity.value,
    } as ItemStorageBaseSchema
  } as ItemCreateSchema
  loading.value = true
  console.log(newItem)
  const {success, data, error} = await itemEndpoint.createNewItem(newItem)
  if(!success){
    // TODO NOTIFY
  }
  if(data){
    items.value.push({
      ...data,
      total_quantity: 0
    })
  }
  loading.value = false
  return true
}

const handleAddItemInstance = async () => {
  let newItem: ItemInstanceCreate = {
    attributes: {
      expiration_date: toISODateString(expiryDate.value ?? null),
      serial_number: serialNumber.value,
      batch_code: batch.value,
      notes: notes.value
    } as ItemAttributesBaseSchema,
    storage: {
      storage_id: parent.value!.id,
      quantity: quantity.value,
    } as ItemStorageBaseSchema
  }
  loading.value = true
  const {success, data, error} = await itemEndpoint.createItemInstance((item.value as ItemSummarySchema).id, newItem)
  if(!success){
    // TODO NOTIFY
  }
  loading.value = false
  return true
}

const saveProduct = async () => {
  //@ts-expect-error
  const { valid } = await form.value.validate()
  if(!valid){
    return false
  }
  let ret
  let id: string|undefined = undefined
  if (typeof item.value === 'object'){
    ret = await handleAddItemInstance()
    id = item.value!.id
  } else {
    ret = await handleCreateNewItem()
  }

  if(ret && route.path.startsWith("/items")){
    itemAddedEventBus.emit(id)
  }

  form.value.reset()
  return ret
}

const saveAndClose = () => {
  saveProduct().then((success: boolean) => {
    if(success){
      forceNavigation.value = true
      emit('close')
    }
  })
}

const close = () => {
  emit('close')
}


const loadItems = async () => {
  loading.value = true
  const {success, data, error} = await itemEndpoint.getAllItemsSummary()
  if(!success){
    // TODO ERROR
  }
  items.value = (data ?? []) as ItemSummarySchema[]
  loading.value = false
}

const loadStorage = async () => {
  loadingParents.value = true
  const {success, data, error} = await storageEndpoint.getAllStorage()
  if(success){
    // TODO ERROR
  }
  parents.value = (data ?? []) as StorageResponseSchema[]
  loadingParents.value = false
}

const loadCategories = async() => {
  loadingCategories.value = true
  const {success, data, error} = await itemEndpoint.getAllCategories()
  if(!success){
    // TODO ERROR
  }
  categories.value = (data ?? []) as CategoryReadSchema[]
  loadingCategories.value = false
}

onBeforeMount(() => {
  loadStorage()
  loadItems()
  loadCategories()
})
</script>

<template>
  <v-card
      :loading="loading || loadingParents || loadingCategories"
      :disabled="loading || loadingParents || loadingCategories"
  >
    <template v-slot:append>
      <v-icon-btn
          icon="mdi-close"
          @click="close"
      />
    </template>
    <template v-slot:title>
      {{ t('create.item.title') }}
    </template>

    <v-card-text>
      <v-form
          @submit.prevent=""
          ref="form"
      >
        <v-row>
          <v-col
            cols="12"
          >
            <v-combobox
                v-model="item"
                v-bind="selectStyling"
                :items="items"
                :label="t('create.item.form.name')"
                item-title="name"
                :hide-no-data="false"
                hide-selected
                :loading="loading"
                :rules="nameRules"
                @update:model-value="checkIfNewItem"
            >
              <template v-slot:no-data>
                <v-list-item>
                  <v-list-item-title
                      v-if="typeof item === 'string' && item.trim() !== ''"
                  >
                    {{ t('create.item.form.new_item')}}
                    <p class="text-primary font-weight-bold d-inline">{{item}}</p>
                  </v-list-item-title>
                  <v-list-item-title
                      v-else
                  >
                    {{ t('create.item.form.start_typing') }}
                  </v-list-item-title>

                </v-list-item>
              </template>
            </v-combobox>
          </v-col>
          <template v-if="!itemFieldsDisabled">
            <v-col
                cols="12"

            >
              <v-textarea
                  v-bind="textAreaStyle"
                  :label="t('create.item.form.description')"
                  :counter="1024"
                  :rules="descriptionRules"
                  v-model="description"
                  :disabled="itemFieldsDisabled"
              />
            </v-col>
            <v-col
                cols="12"
            >
              <v-select
                  v-bind="selectStyling"
                  v-model="selectedCategories"
                  :label="t('create.item.form.categories')"
                  :items="categories"
                  :loading="loadingCategories"
                  item-title="name"
                  item-value="id"
                  multiple
                  :disabled="itemFieldsDisabled"
              >
                <template v-slot:selection="{ item, index }">
                  <v-chip
                      v-if="index < 2"
                      :text="item.title"
                      density="comfortable"
                  />
                  <v-chip
                      v-if="index === 2"
                      density="comfortable"
                      :text="t('create.item.form.categories_overflow', categories.length - 2)"
                  />
                </template>
              </v-select>
            </v-col>
          </template>
          <v-col
            cols="12"
          >
            <v-select
                v-bind="selectStyling"
                v-model="parent"
                :label="t('create.item.form.parent')"
                :items="parents"
                :loading="loadingParents"
                item-title="name"
                item-value="id"
                return-object
                :rules="parentRules"
            >
              <template v-slot:item="{ props: itemProps, item }">
                <v-list-item
                    v-bind="itemProps"
                    :prepend-icon="getStorageIcon(item.raw.storage_type)"
                ></v-list-item>
              </template>
            </v-select>
          </v-col>
          <v-col
            cols="12"
          >
            <v-number-input
              v-bind="numberInputStyling"
              v-model="quantity"
              control-variant="split"
              :min="0"
              :rules="quantityRules"
              :precision="0"
              :label="t('create.item.form.quantity')"
            />
          </v-col>
          <v-col cols="12">

            <v-date-input
              v-bind="dateInputStyling"
              v-model="expiryDate"
              :label="t('create.item.form.expiry_date')"
            />
          </v-col>
          <v-col
            cols="12"
          >
            <v-text-field
              v-bind="textFieldStyling"
              :label="t('create.item.form.batch')"
              v-model="batch"
            />
          </v-col>
          <v-col
              cols="12"
          >
            <v-text-field
                v-bind="textFieldStyling"
                :label="t('create.item.form.serial_number')"
                v-model="serialNumber"
            />
          </v-col>
          <v-col
              cols="12"
          >
            <v-textarea
                v-bind="textAreaStyle"
                :label="t('create.item.form.notes')"
                :counter="1024"
                :rules="notesRules"
                v-model="notes"
            />
          </v-col>
        </v-row>

      </v-form>
    </v-card-text>

    <v-card-actions>
      <v-btn
          v-bind="btnStyle"
          :text="t('create.item.form.save')"
          @click="saveProduct"
          :disabled="loadingParents"
      />
      <v-btn
          v-bind="btnStyle"
          :text="t('create.item.form.save_and_close')"
          @click="saveAndClose"
          :disabled="loadingParents"
      />
    </v-card-actions>
  </v-card>
</template>

<style scoped lang="scss">

</style>