<script setup lang="ts">
import useAuthStore from "@/store/useAuthStore";
import {useTemplateRef} from "vue";
import {notify} from "@kyvg/vue3-notification";
import {HouseholdMemberPublic, HouseholdPublic, HouseholdUpdate} from "@/api/types/households.ts";
import {storeToRefs} from "pinia";
import {ROLE_ADMIN, ROLE_OWNER} from "@/api/types/householdRoles.ts";

const authStore = useAuthStore()
const {household: householdEndpoint} = useAxios()
const {t} = useI18n()
const router = useRouter()

const {textFieldStyling} = useAppStyling()

const {id=""} = defineProps<{
  id?: string
}>()

const {user} = storeToRefs(authStore)



const householdMembers = ref<Array<HouseholdMemberPublic>>([])
const loadingMembers = ref(false)

const householdId = computed(() => {
  return id
})


const household = ref<HouseholdPublic|undefined>()
const newHouseholdName = ref<string|undefined>()

const breadcrumbs = ref<Array<{
  title: string,
  to?: string
}>>([
  {
    title: t('nav.households'),
    to: "/households"
  }
])


const householdName = computed({
  get(){
    if(newHouseholdName.value !== undefined)
    {
      return newHouseholdName.value ?? ''
    }
    return household.value?.name ?? ''
  },
  set(value: string){
    newHouseholdName.value = value
  }
})


const myself = computed(() => householdMembers.value.find(x => x.user_id === user.value?.id))
const isOwner = computed(() => ROLE_OWNER === myself.value?.role)
const isAdmin = computed(() => ROLE_ADMIN === myself.value?.role)

const errorMessage = ref<string|undefined>()

const nameField = useTemplateRef("name-field")

const rules = ref({
  nameRequired: (value: string) => value.length > 0 || t('households.rules.name_required'),
  nameShorterThan: (value: string) => value.length <= 25 || t('households.rules.name_shorter_than')
})

const deletingHousehold = ref(false)

const {
  reallyDo,
  confirmationDialog,
  saveAction
} = useConfirmationSetup(deleteHousehold)

function deleteHousehold(){
  deletingHousehold.value = true
  householdEndpoint.delete(householdId.value).then((success) => {

    if(success){
      router.push("/households")
    }
    deletingHousehold.value = false
  })
}

function removeFromHousehold(id: string){
  const member = householdMembers.value.find(member => member.id === id)
  if(member){
    notify({
      title: t(`toasts.titles.success.${member.joined ? 'kicked' : 'removed'}_from_household`),
      text: t(`toasts.text.success.${member.joined ? 'kicked' : 'removed'}_from_household`),
      type: 'success'
    })
  }
  householdMembers.value = householdMembers.value.filter(member => member.id !== id)
}

async function updateName(){
  //@ts-expect-error this should be correct
  const valid = await nameField.value.validate()
  if(valid.length > 0){
    return
  }
  householdEndpoint.update(householdId.value, {
    name: householdName.value
  } as HouseholdUpdate).then(({success, data}) => {
    if(success){
      reset()
      household.value = data
      notify({
        title: t(`toasts.titles.success.household_updated`),
        text: t(`toasts.text.success.household_updated`),
        type: 'success'
      })
    }
  })
}

function reset(){
  newHouseholdName.value = undefined
}

onBeforeMount(() => {
  loadingMembers.value = true
  householdEndpoint.getAllMembers(householdId.value).then(({success, data, error}) => {
    if(!success){
      errorMessage.value = (error as any) as (string|undefined)
      // TODO ERROR HANDLING
      return
    }

    household.value = data as HouseholdPublic
    breadcrumbs.value.push({
      title: household.value?.name
    })
    householdMembers.value = (data?.members ?? []).sort((a, b) => {
      if (a.user_id === authStore.user?.id) {
        return -1
      }
      if (b.user_id === authStore.user?.id) {
        return 1
      }
      if (a.joined && !b.joined) {
        return -1
      }
      if (!a.joined && b.joined) {
        return 1
      }

      return 0;
    })
    loadingMembers.value = false
  })
})

</script>

<template>
  <template  v-if="errorMessage === undefined ">
    <v-breadcrumbs
      :items="breadcrumbs"
    />
    <v-card
        :disabled="loadingMembers || deletingHousehold"
    >
      <template v-slot:loader>
        <v-progress-linear
          indeterminate
          :active="loadingMembers || deletingHousehold"
          color="primary"
        />
      </template>
      <template v-slot:title>
        <v-text-field
            ref="name-field"
            v-bind="textFieldStyling"
            v-model="householdName"
            @click:clear="householdName = ''"
            :rules="[rules.nameRequired, rules.nameShorterThan]"
        >
          <template v-slot:append>
            <v-icon
                :disabled="newHouseholdName === undefined"
                icon="mdi-content-save"
                @click="updateName"
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
      <v-card-text>
        <household-member-card
            v-for="item in householdMembers"
            :is-owner="isOwner"
            :household-member="item"
            :household="household!"
            @kicked="removeFromHousehold(item.id)"
        />
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn
            v-if="isOwner"
            prepend-icon="mdi-trash-can"
            :text="t('households.edit.delete_household')"
            variant="tonal"
            color="red-accent-1"
            @click="saveAction"
        />
      </v-card-actions>
    </v-card>
  </template>

  <template
      v-else
  >
    <!--TODO-->
    <v-card
        :text="t(`households.edit.${errorMessage}.text`)"
        :title="t(`households.edit.${errorMessage}.title`)"
    >
      <v-card-actions
          class="d-flex justify-end"
      >
        <v-btn
            color="primary"
            :text="t('households.edit.not_found.back')"
            variant="tonal"
            to="/households"
        />

      </v-card-actions>
    </v-card>
    <div class="fill-height"/>
  </template>

</template>

<style scoped lang="scss">

</style>

<route>
{
  "props": true,
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": false
  }
}
</route>