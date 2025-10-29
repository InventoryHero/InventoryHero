<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import { useNotification } from '@kyvg/vue3-notification'
import {
  HouseholdMemberPublic,
  HouseholdPublic,
  Role
} from '@/api/types/households.ts'
import { storeToRefs } from 'pinia'
import {
  ROLE_ADMIN,
  ROLE_MEMBER,
  ROLE_OWNER
} from '@/api/types/householdRoles.ts'

const { household: householdEndpoint } = useAxios()
const authStore = useAuthStore()
const router = useRouter()
const { notify } = useNotification()
const { t } = useI18n()

const emit = defineEmits<{
  (e: 'kicked'): void
}>()

const {
  householdMember,
  household,
  isOwner = false
} = defineProps<{
  householdMember: HouseholdMemberPublic
  household: HouseholdPublic
  isOwner?: boolean
  isAdmin?: boolean
}>()

const { user } = storeToRefs(authStore)
const disabled = ref(user.value?.id === householdMember.user_id)
const username = computed(() => householdMember?.user?.username)
const role = computed(() => householdMember?.role)

const transferHouseholdDialog = ref<boolean>(false)
const transferringOwnership = ref(false)

const kickingUserDialog = ref<boolean>(false)
const kickingUser = ref(false)

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

// TODO FIX KICKED LOGIC
const kicked = ref(false)

function kickFromHousehold(kickConfirmed: boolean) {
  if (!kickConfirmed) {
    kickingUserDialog.value = true
    return
  }
  kickingUser.value = true
  householdEndpoint
    .removeMember(household.id, householdMember.user_id)
    .then(({ success }) => {
      // TODO ERROR HANDLING

      if (success) {
        kicked.value = true
        emit('kicked')
      }

      kickingUserDialog.value = false
      kickingUser.value = false
    })
}
function transferHousehold(confirmed: boolean = false) {
  if (!confirmed) {
    transferHouseholdDialog.value = true
    return
  }
  transferringOwnership.value = true
  householdEndpoint
    .transferOwnership(household.id, householdMember.user_id)
    .then(({ success, error }) => {
      if (!success) {
        notify({
          title: t(`toasts.titles.error.${error}`),
          text: t(`toasts.text.error.${error}`),
          type: 'error'
        })
        transferringOwnership.value = false
        transferHouseholdDialog.value = false
        return
      }
      transferringOwnership.value = false
      transferHouseholdDialog.value = false
      router.push('/households').then(() => {
        notify({
          title: t('toasts.titles.success.household_transferred'),
          text: t('toasts.text.success.household_transferred'),
          type: 'success'
        })
      })
    })
}
function updateRole(role: Role) {
  householdEndpoint
    .updateRole(household.id, householdMember.user_id, role)
    .then(({ success }) => {
      if (!success) {
        return
      }
      householdMember.role = role
    })
}

onBeforeRouteLeave(() => {
  return !transferHouseholdDialog.value && !kickingUserDialog.value
})
</script>
<template>
  <v-dialog
    :model-value="transferHouseholdDialog || kickingUserDialog"
    persistent
    no-click-animation
  >
    <v-card
      v-if="transferHouseholdDialog"
      :loading="transferringOwnership"
      :disabled="transferringOwnership"
    >
      <template v-slot:title>
        <i18n-t keypath="households.transfer.title">
          <template #user>
            <span class="text-primary">{{ username }}</span>
          </template>
        </i18n-t>
      </template>
      <v-card-text>
        {{ t('households.transfer.text', { user: username }) }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          :text="t('households.transfer.cancel')"
          @click="transferHouseholdDialog = false"
        />
        <v-btn
          :text="t('households.transfer.confirm')"
          @click="transferHousehold(true)"
        />
      </v-card-actions>
    </v-card>
    <v-card v-else-if="kickingUserDialog">
      <template v-slot:title>
        <i18n-t keypath="households.kick.title">
          <template #user>
            <span class="text-primary">{{ username }}</span>
          </template>
        </i18n-t>
      </template>
      <v-card-text>
        {{ t('households.kick.text', { user: username }) }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          :text="t('households.kick.cancel')"
          @click="kickingUserDialog = false"
        />
        <v-btn
          :text="t('households.transfer.confirm')"
          @click="kickFromHousehold(true)"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>

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
            <v-icon-btn
              icon="mdi-clipboard-outline"
              color="primary"
              @click="copyToClipboard()"
            />
            <template v-if="webShareApiSupported">
               <v-icon-btn
                   icon="mdi-share-variant"
                   @click="navigatorShare"
               />
            </template>
            <template v-else>
              <s-email
                  :share-options="emailShare"
              >
                <v-icon-btn
                    icon="mdi-email"
                    color="primary"
                />
              </s-email>
              <s-whats-app
                  :share-options="whatsAppShare"
              >
                <v-icon-btn
                    icon="mdi-whatsapp"
                    color="primary"
                />
              </s-whats-app>
            </template>
          </template>
        </v-text-field>
      </span>
      -->

      <template v-if="role !== ROLE_OWNER && !disabled">
        <v-icon-btn
          v-if="role === ROLE_MEMBER"
          variant="text"
          icon="mdi-shield"
          @click="updateRole(ROLE_ADMIN)"
        />
        <v-icon-btn
          v-if="role === ROLE_ADMIN"
          variant="text"
          icon="mdi-shield-off"
          @click="updateRole(ROLE_MEMBER)"
        />
        <v-icon-btn
          v-if="isOwner"
          variant="text"
          icon="mdi-transit-transfer"
          @click="transferHousehold(false)"
        />
        <v-icon-btn
          icon="mdi-account-remove"
          variant="text"
          @click="kickFromHousehold(false)"
        />
      </template>
    </template>
    <v-divider color="primary" />
  </v-card>
</template>

<style scoped lang="scss">
:deep(b) {
  color: rgba(var(--v-theme-primary), 1);
}
</style>
