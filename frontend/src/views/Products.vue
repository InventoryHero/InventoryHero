<script setup lang="ts">


import {computed, onMounted, ref} from "vue";
import {ApiProduct} from "@/types/api.ts";
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {useProducts} from "@/store";
import ProductOverlay from "@/components/products/ProductOverlay.vue";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {useI18n} from "vue-i18n";
import useScrollToTop from "@/composables/useScrollToTop.ts";
import {onBeforeRouteLeave} from "vue-router";

const {t: $t} = useI18n();

// "setup"
const productStore = useProducts()
const {axios: productEndpoint} = useAxios<ProductEndpoint>('product')
const { isVisible: productDetailOverlayVisible, openDialog, closeDialog, dialogProps } = useDialogConfig()
const {scrolledDown, scrollToTop, hasScrolled} = useScrollToTop('scroller')

// props
const props = defineProps<{
  preselectedProduct?: string,
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



// data
const productsLoading = ref(false)
const search = ref<string>("")


function loadProducts(){
  productsLoading.value = true;
  productEndpoint.getProducts({
    id: props.preselectedProduct,
  }).then((response: Array<ApiProduct>) => {
    productStore.storeProducts(response)
    productsLoading.value = false
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
}

onMounted(() => {
  loadProducts();
})
onBeforeRouteLeave(() => {
  productStore.reset()
})
</script>

<template>
  <v-row
      :no-gutters="true"
      justify="center"
      class="fill-height"
  >
    <v-col
        cols="12"
        lg="6"
        class="position-relative"
    >
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
          class="d-flex flex-column fill-height"
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
          <div class="scroller-wrapper">
            <RecycleScroller
                ref="scroller"
                class="scroller"
                :item-size="90"
                :items="filteredProducts"
                :buffer="0"
                :emit-update="true"
                @update="hasScrolled"
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
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>