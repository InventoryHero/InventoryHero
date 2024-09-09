<script setup lang="ts">

import useTextFieldStyle from "@/composables/useTextFieldStyle.ts";
import {useI18n} from "vue-i18n";
import {computed, ref, useTemplateRef} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";

const {t} = useI18n()
const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {notify} = useNotification()
const emit = defineEmits<{
  (e: 'close'): void
}>()

const {textFieldStyle} = useTextFieldStyle()
const email = ref("")
const valid = ref(false)
const emailForm = useTemplateRef("emailForm")
const saving = ref(false)
const sent = ref(false)
const text = computed(() => {
  if(sent.value){
    return t('password_reset.request_finished')
  }
  return t('password_reset.email_description')
})



const emailNeeded = (value: string) => !!value || t('password_reset.email_needed')


async function save(){
  const {valid} = await emailForm.value.validate()
  console.log(valid)
  if(!valid){
    return
  }
  saving.value = true
  userEndpoint.forgotPassword(email.value).then(({success, message}) => {
    saving.value = false
    notify({
      title: t('toasts.titles.success.password_reset_request'),
      text: t('toasts.text.success.password_reset_request'),
      type: 'success'
    })
    sent.value = true
  })

}

function close(){
  //@ts-expect-error
  emailForm.value.reset()
  saving.value = false
  emit('close')
}

</script>

<template>
  <v-card-text>
    <v-form
        ref="emailForm"
        v-model="valid"
    >
      <v-text-field
          v-bind="textFieldStyle"
          :placeholder="t('password_reset.email')"
          :label="t('password_reset.email')"
          v-model="email"
          :rules="[emailNeeded]"
      />
    </v-form>
    <v-sheet
        class="pa-4 mb-2"
        color="accent"
        rounded="lg"
    >
      <v-banner-text>
        {{text}}
      </v-banner-text>
    </v-sheet>

  </v-card-text>
  <v-card-actions
    class="d-flex justify-space-between"
  >
    <v-btn
      variant="outlined"
      color="red-accent-1"
      prepend-icon="mdi-cancel"
      @click.stop="close"
      :disabled="saving"
    >
      {{ t('cancel') }}
    </v-btn>
    <v-btn
      variant="elevated"
      color="primary"
      prepend-icon="mdi-content-save"
      :disabled="!valid || saving"
      :loading="saving"
      @click="save"
    >
      {{ t('save') }}
    </v-btn>
  </v-card-actions>
</template>

<style scoped lang="scss">

</style>