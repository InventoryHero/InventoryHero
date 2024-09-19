<script setup lang="ts">
import {useStorage} from "@/store";
import {LocationEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";
import useHint from "@/composables/useHint.ts";
import {useNotification} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
import {useTemplateRef} from "vue";

const {axios: locationEndpoint} = useAxios<LocationEndpoint>("location")
const storageStore = useStorage()
const {t} = useI18n()
const {notify} = useNotification()

const tab = inject<Ref<TabType>>("tab", ref(TabType.Location))
const {styling} = useAppStyling()

const {
  hintActive: locationNameHintActive,
  message: locationNameHint
} = useHint(t(`add.product.hints.combobox`))

const rules = ref({
  needName: (value: string) => value !== "" || t('add.location.rules.name_needed')
})

const location = ref<string>("")
const postingLocation = ref(false)
const addForm = useTemplateRef('add-form')


async function save(){
  //@ts-expect-error couldn't figure out how to type it properly
  const validation = await addForm.value.validate()
  if(!validation.valid){
    return
  }
  postingLocation.value = true
  const {success, newLocation} = await locationEndpoint.createLocation({
    name: location.value
  })

  postingLocation.value = false
  if(success){
    storageStore.addLocation(newLocation)
    notify({
      title: t('toasts.titles.success.add_location', {
        name: location.value
      }),
      text: t('toasts.text.success.add_location'),
      type: "success"
    })
    clear()
  }
}

function clear(){
  //@ts-expect-error couldn't figure out how to type it properly
  addForm.value.reset()
}

watch(tab, (newValue: TabType, oldValue: TabType) => {
  if(newValue !== TabType.Location && oldValue === TabType.Location){
    clear()
  }
})

</script>

<template>

  <create-card
      :title="$t(`add.location.title`)"
      @save="save"
      @clear="clear"
      :request-in-progress="postingLocation"
  >
    <v-form
        @submit.prevent
        ref="add-form"
        :disabled="postingLocation"
    >

      <v-row
          :no-gutters="true"
          class="mb-2"
      >
        <v-col
            cols="12"
        >
          <v-text-field
              v-bind="styling"
              auto-select-first="exact"
              v-model="location"
              :label="$t('add.location.labels.location')"
              item-title="name"
              :message="locationNameHint"
              :rules="[rules.needName]"
          >
            <template v-slot:message>
              <app-help-indicator
                  v-model="locationNameHintActive"
              />
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </v-form>
  </create-card>

</template>

<style scoped lang="scss">

</style>