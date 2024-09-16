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
import {Notifications, useNotification} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";

// TODO the print settings look a bit clunky


import {applyStorage, getAccessToken, getBrowserLocalStorage} from "axios-jwt";
import useDialogConfig from "@/composables/useDialogConfig.ts";

const configStore = useConfigStore()
const authStore = useAuthStore()
const householdSocket = useHouseholdSocketStore()
const route = useRoute()
const generalSocket = useGeneralSocketStore()
const router = useRouter()
const {mobile} = useDisplay()
const notificationStore = useNotificationStore()

// TODO ADMIN USER TABLE CAN BENEFIT FROM SOCKET (E.G. USER VERIFIED EMAIL)

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


const authorized = computed(() => {
  return authStore.authorized
})


function reloadContent(){
  router.go(0)
}

const {
  isVisible: scanQrCodeModalVisible,
  openDialog: openScanQrCodeModal,
  closeDialog: closeScanQrCodeModal
} = useDialogConfig()

const tab = ref(TabType.Product)
provide("tab", tab)


onUpdated(async () => {
  notificationStore.triggerNotifications()
})


</script>

<template >
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

  <template v-if="route.meta.tokenized ?? false">
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
          <transition name="scale" mode="out-in" >
            <component :is="Component" />
          </transition>
        </router-view>
      </v-container>
    </v-main>
  </template>

  <template
      v-else
  >
    <app-bar
        :nav="(!dockVisible) || isAdminRoute"
        @toggle-nav="navOpen = !navOpen"
        @scan-qr-code="openScanQrCodeModal"
    />
    <nav-drawer
        v-if="(!dockVisible || isAdminRoute) && authorized"
        v-model="navOpen"
    />

    <app-bar-bottom
        v-if="authorized"
        v-model="dockVisible"
    />
    <v-dialog
        noClickAnimation
        class="fill-height"
        v-model="scanQrCodeModalVisible"
    >
      <qr-scanner
          @close="closeScanQrCodeModal"
      />
    </v-dialog>

    <v-main>
      <router-view v-slot="{Component}">
        <transition name="scale" mode="out-in" >
          <v-container
              class="fill-width"
              :class="{
            'fill-height': route.meta?.fillHeight ?? false,
          }"
          >
            <component :is="Component" />
          </v-container>
        </transition>
      </router-view>
    </v-main>
  </template>
</template>

<style scoped lang="scss">

.scale-enter-active,
.scale-leave-active {
  transition: all 0.35s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

</style>
