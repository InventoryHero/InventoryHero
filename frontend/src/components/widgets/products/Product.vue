<script setup lang="ts">

import {useProducts, useContentFilterStore} from "@/store"
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {ProductStorageMapping} from "@/types/api.ts";
import ProductStorageCard from "@/components/widgets/products/Cards/ProductStorageCard.vue";
import {useI18n} from "vue-i18n";
import {useNotification} from "@kyvg/vue3-notification";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";
import useConfirmationSetup from "@/composables/useConfirmationSetup.ts";

const productStore = useProducts()
const scrollStore = useContentFilterStore()
const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
const {t} = useI18n()
const {notify} = useNotification();
const router = useRouter()
const route = useRoute();
const {redirect} = useRedirectToStorage()
const {goBackOneLevel} = useGoBackOneLevel()

const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')

const product = computed(() => {
  return productStore.selectedProduct
})


const name = computed({
  get() {
    if(newName.value === undefined) {
      return product.value?.name
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


const loadingProduct = computed(() => productStore.loadingProducts)
const loadingProductStorage = computed(() => productStore.loadingProductStorage)

const editClicked = ref(false)
const newName = ref<string|undefined>(undefined)
const nameRequiredRule = (value: string) => value !== '' || t('products.product.rules.new_name_empty')
const saving = ref(false)
const deleting = ref(false)

function close(){
  goBackOneLevel()
}

function cancelEdit(){
  newName.value = undefined
  editClicked.value = false
}

async function saveChanges(){
  if(newName.value === product.value?.name || newName.value === undefined){
    newName.value = undefined
    editClicked.value = false
    return
  }
  if(newName.value === '')
  {
    return false
  }
  saving.value = true
  let {success, updatedProduct} = await productEndpoint.updateProduct(product.value!.id, {
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
    title: t('toasts.titles.success.updated_product'),
    text: t('toasts.text.success.updated_product'),
    type: "success"
  })
  return success
}


function deleteProduct(){
  const id = product.value!.id
  deleting.value = true
  productEndpoint.deleteProduct(product.value!.id).then((success) => {
    deleting.value = false
    if(!success){
      return
    }
    goBackOneLevel().then(() => {
      productStore.deleteProduct(id)
      notify({
        title: t('toasts.titles.success.deleted_product'),
        text: t('toasts.text.success.deleted_product'),
        type: "success"
      })
    })

  })
}
const {
  confirmationDialog: deleteConfirmDialog,
  saveAction: saveDelete,
  reallyDo: reallyDelete
} = useConfirmationSetup(deleteProduct)



function deleteSelected(id: number, amount: number){
  productStore.deleteProductAt(id, amount)
  notify({
    title: t('toasts.titles.success.deleted_detail'),
    text: t('toasts.text.success.deleted_detail'),
    type: "success"
  })
}


function showProductDetail(item: ProductStorageMapping){
  scrollStore.pushPosition(route.fullPath, storedAt.value.findIndex(p => p.id === item.id))
  router.push(`${route.fullPath}/detail/${item.id}`)
}

const afterText = computed(() => {
  if(loadingProductStorage.value){
    return t("products.product.loading")
  }
  return t("products.product.all_displayed")
})

</script>

<template>
  <confirmation-dialog
      :dialog-opened="deleteConfirmDialog"
      :title="t('products.delete_product.title')"
      :text="t('products.delete_product.text')"
      :cancel-text="t('products.delete_product.cancel')"
      :confirm-text="t('products.delete_product.confirm')"
      confirm-icon="mdi-delete-outline"
      cancel-icon="mdi-cancel"
      :on-cancel="() => deleteConfirmDialog = false"
      :on-confirm="reallyDelete"
  />
  <v-card
      class="d-flex flex-column fill-height fill-width"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="loadingProduct || loadingProductStorage"
          color="primary"
      />
    </template>
    <template v-if="!loadingProduct">
      <app-content-title
          v-model:title="name"
          v-model:edit="editClicked"
          :disabled="saving||deleting||loadingProduct"
          :rules="[nameRequiredRule]"
          @close="close()"
          edit-toggles-textfield
      />
      <div class="flex-1-1 position-relative">
        <v-card-text class="pt-0 wrapper">
          <RecycleScroller
              class="scroll"
              ref="scroller"
              :items="storedAt"
              :item-size="90"
              :buffer="0"
              :emit-update="true"
              @update="hasScrolled"
              @visible="visible(route.fullPath, storedAt.length-1)"
          >
            <template v-slot="{item}">
              <product-storage-card
                  :storage="item"
                  @show-stored-at-detail="showProductDetail(item)"
                  @deleted="deleteSelected(item.id, item.amount)"
                  @redirect="redirect(item.storage, product?.name ?? '')"
              />
            </template>
            <template #after>
              <app-content-scroll-after
                :text="afterText"
              />
            </template>
          </RecycleScroller>
        </v-card-text>
      </div>
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
  <app-scroll-to-top-btn
      v-if="!editClicked"
      :scrolled-down="scrolledDown"
      @click.stop="scrollToTop"
  />
</template>

<style scoped lang="scss">

</style>