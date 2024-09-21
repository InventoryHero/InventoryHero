<script setup lang="ts">
import {useTemplateRef} from "vue";
import {HouseholdEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import {useAuthStore} from "@/store";

defineOptions({
  inheritAttrs: false
})

const {axios: householdEndpoint} = useAxios<HouseholdEndpoint>("household")
const authStore = useAuthStore()
const {styling} = useAppStyling()
const {t} = useI18n()
const {notify} = useNotification()

const saving = ref(false)
const name = ref<string|undefined>()
const collapsed = defineModel<boolean>("collapsed")
const householdForm = useTemplateRef("household-form")
const rules = ref({
  required: (value: string) => !!value || t('households.rules.name_required'),
  nameShorterThan: (value: string) => value.length <= 25 || t('households.rules.name_shorter_than')
})

const collapseIcon = computed(() =>{
  if(collapsed.value){
    return 'mdi-menu-down'
  }
  return 'mdi-menu-up'
})

async function createHousehold(){
  //@ts-expect-error couldn't figure out how to type templateRef forms
  const { valid } = await householdForm.value.validate();
  if(!valid){
    return
  }

  saving.value = true
  householdEndpoint.createHousehold(name.value!).then(({success, household}) => {
    saving.value = false
    if(!success){
      return
    }
    authStore.addHousehold(household!)
    notify({
      title: t( "toasts.titles.success.household_created", {name: name.value!}),
      text: t( "toasts.text.success.household_created"),
      type: "success"
    })
    clear()
  })
}

function clear(){
  //@ts-expect-error couldn't figure out how to type templateRef forms
  householdForm.value.reset()
}

watch(collapsed, (newValue) => {
  if(!newValue){
    clear()
  }
})

</script>

<template>
  <v-card
      v-bind="$attrs"
      density="compact"
      :elevation="5"
  >
    <template v-slot:loader>
      <v-progress-linear
          :indeterminate="true"
          :active="saving"
          color="primary"
      />
    </template>
    <v-card-title
      class="d-flex justify-space-between align-center"
    >
      {{ t('households.create_new.title')}}
      <app-icon-btn
          :icon="collapseIcon"
          @click="collapsed=!collapsed"
      />
    </v-card-title>
    <v-slide-y-transition >
      <v-container
          v-show="!collapsed"
          class="pt-0 pb-2"
      >
        <v-form
            ref="household-form"
            action=""
            @submit.prevent="(event) => event.preventDefault()"
        >
          <v-row
            no-gutters
            class="mb-2"
          >
            <v-col>
              <v-text-field
                  v-bind="styling"
                  v-model="name"
                  :rules="[rules.required, rules.nameShorterThan]"
                  validate-on="lazy"
                  :label="t('households.create_new.labels.name')"
              />
            </v-col>
          </v-row>
          <v-row
            no-gutters
          >
            <v-col
              class="d-flex justify-end"
            >
              <v-btn
                prepend-icon="mdi-content-save"
                color="primary"
                variant="tonal"
                :text="t('households.create_new.save')"
                density="comfortable"
                @click="createHousehold"
              />
            </v-col>
          </v-row>
        </v-form>

        <!--@click="createHousehold($event)"-->

      </v-container>
    </v-slide-y-transition>
  </v-card>
</template>

<style scoped lang="scss">

</style>