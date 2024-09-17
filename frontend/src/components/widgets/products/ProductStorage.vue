<script setup lang="ts">
import {useProducts} from "@/store";
import {computed, onMounted, ref} from "vue";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import useAxios from "@/composables/useAxios.ts";
import {StorageEndpoint} from "@/api/http";
import {ApiStorage} from "@/types/api.ts";
import useUpdateProductStoredAt from "@/composables/useModifyProductStoredAt.ts";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";
import useEditBtnStyle from "@/composables/useEditBtnStyle.ts";
import useGoBackOneLevel from "@/composables/useGoBackOneLevel.ts";
import {useNotification} from "@kyvg/vue3-notification";


const productStore = useProducts()
const {axios: storageEndpoint} = useAxios<StorageEndpoint>("storage")
const {saving, deleting, updateStoredAt, deleteStoredAt} = useUpdateProductStoredAt()
const {redirect} = useRedirectToStorage()
const {editClicked, editBtnStyle} = useEditBtnStyle()
const {goBackOneLevel} = useGoBackOneLevel({hasId: true})
const {notify} = useNotification()
const {t} = useI18n()



const loading = computed(() => productStore.loadingProducts || productStore.loadingProductStorage)
const loadingStorage = ref(false)
const allStorage = ref<Array<ApiStorage>>([])
const newStorage = ref<ApiStorage | undefined>(undefined)


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
  goBackOneLevel()

}

function clickEditBtn(){
  editClicked.value = true
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
    notify({
      title: t('toasts.titles.success.deleted_detail'),
      text: t('toasts.text.success.deleted_detail'),
      type: "success"
    })
    goBackOneLevel().then(() => {
      productStore.deleteProductAt(id, value)
    })
  })
}

onMounted(() => {
  loadingStorage.value = true
  storageEndpoint.getStorageType().then((response: Array<ApiStorage>) => {
    loadingStorage.value = false
    allStorage.value = response
  })
})

</script>

<template>
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
      <v-card-title
          class="d-flex align-center justify-space-between"
      >
        <div>
          {{ productName }}
        </div>
        <div
            class="ms-4"
        >
          <app-icon-btn
              icon="mdi-pencil"
              v-bind="editBtnStyle"
              :disabled="saving"
              @click="clickEditBtn"

          />
          <app-icon-btn
              icon="mdi-close"
              :disabled="saving"
              @click="close()"
          />

        </div>
      </v-card-title>
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
      <v-card-actions
          v-if="editClicked"
          class="d-flex justify-space-between"
      >
        <v-btn
            prepend-icon="mdi-cancel"
            @click="cancelEdit"
            :text="$t('cancel')"
            :disabled="saving"
        />
        <div>
          <app-confirm-button
              :title="$t('products.confirm.product.delete.title')"
              :body="$t('products.confirm.product.delete.body')"
              :confirm-text="$t('confirm.actions.proceed')"
              :refuse-text="$t('confirm.actions.abort')"
              :text="$t('delete')"
              prepend-icon="mdi-trash-can"
              variant="outlined"
              color="red"
              class="me-2"
              :disabled="saving"
              :loading="deleting"
              @consent="deleteCurrent"

          />
          <app-confirm-button
              :title="$t('products.confirm.product.save.title')"
              :body="$t('products.confirm.product.save.body')"
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
    </template>
    <v-card-text
        v-else
    >
      {{ $t('products.loading') }}
    </v-card-text>
  </v-card>

</template>
<style scoped lang="scss">

</style>