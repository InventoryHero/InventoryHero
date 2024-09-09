<script setup lang="ts">
import {useProducts, useStorage} from "@/store";
import {ApiProduct, ApiStorage, ProductStorageMapping} from "@/types";
import {useI18n} from "vue-i18n";
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import useHint from "@/composables/useHint.ts";
import {useTemplateRef} from "vue";

const storageStore = useStorage()
const productStore = useProducts()
const {axios: productEndpoint} = useAxios<ProductEndpoint>('product')

const {t} = useI18n()
const {notify} = useNotification()

const resourcesLoading = inject<{
 loadingProducts: boolean,
 loadingBoxes: boolean,
 loadingLocations: boolean
}>('loading')
const addForm = useTemplateRef('add-form')
const combobox = useTemplateRef('combobox')
const postingProduct = ref(false)

const newProduct = ref<ApiProduct|string|null>(null)
const amount = ref(0)
const newStarred = ref<boolean|undefined>(undefined)
const selectedStorage = ref<ApiStorage|undefined>(undefined)

const products = computed(() => {
  return productStore.products
})
const storage = computed(() => {
  return [
      ...storageStore.locations,
      ...storageStore.boxes
  ]
})
const starred = computed({
  get(){
    if(newStarred.value === undefined){
      if(Object.prototype.hasOwnProperty.call(newProduct.value ?? {}, 'starred'))
      {
        return (newProduct.value as ApiProduct).starred ?? false
      }
      return false
    }
    return newStarred.value
  },
  set(value: boolean){
    newStarred.value = value
  }
})

const {hintActive: comboboxHintActive, message: comboboxHint } = useHint(t(`add.product.hints.combobox`))
const {hintActive: locationSelectHintActive, message: locationSelectHint } = useHint(t(`add.product.hints.locationSelect`))
const {hintActive: amountHintActive, message: amountHint } = useHint(t(`add.product.hints.amount`))
const {hintActive: starHintActive, message: starHint } = useHint(t(`add.product.hints.star`))

const productsLoading = computed(() =>{
  return resourcesLoading?.loadingProducts ?? false
})

const storageLoading = computed(() =>{
  return (resourcesLoading?.loadingLocations ?? false) || (resourcesLoading?.loadingBoxes ?? false)
})

const rules = {
  isNumber: (value: string) => !isNaN(parseInt(value)) || t('add.product.rules.amount_nan'),
  positive: (value: number) => value >= 0 || t('add.product.rules.amount_negative'),
  needProduct: (value: string|null|undefined) => value !== null && value !== undefined && value !== '' || t('add.product.rules.need_product')
}



function notifySuccess(name: string, amount: number){
  notify({
    title: t('toasts.titles.success.add_product', {
      name: name,
      amount: amount
    }),
    text: t('toasts.text.success.add_product'),
    type: "success"
  })
}

function addExisting(){
  let product = newProduct.value! as ApiProduct
  let data = {
    productId: product.id,
    amount: amount.value,
    storageId: selectedStorage.value?.id
  } as Partial<ProductStorageMapping>

  let request = undefined
  if(starred.value !== product.starred){
    request = productEndpoint.addExistingProduct(data, true, starred.value)
  } else{
    request = productEndpoint.addExistingProduct(data, false)
  }
  request.then(({success}) => {
    postingProduct.value = false
    if(!success){
      return
    }
    notifySuccess(product.name, amount.value)
    if(starred.value !== product.starred){
      productStore.updateStarred(product.id)
    }

    clear()
  })

}

function addNew(){
  postingProduct.value = true
  if(newProduct.value === null || newProduct.value === '')
  {
    return
  }

  productEndpoint.createProduct(
      newProduct.value as string,
      amount.value,
      starred.value,
      selectedStorage.value?.id
  ).then(({success, product}) => {
    postingProduct.value = false
    if(!success){
      return;
    }
    notifySuccess(product!.name, amount.value)
    productStore.addProduct(product!)
    clear()
  })

}

async function save(){
  //@ts-expect-error - couldn't figure out how to type the form-ref properly
  const {valid} = await addForm.value.validate()
  if(!valid){
    return
  }
  postingProduct.value = true
  if(newProduct.value === null){
    return
  }
  if(Object.prototype.hasOwnProperty.call(newProduct.value ?? {}, 'id')){
    addExisting()
  } else{
    addNew()
  }

}

function clear(){
  //@ts-expect-error  - couldn't figure out how to type the form-ref properly
  addForm.value.reset()
  newStarred.value = undefined
}



</script>

<template>

  <create-card
      :title="t(`add.product.title`)"
      @save="save()"
      @clear="clear()"
      :request-in-progress="postingProduct"
  >
    <v-form
        @submit.prevent
        ref="add-form"
        :disabled="postingProduct"
    >

      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <v-combobox
              ref="combobox"
              :clearable="true"
              :persistent-clear="true"
              :hide-no-data="false"
              density="comfortable"
              auto-select-first="exact"
              v-model="newProduct"
              :label="t('add.product.labels.product')"
              :items="products"
              item-title="name"
              :rules="[rules.needProduct]"
              :disabled="productsLoading"
              @keydown.enter="() => {
                //@ts-expect-error
                combobox.blur()
            }"
              :messages="comboboxHint"
              :loading="productsLoading"

          >

            <template #no-data>
              <v-list-item>
                <v-list-item-title
                    v-if="newProduct !== null && newProduct !== '' && !newProduct.hasOwnProperty('id')"
                >
                  {{ t('add.product.new_product')}}
                  <p class="text-primary font-weight-bold d-inline">{{newProduct}}</p>
                </v-list-item-title>
                <v-list-item-title
                    v-else
                >
                  {{ t('add.product.start_typing')}}
                </v-list-item-title>

              </v-list-item>
            </template>
            <template #append>
              <app-help-indicator
                  v-model="comboboxHintActive"
              />
            </template>

          </v-combobox>
        </v-col>
      </v-row>
      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <app-storage-select
              :storage-loading="storageLoading"
              v-model="selectedStorage"
              :storage="storage"
              density="comfortable"
              :label="t('add.product.labels.location')"
              :hide-details="false"
              content-type="product"
              :messages="locationSelectHint"
          >
            <template #hint>
              <app-help-indicator
                  v-model="locationSelectHintActive"
              />
            </template>
          </app-storage-select>
        </v-col>
      </v-row>
      <v-row
          :no-gutters="true"
          class="mb-2 justify-space-between"
      >
        <v-col
            cols="7"
        >
          <v-text-field
              :messages="amountHint"
              type="number"
              density="comfortable"
              :label="t('add.product.labels.amount')"
              v-model.number="amount"
              :rules="[rules.isNumber, rules.positive]"
              class="num-input"
          >
            <template #append>
              <app-help-indicator
                  v-model="amountHintActive"
              />
            </template>
          </v-text-field>
        </v-col>
        <v-col

            cols="4"
        >
          <v-switch
              density="comfortable"
              v-model="starred"
              color="primary"
              :messages="starHint"
              :label="t('add.product.labels.star')"
          >
            <template #append>
              <app-help-indicator
                  v-model="starHintActive"
              />
            </template>
          </v-switch>

        </v-col>
      </v-row>

    </v-form>
  </create-card>



</template>

<style scoped lang="scss">

</style>