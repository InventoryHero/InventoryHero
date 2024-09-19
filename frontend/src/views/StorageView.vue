<script setup lang="ts">
import {useConfigStore, useProducts, useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {BoxEndpoint, LocationEndpoint} from "@/api/http";
import {onMounted} from "vue";
import useRouteTransition from "@/composables/useRouteTransition.ts";

const productStore = useProducts()
const storageStore = useStorage()
const configStore = useConfigStore()
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const route = useRoute()

const props = defineProps<{
  boxId?: string,
  productStorageId?: string,
  locationId?: string
}>()


async function getBoxContent(id: number){
  storageStore.setLoadingContent(true)
  storageStore.selectBox(id)
  const {products, storageLocations} = await boxEndpoint.getContent(id)
  productStore.storeProducts(products)
  productStore.storeProductStorage(storageLocations)
  productStore.setStorage(id)
  storageStore.selectForPrinting(id)
  storageStore.setLoadingContent(false)

}


async function getLocationContent(id: number){
  storageStore.setLoadingContent(true)
  storageStore.setFromStorage(id)
  const {boxes, products, storageLocations} = await locationEndpoint.getContent(id)
  storageStore.selectLocation(id)
  storageStore.storeBoxes(boxes)
  productStore.storeProducts(products)
  productStore.storeProductStorage(storageLocations)
  productStore.setStorage(id)
  storageStore.selectForPrinting(id)
  storageStore.setLoadingContent(false)
}



watch(() => props.locationId, (newValue) => {
  if(!newValue){
    productStore.reset()
    storageStore.deselectLocation()
    return
  }

  getLocationContent(parseInt(newValue))
})

watch(() => props.boxId, (newValue) => {
  if(newValue === undefined){
    productStore.reset()
    if(props.locationId){
      getLocationContent(parseInt(props.locationId))
    }
    storageStore.deselectBox()
    return
  }
  getBoxContent(parseInt(newValue))
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

  await getBoxContent(parseInt(props.boxId))
  if(!props.productStorageId){
    return
  }
  productStore.selectProductStoredAt(parseInt(props.productStorageId))
  productStore.selectProduct(productStore.selectedProductStorage?.productId ?? -1)
}

async function loadLocations(){
  storageStore.setLoadingStorage(true)
  const response = await locationEndpoint.getLocations()
  storageStore.storeLocations(response)
  storageStore.setLoadingStorage(false)

  if(!props.locationId){
    return
  }

  storageStore.selectLocation(parseInt(props.locationId))
  if(!props.boxId){
    await getLocationContent(parseInt(props.locationId))
  } else{
    storageStore.setLoadingStorage(true)
    const response = await boxEndpoint.getBoxes({id: props.boxId});
    storageStore.storeBoxes(response)
    storageStore.setLoadingStorage(false)
    storageStore.setFromStorage(parseInt(props.locationId))
    await getBoxContent(parseInt(props.boxId))
  }

  if(props.productStorageId){
    productStore.selectProductStoredAt(parseInt(props.productStorageId))
    productStore.selectProduct(productStore.selectedProductStorage?.productId ?? -1)
  }
}

const {transitionDirection} = useRouteTransition()
const animation = computed(() =>{
  if(configStore.transitions){
    return "scale-slide-" + transitionDirection.value
  }
  return ""
})

onMounted(async () => {
  if(route.fullPath.startsWith("/box")){
    await loadBoxes()
  } else{
    await loadLocations()
  }
})

onBeforeRouteLeave(() => {
  storageStore.reset()
  productStore.reset()
})
</script>
<template>
  <v-row
      dense
      justify="center"
      class="fill-height"
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