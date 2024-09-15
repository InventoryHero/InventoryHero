<script setup lang="ts">


import {useStorage} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {useI18n} from "vue-i18n";
import {useNotification} from "@kyvg/vue3-notification";
import {TabType} from "@/types/TabType.ts";
import {ApiStorage} from "@/types";
import useHint from "@/composables/useHint.ts";
import {useTemplateRef} from "vue";
import {BoxEndpoint} from "@/api/http";
import useAppStyling from "@/composables/useAppStyling.ts";

const storageStore = useStorage()
const {axios: boxEndpoint} = useAxios<BoxEndpoint>('box')
const {styling} = useAppStyling()

const {t} = useI18n()
const {notify} = useNotification()

const resourcesLoading = inject<Ref<{
  loadingProducts: boolean,
  loadingBoxes: boolean,
  loadingLocations: boolean
}>>('loading', ref({
  loadingProducts: true,
  loadingBoxes: true,
  loadingLocations: true
}))

const locationsLoading = computed(() => resourcesLoading.value.loadingLocations)

const tab = inject<Ref<TabType>>("tab", ref(TabType.Product))
const addForm = useTemplateRef('add-form')
const postingBox = ref(false)
const box = ref("")
const location = ref<ApiStorage|undefined>();
const {
  hintActive: boxNameHintActive,
  message: boxNameHint
} = useHint(t(`add.box.hints.boxName`))
const {
  hintActive: locationSelectHintActive,
  message: locationSelectHint
} = useHint(t(`add.box.hints.locationSelect`))

const rules = ref({
  needName: (value: string) => value !== "" || t('add.box.rules.name_needed')
})



function clear(){
  //@ts-expect-error couldn't figure out how to type it properly
  addForm.value.reset()
}

async function save(){

  //@ts-expect-error couldn't figure out how to type it properly
  const validation = await addForm.value.validate()

  if(!validation.valid){
    return
  }

  postingBox.value = true
  boxEndpoint.createBox({
    name: box.value,
    storageId: location.value?.id ?? undefined
  }).then(({success, newBox}) => {
    postingBox.value = false
    if(!success){
      return
    }
    storageStore.addBox(newBox)
    notify({
      title: t('toasts.titles.success.add_box', {
        name: box.value
      }),
      text: t('toasts.text.success.add_box'),
      type: "success"
    })
    //@ts-expect-error couldn't figure out how to type it properly
    addForm.value.reset()
  })

}


watch(tab, (newValue: TabType, oldValue: TabType) => {
  if(newValue !== TabType.Box && oldValue === TabType.Box){
    clear()
  }
})
</script>

<template>
  <create-card
      :title="$t(`add.box.title`)"
      @save="save"
      @clear="clear"
      :request-in-progress="postingBox"
  >
    <v-form
        @submit.prevent
        ref="add-form"
        :disabled="postingBox"
    >
      <v-row
        no-gutters
        class="mb-2"
      >
        <v-col>
          <v-text-field
              v-bind="styling"
              :persistent-clear="true"
              auto-select-first="exact"
              v-model="box"
              :label="$t('add.box.labels.box')"
              item-title="name"
              :messages="boxNameHint"
              :rules="[rules.needName]"
          >
            <template #append>
              <app-help-indicator
                  v-model="boxNameHintActive"
              />
            </template>
          </v-text-field>
        </v-col>
      </v-row>
      <v-row
          no-gutters
          class="mb-2"
      >
        <v-col>
          <app-storage-select
              :storage-loading="locationsLoading"
              v-model="location"
              :storage="storageStore.locations"
              density="comfortable"
              :label="$t('add.box.labels.location')"
              :messages="locationSelectHint"
              :hide-details="false"
              content-type="box"
          >
            <template #hint>
              <app-help-indicator
                  v-model="locationSelectHintActive"
              />
            </template>
          </app-storage-select>
        </v-col>
      </v-row>
    </v-form>
  </create-card>
</template>

<style scoped lang="scss">
</style>