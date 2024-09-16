<script setup lang="ts">
import {useAuthStore} from "@/store";
import {HouseholdEndpoint} from "@/api/http";
import {HouseholdMember} from "@/types";
import {useTemplateRef} from "vue";
import ConfirmationDialog from "@/components/common/ConfirmationDialog.vue";
import useDialogConfig from "@/composables/useDialogConfig.ts";
import {notify} from "@kyvg/vue3-notification";

const authStore = useAuthStore()
const {axios: householdEndpoint} = useAxios<HouseholdEndpoint>("household")
const {t} = useI18n()
const router = useRouter()

const {styling} = useAppStyling()

const {id=""} = defineProps<{
  id?: string
}>()

const householdMembers = ref<Array<HouseholdMember>>([])
const loadingMembers = ref(false)

const householdId = computed(() => {
  const number = parseInt(id, 10)
  if(isNaN(number)){
    return -1;
  }
  return number
})

const newHouseholdName = ref<string|undefined>()

const household = computed(
    () => authStore.households.find((h) => h.id === householdId.value)
)

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


const isOwner = computed(() => household.value?.creator === authStore.user?.id)

const nameField = useTemplateRef("name-field")

const rules = ref({
  nameRequired: (value: string) => value.length > 0 || t('households.rules.name_required'),
  nameShorterThan: (value: string) => value.length <= 25 || t('households.rules.name_shorter_than')
})



onBeforeMount(() => {
  loadingMembers.value = true
  householdEndpoint.getMembers(householdId.value).then(({success, members}) => {
    if(success){
      householdMembers.value = (members ?? []).sort((a, b) => {
        if (a.username === authStore.user?.username) {
          return -1
        }
        if (b.username ===  authStore.user?.username) {
          return 1
        }
        if (a.joined && !b.joined) {
          return -1
        }
        if (!a.joined && b.joined) {
          return 1
        }

        return 0;
      }).map((member) => ({
        ...member,
        size: member.joined ? 61 : 73
      }))
    }
    loadingMembers.value = false
  })
})

const deletingHousehold = ref(false)
const deleteConfirmed = ref(false)
const {
  isVisible: deleteConfirmDialogVisible,
  openDialog: openDeleteConfirmDialog,
  closeDialog: closeDeleteConfirmDialog
} = useDialogConfig()
function deleteHousehold(){
  if(!deleteConfirmed.value){
    openDeleteConfirmDialog()
    return
  }
  deletingHousehold.value = true
  householdEndpoint.deleteHousehold(householdId.value).then((success) => {
    if(success){
      authStore.removeHousehold(householdId.value, "deleted")
      router.push("/households")
    }
    deletingHousehold.value = false
  })
}

function removeFromHousehold(id: number){
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
  householdEndpoint.updateHousehold(householdId.value, {
    name: householdName.value
  }).then(({success, household}) => {
    if(success){
      authStore.updateHousehold(householdId.value, household!)
      reset()
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

</script>

<template>



  <v-row
    class="fill-height fill-width"
    justify="center"
    no-gutters
  >
    <v-col
        cols="12"
        lg="8"
    >
      <v-card
          v-if="household && isOwner"
          class="d-flex flex-column fill-height"
          :disabled="loadingMembers || deletingHousehold"
      >
        <template v-slot:loader>
          <v-progress-linear
            indeterminate
            :active="loadingMembers || deletingHousehold"
            color="primary"
          />
        </template>
        <v-card-title
          class="flex-0-0"
        >
          <v-text-field
              ref="name-field"
              v-bind="styling"
              v-model="householdName"
              @click:clear="householdName = ''"
              :rules="[rules.nameRequired, rules.nameShorterThan]"
          >
            <template v-slot:append>
              <app-icon-btn
                  :disabled="newHouseholdName === undefined"
                  icon="mdi-content-save"
                  @click="updateName"
              />
            </template>
          </v-text-field>
        </v-card-title>
        <div
            class="position-relative flex-1-1"
        >
          <div
              class="wrapper"
          >
            <v-card-text
                class="scroll"
            >

              <RecycleScroller
                  class="scroll"
                  :items="householdMembers"
              >
                <template v-slot="{ item }">
                  <household-member-card
                    :disabled="item.username === authStore.user?.username"
                    :household-member="item"
                    :household="household"
                    @kicked="removeFromHousehold(item.id)"
                  />
                </template>
              </RecycleScroller>
            </v-card-text>
          </div>
        </div>
        <v-card-actions
          class="d-flex justify-end overflow-auto"
        >
          <v-btn
              prepend-icon="mdi-arrow-left-bottom"
              :text="t('households.edit.to_households')"
              variant="tonal"
              to="/households"
          />
          <v-btn
              prepend-icon="mdi-trash-can"
              :text="t('households.edit.delete_household')"
              variant="tonal"
              color="red-accent-1"
              @click="deleteHousehold"
          />
        </v-card-actions>
      </v-card>

      <template
          v-else
      >
        <v-card
            :text="t(`households.edit.${(!isOwner && household) ? 'no_rights' : 'not_found'}.text`)"
            :title="t(`households.edit.${(!isOwner && household) ? 'no_rights' : 'not_found'}.title`)"
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


    </v-col>
  </v-row>


</template>

<style scoped lang="scss">

</style>