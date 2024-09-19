<script setup lang="ts">

import {ApiStorage, ProductStorageMapping} from "@/types";
import {useContentFilterStore, useProducts} from "@/store";
import {TabType} from "@/types/TabType.ts";
import useScrollToTop from "@/composables/useScrollToTop.ts";

const route = useRoute()
const router = useRouter()
const productStore = useProducts()
const contentFilterStore = useContentFilterStore()
const {t} = useI18n()

const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')

const {tab, items=[], loadingContent=false} = defineProps<{
  tab: TabType ,
  items?: Array<ProductStorageMapping> | Array<ApiStorage>,
  loadingContent?: boolean

}>()

const isBox = computed(() => tab === TabType.Box)

function openBox(item: ApiStorage){
  contentFilterStore.pushPosition(route.fullPath, items.findIndex(p => p.id === item.id))
  contentFilterStore.pushTab(route.fullPath, tab)
  router.push(`${route.fullPath}/box/${item.id}`)
}

function showProduct(item: ProductStorageMapping){
  contentFilterStore.pushPosition(route.fullPath, items.findIndex(p => p.id === item.id))
  contentFilterStore.pushTab(route.fullPath, tab)
  router.push(`${route.fullPath}/product/${item.id}`)
}

function redirectToProduct(productId: number){
  router.push(`/products/product/${productId}`)
}

function deleteProduct(productId: number, productStorageId: number, amount: number){
  productStore.deleteProductAt(productStorageId, amount)
  productStore.deleteProduct(productId)
}




</script>

<template>
  <v-tabs-window-item
      :value="tab"
      class="fill-height position-relative"
  >
    <v-card-text
        class="pb-0 wrapper"
    >
      <RecycleScroller
          :items="items"
          :item-size="isBox ? 85 : 90"
          class="scroll"
          ref="scroller"
          :buffer="0"
          :emit-update="true"
          @update="hasScrolled"
          @visible="visible(route.fullPath, items.length-1)"
      >
        <template v-slot="{item}">
          <storage-card
              v-if="isBox"
              v-bind:storage="item"
              :type="item.type"
              @click.stop="openBox(item)"
          />
          <product-storage-card
              v-else
              :storage="item"
              from-storage
              @deleted="deleteProduct(item.productId, item.id, item.amount)"
              @redirect="redirectToProduct(item.productId)"
              @show-stored-at-detail="showProduct(item)"
          />
        </template>
        <template #after>
          <app-content-scroll-after
            :text="$t('locations.location.all_displayed')"
          />
        </template>
      </RecycleScroller>

    </v-card-text>
  </v-tabs-window-item>

</template>

<style scoped lang="scss">

</style>