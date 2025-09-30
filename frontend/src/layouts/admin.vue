<script setup lang="ts">
import useAuthStore from '@/store/useAuthStore'
import { Notifications } from '@kyvg/vue3-notification'
import useConfigStore from '@/store/useConfigStore.ts'

const currRoute = useRoute()
const { t } = useI18n()
const { mdAndUp } = useDisplay()
const configStore = useConfigStore()
const authStore = useAuthStore()

const transition = computed(() => {
  if (configStore.transitions) {
    return {
      name: 'scale',
      mode: 'out-in'
    }
  }
  return {
    name: '',
    mode: ''
  }
})

const nav = ref(false)
const fabOpen = shallowRef(false)

const showFab = computed(
  () => (currRoute.meta.showFab ?? false) && !mdAndUp.value
)

const rail = computed(() => {
  if (mdAndUp.value) {
    return nav.value
  }
  return false
})

const isDrawerOpen = computed({
  get() {
    if (mdAndUp.value) {
      return true
    }
    return nav.value
  },
  set(value: boolean) {
    nav.value = value
  }
})
</script>

<template>
  <v-app>
    <notifications
      position="top right"
      classes="vue-notification mt-2 me-8"
      :max="2"
    />

    <v-app-bar density="compact">
      <v-app-bar-nav-icon @click.stop="nav = !nav" />
      <v-app-bar-title>
        <v-card
          hover
          width="fit-content"
          to="/"
          elevation="0"
        >
          {{ t('app.title') }}
        </v-card>
      </v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer
      v-model="isDrawerOpen"
      :rail="rail"
      :permanent="mdAndUp"
    >
      <admin-nav-items />
      <template v-slot:append>
        <v-list-item
          to="/settings"
          prepend-icon="mdi-cog"
          :title="t('nav.settings')"
          color="primary"
        />
        <v-divider
          color="primary"
          class="border-opacity-50"
        />
        <v-list-item
          to="/"
          :title="t('nav.leave_admin')"
          prepend-icon="mdi-back"
        />
      </template>
    </v-navigation-drawer>
    <router-view v-slot="{ Component, route }">
      <v-main>
        <transition
          :name="transition.name"
          :mode="transition.mode"
        >
          <v-container
            :key="route.fullPath"
            :class="{
              'fill-width': true,
              'fill-height': route.meta?.fillHeight ?? false
            }"
            fluid
          >
            <v-row justify="center">
              <v-col
                cols="12"
                lg="10"
              >
                <info-banner />

                <component :is="Component" />
              </v-col>
            </v-row>
          </v-container>
        </transition>
      </v-main>
    </router-view>
  </v-app>
</template>

<style scoped lang="scss">
.content-changed-banner {
  position: sticky;
  top: calc(var(--v-layout-top) + 16px);
  z-index: 2;
}
</style>
