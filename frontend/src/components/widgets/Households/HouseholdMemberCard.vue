<script setup lang="ts">

import {Household, HouseholdMember} from "@/types";
import useShareMethods from "@/composables/useShareMethods.ts";
import {useAuthStore} from "@/store";
import {HouseholdEndpoint} from "@/api/http";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";
import {useNotification} from "@kyvg/vue3-notification";


const {axios: householdEndpoint} = useAxios<HouseholdEndpoint>("household")
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
  disabled=false,
} = defineProps<{
  householdMember: HouseholdMember,
  household: Household,
  disabled?: boolean,
}>()

const householdName = computed(() => household.name)
const invite = computed(() => `${window.location.origin}/join/${householdMember.invite}`)
const {
  webShareApiSupported,
  copiedConfirm,
  emailShare,
  whatsAppShare,
  navigatorShare,
  copyToClipboard
} = useShareMethods(invite, householdName)


// transfer ownership
const transferringOwnership = ref(false)
const transferConfirmed = ref(false)
const {
  isVisible: transferOwnershipConfirmDialogVisible,
  openDialog: openTransferOwnershipConfirmDialog,
  closeDialog: closeTransferOwnershipConfirmDialog
} = useDialogConfig()

function transferHousehold(){
  if(!transferConfirmed.value){
    openTransferOwnershipConfirmDialog()
    return
  }
  transferringOwnership.value = true
  householdEndpoint.transferHousehold(household.id, householdMember.username).then((success) => {
    if(!success){
      return
    }
    authStore.fetchHouseholds().then(() => {
      router.push("/").then(() => {
        notify({
          title: t("toasts.titles.success.household_transferred"),
          text: t("toasts.text.success.household_transferred"),
          type: 'success'
        })
      })
    })

  })
}

// remove / kick from household
const isInviteDeletion = ref(false)
const kickingUser = ref(false)
const kicked = ref(false)
const kickConfirmed = ref(false)
const {
  isVisible: kickConfirmDialogVisible,
  openDialog: openKickConfirmDialog,
  closeDialog: closeKickConfirmDialog
} = useDialogConfig()
const confirmDialogConfig = computed(() => {
  if(isInviteDeletion.value){
    return {
      text: t('households.edit.delete_invite.confirm.text'),
      title: t('households.edit.delete_invite.confirm.title'),
      cancelText: t('households.edit.delete_invite.confirm.abort'),
      confirmText: t('households.edit.delete_invite.confirm.confirm'),
      confirmIcon: "mdi-delete",
    }
  } else{
    return {
      text: t('households.edit.kick.confirm.text'),
      title: t('households.edit.kick.confirm.title'),
      cancelText: t('households.edit.kick.confirm.abort'),
      confirmText: t('households.edit.kick.confirm.confirm'),
      confirmIcon: "mdi-account-off",
    }
  }
})
function deleteInvite(){
  isInviteDeletion.value = true
  removeFromHousehold()
}
function kickFromHousehold(){
  isInviteDeletion.value = false
  removeFromHousehold()
}

function removeFromHousehold(){
  if(!kickConfirmed.value){
    openKickConfirmDialog()
    return
  }


  kickingUser.value = true
  householdEndpoint.kickFromHousehold(household.id, householdMember.id).then((success) => {

    if(success){
      kicked.value = true
      emit('kicked')
    }
    closeKickConfirmDialog()
    kickingUser.value = false

  })
}
</script>
<template>

  <confirmation-dialog
    :dialog-opened="kickConfirmDialogVisible"
    v-bind="confirmDialogConfig"
    :on-cancel="closeKickConfirmDialog"
    :on-confirm="() => {
      kickConfirmed = true
      removeFromHousehold()
    }"
  >
    <template v-slot:text>
      <p v-html="confirmDialogConfig.text" />
    </template>
  </confirmation-dialog>

  <confirmation-dialog
    :dialog-opened="transferOwnershipConfirmDialogVisible"
    :title="t('households.edit.transfer_ownership.confirm.title')"
    :cancel-text="t('households.edit.transfer_ownership.confirm.abort')"
    :confirm-text="t('households.edit.transfer_ownership.confirm.confirm')"
    cancel-icon="mdi-cancel"
    confirm-icon="mdi-account-arrow-right"
    :on-cancel="closeTransferOwnershipConfirmDialog"
    :on-confirm="() => {
      transferConfirmed = true
      transferHousehold()
    }"
  >
    <template v-slot:text>
      <p v-html="t('households.edit.transfer_ownership.confirm.text', {user: householdMember.username})" />
    </template>
  </confirmation-dialog>

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

  <v-card
    v-if="!kicked"
    density="compact"
    elevation="0"
    :disabled="disabled || transferringOwnership || kickingUser"
    class="fill-width"
  >
    <template v-slot:loader>
      <v-progress-linear
        indeterminate
        :active="transferringOwnership || kickingUser"
        color="primary"
      />
    </template>
    <v-card-text
      class="d-flex align-center"
    >
      <span
        v-if="householdMember.joined"
        class="d-inline-block text-wrap flex-1-1"
      >
        {{ householdMember.username }}
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
      <div
        class="flex-0-0"
      >
        <template v-if="householdMember.joined">
          <app-icon-btn
            icon="mdi-transfer"
            @click="transferHousehold"
          />
          <app-icon-btn
              icon="mdi-account-remove"
              @click="kickFromHousehold"
          />
        </template>
        <app-icon-btn
          v-else
          icon="mdi-trash-can"
          @click="deleteInvite"
        />
      </div>
    </v-card-text>
    <v-divider
      color="primary"
    />
  </v-card>
</template>

<style scoped lang="scss">

</style>