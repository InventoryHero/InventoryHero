<script setup lang="ts">

import DefaultLayout from "@/layouts/DefaultLayout.vue";
import {useAuthStore, useConfigStore} from "@/store";
import {storeToRefs} from "pinia";
import NotInitialized from "@/layouts/NotInitialized.vue";

const route = useRoute()
const configStore = useConfigStore()
const authStore = useAuthStore()

const {authorized} = storeToRefs(authStore)

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

onBeforeMount(() => {
  initializeApp()
})
</script>

<template>
  <v-app>
    <component
        :is="isInitialized ? (route.meta.layout ?? DefaultLayout) : NotInitialized"
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
@import "@/scss/transitions/scale-transition";
</style>