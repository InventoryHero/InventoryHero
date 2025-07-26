<script setup lang="ts">
import useAppStyling from "@/composables/useAppStyling.ts";
import useGlobalModal from "@/composables/useGlobalModal.ts";
import {templateRef} from "@vueuse/core";
import itemAddedEventBus from "@/services/itemAddedEventBus.ts";
import categoryAddedEventBus from "@/services/categoryAddedEventBus.ts";

const {t} = useI18n()
const {textFieldStyling, btnStyle} = useAppStyling()
const {isDirty, isAwaitingConfirmation, leave, stay, forceClose, close, onBeforeRouteLeaveHandler} = useGlobalModal()
const {items} = useAxios()
const route = useRoute()

const active = defineModel<boolean>()
const {
  height,
  width
} = defineProps<{
  height?: string|number|undefined,
  width?: string|number|undefined,
}>()

const name = ref<string|null>(null)
const loading = ref<boolean>(false)
const form = templateRef("form")

const nameRules = ref([
  (value: string|null) => !!value || t('create.category.form.rules.name_required')
])

const save = async () => {
  const {valid} = await form.value!.validate()
  if(!valid){
    return
  }
  loading.value = true
  const {success, data, error} = await items.createNewCategory({
    name: name.value!
  })
  if(!success){
    // TODO

    return false
  }
  if(route.path.startsWith("/items")){
    categoryAddedEventBus.emit(data!)
  }
  form.value!.reset()
  return true
}

const saveAndClose = async () => {
  const success = await save()
  if(success){
    forceClose()
  }
}

watch(name, (newValue) => {
  isDirty.value = newValue !== null;
})
onBeforeRouteLeave(() => {
  return onBeforeRouteLeaveHandler()
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
        :disabeld="loading"
      :title="t('create.category.title')"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="close"
        />
      </template>
      <v-card-text>
        <v-form
          @submit.prevent=""
          ref="form"
        >
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                :label="t('create.category.form.name')"
                v-model="name"
                :rules="nameRules"
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
          :text="t('create.category.form.save')"
          @click="save"
          :disabled="loading"
        />
        <v-btn
            v-bind="btnStyle"
            :text="t('create.category.form.save_and_close')"
            @click="saveAndClose"
            :disabled="loading"
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