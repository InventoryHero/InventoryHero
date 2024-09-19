<script setup lang="ts">
import {useConfigStore, useProducts} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {onMounted} from "vue";
import useRouteTransition from "@/composables/useRouteTransition.ts";

const productStore = useProducts()
const configStore = useConfigStore()
const {axios: productEndpoint} = useAxios<ProductEndpoint>('product')


const props = defineProps<{
  productId?: string,
  productStorageId?: string,
  preselectedProduct?: string
}>()


async function getStorageMappings(id: number){
  productStore.selectProduct(id)
  productStore.setLoadingProductStorage(true)
  const storageMappings = await productEndpoint.getProductStorage(id, productStore.storedAt);
  productStore.storeProductStorage(storageMappings)
  productStore.setLoadingProductStorage(false)
}


watch(() => props.productId, (newValue) => {

  if(newValue === undefined){
    productStore.deselectProduct()
    return
  }
  getStorageMappings(parseInt(newValue))
})

watch(() => props.productStorageId, (newValue) => {
  if(newValue === undefined){
    productStore.deselectProductStoredAt()
    return
  }
  productStore.selectProductStoredAt(parseInt(newValue))
})

watch(() => props.preselectedProduct, (newValue) => {
  if(newValue === undefined){
    productStore.setLoadingProducts(true)
    productEndpoint.getProducts().then((response) => {
      productStore.storeProducts(response)
      productStore.setLoadingProducts(false)
    })
  }
})

onMounted(async () => {
  productStore.setLoadingProducts(true)
  const response = await productEndpoint.getProducts({ id: props.preselectedProduct });
  productStore.storeProducts(response)
  productStore.setLoadingProducts(false)
  if(!props.productId){
    return
  }
  const productId = parseInt(props.productId)
  await getStorageMappings(productId)

  if(!props.productStorageId){
    return
  }
  productStore.selectProductStoredAt(parseInt(props.productStorageId))
})

const {transitionDirection} = useRouteTransition()
const animation = computed(() =>{
  if(configStore.transitions){
    return "scale-slide-" + transitionDirection.value
  }
  return ""
})

onBeforeRouteLeave(() => {
  productStore.reset()
})

</script>

<template>
  <v-row
      :no-gutters="true"
      justify="center"
      class="fill-height fill-width"
  >
    <v-col
        cols="12"
        md="10"
        lg="8"
    >
      <v-container
          class="position-relative fill-height fill-width pa-0"
          fluid
      >
        <router-view v-slot="{Component, route }">
          <transition
              :name="animation"
          >
            <v-container
                class="fill-height fill-width pa-0"
                fluid
                :key="route.path"
            >
              <component :is="Component"  />
            </v-container>

          </transition>
        </router-view>
      </v-container>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
@import "@/scss/transitions/scale-slide";
</style>