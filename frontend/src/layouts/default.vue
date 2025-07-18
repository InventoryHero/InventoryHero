<script setup lang="ts">
import {
  useNotificationStore
} from "@/store"
import {Notifications} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";
import NavItems from "@/layouts/NavigationDrawer/NavItems.vue";
import {useModal} from "@/composables-new/useModal.ts";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";
import {storeToRefs} from "pinia";

const route = useRoute()
const router = useRouter()
const {t} = useI18n()
const notificationStore = useNotificationStore()
const { mdAndUp, xs, sm, md, lg, xl } = useDisplay()
const { activeModal, closeModal, confirmLeave, cancelLeave, isAwaitingConfirmation } = useModal()



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

watch(activeModal, (newVal) => {
  if(newVal && !mdAndUp.value){
    nav.value = false
  }
  else if(newVal){
    nav.value = true
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

  <v-app-bar
      density="compact"
  >
    <v-app-bar-nav-icon
        @click.stop="nav = !nav"
    />
    <v-app-bar-title>
      <v-card
          hover
          width="fit-content"
          to="/"

      >
        {{ t('app.title') }}
      </v-card>
    </v-app-bar-title>
    <template v-slot:append>
      <app-icon-btn
          icon="mdi-qrcode-scan"
          color="primary"
          to="/qr/scan"
      />
    </template>


  </v-app-bar>

  <v-navigation-drawer
      v-model="isDrawerOpen"
      :rail="rail"
      :permanent="mdAndUp"
  >
    <nav-items />
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
      <template
          v-if="false"
      >
        <!--TODO ADMIN-->
        <v-list-item
            to="/administration"
            prepend-icon="mdi-shield-account"
            :title="t('nav.administration')"
            color="primary"
        />
      </template>
      <v-divider color="primary" class="border-opacity-50"/>
      <v-list-item
          to="/logout"
          :title="t('nav.logout')"
          prepend-icon="mdi-logout"

      />
    </template>
  </v-navigation-drawer>

  <v-main>
    <confirm-leave-dialog
        v-model="isAwaitingConfirmation"
        @cancel="cancelLeave"
        @confirm="confirmLeave"
    />
    <v-dialog
      :model-value="!!activeModal"
      @update:model-value="closeModal(null)"
      scrollable
      :height="!(xs || sm) ? '700px' : '100%'"
      :width="!(xs || sm) ? '600px' : '100%'"
    >
      <component
        v-if="activeModal"
        :is="activeModal!.component"
        v-bind="activeModal!.props ?? {}"
        @close="closeModal"
      />
    </v-dialog>
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
          <info-banner />
          <slot />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<style scoped lang="scss">
.content-changed-banner {
  position: sticky;
  top: calc(var(--v-layout-top) + 16px);
  z-index: 2;
}
</style>