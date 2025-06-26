<script setup lang="ts">
import {useAuthStore, useHouseholdSocketStore} from "@/store";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import HouseholdInvite from "@/components/widgets/Households/Card/HouseholdInvite.vue";
import {useNotification} from "@kyvg/vue3-notification";
import {HouseholdWithMemberPublic} from "@/api/types/households.ts";
import {storeToRefs} from "pinia";
import {ROLE_ADMIN, ROLE_OWNER} from "@/api/types/householdRoles.ts";

defineOptions({
  inheritAttrs: false
})
const authStore = useAuthStore()
const {household: defaultHousehold, user} = storeToRefs(authStore)
const {household: householdEndpoint, userEndpoint} = useAxios()

//TODO const householdSocket = useHouseholdSocketStore()
const {notify} = useNotification()
const {t} = useI18n()

const {
  household
} = defineProps<{
  household: HouseholdWithMemberPublic
}>()

const emit = defineEmits<{
  left: [id: string]
}>()

const isDefaultHousehold = computed(() => household.id === defaultHousehold.value?.id)
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

const isAdmin = computed(() => household.member.role == ROLE_ADMIN)
const isOwner = computed(() => household.member.role == ROLE_OWNER)


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

async function setAsHousehold(){

  const {success, data: newDefault} = await userEndpoint.setDefaultHousehold({
    id: household.id
  })
  console.log(success)
  if(success){
    defaultHousehold.value = newDefault
    await authStore.followReturnUrl()
  }
  // TODO ERROR
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
    // TODO
    //householdSocket.leaveHousehold()
  }

  householdEndpoint.leaveHousehold(household.id).then((success) => {
    if(success) {
      notify({
        title: t('toasts.titles.success.household_left'),
        text: t('toasts.text.success.household_left'),
        type: 'success'
      })
      emit('left', household.id)
    }
    requestInProgress.value = false
  })
}

</script>

<template>



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
      :loading="requestInProgress"
      :disabled="requestInProgress"
  >
    <template v-slot:loader="{isActive}">
      <v-progress-linear
        indeterminate
        :active="isActive"
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
            v-if="isOwner || isAdmin"
            icon="mdi-store-edit"
            class="me-1"
            :to="`/households/edit/${household.id}`"
        />
        <app-icon-btn
            v-if="isOwner || isAdmin"
            icon="mdi-account-plus"
            class="me-1"
            @click.stop="openInviteDialog"
        />
        <app-icon-btn
            v-if="!isOwner"
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

  </v-card>
  <v-divider
      class="border-opacity-50"
  />
</template>

<style scoped lang="scss">

</style>