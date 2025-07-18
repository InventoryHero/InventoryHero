<script setup lang="ts">

import Default from "@/layouts/default.vue";
import {useAuthStore, useConfigStore} from "@/store";
import {storeToRefs} from "pinia";
import NotInitialized from "@/layouts/NotInitialized.vue";

const route = useRoute()
const router = useRouter()
const configStore = useConfigStore()
const authStore = useAuthStore()

const {authorized} = storeToRefs(authStore)
console.log(route.meta)
const transition = computed(() => {
  if(configStore.transitions){
    return {
      name: "scale",
      mode: "out-in"
    }
  }
  return {
    name: "", mode: ""
  }
})




const isInitialized = ref(false)
async function initializeApp() {
  try {
    await router.isReady();
    configStore.init()
    await authStore.init()
    await authStore.isAuthorized()
    if(authorized.value)
    {
      // TODO CONNECT TO SOCKETS
    }
  } catch (error) {
    console.error("Failed to initialize application:", error)
    // Handle initialization error, maybe redirect to an error page
  } finally {
    // Once everything is done (or has failed), flip the switch to render the app.
    isInitialized.value = true;
  }
}

const layoutComponent = computed(() => {
  if(!isInitialized.value){
    return NotInitialized
  }

  const layoutName = route.meta.layout || 'default';
  return defineAsyncComponent(() => import(`./layouts/${layoutName}.vue`));
})
onBeforeMount(() => {
  initializeApp()
})


</script>

<template>
  <v-app v-if="configStore.initialized">
    <component

        :is="layoutComponent"
        v-bind="route.meta.layoutProps ?? {}"
    >
      <router-view v-slot="{Component, route}">
        <transition
            :name="transition.name"
            :mode="transition.mode"
        >
          <div :key="route.meta?.key ?? route.path">
            <component

                :is="Component"
            />
          </div>
        </transition>
      </router-view>
    </component>
  </v-app>

</template>

<style scoped lang="scss">

</style>