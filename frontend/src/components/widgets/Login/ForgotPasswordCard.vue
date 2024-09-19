<script setup lang="ts">

import useTextFieldStyle from "@/composables/useAppStyling.ts";
import {useI18n} from "vue-i18n";
import {computed, ref, useTemplateRef} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import useAppStyling from "@/composables/useAppStyling.ts";

const {t} = useI18n()
const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {notify} = useNotification()
const emit = defineEmits<{
  (e: 'close'): void
}>()

const {styling} = useAppStyling()
const email = ref("")
const valid = ref(false)
const emailForm = useTemplateRef("emailForm")
const saving = ref(false)
const sent = ref(false)
const text = computed(() => {
  return t('password_reset.description')
})



const emailNeeded = (value: string) => !!value || t('password_reset.rules.email_needed')


async function save(){
  //@ts-expect-error couldn't figure out how to type the form-ref properly
  const {valid} = await emailForm.value.validate()
  if(!valid){
    return
  }
  saving.value = true
  userEndpoint.forgotPassword(email.value).then(() => {
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
  //@ts-expect-error couldn't figure out how to type the form-ref properly
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
        class="mb-2"
    >
      <v-row>
        <v-col>
          <v-text-field
              v-bind="styling"
              :placeholder="t('password_reset.email_placeholder')"
              :label="t('password_reset.email_label')"
              v-model="email"
              :rules="[emailNeeded]"
          />
        </v-col>
      </v-row>
    </v-form>
    <v-sheet
        class="pa-4 mb-2 d-flex justify-center"
        color="accent"
        rounded="lg"
    >
        {{text}}
    </v-sheet>

  </v-card-text>
  <v-card-actions
  >
    <v-btn
      variant="tonal"
      color="red-accent-1"
      prepend-icon="mdi-cancel"
      @click.stop="close"
      :disabled="saving"
    >
      {{ t('cancel') }}
    </v-btn>
    <v-spacer />
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