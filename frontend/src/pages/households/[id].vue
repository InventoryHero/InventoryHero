<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import { useTemplateRef } from 'vue'
import { notify } from '@kyvg/vue3-notification'
import {
  HouseholdUpdate,
  HouseholdWithMembersPublic
} from '@/api/types/households.ts'
import { storeToRefs } from 'pinia'
import { ROLE_ADMIN, ROLE_OWNER } from '@/api/types/householdRoles.ts'
import { BreadcrumbItem } from 'vuetify/lib/components/VBreadcrumbs/VBreadcrumbs.mjs'

definePage({
  props: true,
  meta: {
    requiresAuth: true,
    requiresHousehold: false,
    layout: 'default'
  }
})

const authStore = useAuthStore()
const { household: householdEndpoint } = useAxios()
const { t } = useI18n()
const router = useRouter()
const route = useRoute()
const { textFieldStyling, btnStyle } = useAppStyling()

const { id = '' } = defineProps<{
  id?: string
}>()

const { user } = storeToRefs(authStore)
const nameField = useTemplateRef('name-field')

const loading = ref(false)
const deleteConfirmationVisible = ref<boolean>(false)
const household = ref<HouseholdWithMembersPublic>()
const newHouseholdName = ref<string | undefined>()
const deletingHousehold = ref(false)

const householdMembers = computed(() => {
  return (
    household.value?.members?.sort((a, b) => {
      if (a.user_id === authStore.user?.id) {
        return -1
      }
      if (b.user_id === authStore.user?.id) {
        return 1
      }

      return 0
    }) ?? []
  )
})
const householdId = computed(() => {
  return id
})

const breadcrumbs = computed(
  () =>
    [
      {
        title: t('nav.households'),
        to: '/households'
      },
      {
        to: route.fullPath,
        title: household.value?.name
      }
    ] as BreadcrumbItem[]
)

const householdName = computed({
  get() {
    if (newHouseholdName.value !== undefined) {
      return newHouseholdName.value ?? ''
    }
    return household.value?.name ?? ''
  },
  set(value: string) {
    newHouseholdName.value = value
  }
})

const myself = computed(() =>
  householdMembers.value?.find((x) => x.user_id === user.value?.id)
)
const isOwner = computed(() => ROLE_OWNER === myself.value?.role)

const rules = computed(() => [
  (value: string) => value.length > 0 || t('households.rules.name_required'),
  (value: string) =>
    value.length <= 25 || t('households.rules.name_shorter_than')
])

const deleteHousehold = async (confirmed: boolean) => {
  if (!confirmed) {
    deleteConfirmationVisible.value = true
    return
  }

  deletingHousehold.value = true
  const { success } = await householdEndpoint.delete(householdId.value)
  if (!success) {
    deleteConfirmationVisible.value = false
    deletingHousehold.value = false
    return
  }

  deleteConfirmationVisible.value = false
  router.push('/households')
  deletingHousehold.value = false
}

function removeFromHousehold(id: string) {
  const member = household.value?.members.find((member) => member.id === id)
  if (member) {
    household.value!.members = household.value!.members.filter(
      (m) => m.id !== id
    )
    notify({
      title: t('household.kicked_from_household', {
        user: member.user.username
      }),
      type: 'success'
    })
  }
}

async function updateName() {
  //@ts-expect-error this should be correct
  const valid = await nameField.value.validate()
  if (valid.length > 0) {
    return
  }
  householdEndpoint
    .update(householdId.value, {
      name: householdName.value
    } as HouseholdUpdate)
    .then(({ success, data }) => {
      if (success) {
        reset()
        household.value = {
          ...household.value!,
          ...data
        }
        notify({
          title: t(`household.household_updated`),
          type: 'success'
        })
      }
    })
}

function reset() {
  newHouseholdName.value = undefined
}

onBeforeMount(async () => {
  loading.value = true
  const { success, data, error } = await householdEndpoint.getAllMembers(
    householdId.value
  )

  if (!success) {
    await router.push(`/households/error?message=${error}`)
    return
  }

  household.value = data as HouseholdWithMembersPublic
  loading.value = false
})

onBeforeRouteLeave(() => {
  if (deleteConfirmationVisible.value) {
    return false
  }
})
</script>

<template>
  <confirm-household-delete-dialog
    v-model:active="deleteConfirmationVisible"
    :loading="deletingHousehold"
    @delete="deleteHousehold(true)"
  />

  <v-skeleton-loader
    type="text"
    width="250px"
    class="mb-2"
    :loading="loading"
  >
    <v-breadcrumbs :items="breadcrumbs" />
  </v-skeleton-loader>

  <v-skeleton-loader
    :loading="loading"
    type="text,list-item-two-line@5,actions"
  >
    <v-card
      :disabled="loading || deletingHousehold"
      :loading="deletingHousehold"
      class="household-card"
    >
      <template v-slot:loader="{ isActive }">
        <v-progress-linear
          indeterminate
          :active="isActive"
          color="primary"
        />
      </template>
      <template v-slot:title>
        <v-text-field
          ref="name-field"
          v-bind="textFieldStyling"
          density="compact"
          v-model="householdName"
          @click:clear="householdName = ''"
          :rules="rules"
        >
          <template v-slot:append>
            <v-icon-btn
              :disabled="newHouseholdName === undefined"
              color="primary"
              variant="plain"
              icon="mdi-content-save"
              @click="updateName"
              class="ms-n2 me-n2"
            />
          </template>
          <template v-slot:append-inner>
            <v-icon
              v-if="newHouseholdName !== undefined"
              icon="mdi-undo"
              @click="newHouseholdName = undefined"
            />
          </template>
        </v-text-field>
      </template>
      <v-card-text class="overflow-auto">
        <v-list>
          <household-member-card
            v-for="item in householdMembers"
            :is-owner="isOwner"
            :household-member="item"
            :household="household!"
            @kicked="removeFromHousehold(item.id)"
          />
        </v-list>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
          v-bind="btnStyle"
          v-if="isOwner"
          prepend-icon="mdi-trash-can"
          :text="t('households.edit.delete_household')"
          variant="tonal"
          color="red-accent-1"
          @click="deleteHousehold(false)"
        />
      </v-card-actions>
    </v-card>
  </v-skeleton-loader>
</template>

<style scoped lang="scss">
.household-card {
  height: calc(100dvh - 140px);
  display: flex;
  flex-direction: column;
}
</style>
