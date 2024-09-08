<script setup lang="ts">

import {useProducts, useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {LocationEndpoint} from "@/api/http";
import useEditBtnStyle from "@/composables/useEditBtnStyle.ts";
import {useI18n} from "vue-i18n";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {computed, onMounted, ref, watch} from "vue";
import {ApiProduct, ApiStorage, StorageTypes} from "@/types";
import ProductOverlay from "@/components/products/ProductOverlay.vue";

interface LocationContent {
  item: ApiProduct | ApiStorage,
  id: string,
  type: StorageTypes | string
}

const storageStore = useStorage()
const productStore = useProducts()

const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const {editClicked, editBtnStyle} = useEditBtnStyle()
const {t} = useI18n()
const {
  isVisible: productDetailOverlayVisible,
  openDialog: openProductDialog,
  closeDialog: closeProductDialog,
  dialogProps: productDialogProps
} = useDialogConfig()

const {
  isVisible: boxDialogVisible,
  openDialog: openBoxDialog,
  closeDialog: closeBoxDialog,
  dialogProps: boxDialogProps
} = useDialogConfig()

const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'deleted', id: number): void
}>()


const locationContent = computed(() => {
  return [
      ...productStore.products.map(product => ({
        item: product,
        id: `product${product.id}`,
        type: 'product'
      })),
      ...storageStore.boxes.map(box => ({
        item: box,
        id: `box${box.id}`,
        type: StorageTypes.Box
      }))
  ] as Array<LocationContent>
})

const locationName = computed({
  get(){
    if(newName.value !== undefined){
      return newName.value
    }
    return storageStore.selectedLocation?.name
  },
  set(value: string){
    newName.value = value
  }
})


const loadingContent = ref(false)
const saving = ref(false)
const deleting = ref(false)
const newName = ref<string|undefined>(undefined)
const nameRequiredRule = (value: string) => value !== '' || t('locations.location.rules.new_name_empty')


const location = computed(() => {
  return storageStore.selectedLocation ?? ({} as ApiStorage)
})

function close(){
  editClicked.value = false
  emit("close")
}
function cancelEdit(){
  newName.value = undefined
  editClicked.value = false
}
function saveChanges(){
  if(newName.value === ''){
    return
  }
  saving.value = true
  locationEndpoint.updateLocation(location.value?.id, {
    name: newName.value
  }).then(({updated}) => {
    if(updated){
      storageStore.updateLocation(updated)
    }
    saving.value = false
    cancelEdit()
  })

}
function deleteLocation(){
  deleting.value = true
  locationEndpoint.deleteStorage(location.value.id).then((success) => {
    deleting.value = false
    if(!success){
      return
    }
    emit('deleted', location.value.id)
  })
}
function displayProductOverlay(item: ApiProduct){
  productStore.selectProduct(item)
  openProductDialog()
}
function deleteProduct(id: number){
  closeProductDialog()
  productStore.deleteProduct(id)
  storageStore.removeProductFromLocation(location.value.id)
}
function closeProductOverlay(){
  closeProductDialog()
  productStore.deselectProduct()
}

function openBoxOverlay(item: ApiStorage){
  storageStore.selectBox(item)
  openBoxDialog()
}

function loadContent(callback?: () => void){
  loadingContent.value = true
  locationEndpoint.getContent(location.value.id).then(({boxes, products}) => {
    productStore.setStorage(location.value.id)
    if(callback){
      callback()
    }
    storageStore.storeBoxes(boxes)
    productStore.storeProducts(products)
    loadingContent.value = false
  })
}

function deleteBox(id: number){
  closeBoxDialog()
  loadContent(() => {

    storageStore.deleteBox(id)
    storageStore.removeBoxFromLocation(location.value.id, id)
    storageStore.deselectBox()
  })
}
function closeBoxOverlay(){
  // reload the products as upon opening a box the products get reset...
  // this should automatically handle any relocations from a box etc.

  closeBoxDialog()
  loadContent(() => {

    storageStore.deselectBox()
  })
}

onMounted(() => {
  loadContent()
})


</script>

<template>
  <v-dialog
      v-model="productDetailOverlayVisible"
      v-bind="productDialogProps"
  >
    <product-overlay
        @close="closeProductOverlay()"
        @deleted="deleteProduct"
    />
  </v-dialog>
  <v-dialog
      v-model="boxDialogVisible"
      v-bind="boxDialogProps"
  >
    <box-overlay
        @close="closeBoxOverlay"
        @deleted="deleteBox"
    />
  </v-dialog>
  <v-card
      class="position-relative d-flex flex-column fill-height"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="loadingContent"
          color="primary"
      />
    </template>
    <v-card-title
        class="d-flex align-center justify-space-between"
    >
      <div v-if="!editClicked">
        {{ locationName }}
      </div>
      <div style="width: 80%" v-else>
        <app-overlay-title
            v-model="locationName"
            :rules="[nameRequiredRule]"
            :edit="editClicked"

        />
      </div>
      <div
          class="ms-4"
      >
        <app-icon-btn
            icon="mdi-pencil"
            variant="flat"
            class="me-2"
            v-bind="editBtnStyle"
            :disabled="saving||deleting"
            @click="editClicked = true"

        />
        <app-icon-btn
            icon="mdi-window-minimize"
            variant="flat"
            @click="close()"
            :disabled="saving||deleting"

      />

      </div>
    </v-card-title>
    <v-card-text
        class="flex-1-1 pt-0 pl-4 pr-4 overflow-hidden"
    >
      <RecycleScroller
          :items="locationContent"
          :item-size="90"
          style="height: 100%;"
      >
        <template v-slot="{item}">
          <product-card
              v-if="item.type === 'product'"
              :total-amount="item.item.totalAmount"
              :id="item.item.id"
              :creation-date="item.item.creationDate"
              :name="item.item.name"
              @expand="displayProductOverlay(item.item)"
          />
          <storage-card
              v-else
              v-bind:storage="item.item"
              :type="item.type"
              @click.stop="openBoxOverlay(item.item)"
          />
        </template>
        <template #after>
          <v-row
              :no-gutters="true"
              justify="center"
          >
            <p>
              {{ $t("locations.location.all_displayed")}}
            </p>
          </v-row>
        </template>
      </RecycleScroller>

    </v-card-text>
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
            :title="$t('locations.confirm.delete.title')"
            :body="$t('locations.confirm.delete.body')"
            :confirm-text="$t('confirm.actions.proceed')"
            :refuse-text="$t('confirm.actions.abort')"
            :text="$t('delete')"
            prepend-icon="mdi-trash-can"
            variant="outlined"
            color="red"
            class="me-2"
            :disabled="saving"
            :loading="deleting"
            @consent="deleteLocation"

        />
        <app-confirm-button
            :title="$t('locations.confirm.save.title')"
            :body="$t('locations.confirm.save.body')"
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
  </v-card>

</template>

<style scoped lang="scss">

</style>