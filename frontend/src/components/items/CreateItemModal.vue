<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";
import {useTemplateRef} from "vue";
import {VForm} from "vuetify/components";
import {useModal} from "@/composables-new/useModal.ts";
import {StorageResponseSchema} from "@/api/types/storage.ts";
import {ItemSummarySchema} from "@/api/types/items.ts";

const {t} = useI18n()
const {textFieldStyling, btnStyle, selectStyling, numberInputStyling, dateInputStyling} = useAppStyling()
const {getStorageIcon} = useStorageHelper()
const {items: itemEndpoint, storage: storageEndpoint} = useAxios()
const {forceNavigation} = useModal()

const nameRules = ref([
  (v: string|null) => !!v || t('create.item.form.name_required')
])
const quantityRules = ref([
  (v: number | null | undefined) => v != null || t("create.item.form.quantity_required")
])

const name = ref<string|null|ItemSummarySchema>()
const parent = ref<StorageResponseSchema|null>(null)
const quantity = ref<number>(0)
const form = useTemplateRef("form")
const loading = ref<boolean>(false)
const loadingParents = ref<boolean>(false)
const parents = ref<StorageResponseSchema[]>([])
const items = ref<ItemSummarySchema[]>([])
const expiryDate = ref<Date|null>()

const selectionPage = ref<boolean>(true)
const addNewItem = ref<boolean>(false)

const onClickAddNew = () => {
  addNewItem.value = true
  selectionPage.value = false
}

const onClickAddInstance = () => {
  addNewItem.value = false
  // TODO load items here
  selectionPage.value = false
}

const emit = defineEmits<{
  (e: 'close'): void
}>()

const saveRoom = async () => {
  //@ts-expect-error
  const { valid } = await form.value.validate()
  if(!valid){
    return false
  }
  return false
  /*loading.value = true
  const {success, data, error} = await storageEndpoint.createStorage({
    name: name.value!,
    storage_type: "room"
  })
  if(!success){
    // TODO RETURN TO ERROR
    forceNavigation.value = true
    await router.push("/error")
    return false
  }
  loading.value = false

  if(route.path === "/rooms"){
    roomAddedEventBus.emit()
  }
  name.value = null
  return true*/
}

const saveAndClose = () => {
  saveRoom().then((success: boolean) => {
    if(success){
      forceNavigation.value = true
      emit('close')
    }
  })
}

const close = () => {
  emit('close')
}

onBeforeMount(() => {
  loadingParents.value = true
  storageEndpoint.getAllStorage().then(({success, data, error}) => {
    if(success){
      // TODO ERROR
    }
    parents.value = (data ?? []) as StorageResponseSchema[]
    loadingParents.value = false
  })
})
</script>

<template>
  <v-card
      :loading="loading"
      :disabled="loading"
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
    <v-card-text
        class="d-flex flex-column justify-center fill-height"
        v-if="selectionPage"
    >
      <v-btn
          v-bind="btnStyle"
          :text="t('create.items.create_new')"
          variant="tonal"
          @click="onClickAddNew"
      />
      <v-divider class="mt-4 mb-4"/>
      <v-btn
          v-bind="btnStyle"
          :text="t('create.items.add_instance')"
          variant="tonal"
          @click="onClickAddInstance"
      />
    </v-card-text>
    <v-card-text v-else>
      <v-form
          @submit.prevent=""
          ref="form"
      >
        <v-row>
          <v-col
            cols="12"
          >
            <v-text-field
                v-if="addNewItem"
                v-bind="textFieldStyling"
                v-model="name"
                :label="t('create.item.form.name')"
                :rules="nameRules"
            />
            <v-select
                v-else
                :items="items"
            />
          </v-col>
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
            />
          </v-col>
          <v-col
              cols="12"
          >
            <v-text-field
                v-bind="textFieldStyling"
                :label="t('create.item.form.serial_number')"
            />
          </v-col>
          <v-col
              cols="12"
          >
            <v-text-area
                v-bind="textFieldStyling"
                :label="t('create.item.form.serial_number')"
            />
          </v-col>
        </v-row>

      </v-form>
    </v-card-text>

    <v-card-actions
      v-if="!selectionPage"
    >
      <v-btn
          v-bind="btnStyle"
          :text="t('create.item.form.save')"
          @click="saveRoom"
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