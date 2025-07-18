<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";
import {useTemplateRef} from "vue";
import {VForm} from "vuetify/components";
import {useModal} from "@/composables-new/useModal.ts";
import roomAddedEventBus from "@/services/roomAddedEventBus.ts";

const {t} = useI18n()
const {textFieldStyling, btnStyle} = useAppStyling()
const {storage: storageEndpoint} = useAxios()
const router = useRouter()
const route = useRoute()
const {forceNavigation} = useModal()

const nameRules = ref([
  (v: string|null) => !!v || t('create.room.form.name_required')
])

const name = ref<string|null>()
const form = useTemplateRef("form")
const loading = ref<boolean>(false)

const emit = defineEmits<{
  (e: 'close'): void
}>()

const saveRoom = async () => {
  //@ts-expect-error
  const { valid } = await form.value.validate()
  if(!valid){
    return false
  }

  loading.value = true
  const {success, data, error} = await storageEndpoint.createStorage({
    name: name.value!,
    storage_type: "room"
  })
  if(!success){
    // TODO RETURN TO ERROR
    forceNavigation.value = true
    await router.push("/error")
    return false
  }
  loading.value = false

  if(route.name === "/storage/rooms/room.[id]"){
    roomAddedEventBus.emit()
  }
  name.value = null
  return true
}

const saveAndClose = () => {
  saveRoom().then((success: boolean) => {
    if(success){
      forceNavigation.value = true
      emit('close')
    }
  })
}

const close = () => {
  emit('close')
}

</script>

<template>
<v-card
  :loading="loading"
  :disabled="loading"
>
  <template v-slot:append>
    <v-icon-btn
      icon="mdi-close"
      @click="close"
    />
  </template>
  <template v-slot:title>
    {{ t('create.room.title') }}
  </template>

  <v-card-text>
    <v-form
      @submit.prevent=""
      ref="form"
    >
      <v-text-field
          v-bind="textFieldStyling"
          v-model="name"
          :label="t('create.room.form.name')"
          :rules="nameRules"
      />
    </v-form>
  </v-card-text>

  <v-card-actions>
    <v-btn
        v-bind="btnStyle"
        :text="t('create.room.form.save')"
        @click="saveRoom"
    />
    <v-btn
      v-bind="btnStyle"
      :text="t('create.room.form.save_and_close')"
      @click="saveAndClose"
    />
  </v-card-actions>
</v-card>
</template>

<style scoped lang="scss">

</style>