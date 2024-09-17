<script setup lang="ts">


import {computed, ref} from "vue";
import {ApiProduct} from "@/types/api.ts";
import {useProducts, useScrollPositionStore} from "@/store";
import {useI18n} from "vue-i18n";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import router from "@/router";


const {t: $t} = useI18n();

// "setup"
const productStore = useProducts()
const scrollStore = useScrollPositionStore()
const route = useRoute()

const {
  scrolledDown,
  scrollToTop,
  hasScrolled,
  visible
} = useScrollToTop('scroller')

// props
const props = defineProps<{
  preselectedProduct?: string
  filteredFrom?: string
}>()

//computed
const productPreselected = computed(() => {
  return props.preselectedProduct ?? false
})

const filteredProducts = computed(() => {
  if(search.value === "")
  {
    return productStore.products
  }
  return productStore.products.filter(product => product.name.toLowerCase().includes(search.value.toLowerCase()))
})

const allDisplayed = computed(() => {
  return productStore.size !== 0 && filteredProducts.value.length !== 0
})

const filterEmpty = computed(() => {
  return productStore.size !== 0 && filteredProducts.value.length === 0
})

const productsLoading = computed(() => productStore.loadingProducts)

// data
const search = ref<string>("")

function displayProductOverlay(item: ApiProduct){
  scrollStore.pushPosition(route.fullPath, filteredProducts.value.findIndex(p => p.id === item.id))
  router.push(`${route.fullPath}/product/${item.id}`)
}

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
      <text-filter
          v-model:filter="search"
          v-if="!productPreselected"
      />
      <app-preselection-filter
          v-else
          @click:close="$router.push('/products')"
          :title="$t('products.prefiltered', {box: filteredFrom})"
      />
    </v-card-title>
    <v-card-text
        class="d-flex position-relative flex-1-1"
    >
      <div class="wrapper">
        <RecycleScroller
            ref="scroller"
            class="scroll"
            :item-size="90"
            :items="filteredProducts"
            :buffer="0"
            :emit-update="true"
            @update="hasScrolled"
            @visible="visible(route.fullPath, filteredProducts.length-1)"
        >
          <template v-slot="{ item }">
            <v-row
                :no-gutters="true"
                justify="center"
            >
              <v-col
                  cols="11"
              >
                <product-card
                    :total-amount="item.totalAmount"
                    :id="item.id"
                    :creation-date="item.creationDate"
                    :name="item.name"
                    @expand="displayProductOverlay(item)"
                />
              </v-col>
            </v-row>
          </template>
          <template #after>
            <v-row
                :no-gutters="true"
                justify="center"
            >
              <v-card
                  :elevation="0"
              >
                <v-card-title class="text-wrap text-center">
                  <p
                      class="pb-1"
                      v-if="productsLoading"
                  >
                    {{ $t('products.loading')}}
                  </p>
                  <p
                      class="pb-1 "
                      v-else-if="allDisplayed"
                  >
                    {{ $t('products.all_displayed') }}
                  </p>
                  <p
                      class="pb-1"
                      v-else-if="filterEmpty"
                  >
                    {{ $t('products.no_matches')}}
                  </p>
                  <p
                      class="pb-1"
                      v-else
                  >
                    {{ $t('products.no_products')}}
                  </p>
                </v-card-title>
              </v-card>
            </v-row>
          </template>
        </RecycleScroller>
      </div>
    </v-card-text>

  </v-card>
  <app-scroll-to-top-btn
      :scrolled-down="scrolledDown"
      @click.stop="scrollToTop"
  />


</template>

<style scoped lang="scss">

</style>