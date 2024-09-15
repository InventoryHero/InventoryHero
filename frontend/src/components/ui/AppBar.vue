<script setup lang="ts">
import {useAuthStore} from "@/store";

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

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

const tabsVisible = computed(() => route.path === "/create")

const tab = inject<string>("tab")




function toggleNav(){
  emit('toggleNav')
}

</script>

<template>
  <v-app-bar
      density="comfortable"
  >
    <template v-slot:prepend>
      <v-app-bar-nav-icon
          v-if="displayNav"
          @click.stop="toggleNav()"
      ></v-app-bar-nav-icon>
    </template>
    <v-app-bar-title>
      <v-card
        hover
        width="fit-content"
        to="/"

      >
        {{ $t('app.title') }}
      </v-card>
    </v-app-bar-title>
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


  <template
      v-slot:extension
      v-if="tabsVisible"
  >
    <v-tabs

      v-model="tab"
      rounded="0"
      color="primary"

    >
      <v-tab
        value="product"
        prepend-icon="mdi-cart"
      >
        {{ $t('add.product.tab') }}
      </v-tab>
      <v-tab
        value="box"
        prepend-icon="mdi-package-variant"
      >
        {{ $t('add.box.tab') }}
      </v-tab>
      <v-tab
        value="location"
        prepend-icon="mdi-archive-marker"
      >
        {{ $t('add.location.tab') }}
      </v-tab>
    </v-tabs>
  </template>
  </v-app-bar>
</template>

<style scoped lang="scss">

.hovering{
  cursor: pointer !important;
}


</style>