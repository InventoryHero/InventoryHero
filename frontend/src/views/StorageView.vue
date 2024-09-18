<script setup lang="ts">
import {useProducts, useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, ProductEndpoint} from "@/api/http";
import {onMounted} from "vue";

const productStore = useProducts()
const storageStore = useStorage()
const {axios: productEndpoint} = useAxios<ProductEndpoint>('product')
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const route = useRoute()

const props = defineProps<{
  boxId?: string,
  productStorageId?: string
}>()


async function getStorageContent(id: number){
  storageStore.setLoadingContent(true)
  boxEndpoint.getContent(id).then(({products, storageLocations}) => {
    storageStore.selectBox(id)
    productStore.storeProducts(products)
    productStore.storeProductStorage(storageLocations)
    productStore.setStorage(id)
    storageStore.selectForPrinting(id)
    storageStore.setLoadingContent(false)
  })
}


watch(() => props.boxId, (newValue) => {
  if(newValue === undefined){
    productStore.reset()
    storageStore.deselectBox()
    return
  }
  getStorageContent(parseInt(newValue))
})

watch(() => props.productStorageId, (newValue) => {
  if(newValue === undefined){
    productStore.deselectProductStoredAt()
    return
  }
  productStore.selectProductStoredAt(parseInt(newValue))
  productStore.selectProduct(productStore.selectedProductStorage?.productId ?? -1)
})


async function loadBoxes(){
  storageStore.setLoadingStorage(true)
  const response = await boxEndpoint.getBoxes();
  storageStore.storeBoxes(response)
  storageStore.setLoadingStorage(false)

  if(!props.boxId){
    return
  }

  await getStorageContent(parseInt(props.boxId))
}

async function loadLocations(){

}

onMounted(async () => {

  if(route.fullPath.startsWith("/box")){
    await loadBoxes()
  } else{
    await loadLocations()
  }
  console.log("hello")

  /*if(!props.productId){
    return
  }
  const productId = parseInt(props.productId)
  await getStorageMappings(productId)

  if(!props.productStorageId){
    return
  }
  productStore.selectProductStoredAt(parseInt(props.productStorageId))*/
})

onBeforeRouteLeave(() => {
  storageStore.reset()
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
        lg="8"
        class="fill-width"
    >
      <router-view v-slot="{Component, route }">
        <v-container
            class="position-relative fill-width fill-height pa-0"
            :key="route.path"
            fluid
        >
          <component :is="Component"  />
        </v-container>
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>