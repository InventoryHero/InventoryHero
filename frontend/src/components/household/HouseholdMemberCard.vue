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

const kickFromHousehold = async (kickConfirmed: boolean) => {
  if (!kickConfirmed) {
    kickingUserDialog.value = true
    return
  }
  kickingUser.value = true
  const { success } = await householdEndpoint.removeMember(
    household.id,
    householdMember.user_id
  )

  if (success) {
    emit('kicked')
  }

  kickingUserDialog.value = false
  kickingUser.value = false
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
        console.error(error)
        transferringOwnership.value = false
        transferHouseholdDialog.value = false
        return
      }
      transferringOwnership.value = false
      transferHouseholdDialog.value = false
      router.push('/households').then(() => {
        notify({
          title: t('households.household_transfer.success'),
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
  if (transferHouseholdDialog.value) {
    return false
  }

  if (kickingUserDialog.value) {
    return false
  }
})
</script>
<template>
  <confirm-kick-from-household-dialog
    v-model:active="kickingUserDialog"
    :loading="kickingUser"
    :username="username"
    @kick="kickFromHousehold(true)"
  />

  <confirm-transfer-household-dialog
    v-model:active="transferHouseholdDialog"
    :loading="transferringOwnership"
    :username="username"
    @transfer="transferHousehold(true)"
  />

  <v-list-item
    density="compact"
    elevation="0"
    :disabled="disabled || transferringOwnership || kickingUser"
    class="fill-width"
    :title="username"
    :subtitle="t(`household.roles.${role}`)"
  >
    <template v-slot:append>
      <template v-if="role !== ROLE_OWNER && !disabled">
        <v-icon-btn
          variant="text"
          :icon="role === ROLE_MEMBER ? 'mdi-shield' : 'mdi-shield-off'"
          @click="updateRole(role === ROLE_MEMBER ? ROLE_ADMIN : ROLE_MEMBER)"
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
  </v-list-item>
  <v-divider color="primary" />
</template>

<style scoped lang="scss">
:deep(b) {
  color: rgba(var(--v-theme-primary), 1);
}
</style>
