<script setup lang="ts">
import {useAuthStore, useConfigStore, useGeneralSocketStore, useHouseholdSocket} from "@/store"
import AppBarBottom from "@/components/ui/AppBarBottom.vue";
import AppBar from "@/components/ui/AppBar.vue";
import {Notifications} from "@kyvg/vue3-notification";
import NavDrawer from "@/components/ui/NavDrawer.vue";
import {useRoute, useRouter} from "vue-router";
import AppCreateBar from "@/components/ui/AppCreateBar.vue";
import {computed, defineComponent, onMounted, onUpdated, ref, watch} from "vue";
import {useDisplay} from "vuetify";
import {applyStorage, getBrowserLocalStorage} from "axios-jwt";

const config = useConfigStore()
const authStore = useAuthStore()
const householdSocket = useHouseholdSocket()
const route = useRoute()
const generalSocket = useGeneralSocketStore()
const router = useRouter()
const {mobile} = useDisplay()

/*
  TODO localize (even for en)
  toasts.titles.success.updated_successfully (userupdate)
  toasts.titles.success.resent_confirmation (user email confirm resend)
 */

const navOpen = ref(false)
const isAdminRoute = computed(() => {
  return route.path.includes("/administration")
})
const dockVisible = computed(() =>{
  if(!mobile){
    return false
  }
  if(isAdminRoute.value){
    return false
  }
  if(isAddRoute.value){
    return false
  }

  return config.dock
})
const isAddRoute = computed(() => {
  return route.path.startsWith("/create")
})

const authorized = computed(() => {
  return authStore.isAuthorized()
})
const transition = computed(() => {
  if (config.transitions){
    return "scale"
  }
  return ""
})

function reloadContent(){
  router.go()
}

watch(authorized, (newValue, oldValue) => {
  if(newValue)
  {
    householdSocket.updateHeaders()
    householdSocket.bindActions()

    generalSocket.updateHeaders()
    generalSocket.bindActions()
  } else{
    householdSocket.leaveHousehold()
  }

})

onMounted(() => {
  applyStorage(getBrowserLocalStorage());
  if(authStore.isAuthorized())
  {
    householdSocket.updateHeaders()
    generalSocket.updateHeaders()
    generalSocket.bindActions()
  }
})

onUpdated(() => {
  householdSocket.updateHeaders()
  householdSocket.bindActions()
})
</script>

<template>


  <notifications
    position="top right"
    classes="vue-notification mt-2 me-8"
    :max="2"
  />

  <notifications
      position="bottom right"
      style="bottom: 40px"
      classes="vue-notification me-2"
      :max="1"
      group="newContent"
      :ignore-duplicates="true"
      :duration="-1"
      @click="(item) => {reloadContent()}"
      width="30svh"
  >
  </notifications>


  <v-app v-if="!authorized">
    <app-bar
        :nav="!dockVisible && !isAddRoute"
        @toggle-nav="navOpen = !navOpen"
    />
    <v-main >
      <v-container
          :fluid="true"
          :class="{
            'fill-height': $route.meta?.fillHeight ?? false
          }"
      >
        <router-view v-slot="{Component}">
          <transition name="scale" mode="out-in">
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
      v-if="isAddRoute"
    />

    <nav-drawer
        v-if="!dockVisible || isAdminRoute"
        v-model="navOpen"
    />

    <app-bar-bottom
        v-model="dockVisible"
    />


    <v-main
        class=""
    >
      <v-container
          :fluid="true"
          :class="{
            'fill-height': $route.meta?.fillHeight ?? false,
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
