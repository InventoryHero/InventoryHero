<script setup lang="ts">

import {Household, HouseholdMember} from "@/types";
import useShareMethods from "@/composables/useShareMethods.ts";
import {useAuthStore} from "@/store";
import {HouseholdEndpoint} from "@/api/http";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {useNotification} from "@kyvg/vue3-notification";
import {HouseholdMemberPublic, HouseholdPublic, Role} from "@/api/types/households.ts";
import {storeToRefs} from "pinia";
import {ROLE_ADMIN, ROLE_MEMBER, ROLE_OWNER} from "@/api/types/householdRoles.ts";


const {household: householdEndpoint} = useAxios()
const authStore = useAuthStore()
const router = useRouter()
const {notify} = useNotification()

const emit = defineEmits<{
  (e: 'kicked'): void
}>()

const {styling} = useAppStyling()
const {t} = useI18n()

const {
    householdMember,
    household,
    isOwner=false
} = defineProps<{
    householdMember: HouseholdMemberPublic,
    household: HouseholdPublic,
    isOwner?: boolean,
    isAdmin?: boolean
}>()



const {user} = storeToRefs(authStore)
const disabled = ref(user.value?.id === householdMember.user_id)
const username = computed(() => householdMember?.user?.username)


const role = computed(() => householdMember?.role)

const householdName = computed(() => household.name)

// TODO INVITES
/*
const invite = computed(() => `${window.location.origin}/join/${householdMember.invite}`)
const {
  webShareApiSupported,
  copiedConfirm,
  emailShare,
  whatsAppShare,
  navigatorShare,
  copyToClipboard
} = useShareMethods(invite, householdName)
*/

// transfer ownership
const transferringOwnership = ref(false)
const transferConfirmed = ref(false)
const {
  isVisible: transferOwnershipConfirmDialogVisible,
  openDialog: openTransferOwnershipConfirmDialog,
  closeDialog: closeTransferOwnershipConfirmDialog
} = useDialogConfig()

// remove / kick from household
const kickingUser = ref(false)
const kicked = ref(false)
const kickConfirmed = ref(false)
const {
  isVisible: kickConfirmDialogVisible,
  openDialog: openKickConfirmDialog,
  closeDialog: closeKickConfirmDialog
} = useDialogConfig()
const confirmDialogConfig = computed(() => {
  return {
    text: t('households.edit.kick.confirm.text'),
    title: t('households.edit.kick.confirm.title'),
    cancelText: t('households.edit.kick.confirm.abort'),
    confirmText: t('households.edit.kick.confirm.confirm'),
    confirmIcon: "mdi-account-off",
  }
})

function kickFromHousehold(){
  removeFromHousehold()
}
function removeFromHousehold(){
  if(!kickConfirmed.value){
    openKickConfirmDialog()
    return
  }
  kickingUser.value = true
  householdEndpoint.removeMember(household.id, householdMember.user_id).then(({success}) => {
    // TODO ERROR HANDLING

    if(success){
      kicked.value = true
      emit('kicked')
    }

    closeKickConfirmDialog()
    kickingUser.value = false

  })
}
function transferHousehold(){
  if(!transferConfirmed.value){
    openTransferOwnershipConfirmDialog()
    return
  }
  transferringOwnership.value = true
  householdEndpoint.transferOwnership(household.id, householdMember.user_id).then(({success, error}) => {
    if(!success){
      notify({
        title: t(`toasts.titles.error.${error}`),
        text: t(`toasts.text.error.${error}`),
        type: 'error'
      })
      transferringOwnership.value = false
      closeTransferOwnershipConfirmDialog()
      return
    }
    router.push("/households").then(() => {
      notify({
        title: t("toasts.titles.success.household_transferred"),
        text: t("toasts.text.success.household_transferred"),
        type: 'success'
      })
    })

  })
}
function updateRole(role: Role){
  householdEndpoint.updateRole(household.id, householdMember.user_id, role).then(({success}) => {
    if(!success){
      return
    }
    householdMember.role = role
  })
}


</script>
<template>


  <!--
    <v-snackbar
        v-model="copiedConfirm"
        :timeout="2000"
        elevation="24"
        rounded="pill"
        color="success"
        :multi-line="false"
        @click="copiedConfirm=false"

    >
      <p
          class="d-flex justify-center"
      >
        {{ $t('toasts.titles.success.copied_to_clipboard')}}
      </p>
    </v-snackbar>
  -->
  <v-card
    v-if="!kicked"
    density="compact"
    elevation="0"
    :disabled="disabled || transferringOwnership || kickingUser"
    class="fill-width"
    :title="username"
    :subtitle="t(`household.roles.${role}`)"
  >
    <template v-slot:loader>
      <v-progress-linear
        indeterminate
        :active="transferringOwnership || kickingUser"
        color="primary"
      />
    </template>
    <template v-slot:append>
      <!--<span
        v-if="householdMember.joined"
        class="d-inline-block text-wrap flex-1-1"
      >
        {{ username }}
      </span>
      <span
        v-else
        class="flex-1-1"
      >
        <v-text-field
          v-bind="styling"
          :label="t('households.edit.invite_link')"
          :clearable="false"
          :model-value="invite"
          density="compact"
          readonly
        >
          <template v-slot:append>
            <app-icon-btn
              icon="mdi-clipboard-outline"
              color="primary"
              @click="copyToClipboard()"
            />
            <template v-if="webShareApiSupported">
               <app-icon-btn
                   icon="mdi-share-variant"
                   @click="navigatorShare"
               />
            </template>
            <template v-else>
              <s-email
                  :share-options="emailShare"
              >
                <app-icon-btn
                    icon="mdi-email"
                    color="primary"
                />
              </s-email>
              <s-whats-app
                  :share-options="whatsAppShare"
              >
                <app-icon-btn
                    icon="mdi-whatsapp"
                    color="primary"
                />
              </s-whats-app>
            </template>
          </template>
        </v-text-field>
      </span>
      -->

      <template v-if="role !== ROLE_OWNER">
        <app-icon-btn
          v-if="role === ROLE_MEMBER"
          icon="mdi-shield"
          @click="updateRole(ROLE_ADMIN)"
        />
        <app-icon-btn
          v-if="role === ROLE_ADMIN"
          icon="mdi-shield-off"
          @click="updateRole(ROLE_MEMBER)"
        />
        <app-icon-btn
            v-if="isOwner"
            icon="mdi-transit-transfer"
            @click="transferHousehold"
        />
        <app-icon-btn
            icon="mdi-account-remove"
            @click="kickFromHousehold"
        />
      </template>
    </template>
    <v-divider
      color="primary"
    />
  </v-card>
</template>

<style scoped lang="scss">

</style>