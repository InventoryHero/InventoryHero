<script lang="ts">
import {useAuthStore, useConfigStore, useSocketStore} from "@/store"
import AppBarBottom from "@/components/ui/AppBarBottom.vue";
import AppBar from "@/components/ui/AppBar.vue";
import {Notifications} from "@kyvg/vue3-notification";
import NavDrawer from "@/components/ui/NavDrawer.vue";
import {useRoute} from "vue-router";
import {isLoggedIn} from "axios-jwt";
import AppCreateBar from "@/components/ui/AppCreateBar.vue";
import {defineComponent} from "vue";

export default defineComponent({
  components: {
    AppCreateBar,
    NavDrawer,
    Notifications,
    AppBarBottom,
    AppBar
  },
  setup()
  {
    const config = useConfigStore()
    const authStore = useAuthStore()
    const socketStore = useSocketStore()
    const route = useRoute()

    if(authStore.isAuthorized())
    {
      socketStore.bindActions().then(() => {
        socketStore.joinHousehold()
      })
    }

    return {config, route, authStore, socketStore};
  },
  data(){
    return {
      navOpen: false
    }
  },
  watch: {
    authorized(){
      if(this.authorized){
        this.socketStore.bindActions().then(() => {
          this.socketStore.joinHousehold()
        })
      }
      else {
        this.socketStore.disconnect()
      }
    }
  },
  computed:{
    dockVisible(){
      return this.config.dock && !this.isAddRoute
    },
    isAddRoute(){
      return this.route.path === "/add"
    },
    authorized(){
      return this.authStore.isAuthorized()
    },
    isCreateRoute(){
      return this.route.path.includes("/create")
    }
  },
  methods:{
    reloadContent(){
      this.$router.go()
    }
  }
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
        :nav="!config.dock"
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
      :nav="!this.config.dock"
      @toggle-nav="navOpen = !navOpen"
    />
    <app-create-bar
      v-if="isCreateRoute"
    />
    <app-bar-bottom
        v-if="dockVisible"
    />
    <nav-drawer
        v-else
        v-model="navOpen"
    />


    <v-main
        class=""
    >
      <v-container
          :fluid="true"
          :class="{
            'fill-height': $route.meta?.fillHeight ?? false
          }"
      >
        <router-view v-slot="{Component}">
          <transition name="scale" mode="out-in" >
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
