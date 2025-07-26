<script setup lang="ts">
import useAuthStore from "@/store/useAuthStore";
import HouseholdInvite from "@/components/household/HouseholdInvite.vue";
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
const route = useRoute();
const router = useRouter();

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

const inviteDialogVisible = ref<boolean>(false)
const leaveConfirmationDialog = ref<boolean>(false)

async function setAsHousehold(){
  const redirectPath = route.query.redirect as string || undefined;
  const {success, data: newDefault} = await userEndpoint.setDefaultHousehold({
    id: household.id
  })
  console.log(success)
  if(!success){
    // TODO ERROR
  }

  defaultHousehold.value = newDefault

  if(redirectPath){
    router.replace(redirectPath)
  }

  // TODO ERROR
}


function leaveHousehold(confirmed: boolean){
  if(!confirmed){
    leaveConfirmationDialog.value = true
    return
  }

  requestInProgress.value = true
  if(isDefaultHousehold.value){
    // TODO
    //householdSocket.leaveHousehold()
  }

  householdEndpoint.leaveHousehold(household.id).then((success) => {
    if(!success) {
      // TODO ERROR
    }
    notify({
      title: t('toasts.titles.success.household_left'),
      text: t('toasts.text.success.household_left'),
      type: 'success'
    })
    leaveConfirmed.value = false
    emit('left', household.id)
    requestInProgress.value = false
  })
}

onBeforeRouteLeave(() => {
  return !inviteDialogVisible.value && !leaveConfirmationDialog.value
})

</script>

<template>
  <v-dialog
      :model-value="inviteDialogVisible || leaveConfirmationDialog"
      persistent
      no-click-animation
  >
    <household-invite
        v-if="inviteDialogVisible"
        :household="household"
        @close="inviteDialogVisible = false"
    />

    <v-card
      v-else-if="leaveConfirmationDialog"
      :title="t('households.leave.title')"
      :text="t('households.leave.text')"
      :loading="requestInProgress"
      :disabled="requestInProgress"
    >
      <template v-slot:title>
        <i18n-t keypath="households.leave.title">
          <template #name>
            <span class="text-primary">{{household.name}}</span>
          </template>
        </i18n-t>
      </template>
      <v-card-actions>
        <v-btn
            :text="t('households.leave.cancel')"
            @click="leaveConfirmationDialog = false"
        />
        <v-btn
          :text="t('households.leave.confirm')"
          @click="leaveHousehold"
        />
      </v-card-actions>

    </v-card>
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
        <v-icon-btn
            v-if="isOwner || isAdmin"
            variant="text"
            size="medium"
            density="comfortable"
            class="me-2"
            icon="mdi-store-edit"
            @click="router.push(`/households/${household.id}`)"
        />
        <v-icon-btn
            v-if="isOwner || isAdmin"
            variant="text"
            size="medium"
            density="comfortable"
            class="me-2"
            icon="mdi-account-plus"
            @click.stop="inviteDialogVisible = true"
        />
        <v-icon-btn
            v-if="!isOwner"
            variant="text"
            size="medium"
            density="comfortable"
            class="me-2"
            icon="mdi-location-exit"
            @click.stop="leaveHousehold(false)"
        />
        <v-icon-btn
            variant="text"
            size="medium"
            density="comfortable"
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