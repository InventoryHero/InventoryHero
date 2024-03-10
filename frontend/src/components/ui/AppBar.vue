<script lang="ts">

import {defineComponent} from "vue";
import {useAuthStore} from "@/store";
import {useRoute} from "vue-router";

export default defineComponent({
  name: "AppBar",
  setup(){
    const authStore = useAuthStore()
    const route = useRoute()
    return {authStore, route}
  },
  emits: {
    toggleNav(){
      return true
    }
  },
  computed: {
    displayNav(){
      return this.nav && this.isAuthorized
    },
    isAuthorized(){
      return this.authStore.isAuthorized();
    },
    isSettings(){
      return this.route.name === "settings"
    },

  },
  data(){
    return{
      userDropdown: false,
      scanQrCode: false,
    }
  },
  methods:{
    toggleNav(){
      this.$emitter.emit('nav-opened')
      this.$emit('toggleNav')
    }
  },
  props:{
    nav:{
      type: Boolean,
      default: false
    }
  },
  beforeMount() {
  }
})
</script>

<template>
  <v-app-bar
      density="compact"
  >
    <v-app-bar-nav-icon
        v-if="displayNav"
        @click.stop="toggleNav()"
    ></v-app-bar-nav-icon>
    <v-toolbar-title>
      {{ $t('app.title') }}
    </v-toolbar-title>
    <template v-slot:append>
      <app-icon-btn
        v-if="isAuthorized"
        icon="mdi-qrcode-scan"
        color="primary"
        class="me-2"
        size="small"
        @click="scanQrCode=true"
      />
      <app-bar-overflow-menu
          v-if="isAuthorized"
      />

      <template
          v-else
      >
        <v-btn
            v-if="!isSettings"
            icon="fa:fas fa-gears"
            size="small"
            @click="() => {$router.push('/settings')}"
        />
        <v-btn
            v-else
            icon="fa:fas fa-arrow-left"
            size="small"
            @click="() => {$router.push('/login')}"
        />

      </template>

    </template>
  </v-app-bar>


  <scan-qr-code-modal
    v-model="scanQrCode"
  />

</template>

<style scoped lang="scss">
  .header{
    width: 100%;
    height: var(--header-height);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 4;
    background: var(--clr-bg);
    display: flex;
    align-items: center;
    .user-dropdown{
      display: flex;
      justify-content: end;
      .active
      {
        color: var(--clr-filter-pressed);
      }
      .inactive{
        color: var(--clr-icon-inactive);
      }
    }
    .title{
      display: flex;
      justify-content: center;
    }
  }
</style>