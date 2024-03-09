<script lang="ts">
import {Product, ProductLocations} from "@/types/index.ts";

import {useAuthStore, useConfigStore} from "@/store";
import {defineComponent} from "vue"
import ProductDetailCard from "@/components/products/ProductDetailCard.vue"
import useNewAxios from "@/composables/useNewAxios.ts";
import {ProductEndpoint} from "@/api/http";

export default defineComponent({
  components: {
    ProductDetailCard
  },
  setup(){
    const authData = useAuthStore()
    const config = useConfigStore()
    const {axios} = useNewAxios("product")
    return {authData, config, axios: axios as ProductEndpoint}
  },
  computed: {
    filteredItems() {
      if (this.search === "") {
        return this.products
      }
      return this.products.filter(product => product.name.toLowerCase().includes(this.search.toLowerCase()))
    },
    overlayStorageLocations(){
      return this.overlayProduct?.storage_locations ?? []
    },
    scrolledDown(){
      return this.visibleStartIdx !== 0
    }
  },
  watch:{
    async preselectedProduct(){
      if(this.preselectedProduct === undefined)
      {
        this.products = []
        await this.loadProducts()
      }
    },
  },
  props:{
    preselectedProduct:{
      type: String,
      default: undefined
    },
    filteredFrom:{
      type: String,
      default: undefined
    }
  },
  methods: {
    async loadProducts(){
      this.productsLoading = true;
      this.products = await this.axios.getProducts({
        id: this.preselectedProduct,
        getStoredAt: true
      })
      this.productsLoading = false
    },
    updateFilter(filterValue: string)
    {
      this.search = filterValue
    },
    displayProductOverlay(item: Product)
    {
      this.overlayProduct = item
    },
    async deleteProduct(product: number|undefined)
    {
      await this.loadProducts()
    },
    async updateProduct(product: Product)
    {
      for(let i = 0; i < this.products.length; i++)
      {
        if(this.products.at(i)?.id === product.id)
        {
            this.products[i].name = product.name
            break
        }
      }
      this.overlayProduct = product
    },
    updateMapping(mapping: ProductLocations, callback: () => void){
      let i = 0;
      for(; i < this.products.length; i++)
      {
        if(this.products.at(i)?.id === mapping?.product_id){
          break
        }
      }
      let product = this.products.at(i)
      if(i >= this.products.length || product === undefined){
        this.overlayProduct = undefined
        this.loadProducts()
        return
      }

      let m = 0;

      let mappings = product.storage_locations.length ?? 0
      for(; m < mappings; m++)
      {
          if(product.storage_locations.at(m)?.id === mapping.id)
          {
            break
          }
      }

      if(m >= mappings){
        this.overlayProduct = undefined
        this.loadProducts()
        return
      }

      if(this.products[i].storage_locations[m].amount !== mapping.amount){
        this.products[i].total_amount -=  this.products[i].storage_locations[m].amount;
        this.products[i].storage_locations[m].amount = mapping.amount
        this.products[i].total_amount += this.products[i].storage_locations[m].amount
      }
      this.products[i].storage_locations[m].storage = mapping.storage
      this.products[i].storage_locations[m].storage_type = mapping.storage_type

      if(this.overlayProduct?.id === this.products[i].id)
      {
        this.overlayProduct = this.products[i]
        this.overlayStorageLocations = this.products[i].storage_locations
        callback()
      }

    },
    async deleteMapping(id: number, callback: () => void){
      await this.loadProducts()
      if(this.overlayProduct?.id === id)
      {
        this.overlayProduct = this.products.find((item) => item.id === id)

        callback()
      }
    },
    onUpdate (viewStartIndex: number, viewEndIndex: number, visibleStartIndex: number, visibleEndIndex: number) {
      this.visibleStartIdx = visibleStartIndex
    },
    scrollToTop(){
      this.$refs.scroller.scrollToItem(0)
    }
  },
  data(){
    return {
      products: [] as Array<Product>,
      productsLoading: true,
      overlayProduct: undefined as Product|undefined,
      search: "",
      visibleStartIdx: 0,
    }
  },
  async mounted(){
    await this.loadProducts()
  }
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
        class="position-relative d-flex flex-column fill-height"
    >
      <product-overlay
          v-model="overlayProduct"
          :storage-locations="overlayStorageLocations"
          @deleted="deleteProduct($event)"
          @updated="updateProduct($event)"
          @updateMapping="updateMapping"
          @delete-mapping="deleteMapping"
      />

      <div class="flex-0-1">
        <text-filter
            @update-filter="updateFilter"
            :filter="search"
            v-if="preselectedProduct === undefined"
        />
        <app-preselection-filter
            v-else
            @click:close="$router.push('/products')"
            :title="$t('products.prefiltered', {box: filteredFrom})"
        />
      </div>
      <v-card
          ref="wrapper"
          class="mt-4 flex-1-1"
      >
        <v-progress-linear
            :indeterminate="true"
            :active="productsLoading"
            color="primary"
        />
        <v-card-text
            class="pt-1 pl-0 pr-0 pb-0"
        >
          <app-scroll-to-top-btn
              v-model="scrolledDown"
              @click="scrollToTop()"
          />
          <RecycleScroller
              :item-size="90"
              :items="filteredItems"
              ref="scroller"
              style="height: 100%;"
              :buffer="0"
              :emit-update="true"
              @update="onUpdate"
          >
            <template #default="{item}">
              <v-row
                  :no-gutters="true"
                  justify="center"
              >
                <v-col
                    cols="11"
                >
                  <product-card
                      :id="item.id"
                      :name="item.name"
                      :creationDate="item.creation_date"
                      :starred="item.starred"
                      :totalAmount="item.total_amount"
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
                        class="pb-1 "
                        v-if="products.length !== 0 && filteredItems.length !== 0"
                    >
                      {{ $t('products.all_displayed') }}
                    </p>
                    <p
                        class="pb-1"
                        v-else-if="products.length !== 0 && filteredItems.length === 0"
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
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.v-card-text {
  overflow: hidden;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}
</style>