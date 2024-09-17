<script setup lang="ts">

import {useProducts} from "@/store"
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {ApiProduct, ProductStorageMapping} from "@/types/api.ts";
import ProductStorageCard from "@/components/widgets/products/ProductStorageCard.vue";
import {useI18n} from "vue-i18n";
import {useNotification} from "@kyvg/vue3-notification";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import StoredAtDetail from "@/components/widgets/products/StoredAtDetail.vue";

const productStore = useProducts()
const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
const i18n = useI18n()
const {notify} = useNotification();
const { isVisible: storedAtDetailOverlayVisible, openDialog, closeDialog, dialogProps } = useDialogConfig()



const emit = defineEmits<{
  (e: 'close'): void,
  (e: 'deleted', id: number): void
}>()


const product = computed(() => {
  return productStore.selectedProduct ?? ({} as ApiProduct)
})

const editBtnStyle = computed(() => {
  if(editClicked.value){
    return {
      color: "primary"
    }
  }
  return {
    color: ''
  }
})

const name = computed({
  get() {
    if(newName.value === undefined) {
      return product.value.name
    }
    return newName.value
  },
  set(newValue: string) {
    newName.value = newValue
  }
})

const storedAt = computed(() => {
  return productStore.productStorage
})

const loading = ref(false)
const editClicked = ref(false)
const newName = ref<string|undefined>(undefined)
const nameRequiredRule = (value: string) => value !== '' || i18n.t('products.product.rules.new_name_empty')
const saving = ref(false)
const deleting = ref(false)

function close(){
  emit('close')
}

function cancelEdit(){
  newName.value = undefined
  editClicked.value = false
}

async function saveChanges(){
  if(newName.value === product.value.name || newName.value === undefined){
    newName.value = undefined
    editClicked.value = false
    return
  }
  if(newName.value === '')
  {
    return false
  }
  saving.value = true
  let {success, updatedProduct} = await productEndpoint.updateProduct(product.value.id, {
    name: newName.value
  })
  saving.value = false
  if(!success){
    return false
  }

  if(updatedProduct !== undefined){
    productStore.updateProduct(updatedProduct)
  }
  newName.value = undefined
  editClicked.value = false

  notify({
    title: i18n.t('toasts.titles.success.updated_product'),
    text: i18n.t('toasts.text.success.updated_product'),
    type: "success"
  })
  return success
}

function closeDetail(){
  closeDialog()
  productStore.deselectProductStoredAt()
}
function deleteProduct(){
  deleting.value = true
  productEndpoint.deleteProduct(product.value.id).then((success) => {
    deleting.value = false
    if(!success){
      return
    }

    emit('deleted', product.value.id)
  })
}

function deleteSelected(id: number, amount: number){

  closeDialog()

  productStore.deleteProductAt(id, amount)
  notify({
    title: i18n.t('toasts.titles.success.deleted_detail'),
    text: i18n.t('toasts.text.success.deleted_detail'),
    type: "success"
  })
}

onMounted(() => {
  loading.value = true;
  productEndpoint.getProductStorage(product.value.id, productStore.storedAt).then((response: Array<ProductStorageMapping>) => {
    productStore.storeProductStorage(response)
    loading.value = false
  })
})
</script>

<template>
  <v-dialog
      v-model="storedAtDetailOverlayVisible"
      v-bind="dialogProps"
  >
    <stored-at-detail
      @close="closeDetail"
      @deleted="deleteSelected"
    />
  </v-dialog>


  <v-card
      class="position-relative d-flex flex-column fill-height"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="loading"
          color="primary"
      />
    </template>

    <v-card-title
        class="d-flex align-center justify-space-between"
    >
      <div v-if="!editClicked">
        {{ name }}
      </div>
      <div style="width: 80%" v-else>
        <app-overlay-title
            v-model="name"
            :rules="[nameRequiredRule]"
            :edit="editClicked"
            :disabled="saving||deleting"
        />
      </div>

      <div>
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
            :disabled="saving||deleting"
            @click="close()"
        />
      </div>
    </v-card-title>

    <v-card-text class="flex-1-1 pt-0 pl-4 pr-4 overflow-hidden">
      <RecycleScroller
          :items="storedAt"
          :item-size="120"
          style="height: 100%;"
      >
        <template v-slot="{item}">
          <product-storage-card
              :storage="item"
              @show-stored-at-detail="openDialog()"
              @deleted="deleteSelected"
          />
        </template>
        <template #after>
          <v-row
              :no-gutters="true"
              justify="center"
          >
            <p class="text-center">
              {{ $t("products.locations.all_displayed")}}
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
            @consent="deleteProduct"

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
  </v-card>
</template>

<style scoped lang="scss">

</style>