<script setup lang="ts">

import {RoomResponseSchema, RoomUpdateSchema} from "@/api/types/storage.ts";
import useAppStyling from "@/composables/useAppStyling.ts";
import {templateRef} from "@vueuse/core";

const {isDirty, forceClose, onBeforeRouteLeaveHandler} = useGlobalModal()
const {t} = useI18n()
const {textFieldStyling, btnStyle} = useAppStyling()
const {storage} = useAxios()

const active = defineModel<boolean>()
const room = defineModel<RoomResponseSchema>("room", {
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
const newName = ref<string|null|undefined>(room.value.name)
const nameRules = ref([
  (value: string|undefined|null) => !!value || t('rooms.room.edit.rules.name_required')
])

const resetName = () => {
  newName.value = room.value.name
}


const handleSave = async () => {
  const {valid} = await form.value.validate()
  if(!valid){
    return
  }
  const {success, data, error} = await storage.updateStorage(room.value.id, {
      name: newName.value!,
      storage_type: "room"
    } as RoomUpdateSchema
  )
  if(!success){
    // TODO
    return
  }

  room.value.name = data!.name
  forceClose()
}

watch(newName, () => {
  isDirty.value = newName.value !== room.value.name
})

onBeforeRouteLeave(() => {
  return onBeforeRouteLeaveHandler()
})
</script>

<template>
<v-dialog
  v-model="active"
  :height="height"
  :width="width"
>
  <v-card
    :title="t('rooms.room.edit.title', {name: room.name})"
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
        <v-text-field
            v-bind="textFieldStyling"
            :label="t('rooms.room.edit.name')"
            v-model="newName"
            :rules="nameRules"
            :append-inner-icon="newName !== room.name ? 'mdi-undo' : ''"
            @click:append-inner="resetName"
        />
      </v-form>
    </v-card-text>
    <v-card-actions
      class="justify-end"
    >
      <v-btn
          v-bind="btnStyle"
          color="secondary"
          prepend-icon="mdi-cancel"
          :text="t('rooms.room.edit.cancel')"
          @click="forceClose"
      />
      <v-btn
          v-bind="btnStyle"
          prepend-icon="mdi-content-save"
          :text="t('rooms.room.edit.save')"
          @click="handleSave"
      />
    </v-card-actions>
  </v-card>

</v-dialog>
</template>

<style scoped lang="scss">

</style>