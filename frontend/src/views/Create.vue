<script setup lang="ts">
import {onBeforeRouteLeave, onBeforeRouteUpdate, useRoute, useRouter} from "vue-router";
import {useConfigStore, useProducts, useStorage} from "@/store";
import {BoxEndpoint, LocationEndpoint, ProductEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";

const config = useConfigStore()
const route = useRoute()
const router = useRouter();
const productStore = useProducts();
const storageStore = useStorage();
const {axios: productEndpoint} = useAxios<ProductEndpoint>("product")
const {axios: boxEndpoint} = useAxios<BoxEndpoint>("box")
const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")

const confirm = ref(false)
const forceLeave = ref(false)
const dst = ref("/")
const animationName = ref("slide-left")

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
provide('loading', loading)

const addRoutes = computed(()=> {
    // child routes of create in order to allow swipe navigation
    return ["/create/product", "/create/box", "/create/location"]
})
const currentRoute = computed(() => {
  return addRoutes.value.indexOf(route.fullPath)
})
const transition = computed(() => {
  if(config.transitions){
    return animationName.value
  }
  return ""
})

function leave(){
  confirm.value = false
  forceLeave.value = true
  productStore.reset()
  storageStore.reset()
  router.push(dst.value)
}

function stay(){
  confirm.value = false
  dst.value = "/"
}

function swipe (direction: "Right"|"Left"|"Up"|"Down") {
  let dir = 0
  switch(direction){
    case "Right":
      dir = -1
      break
    case "Left":
      dir = +1
      break
  }
  let newRoute = (((currentRoute.value+dir) % (addRoutes.value.length)) + addRoutes.value.length) % addRoutes.value.length
  router.push(addRoutes.value[newRoute])
}

onBeforeRouteLeave((to) => {
  if(forceLeave.value)
  {
    forceLeave.value = false
    return true
  }
  dst.value = to.fullPath
  confirm.value = true
  return false
})

onBeforeRouteUpdate((to, from) => {
  let direction = addRoutes.value.indexOf(to.fullPath) - addRoutes.value.indexOf(from.fullPath)
  if (direction == -1 || direction == (addRoutes.value.length - 1)){
    animationName.value = "slide-right"
  }
  else{
    animationName.value = "slide-left"
  }

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
</script>

<template>

  <v-row
      :no-gutters="true"
      class="justify-center fill-height"
      v-touch="{
        left: () => swipe('Left'),
        right: () => swipe('Right'),
        up: () => swipe('Up'),
        down: () => swipe('Down')
      }"

  >
    <v-col
        cols="12"
        lg="6"
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
      <router-view v-slot="{Component}">
        <transition :name="transition" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">


.slide-left-enter-active{
  transition: all 0.75s ease-out;
}
.slide-left-leave-active {
  transition: all 0.75s ease-out;
}

.slide-left-enter-from {
  transform: scale(0);
}

.slide-left-leave-to {
  transform: translateX(-200%);
}

.slide-right-enter-active{
  transition: all 0.75s ease-out;
}
.slide-right-leave-active {
  transition: all 0.75s ease-out;
}

.slide-right-leave-to{
  position: relative;
  transform: translateX(200%);
}

.slide-right-enter-from {
  transform: scale(0);
}





</style>