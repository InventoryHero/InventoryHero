<script setup lang="ts">
import {
  useAuthStore,
  useConfigStore,
  useGeneralSocketStore,
  useHouseholdSocketStore,
  useNotificationStore
} from "@/store"
import AppBarBottom from "@/components/ui/AppBarBottom.vue";
import AppBar from "@/components/ui/AppBar.vue";
import {Notifications} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";
import {applyStorage, getAccessToken, getBrowserLocalStorage} from "axios-jwt";
import {RouteLocationNormalizedGeneric} from "vue-router";

const configStore = useConfigStore()
const authStore = useAuthStore()
const householdSocket = useHouseholdSocketStore()
const route = useRoute()
const generalSocket = useGeneralSocketStore()
const router = useRouter()
const {mobile} = useDisplay()
const notificationStore = useNotificationStore()

// TODO ADMIN USER TABLE CAN BENEFIT FROM SOCKET (E.G. USER VERIFIED EMAIL)
// TODO the print settings look a bit clunky

// the setup actually runs the earliest, loading content here makes sense
// to handle this, the whole App is wrapped in a supsense
applyStorage(getBrowserLocalStorage());
configStore.init()
await authStore.init()
if(await authStore.isAuthorized())
{
  getAccessToken().then((token) => {
    householdSocket.updateHeaders(token)
    generalSocket.updateHeaders(token)
  })
}


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
  return configStore.dock
})

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

const authorized = computed(() => {
  return authStore.authorized
})

const tokenized = computed(() => route.meta.tokenized ?? false)


function reloadContent(){
  router.go(0)
}


const tab = ref(TabType.Product)
provide("tab", tab)

function getKey(route: RouteLocationNormalizedGeneric): string{
  return route.meta?.key?? route.path
}


// todo translate: toasts.text.error.user_not_in_household


onUpdated(async () => {
  notificationStore.triggerNotifications()
})


</script>

<template >

  <notifications
      v-if="!tokenized"
      position="top right"
      classes="vue-notification mt-2 me-8"
      :max="2"
  />
  <notifications
      v-if="!tokenized && authorized"
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

  <v-app-bar
      density="compact"
      v-if="tokenized"
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
  <app-bar
      v-else
      :nav="(!dockVisible) || isAdminRoute"
      @toggle-nav="navOpen = !navOpen"
  />
  <template v-if="authorized && !tokenized">
    <nav-drawer
        v-if="(!dockVisible || isAdminRoute)"
        v-model="navOpen"
    />

    <app-bar-bottom
        v-model="dockVisible"
    />


    <!--<v-dialog
        no-click-animation
        class="fill-height"
        v-model="scanQrCodeModalVisible"
    >
      <qr-scanner
          @close="closeScanQrCodeModal"
      />
    </v-dialog>-->

  </template>

  <v-main>
    <router-view v-slot="{Component, route}">
      <transition
          :name="transition.name"
          :mode="transition.mode"
      >

        <v-container
            :key="getKey(route)"
            class="fill-width"
            :class="{
              'fill-height': route.meta?.fillHeight ?? false,
            }"
            fluid
        >

          <component
              :is="Component"
          />
        </v-container>
      </transition>
    </router-view>
  </v-main>

</template>

<style scoped lang="scss">
@import "@/scss/transitions/scale-transition";
</style>
