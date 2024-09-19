<script setup lang="ts">
import {useContentFilterStore, useProducts, useStorage} from "@/store";
import useStorageTitle from "@/composables/useStorageTitle.ts";
import {computed, onMounted, ref} from "vue";
import useRedirectToStorage from "@/composables/useRedirectToStorage.ts";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, LocationEndpoint} from "@/api/http";
import {ApiProduct, ApiStorage, StorageTypes} from "@/types";
import {useI18n} from "vue-i18n";
import ProductStorageCard from "@/components/widgets/products/Cards/ProductStorageCard.vue";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";
import useConfirmationSetup from "@/composables/useConfirmationSetup.ts";

const storageStore = useStorage()
const productStore = useProducts()
const contentFilterStore = useContentFilterStore()
const {redirect} = useRedirectToStorage()
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {t} = useI18n()
const router = useRouter()
const route = useRoute()
const {goBackOneLevel} = useGoBackOneLevel()

provide("storageType", StorageTypes.Box)


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
  return productStore.productStorage
})


const {name, icon} = useStorageTitle(boxStoredAt)
const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')

const loadingStorage = ref(false)
const locations = ref<Array<ApiStorage>>([])
const nameRequiredRule = (value: string) => value !== '' || t('boxes.box.rules.new_name_empty')
const newName = ref<string|undefined>(undefined)
const newStorage = ref<ApiStorage|undefined>(undefined)
const saving = ref(false)
const deleting = ref(false)
const editClicked = ref(false)
const scrollToTopHidden = ref(false)

const loadingProducts = computed(() => storageStore.loadingContent)
const loadingBox = computed(() => storageStore.loadingStorage || loadingStorage.value)

function cancelEdit(){
  newName.value = undefined
  newStorage.value = undefined
  editClicked.value = false
}

function close(){
  editClicked.value = false
  goBackOneLevel()
}

function displayProductOverlay(item: ApiProduct){
  contentFilterStore.pushPosition(route.fullPath, productsStoredInBox.value.findIndex(p => p.id === item.id))
  router.push(`${route.fullPath}/product/${item.id}`)
}

function deleteProduct(productId: number, productStorageId: number, amount: number){
  productStore.deleteProductAt(productStorageId, amount)
  productStore.deleteProduct(productId)
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
  const id = box.value.id
  deleting.value = true
  boxEndpoint.deleteStorage(box.value.id).then((success) => {
    if(!success){
      return
    }
    goBackOneLevel().then(() => {
      deleting.value = false
      storageStore.deleteBox(id)
    })
  })
}
const {
  confirmationDialog,
  saveAction: saveDelete,
  reallyDo
} = useConfirmationSetup(deleteBox)


function redirectToProduct(productId: number){
  router.push(`/products/product/${productId}`)
}

onMounted(() => {
  loadingStorage.value = true
  locationEndpoint.getLocations().then((loc: Array<ApiStorage>) => {
    locations.value = loc
    loadingStorage.value = false
  })
})

const afterText = computed(() => {
  if(loadingProducts.value){
    return t('boxes.box.loading')
  }
  return t("boxes.box.all_displayed")
})

</script>

<template>
  <confirmation-dialog
    v-model:dialog-opened="confirmationDialog"
    :title="t('boxes.confirm_delete.title')"
    :text="t('boxes.confirm_delete.text')"
    :confirm-text="t('boxes.confirm_delete.confirm')"
    :cancel-text="t('boxes.confirm_delete.cancel')"
    confirm-icon="mdi-delete-outline"
    cancel-icon="mdi-cancel"
    :on-cancel="() => confirmationDialog = false"
    :on-confirm="reallyDo"
  />
  <v-card
      class="position-relative d-flex flex-column fill-height fill-width"
  >
    <template v-slot:loader>
      <v-progress-linear
        indeterminate
        :active="loadingBox || loadingProducts || deleting"
        color="primary"
      />
    </template>
    <template v-if="!loadingBox">
      <app-content-title
          v-model:title="boxName"
          v-model:edit="editClicked"
          :rules="[nameRequiredRule]"
          :disabled="saving||deleting"
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
          class="wrapper"
        >
          <RecycleScroller
            ref="scroller"
            class="scroll"
            :buffer="0"
            :emit-update="true"
            @update="hasScrolled"
            @visible="visible(route.fullPath, productsStoredInBox.length-1)"
            :items="productsStoredInBox"
            :item-size="90"
          >
            <template v-slot="{item}">

              <product-storage-card
                :storage="item"
                from-storage

                @show-stored-at-detail="displayProductOverlay(item)"
                @deleted="deleteProduct(item.productId, item.id, item.amount)"
                @redirect="redirectToProduct(item.productId)"

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
        :deleting="deleting"
        :saving="saving"
        @cancel="cancelEdit"
        @delete="saveDelete"
        @save="saveChanges"
      />
      <v-card-actions
          v-if="!editClicked"
          class="pb-0 pt-0 mt-0 mb-0"
      >
        <app-storage-qr-code-btn
            color="primary"
            use-preselected
            v-model:active="scrollToTopHidden"
        />

      </v-card-actions>
    </template>
    <app-content-scroll-after
      v-else
      class="mt-2"
      :text="t('boxes.loading' )"
    />

  </v-card>
  <app-scroll-to-top-btn
      v-if="!editClicked && !scrollToTopHidden"
      :scrolled-down="scrolledDown"
      @click.stop="scrollToTop"
  />
</template>

<style scoped lang="scss">

</style>