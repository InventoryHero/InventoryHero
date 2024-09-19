<script setup lang="ts">
import {useProducts} from "@/store";
import {computed, onMounted, ref} from "vue";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import useAxios from "@/composables/useAxios.ts";
import {StorageEndpoint} from "@/api/http";
import {ApiStorage} from "@/types/api.ts";
import useUpdateProductStoredAt from "@/composables/useModifyProductStoredAt.ts";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";
import {useNotification} from "@kyvg/vue3-notification";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";
import useConfirmationSetup from "@/composables/useConfirmationSetup.ts";


const productStore = useProducts()
const {axios: storageEndpoint} = useAxios<StorageEndpoint>("storage")
const {saving, deleting, updateStoredAt, deleteStoredAt} = useUpdateProductStoredAt()
const {redirect} = useRedirectToStorage()
const {notify} = useNotification()
const {t} = useI18n()
const {goBackOneLevel} = useGoBackOneLevel()



const loading = computed(() => productStore.loadingProducts || productStore.loadingProductStorage)
const loadingStorage = ref(false)
const allStorage = ref<Array<ApiStorage>>([])
const newStorage = ref<ApiStorage | undefined>(undefined)
const editClicked = ref(false)


const product = computed(() => {
  return productStore.selectedProduct
})

const productName = computed(() => {
  return product.value?.name
})

const currProductAt = computed(() => {
  return productStore.selectedProductStorage
})

const storage = computed({
  get(){
    if(newStorage.value !== undefined){
      return newStorage.value
    }
    return productStore.selectedProductStorage?.storage ?? undefined
  },
  set(value: ApiStorage|undefined){
    newStorage.value = value
  }
})



const {name, icon} = useStorageTitle(storage)

function close(){
  // TODO NOT BACK FOR ALL THE ROUTES; IS CONFUSING WHEN BEING REDIRECTED FROM SOMEWHERE
  goBackOneLevel()
}



function cancelEdit(){
  newStorage.value = undefined
  editClicked.value = false

}
function saveChanges(){
  updateStoredAt(currProductAt.value!, {
    storage: storage.value
  }).then((success: boolean) => {
    if(success){
      cancelEdit()
    }
  })
}

function deleteCurrent(){
  const id = currProductAt.value!.id
  const value = currProductAt.value!.amount
  deleteStoredAt(currProductAt.value!).then((success) => {
    if(!success){
      return
    }
    goBackOneLevel().then(() => {
      productStore.deleteProductAt(id, value)
      notify({
        title: t('toasts.titles.success.deleted_detail'),
        text: t('toasts.text.success.deleted_detail'),
        type: "success"
      })
    })

  })
}
const {
  confirmationDialog: deleteConfirmDialog,
  saveAction: saveDelete,
  reallyDo: reallyDelete
} = useConfirmationSetup(deleteCurrent)


onMounted(() => {
  loadingStorage.value = true
  storageEndpoint.getStorageType().then((response: Array<ApiStorage>) => {
    loadingStorage.value = false
    allStorage.value = response
  })
})

</script>

<template>
  <confirmation-dialog
      v-model:dialog-opened="deleteConfirmDialog"
      :title="$t('products.delete_detail.title', {storage: storage?.storage?.name ?? 'void'})"
      :text="$t('products.delete_detail.text')"
      :cancel-text="$t('products.delete_detail.cancel')"
      :confirm-text="$t('products.delete_detail.confirm')"
      confirm-icon="mdi-delete-outline"
      cancel-icon="mdi-cancel"
      :on-cancel="() => deleteConfirmDialog = false"
      :on-confirm="reallyDelete"
  />
  <v-card
      class="position-relative d-flex flex-column fill-width fill-height"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="saving || deleting || loading"
          color="primary"
      />
    </template>

    <template v-if="!loading">
      <app-content-title
          v-model:title="productName"
          v-model:edit="editClicked"
          :disabled="saving||deleting||loading"
          @close="close()"
      />
      <v-card-subtitle >
        <app-storage-title
            :icon="icon"
            :title="name"
            color="primary"
            @click="redirect(storage, productName ?? '')"
            v-if="!editClicked"
            :disabled="loading"
        />
        <app-storage-select
            class="mt-1"
            v-model="storage"
            :storage="allStorage"
            :storage-loading="loadingStorage"
            v-else
        />
      </v-card-subtitle>
      <v-card-text class="flex-1-1 pt-0 pl-4 pr-4 overflow-hidden">
        <!-- TODO amount adjustment needs to be handled here -->
      </v-card-text>
      <app-content-actions
          :active="editClicked"
          @cancel="cancelEdit"
          @delete="saveDelete"
          @save="saveChanges"
          :saving="saving"
          :deleting="deleting"
      />

    </template>
    <app-content-scroll-after
      class="mt-2"
      v-else
      :text="$t('products.loading')"
    />
  </v-card>

</template>
<style scoped lang="scss">

</style>