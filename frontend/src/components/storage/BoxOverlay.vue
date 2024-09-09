<script setup lang="ts">
import {useProducts, useStorage} from "@/store";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import {computed, onMounted, ref} from "vue";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, LocationEndpoint} from "@/api/http";
import {ApiProduct, ApiStorage} from "@/types";
import useEditBtnStyle from "@/composables/useEditBtnStyle.ts";
import {useI18n} from "vue-i18n";
import ProductOverlay from "@/components/products/ProductOverlay.vue";
import useDialogConfig from "@/composables/useDialogConfig.ts";

const storageStore = useStorage()
const productStore = useProducts()
const {redirect} = useRedirectToStorage()
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {editClicked, editBtnStyle} = useEditBtnStyle()
const {t} = useI18n()
const { isVisible: productDetailOverlayVisible, openDialog, closeDialog, dialogProps } = useDialogConfig()



const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'deleted', id: number): void
}>()

const box = computed(() => {
  return storageStore.selectedBox ?? ({} as ApiStorage)
})
const boxName = computed({
  get(){
    if(newName.value !== undefined){
      return newName.value
    }
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
  return productStore.products
})


const {name, icon} = useStorageTitle(boxStoredAt)

const loadingStorage = ref(false)
const locations = ref<Array<ApiStorage>>([])
const nameRequiredRule = (value: string) => value !== '' || t('boxes.box.rules.new_name_empty')
const newName = ref<string|undefined>(undefined)
const newStorage = ref<ApiStorage|undefined>(undefined)
const saving = ref(false)
const deleting = ref(false)
const loadingProducts = ref(false)

function cancelEdit(){
  newName.value = undefined
  newStorage.value = undefined
  editClicked.value = false
}

function close(){
  editClicked.value = false
  emit("close")
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
    deleting.value = false
    if(!success){
      return
    }

    emit('deleted', box.value.id)
  })
}

function displayProductOverlay(item: ApiProduct){
  productStore.selectProduct(item)
  openDialog()
}

function closeDetailOverlay(){
  closeDialog()
  productStore.deselectProduct()
}

function deleteProduct(id: number){
  closeDialog()
  productStore.deleteProduct(id)
  storageStore.removeProductfromBox(box.value.id)
}

onMounted(() => {
  loadingStorage.value = true
  locationEndpoint.getLocations().then((loc: Array<ApiStorage>) => {
    loadingStorage.value = false
    locations.value = loc
  })

  loadingProducts.value = true
  boxEndpoint.getContent(box.value.id).then(({products}) => {
    productStore.setStorage(box.value.id)
    productStore.storeProducts(products)
  })
})
</script>

<template>
  <v-dialog
      v-model="productDetailOverlayVisible"
      v-bind="dialogProps"
  >
    <product-overlay
        @close="closeDetailOverlay()"
        @deleted="deleteProduct"
    />
  </v-dialog>
  <v-card
      class="position-relative d-flex flex-column fill-height"
  >
    <v-card-title
        class="d-flex align-center justify-space-between"
    >
      <div v-if="!editClicked">
        {{ boxName }}
      </div>
      <div style="width: 80%" v-else>
        <app-overlay-title
            v-model="boxName"
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
    <v-card-subtitle>
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
    <v-card-text
      class="flex-1-1 pt-0 pl-4 pr-4 overflow-hidden"
    >
      <RecycleScroller
          :items="productsStoredInBox"
          :item-size="110"
          style="height: 100%;"
      >
        <template v-slot="{item}">
          <product-card
              :total-amount="item.totalAmount"
              :id="item.id"
              :creation-date="item.creationDate"
              :name="item.name"
              @expand="displayProductOverlay(item)"
          />
        </template>
        <template #after>
          <v-row
              :no-gutters="true"
              justify="center"
          >
            <p>
              {{ $t("boxes.box.all_displayed")}}
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
  </v-card>
</template>

<style scoped lang="scss">

</style>