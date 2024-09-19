<script setup lang="ts">
import {Household} from "@/types"
import {useAuthStore, useHouseholdSocketStore} from "@/store";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import HouseholdInvite from "@/components/widgets/Households/Card/HouseholdInvite.vue";
import {HouseholdEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";

defineOptions({
  inheritAttrs: false
})
const authStore = useAuthStore()
const {axios: householdEndpoint} = useAxios<HouseholdEndpoint>("household")
const householdSocket = useHouseholdSocketStore()
const {notify} = useNotification()
const {t} = useI18n()
const router = useRouter()

const {
  household
} = defineProps<{
  household: Household
}>()

const isDefaultHousehold = computed(() => household.id === authStore.household?.id)

const selectedIcon = computed(() => {
  if(isDefaultHousehold.value){
    return 'mdi-checkbox-outline'
  }
  return 'mdi-checkbox-blank-outline'
})

const colorIfDefault = computed(() => {
  if(isDefaultHousehold.value){
    return 'primary'
  }
  return ''
})

const isOwnHousehold = computed(() => household.creator === authStore.user?.id)


const requestInProgress = ref(false)
const leaveConfirmed = ref(false)


const {
  isVisible: inviteDialogVisible,
  openDialog: openInviteDialog,
  closeDialog: closeInviteDialog,
} = useDialogConfig()

const {
  isVisible: confirmLeaveDialogVisible,
  openDialog: openConfirmLeaveDialog,
  closeDialog: closeConfirmLeaveDialog,
} = useDialogConfig()

function setAsHousehold(){
  authStore.changeHousehold(household)
  authStore.followReturnUrl()
}

function reallyLeave(){
  leaveConfirmed.value = true
  closeConfirmLeaveDialog()
  leaveHousehold()
}

function leaveHousehold(){
  if(!leaveConfirmed.value){
    openConfirmLeaveDialog()
    return
  }

  requestInProgress.value = true
  if(isDefaultHousehold.value){
    householdSocket.leaveHousehold()
  }
  householdEndpoint.leaveHousehold(household.id).then((success) => {
    if(success) {
      notify({
        title: t('toasts.titles.success.household_left'),
        text: t('toasts.text.success.household_left'),
        type: 'success'
      })
      if (isDefaultHousehold.value) {
        authStore.changeHousehold(undefined)
      }
      authStore.leftHousehold(household)
    }
    requestInProgress.value = false
  })
}

</script>

<template>

  <confirmation-dialog
      v-model:dialog-opened="confirmLeaveDialogVisible"
      :text="t('households.leave.confirm.text')"
      :cancel-text="t('households.leave.confirm.stay')"
      :confirm-text="t('households.leave.confirm.leave')"
      confirm-icon="mdi-location-exit"
      cancel-icon="mdi-home"
      :on-cancel="closeConfirmLeaveDialog"
      :on-confirm="reallyLeave"
  >
    <template v-slot:title>
      <p
          v-html="t('households.leave.confirm.title', {name: household.name})"
      />
    </template>
  </confirmation-dialog>


  <v-dialog
      v-model="inviteDialogVisible"
      persistent
      no-click-animation
  >
    <household-invite
        :household="household"
        @close="closeInviteDialog"
    />
  </v-dialog>

  <v-card
      density="comfortable"
      class="pb-1"
      elevation="0"
  >
    <template v-slot:loader>
      <v-progress-linear
        indeterminate
        :active="requestInProgress"
        color="primary"
      />
    </template>
    <v-card-text
        class="d-flex justify-space-between align-center"
    >
      <span
          class="d-inline-block text-truncate flex-1-1"
      >
        {{ household.name }}
      </span>
      <v-sheet
          class="flex-0-0"
      >
        <app-icon-btn
            v-if="isOwnHousehold"
            icon="mdi-store-edit"
            class="me-1"
            :to="`/households/edit/${household.id}`"
        />
        <app-icon-btn
            v-if="isOwnHousehold"
            icon="mdi-account-plus"
            class="me-1"
            @click.stop="openInviteDialog"
        />
        <app-icon-btn
            v-if="!isOwnHousehold"
            icon="mdi-location-exit"
            class="me-1"
            @click.stop="leaveHousehold"
        />
        <app-icon-btn
            :icon="selectedIcon"
            :color="colorIfDefault"
            @click="setAsHousehold"
        />
      </v-sheet>
    </v-card-text>
    <v-divider
        class="border-opacity-50"
    />
  </v-card>
</template>

<style scoped lang="scss">

</style>