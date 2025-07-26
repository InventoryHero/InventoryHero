<script setup lang="ts">

import {BoxResponseSchema, BoxUpdateSchema, RoomResponseSchema} from "@/api/types/storage.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
import {templateRef} from "@vueuse/core";
import {StorageResponseSchema} from "@/api/types/items.ts";

const {isDirty, forceClose, onBeforeRouteLeaveHandler} = useGlobalModal()
const {t} = useI18n()
const {textFieldStyling, btnStyle, selectStyling} = useAppStyling()
const {storage} = useAxios()

const active = defineModel<boolean>()
const box = defineModel<BoxResponseSchema>("box", {
  required: true
})

const {
  width,
  height
} = defineProps<{
  width: string,
  height: string
}>()

const form = templateRef("form")
const newName = ref<string|null|undefined>(box.value.name)
const nameRules = ref([
  (value: string|undefined|null) => !!value || t('boxes.box.edit.rules.name_required')
])

const parents = ref<Array<RoomResponseSchema>>([])

const newParent = ref<StorageResponseSchema>(box.value.parent!)
const parentRules = ref([
  (value: RoomResponseSchema|null|undefined) => !!value || t('boxes.box.edit.rules.parent_required')
])

const resetName = () => {
  newName.value = box.value.name
}


const handleSave = async () => {
  const {valid} = await form.value.validate()
  if(!valid){
    return
  }
  const {success, data, error} = await storage.updateStorage(box.value.id, {
      name: newName.value !== box.value.name ?  newName.value! : undefined,
      storage_type: "box",
      parent_id: newParent.value.id !== box.value.parent_id ? newParent.value.id : undefined
    } as BoxUpdateSchema
  )
  if(!success){
    // TODO
    return
  }

  box.value = data! as BoxResponseSchema
  forceClose()
}

watch(newName, () => {
  isDirty.value =
      newName.value !== box.value.name ||
      newParent.value.id !== box.value.parent_id
})

onBeforeRouteLeave(() => {
  return onBeforeRouteLeaveHandler()
})

onBeforeMount(() => {
  storage.getAllStorage("room").then(({success, data, error}) => {
    if(success){
      // TODO ERROR
    }
    parents.value = (data ?? []) as RoomResponseSchema[]
  })
})
</script>

<template>
<v-dialog
  v-model="active"
  :height="height"
  :width="width"
>
  <v-card
    :title="t('boxes.box.edit.title')"
  >
    <template v-slot:append>
      <v-icon-btn
        icon="mdi-close"
        @click="forceClose"
      />
    </template>
    <v-card-text>
      <v-form
        ref="form"
        @submit.prevent
      >
        <v-row>
          <v-col cols="12">
            <v-text-field
                v-bind="textFieldStyling"
                :label="t('boxes.box.edit.name')"
                v-model="newName"
                :rules="nameRules"
                :append-inner-icon="newName !== box.name ? 'mdi-undo' : ''"
                @click:append-inner="resetName"
            />
          </v-col>
          <v-col cols="12">
            <v-select
                v-bind="selectStyling"
                v-model="newParent"
                :items="parents"
                :rules="parentRules"
                item-title="name"
                return-object
            />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
    <v-card-actions
      class="justify-end"
    >
      <v-btn
          v-bind="btnStyle"
          :text="t('boxes.box.edit.cancel')"
          @click="forceClose"
      />
      <v-btn
          v-bind="btnStyle"
          :text="t('boxes.box.edit.save')"
          @click="handleSave"
      />
    </v-card-actions>
  </v-card>

</v-dialog>
</template>

<style scoped lang="scss">

</style>