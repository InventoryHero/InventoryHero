<script setup lang="ts">
import {useAuthStore, useProducts, useStorage} from "@/store";
import {BoxEndpoint, LocationEndpoint, ProductEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";
import { TabType} from "@/types/TabType.ts";

const router = useRouter();
const productStore = useProducts();
const storageStore = useStorage();
const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")

const tab = inject<Ref<TabType>>("tab", ref(TabType.Product))
const tabs = ref<TabType[]>([TabType.Product, TabType.Box, TabType.Location]);
const confirm = ref(false)
const forceLeave = ref(false)
const destination = ref("/")
const loadingProducts = ref(false)
const loadingBoxes = ref(false)
const loadingLocations = ref(false)

const loading = computed(() => {
  return {
    loadingProducts: loadingProducts.value,
    loadingBoxes: loadingBoxes.value,
    loadingLocations: loadingLocations.value
  }
})

const authStore = useAuthStore()
provide('loading', loading)

function leave(){
  confirm.value = false
  forceLeave.value = true
  productStore.reset()
  storageStore.reset()
  router.push(destination.value)
}

function stay(){
  confirm.value = false
  destination.value = "/"
}

onBeforeRouteLeave((to) => {
  if(forceLeave.value || !authStore.household)
  {
    forceLeave.value = false
    return true
  }
  destination.value = to.fullPath
  confirm.value = true
  return false
})



onMounted(()=> {
  loadingProducts.value = true
  productEndpoint.getProducts().then((products) => {
    productStore.storeProducts(products)
    loadingProducts.value = false
  })

  loadingBoxes.value = true
  boxEndpoint.getBoxes().then((boxes) =>{
    storageStore.storeBoxes(boxes)
    loadingBoxes.value = false
  })

  loadingLocations.value = true
  locationEndpoint.getLocations().then((locations) =>{
    storageStore.storeLocations(locations)
    loadingLocations.value = false
  })
})


function swipeTabs (direction: number = 0) {
  let index = tabs.value.findIndex((t) => t === tab.value)
  if(index === -1){
    index = 0
  }
  index = (index + direction + tabs.value.length) % tabs.value.length
  tab.value = tabs.value[index]
}

</script>

<template>
  <v-container
      class="pa-0 fill-height fill-width"
  >
    <app-confirm-modal
        :dialog="confirm"
        :title="$t('confirm.leave.title')"
        :body="$t('confirm.leave.text')"
    >
      <v-btn
          prepend-icon="mdi-cancel"
          @click="stay()"
      >
        {{ $t('confirm.leave.deny') }}
      </v-btn>
      <v-btn
          prepend-icon="mdi-check-circle"
          @click="leave()"
      >
        {{ $t('confirm.leave.accept') }}
      </v-btn>
    </app-confirm-modal>

    <v-tabs-window
        v-model="tab"
        class="fill-height fill-width"
        v-touch="{
          left: () => swipeTabs(1),
          right: () => swipeTabs(-1),
        }"
    >
      <v-tabs-window-item
          value="product"
      >
        <create-product-card />
      </v-tabs-window-item>
      <v-tabs-window-item
          value="box"
      >
        <create-box-card />
      </v-tabs-window-item>
      <v-tabs-window-item
          value="location"
      >
        <create-location-card />
      </v-tabs-window-item>
    </v-tabs-window>

  </v-container>

</template>

<style scoped lang="scss">

</style>