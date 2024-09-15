<script setup lang="ts">
import {useAuthStore} from "@/store";
import useDialogConfig from "@/composables/useDialogConfig.ts";

const authStore = useAuthStore()
const route = useRoute()

const emit = defineEmits<{
  (e: 'toggleNav'): void,
  (e: 'scanQrCode'): void
}>()

const {nav=false} = defineProps<{
  nav?: boolean
}>()

const displayNav = computed(() => {
  return nav && isAuthorized.value
})
const isAuthorized = computed(() => {
  return authStore.authorized
})

const isSettings = computed(() => {
  return route.name === "settings"
})





function toggleNav(){
  emit('toggleNav')
}

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
      <v-card
          hover
          width="fit-content"
          color="dark-grey"
          to="/"
      >
        {{ $t('app.title') }}
      </v-card>
    </v-toolbar-title>
    <template v-slot:append>
      <app-icon-btn
        v-if="isAuthorized"
        icon="mdi-qrcode-scan"
        color="primary"
        @click="emit('scanQrCode')"
      />
      <app-bar-overflow-menu
          v-if="isAuthorized"
      />

      <template
          v-else
      >
        <app-icon-btn
            v-if="!isSettings"
            icon="mdi-cog"
            size="x-large"
            @click="() => {$router.push('/settings')}"
        />
        <app-icon-btn
            v-else
            icon="mdi-arrow-left"
            size="x-large"
            @click="() => {$router.push('/login')}"
        />

      </template>

    </template>

  </v-app-bar>




</template>

<style scoped lang="scss">

.hovering{
  cursor: pointer !important;
}
</style>