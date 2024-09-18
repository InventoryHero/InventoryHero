<script setup lang="ts">
import {useProducts, useStorage} from "@/store";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import {computed, onMounted, ref} from "vue";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, LocationEndpoint} from "@/api/http";
import {ApiProduct, ApiStorage, StorageTypes} from "@/types";
import {useI18n} from "vue-i18n";
import ProductStorageCard from "@/components/widgets/products/Cards/ProductStorageCard.vue";

const storageStore = useStorage()
const productStore = useProducts()
const {redirect} = useRedirectToStorage()
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {t} = useI18n()
const router = useRouter()
const route = useRoute()

provide("storageType", StorageTypes.Box)


const box = computed(() => {
  console.log(storageStore.selectedBox)
  return storageStore.selectedBox ?? ({} as ApiStorage)
})
const boxName = computed({
  get(){
    if(newName.value !== undefined){
      return newName.value
    }
    console.log(storageStore.selectedBox)
    return storageStore.selectedBox?.name
  },
  set(value: string){
    newName.value = value
  }
})

const boxStoredAt = computed({
  get(){
    if(newStorage.value !== undefined){
      return newStorage.value
    }
    return storageStore.selectedBox?.storage ?? undefined
  },
  set(value: ApiStorage|undefined){
    newStorage.value = value
  }
})

const productsStoredInBox = computed(() => {
  return productStore.productStorage
})


const {name, icon} = useStorageTitle(boxStoredAt)

const loadingStorage = ref(false)
const locations = ref<Array<ApiStorage>>([])
const nameRequiredRule = (value: string) => value !== '' || t('boxes.box.rules.new_name_empty')
const newName = ref<string|undefined>(undefined)
const newStorage = ref<ApiStorage|undefined>(undefined)
const saving = ref(false)
const deleting = ref(false)
const editClicked = ref(false)

const loadingProducts = computed(() => storageStore.loadingContent)
const loadingBox = computed(() => storageStore.loadingStorage || loadingStorage.value)

function cancelEdit(){
  newName.value = undefined
  newStorage.value = undefined
  editClicked.value = false
}

function close(){
  editClicked.value = false
  router.back()
}

function saveChanges(){

  if(newName.value === ''){
    return
  }
  saving.value = true
  boxEndpoint.updateBox(box.value?.id, {
    name: newName.value,
    storageId: boxStoredAt.value?.id
  }).then(({updated}) => {
    if(updated){
      storageStore.updateBox(updated)
      cancelEdit()
    }
    saving.value = false
  })
}

function deleteBox(){
  deleting.value = true
  boxEndpoint.deleteStorage(box.value.id).then((success) => {
    if(!success){
      return
    }
    router.back()
    deleting.value = false
    storageStore.deleteBox(box.value.id)
  })
}

function displayProductOverlay(item: ApiProduct){
 // scrollStore.pushPosition(route.fullPath, storedAt.value.findIndex(p => p.id === item.id))
  router.push(`${route.fullPath}/product/${item.id}`)
}


function deleteProduct(productId: number, productStorageId: number, amount: number){
  productStore.deleteProductAt(productStorageId, amount)
  productStore.deleteProduct(productId)
}

onMounted(() => {
  loadingStorage.value = true
  locationEndpoint.getLocations().then((loc: Array<ApiStorage>) => {
    locations.value = loc
    loadingStorage.value = false
  })

})
</script>

<template>
  <v-card
      class="position-relative d-flex flex-column fill-height fill-width"
      :disabled="loadingBox || deleting"
  >
    <template v-slot:loader>
      <v-progress-linear
        indeterminate
        :active="loadingBox || loadingProducts || deleting"
        color="primary"
      />
    </template>
    <template v-if="!loadingBox && !deleting">
      <app-content-title
          v-model:title="boxName"
          v-model:edit="editClicked"
          :rules="[nameRequiredRule]"
          :disabled="saving||deleting||loadingBox"
          @close="close()"
          edit-toggles-textfield
      />
      <v-card-subtitle >
        <app-storage-title
            :icon="icon"
            :title="name"
            color="primary"
            @click="redirect(boxStoredAt, boxName ?? '', 'box')"
            v-if="!editClicked"
            :disabled="saving||deleting"
        />
        <app-storage-select
            class="mt-1"
            v-model="boxStoredAt"
            :storage="locations"
            :disabled="saving||deleting"
            v-else
        />
      </v-card-subtitle>

      <div
        class="flex-1-1 position-relative"
      >
        <v-card-text
          class="wrapper pt-0"
        >
          <RecycleScroller

            class="scroll"
            ref="scroller"
            :items="productsStoredInBox"
            :item-size="104"
          >
            <template v-slot="{item}">

              <product-storage-card
                :storage="item"
                from-storage

                @show-stored-at-detail="displayProductOverlay(item)"
                @deleted="deleteProduct(item.productId, item.id, item.amount)"
                @redirect="console.log('lets go to products')"

              />
            </template>
            <template #after>
              <v-row
                  dense
                  justify="center"
                  class="mt-2"
              >
                <span
                    v-if="loadingProducts"
                >
                  {{ t('boxes.loading_content') }}
                </span>
                <span
                  v-else
                >
                  {{ $t("boxes.box.all_displayed")}}
                </span>
              </v-row>
            </template>
          </RecycleScroller>
        </v-card-text>
      </div>
      <v-card-actions
          v-if="editClicked"
          class="d-flex justify-space-between"
      >
        <v-btn
            prepend-icon="mdi-cancel"
            @click="cancelEdit"
            :text="$t('cancel')"
            :disabled="saving||deleting"
        />
        <div>
          <app-confirm-button
              :title="$t('boxes.confirm.delete.title')"
              :body="$t('boxes.confirm.delete.body')"
              :confirm-text="$t('confirm.actions.proceed')"
              :refuse-text="$t('confirm.actions.abort')"
              :text="$t('delete')"
              prepend-icon="mdi-trash-can"
              variant="outlined"
              color="red"
              class="me-2"
              :disabled="saving"
              :loading="deleting"
              @consent="deleteBox"

          />
          <app-confirm-button
              :title="$t('boxes.confirm.save.title')"
              :body="$t('boxes.confirm.save.body')"
              :confirm-text="$t('confirm.actions.proceed')"
              :refuse-text="$t('confirm.actions.abort')"
              :text="$t('save')"
              prepend-icon="mdi-content-save-all"
              color="primary"
              variant="elevated"
              :loading="saving"
              :disabled="deleting"
              @consent="saveChanges"
          />
        </div>
      </v-card-actions>
      <v-card-actions v-else>
        <app-storage-qr-code-btn
            color="primary"
            use-preselected
        /></v-card-actions>
    </template>
    <v-row
        v-else
        dense
        justify="center"
        class="align-center"
    >
      {{ t('boxes.loading_box' )}}
    </v-row>
  </v-card>
</template>

<style scoped lang="scss">

</style>