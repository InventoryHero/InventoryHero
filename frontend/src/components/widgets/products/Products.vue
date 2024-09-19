<script setup lang="ts">


import {computed, ref} from "vue";
import {ApiProduct} from "@/types/api.ts";
import {useProducts, useContentFilterStore} from "@/store";
import {useI18n} from "vue-i18n";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import router from "@/router";
import AppContentScrollAfter from "@/components/ui/AppContentScrollAfter.vue";


const {t: $t} = useI18n();

// "setup"
const productStore = useProducts()
const contentFilterStore = useContentFilterStore()
const route = useRoute()
const {styling} = useAppStyling()

const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')

const allProducts = computed(() => productStore.products)

const filteredProducts = computed(() => {
  if(!search.value)
  {
    return allProducts.value
  }
  return allProducts.value.filter(product => product.name.toLowerCase().includes(search.value?.toLowerCase() ?? ''))
})

const allDisplayed = computed(() => {
  return productStore.size !== 0 && filteredProducts.value.length !== 0
})

const filterEmpty = computed(() => {
  return productStore.size !== 0 && filteredProducts.value.length === 0
})

const productsLoading = computed(() => productStore.loadingProducts)

// data
const search = ref<string|null>(null)

function displayProductOverlay(item: ApiProduct){
  contentFilterStore.pushConfig(route.fullPath, filteredProducts.value.findIndex(p => p.id === item.id), search.value)
  router.push(`${route.fullPath}/product/${item.id}`)
}

const afterText = computed(() => {
  if(productsLoading.value){
    return $t('products.loading')
  }
  if(allDisplayed.value){
    return $t('products.all_displayed')
  }
  if(filterEmpty.value){
    return $t('products.no_matches')
  }
  return $t('products.no_products')
})


onMounted(() => {
  search.value = contentFilterStore.popFilter(route.fullPath)
})

</script>

<template>
  <v-card
      class="position-relative d-flex flex-column fill-height fill-width"
      :loading="productsLoading"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="productsLoading"
          color="primary"
      />
    </template>
    <v-card-title class="flex-0-1">
      <v-text-field
          v-model="search"
          v-bind="styling"
          :placeholder="$t('products.filter')"
          density="compact"
      />
    </v-card-title>
    <div
      class="position-relative flex-1-1"
    >

      <v-card-text class="pb-0 wrapper">
          <RecycleScroller
              ref="scroller"
              class="scroll"
              :item-size="85"
              :items="filteredProducts"
              :buffer="0"
              :emit-update="true"
              @update="hasScrolled"
              @visible="visible(route.fullPath, filteredProducts.length-1)"
          >
            <template v-slot="{ item }">
              <product-card
                  :total-amount="item.totalAmount"
                  :id="item.id"
                  :creation-date="item.creationDate"
                  :name="item.name"
                  @expand="displayProductOverlay(item)"
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
  </v-card>
  <app-scroll-to-top-btn
      :scrolled-down="scrolledDown"
      @click.stop="scrollToTop"
  />


</template>

<style scoped lang="scss">

</style>