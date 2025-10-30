<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import useAppStyling from '@/composables/useAppStyling.ts'
import { storeToRefs } from 'pinia'
import { HouseholdPublic } from '@/api/types/households.ts'
import { useNotification } from '@kyvg/vue3-notification'
const authData = useAuthStore()
const { household: householdEndpoint, userEndpoint } = useAxios()

const { t } = useI18n()
const $router = useRouter()
const { selectStyling } = useAppStyling()
const { notify } = useNotification()

const { collapsible = false } = defineProps<{
  collapsible?: boolean
}>()

const { household: selectedHousehold } = storeToRefs(authData)
const tmpSelected = ref<string | undefined>(selectedHousehold.value?.id)
const collapsed = ref(false)
const loadingUserHouseholds = ref(false)
const userHouseholds = ref<Array<HouseholdPublic>>([])
const savingNewDefaultHousehold = ref<boolean>(false)

const icon = computed(() => {
  if (collapsed.value) {
    return 'mdi-menu-down'
  }
  return 'mdi-menu-up'
})

const noDataText = computed(() => {
  if (loadingUserHouseholds.value) {
    return t('households.household_card.loading_households')
  }
  return t('households.household_card.create_new_household')
})

const placeholderText = computed(() => {
  if (loadingUserHouseholds.value) {
    return t('households.household_card.loading_households')
  } else if (userHouseholds.value.length === 0) {
    return t('households.household_card.create_new_household')
  }
  return t('households.household_card.select_household')
})

const saveBtnDisabled = computed(() => {
  return selectedHousehold.value?.id === tmpSelected.value
})

function saveHouseholdChanges() {
  if (tmpSelected.value === undefined) {
    notify({
      title: t('households.household_card.save_not_possible')
    })
    return
  }

  savingNewDefaultHousehold.value = true
  userEndpoint
    .setDefaultHousehold({
      id: tmpSelected.value
    })
    .then(({ success, data }) => {
      if (!success) {
        savingNewDefaultHousehold.value = false
        tmpSelected.value = selectedHousehold.value.id
        return
      }

      selectedHousehold.value = data!
      tmpSelected.value = data!.id
      savingNewDefaultHousehold.value = false
    })
}
function editHouseholds() {
  $router.push('/households')
}

onMounted(() => {
  householdEndpoint.all().then(({ success, data: households }) => {
    if (!success) {
      userHouseholds.value = []
      loadingUserHouseholds.value = false
      return
    }
    userHouseholds.value = households ?? []
    loadingUserHouseholds.value = false
  })
})
</script>

<template>
  <v-card
    v-bind="$attrs"
    density="compact"
    rounded="20"
    :disabled="savingNewDefaultHousehold"
    :loading="savingNewDefaultHousehold"
  >
    <v-card-title class="d-flex justify-space-between align-center">
      {{ t('households.household_card.title') }}
      <div>
        <v-icon-btn
          variant="text"
          icon="mdi-store-edit"
          color="primary"
          @click="editHouseholds"
        />
        <v-icon-btn
          variant="text"
          v-if="collapsible"
          :icon="icon"
          @click="collapsed = !collapsed"
        />
      </div>
    </v-card-title>
    <v-slide-y-transition>
      <v-container
        class="pt-0"
        v-show="!collapsed"
      >
        <v-select
          v-bind="selectStyling"
          :items="userHouseholds"
          item-title="name"
          item-value="id"
          :placeholder="placeholderText"
          :no-data-text="noDataText"
          v-model="tmpSelected"
          :loading="loadingUserHouseholds"
          :clearable="false"
        >
          <template v-slot:append>
            <v-icon-btn
              variant="text"
              :color="saveBtnDisabled ? '' : 'primary'"
              icon="mdi-content-save-check"
              :disabled="saveBtnDisabled"
              @click="saveHouseholdChanges"
            />
          </template>
        </v-select>
      </v-container>
    </v-slide-y-transition>
  </v-card>
</template>

<style scoped lang="scss"></style>
