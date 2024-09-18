<script setup lang="ts">

import {useProducts, useScrollPositionStore} from "@/store"
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {ProductStorageMapping} from "@/types/api.ts";
import ProductStorageCard from "@/components/widgets/products/Cards/ProductStorageCard.vue";
import {useI18n} from "vue-i18n";
import {useNotification} from "@kyvg/vue3-notification";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";

const productStore = useProducts()
const scrollStore = useScrollPositionStore()
const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
const {t} = useI18n()
const {notify} = useNotification();
const router = useRouter()
const route = useRoute();
const {redirect} = useRedirectToStorage()

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
  router.back()
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
    productStore.deleteProduct(id)
    router.back()
    notify({
      title: t('toasts.titles.success.deleted_product'),
      text: t('toasts.text.success.deleted_product'),
      type: "success"
    })
  })
}

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
</script>

<template>
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
              :item-size="104"
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
              <v-row
                dense
                justify="center"
                class="mt-2"
              >
                <p
                    v-if="!loadingProductStorage"
                    class="text-center"
                >
                  {{ $t("products.locations.all_displayed")}}
                </p>
                <p
                    v-else
                    class="text-center"
                >
                  {{ $t("products.locations.loading")}}
                </p>
              </v-row>
            </template>
          </RecycleScroller>
        </v-card-text>
      </div>
      <v-card-actions
          v-if="editClicked"
          class="d-flex justify-space-between flex-0-0"
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
    </template>
    <v-row
      v-else
      dense
      justify="center"
      class="align-center"
    >
      {{ $t('products.loading')}}
    </v-row>
  </v-card>
  <app-scroll-to-top-btn
      :scrolled-down="scrolledDown"
      @click.stop="scrollToTop"
      density="compact"
  />
</template>

<style scoped lang="scss">

</style>