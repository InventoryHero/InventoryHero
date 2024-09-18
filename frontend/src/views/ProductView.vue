<script setup lang="ts">
import {useProducts} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {ProductEndpoint} from "@/api/http";
import {onMounted} from "vue";

const productStore = useProducts()
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
        class=""
    >
      <router-view v-slot="{Component, route }">
        <transition
          name="scale"
        >
          <v-container
              class="position-relative fill-width fill-height pa-0"
              fluid
              :key="route.path"
          >
            <component :is="Component"  />
          </v-container>
        </transition>
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
@import "@/scss/transitions/scale-transition";
</style>