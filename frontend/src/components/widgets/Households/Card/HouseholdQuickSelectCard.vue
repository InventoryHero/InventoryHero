<script setup lang="ts">
import {useAuthStore} from "@/store";
import {HouseholdEndpoint} from "@/api/http";
import {Household} from "@/types";
import useAxios from "@/composables/useAxios.ts";
import {useI18n} from "vue-i18n";
import {useRouter} from "vue-router";
import useAppStyling from "@/composables/useAppStyling.ts";
const authData = useAuthStore();
const {axios} = useAxios<HouseholdEndpoint>("household");

const {t: $t} = useI18n()
const $router = useRouter()
const {styling} = useAppStyling()


const {
  collapsible=false
} = defineProps<{
  collapsible?: boolean
}>()

const collapsed = ref(false)
const loadingUserHouseholds = ref(false)
const userHouseholds = ref<Array<Household>>([])

const updatedHousehold = ref<Household|undefined>()
const selectedHousehold = computed({
  get(){
    if(updatedHousehold.value){
      return updatedHousehold.value
    }
    return authData.household
  },
  set(value: Household){
    updatedHousehold.value = value
  }

})

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
    return selectedHousehold.value?.id === authData.household?.id
})

function saveHouseholdChanges(){
  authData.changeHousehold(selectedHousehold.value)
  updatedHousehold.value = undefined
}
function editHouseholds(){
  $router.push("/households")
}

onMounted(() => {
  loadingUserHouseholds.value = true
  axios.getHouseholds().then((households: Array<Household>) => {
    const selected = households.find(h => h.id === authData.household?.id)
    if(selected){
      selectedHousehold.value = selected
    }
    userHouseholds.value = households
    loadingUserHouseholds.value = false
  })
})

</script>

<template>

  <v-row
    no-gutters
    class="mt-2"
  >
    <v-col>
      <v-card
          v-bind="$attrs"
          density="compact"
          rounded="20"
      >
        <v-card-title
            class="d-flex justify-space-between align-center"
        >
          {{ $t('account.household_card.title') }}
          <div>
            <app-icon-btn
              icon="mdi-store-edit"
              color="primary"
              @click="editHouseholds"
            />
            <app-icon-btn
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
                v-bind="styling"
                :items="userHouseholds"
                density="compact"
                item-title="name"
                :single-line="true"
                :placeholder="placeholderText"
                :no-data-text="noDataText"
                return-object
                v-model="selectedHousehold"
                :loading="loadingUserHouseholds"
                :clearable="false"
            >
             <template v-slot:append>
               <app-icon-btn
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
    </v-col>
  </v-row>





</template>

<style scoped lang="scss">

</style>