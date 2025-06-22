<script setup lang="ts">
import {
  useNotificationStore
} from "@/store"
import AppBar from "@/components/ui/AppBar.vue";
import {Notifications} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";
import NavItems from "@/layouts/NavigationDrawer/NavItems.vue";

const route = useRoute()
const router = useRouter()
const notificationStore = useNotificationStore()
const { mdAndUp, xs, sm, md, lg, xl } = useDisplay()

const nav = ref(false)
const fabOpen = shallowRef(false)

const {
  showFab = false
} = defineProps<{
  showFab?: boolean
}>()

const rail = computed(() => {
  if(mdAndUp.value) {
    return nav.value
  }
  return false
})

const isDrawerOpen = computed({
  get(){
    if(mdAndUp.value) {
      return true
    }
    return nav.value
  },
  set(value: boolean){
    nav.value = value
  }
})

function reloadContent(){
  router.go(0)
}

const tab = ref(TabType.Product)
provide("tab", tab)

onUpdated(async () => {
  notificationStore.triggerNotifications()
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
  />

  <app-bar>
    <v-app-bar-nav-icon
        @click.stop="nav = !nav"
    ></v-app-bar-nav-icon>
  </app-bar>

  <v-navigation-drawer
      v-model="isDrawerOpen"
      :rail="rail"
      :permanent="mdAndUp"
  >
    <nav-items />
  </v-navigation-drawer>

  <v-main
  >
    <v-fab
        v-if="showFab && !mdAndUp"
        app
        location="right bottom"
        icon
        color="primary"
    >
      <v-icon icon="mdi-plus"/>
      <v-speed-dial
          location="top center"
          transition="slide-x-transition"
          v-model="fabOpen"
          activator="parent"
      >
        <v-btn key="1" color="success" icon>
          <v-icon size="24">$success</v-icon>
        </v-btn>

        <v-btn key="2" color="info" icon>
          <v-icon size="24">$info</v-icon>
        </v-btn>

        <v-btn key="3" color="warning" icon>
          <v-icon size="24">$warning</v-icon>
        </v-btn>

        <v-btn key="4" color="error" icon>
          <v-icon size="24">$error</v-icon>
        </v-btn>
      </v-speed-dial>
    </v-fab>
    <v-container
        :class="{
          'fill-width': true,
          'fill-height': route.meta?.fillHeight ?? false,
        }"
        fluid
    >

      <v-row
          justify="center"
      >
        <v-col
            cols="12"
            lg="10"
        >
          <slot />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<style scoped lang="scss">

</style>