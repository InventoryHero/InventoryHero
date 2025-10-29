<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import { Notifications } from '@kyvg/vue3-notification'
import useConfigStore from '@/stores/useConfigStore'

const currRoute = useRoute()
const { t } = useI18n()
const { mdAndUp } = useDisplay()
const { activeModal, isDirty, isAwaitingConfirmation, openModal, forceClose } =
  useGlobalModal()
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
const { user } = storeToRefs(authStore)

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

watch(activeModal, (newVal) => {
  if (!!newVal && !mdAndUp.value) {
    nav.value = false
  }
})

onBeforeRouteLeave(() => {})
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
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-qrcode-scan"
          variant="plain"
          color="primary"
          @click="openModal('scanQrCodeModal')"
        />
      </template>
    </v-app-bar>

    <v-navigation-drawer
      v-model="isDrawerOpen"
      :rail="rail"
      :permanent="mdAndUp"
    >
      <nav-items
        @open-create-item-modal="openModal('createItemModal')"
        @open-create-box-modal="openModal('createBoxModal')"
        @open-create-room-modal="openModal('createRoomModal')"
        @open-create-category-modal="openModal('createCategoryModal')"
      />
      <template v-slot:append>
        <v-list-item
          to="/settings"
          prepend-icon="mdi-cog"
          :title="t('nav.settings')"
          color="primary"
        />
        <v-spacer />
        <v-list-item
          to="/account"
          prepend-icon="mdi-account"
          :title="t('nav.account')"
          color="primary"
        />
        <template v-if="user?.admin">
          <v-list-item
            to="/administration"
            prepend-icon="mdi-shield-account"
            :title="t('nav.administration')"
            color="primary"
          />
        </template>
        <v-divider
          color="primary"
          class="border-opacity-50"
        />
        <v-list-item
          to="/logout"
          :title="t('nav.logout')"
          prepend-icon="mdi-logout"
        />
      </template>
    </v-navigation-drawer>
    <router-view v-slot="{ Component, route }">
      <v-main>
        <component
          v-if="!!activeModal"
          :model-value="!!activeModal"
          @update:model-value="forceClose"
          :is="activeModal.component"
          v-bind="{
            height: mdAndUp ? '700px' : '100%',
            width: mdAndUp ? '600px' : '100%',
            ...(activeModal.props ?? {})
          }"
        />
        <v-fab
          v-if="showFab"
          app
          location="right bottom"
          icon
          color="primary"
        >
          <v-icon icon="mdi-plus" />

          <fab-items
            v-model="fabOpen"
            @open-create-item-modal="openModal('createItemModal')"
            @open-create-box-modal="openModal('createBoxModal')"
            @open-create-room-modal="openModal('createRoomModal')"
            @open-create-category-modal="openModal('createCategoryModal')"
          />
        </v-fab>
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
