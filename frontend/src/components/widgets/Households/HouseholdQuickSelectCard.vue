<script setup lang="ts">
import {computed, defineComponent, onMounted, PropType, ref} from 'vue'
import {useAuthStore} from "@/store";
import useNewAxios from "@/composables/useAxios.ts";
import {HouseholdEndpoint} from "@/api/http";
import {Household} from "@/types";
import useAxios from "@/composables/useAxios.ts";
import {useI18n} from "vue-i18n";
import {useRouter} from "vue-router";
const authData = useAuthStore();
const {axios} = useAxios<HouseholdEndpoint>("household");

const {t: $t} = useI18n()
const $router = useRouter()

const {collapsible=false} = defineProps<{
  collapsible?: boolean
}>()

const collapsed = ref(false)
const loadingUserHouseholds = ref(false)
const userHouseholds = ref<Array<Household>>([])
const selectedHousehold = ref<Household|undefined>(undefined)

const icon = computed(() =>{
  if(collapsed.value){
    return 'mdi-menu-down'
  }
  return 'mdi-menu-up'
})

const noDataText = computed(() => {
  if(loadingUserHouseholds.value){
    return $t('account.household_card.loading_households')
  }
  return $t('account.household_card.create_new_household')
})

const placeholderText = computed(() => {
  if(loadingUserHouseholds.value){
    return $t('account.household_card.loading_households')
  } else if(userHouseholds.value.length === 0){
    return $t('account.household_card.create_new_household')
  }
  return $t('account.household_card.select_household')
})

const saveBtnDisabled = computed(() => {
    return selectedHousehold.value?.id === authData.household
})

function saveHouseholdChanges(){
  authData.changeHousehold(selectedHousehold.value)
}
function editHouseholds(){
  $router.push("/households")
}

onMounted(() => {
  loadingUserHouseholds.value = true
  axios.getHouseholds().then((households: Array<Household>) => {
    const selected = households.find(h => h.id === authData.household)
    if(selected){
      selectedHousehold.value = selected
    }
    userHouseholds.value = households
    loadingUserHouseholds.value = false
  })
})

</script>

<template>

  <v-card
      class="mt-4"
      v-bind="$attrs"
      density="compact"
  >
    <v-card-title
        class="d-flex justify-space-between align-center"
        :class="{
            shadowed: !collapsed
          }"
    >
      {{ $t('account.household_card.title') }}
      <v-btn
          v-if="collapsible"
          density="compact"
          :icon="icon"
          variant="flat"
          size="small"
          @click="collapsed = !collapsed"
      >
      </v-btn>
    </v-card-title>
    <v-slide-y-transition

    >
        <v-container :fluid="true" class="pa-0 ma-0" v-show="!collapsed">
          <v-card-text>
            <v-select
                :items="userHouseholds"
                :chips="true"
                item-title="name"
                hide-details="auto"
                :single-line="true"
                :placeholder="placeholderText"
                :no-data-text="noDataText"
                return-object
                v-model="selectedHousehold"
                density="compact"
                color="primary"
                :loading="loadingUserHouseholds"
            />
          </v-card-text>
          <v-card-actions
            class="d-flex justify-space-between"
          >
            <v-btn
                variant="elevated"
                density="compact"
                rounded="sm"
                :text="$t('account.household_card.edit_households')"
                color="primary"
                @click="editHouseholds"
            />
            <v-btn
                variant="elevated"
                density="compact"
                rounded="sm"
                :text="$t('account.household_card.save_changes')"
                color="primary"
                :disabled="saveBtnDisabled"
                @click="saveHouseholdChanges"
            />
          </v-card-actions>
        </v-container>
    </v-slide-y-transition>
  </v-card>





</template>

<style scoped lang="scss">

</style>