<script setup lang="ts">
import {
  useNotificationStore
} from "@/store"
import AppBar from "@/components/ui/AppBar.vue";
import {Notifications} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";
import NavItems from "@/layouts/NavigationDrawer/NavItems.vue";
import {useModal} from "@/composables-new/useModal.ts";
import useContentRefreshStore from "@/store/useContentRefreshStore.ts";
import {storeToRefs} from "pinia";

const route = useRoute()
const router = useRouter()
const notificationStore = useNotificationStore()
const { mdAndUp, xs, sm, md, lg, xl } = useDisplay()
const { activeModal, closeModal, confirmLeave, cancelLeave, isAwaitingConfirmation } = useModal()
const contentRefreshStore = useContentRefreshStore()


const nav = ref(false)
const fabOpen = shallowRef(false)
const {isVisible, actionCallback, title, subtitle} = storeToRefs(contentRefreshStore)

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

const handleClickOnRefreshBanner = () => {
  if(actionCallback.value) {
    actionCallback.value()
  }
  contentRefreshStore.clearBanner()
}

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

    <v-dialog
        v-model="isAwaitingConfirmation"
        persistent
        width="auto"
    >
      <v-card class="pa-4" >
        <v-card-title class="text-h6">Unsaved Changes</v-card-title>
        <v-card-text>
          Are you sure you want to leave? Your changes will be lost.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="cancelLeave">Stay</v-btn>
          <v-btn color="error" variant="tonal" @click="confirmLeave">Discard Changes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
          <v-alert
              v-if="isVisible"
              density="compact"
              class="text-center content-changed-banner mb-4"
              width="100%"
              color="info"
              @click="handleClickOnRefreshBanner"
          >
            <template v-slot:text>
              <span class="text-center text-h5">
                {{title}}
              </span>
              <br/>
              <span v-if="subtitle" class="text-center text-medium-emphasis">
                {{subtitle}}
              </span>
            </template>

          </v-alert>
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