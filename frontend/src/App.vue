<script setup lang="ts">
import {useAuthStore, useConfigStore, useGeneralSocketStore, useHouseholdSocketStore} from "@/store"
import AppBarBottom from "@/components/ui/AppBarBottom.vue";
import AppBar from "@/components/ui/AppBar.vue";
import {Notifications} from "@kyvg/vue3-notification";



import {applyStorage, getAccessToken, getBrowserLocalStorage} from "axios-jwt";

const configStore = useConfigStore()
const authStore = useAuthStore()
const householdSocket = useHouseholdSocketStore()
const route = useRoute()
const generalSocket = useGeneralSocketStore()
const router = useRouter()
const {mobile} = useDisplay()
// TODO ADMIN USER TABLE CAN BENEFIT FROM SOCKET (E.G. USER VERIFIED EMAIL)

/*
  TODO localize (even for en) - general translations rn
  check everything through
 */

const navOpen = ref(false)
const isAdminRoute = computed(() => {
  return route.path.includes("/administration")
})
const dockVisible = computed(() =>{
  if(!mobile.value){
    return false
  }
  if(isAdminRoute.value){
    return false
  }
  if(isAddRoute.value){
    return false
  }

  return configStore.dock
})
const isAddRoute = computed(() => {
  return route.path.startsWith("/create")
})

const authorized = computed(() => {
  return authStore.authorized
})
const transition = computed(() => {
  if (configStore.transitions){
    return "scale"
  }
  return ""
})

function reloadContent(){
  router.go(0)
}


onMounted(async () => {
  applyStorage(getBrowserLocalStorage());
  configStore.init()
  await authStore.init()
  if(await authStore.isAuthorized())
  {
    getAccessToken().then((token) => {
      householdSocket.updateHeaders(token)
      generalSocket.updateHeaders(token)
      generalSocket.bindActions()
    })

  }
})

onUpdated(async () => {
  /*applyStorage(getBrowserLocalStorage());
  householdSocket.updateHeaders()x
  householdSocket.bindActions()

  generalSocket.updateHeaders()
  generalSocket.bindActions()*/
})
</script>

<template>


  <notifications
      v-if="!(route.meta.tokenized ?? false)"
      position="top right"
      classes="vue-notification mt-2 me-8"
      :max="2"
  />

  <notifications
      v-if="!(route.meta.tokenized ?? false)"
      position="bottom right"
      style="bottom: 40px"
      classes="vue-notification me-2"
      :max="1"
      group="newContent"
      :ignore-duplicates="true"
      :duration="-1"
      @click="(item) => {reloadContent()}"
      width="30svh"
  />

  <v-app v-if="route.meta.tokenized ?? false">
    <v-app-bar
        density="compact"
    >
      <v-toolbar-title>
        <v-card
            hover
            style="width: 130px"
            color="dark-grey"
            @click="router.push('/')"
        >
          {{ $t('app.title') }}
        </v-card>
      </v-toolbar-title>
    </v-app-bar>
    <v-main
        class=""
    >
      <v-container
          :fluid="true"
          :class="{
            'fill-height': route.meta?.fillHeight ?? false,
          }"
      >
        <router-view v-slot="{Component}">
          <transition :name="transition" mode="out-in" >
            <component :is="Component" />
          </transition>
        </router-view>

      </v-container>
    </v-main>
  </v-app>
  <v-app
      v-else
  >
    <app-bar
      :nav="(!dockVisible && !isAddRoute) || isAdminRoute"
      @toggle-nav="navOpen = !navOpen"
    />
    <app-create-bar
      v-if="isAddRoute && authorized"
    />

    <nav-drawer
        v-if="(!dockVisible || isAdminRoute) && authorized"
        v-model="navOpen"
    />

    <app-bar-bottom
        v-if="authorized"
        v-model="dockVisible"
    />


    <v-main
        class=""
    >
      <v-container
          :fluid="true"
          :class="{
            'fill-height': route.meta?.fillHeight ?? false,
          }"
      >
        <router-view v-slot="{Component}">
          <transition :name="transition" mode="out-in" >
            <component :is="Component" />
          </transition>
        </router-view>

      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped lang="scss">

.scale-enter-active,
.scale-leave-active {
  transition: all 0.15s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

</style>
