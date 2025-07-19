<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";
import {useTemplateRef} from "vue";
import {VForm} from "vuetify/components";

import boxAddedEventBus from "@/services/boxAddedEventBus.ts";
import {RoomResponseSchema} from "@/api/types/storage.ts";
import useGlobalModal from "@/composables/useGlobalModal.ts";

const {t} = useI18n()
const {textFieldStyling, btnStyle, selectStyling} = useAppStyling()
const {storage: storageEndpoint} = useAxios()
const router = useRouter()
const route = useRoute()
const {isDirty, isAwaitingConfirmation, leave, stay, forceClose, close} = useGlobalModal()

const active = defineModel<boolean>()

const {
  height,
  width
} = defineProps<{
  height?: string|number|undefined,
  width?: string|number|undefined,
}>()


const nameRules = ref([
  (v: string|null) => !!v || t('create.box.form.name_required')
])

const name = ref<string|null>()
const form = useTemplateRef("form")
const loading = ref<boolean>(false)
const parents = ref<RoomResponseSchema[]>([])
const parent = ref<RoomResponseSchema|null>(null)

const saveBox = async () => {
  //@ts-expect-error
  const { valid } = await form.value.validate()
  if(!valid){
    return false
  }

  loading.value = true
  const {success, data, error} = await storageEndpoint.createStorage({
    name: name.value!,
    storage_type: "box",
    parent_id: parent.value?.id ?? undefined
  })
  if(!success){
    // TODO RETURN TO ERROR
    await router.push("/error")
    return false
  }
  loading.value = false

  if(route.path === "/storage/boxes"){
    boxAddedEventBus.emit()
  }
  name.value = null
  return true
}

const saveAndClose = () => {
  saveBox().then((success: boolean) => {
    if(success){
      forceClose()
    }
  })
}

watch([name, parent], () => {
  isDirty.value = true
})

watch(active, () => {
  if(form.value){
    form.value.reset()
  }
  isDirty.value = false
})

onBeforeMount(() => {
  storageEndpoint.getAllStorage("room").then(({success, data, error}) => {
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
      scrollable
      :height="height"
      :width="width"
  >
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
        {{ t('create.box.title') }}
      </template>

      <v-card-text>
        <v-form
          @submit.prevent=""
          ref="form"
        >
          <v-row
          >
            <v-col
              cols="12"
            >
              <v-text-field
                  v-bind="textFieldStyling"
                  v-model="name"
                  :label="t('create.box.form.name')"
                  :rules="nameRules"
              />

            </v-col>
            <v-col
              cols="12"
            >
              <v-select
                  v-bind="selectStyling"
                  v-model="parent"
                  :label="t('create.box.form.parent')"
                  :items="parents"
                  item-title="name"
                  item-value="id"
                  return-object
              >
                <template v-slot:item="{ props: itemProps, item }">
                  <v-list-item
                      v-bind="itemProps"
                      prepend-icon="mdi-door"
                  ></v-list-item>
                </template>
              </v-select>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-btn
            v-bind="btnStyle"
            :text="t('create.box.form.save')"
            @click="saveBox"
        />
        <v-btn
          v-bind="btnStyle"
          :text="t('create.box.form.save_and_close')"
          @click="saveAndClose"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
  <confirm-leave-dialog
      v-model="isAwaitingConfirmation"
      @cancel="stay"
      @confirm="leave"
  />
</template>

<style scoped lang="scss">

</style>