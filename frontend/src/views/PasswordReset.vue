<script setup lang="ts">
import {onBeforeMount, ref, useTemplateRef} from 'vue'
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useI18n} from "vue-i18n";
import {useRouter} from "vue-router";
import {useNotification} from "@kyvg/vue3-notification";

const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {t: $t} = useI18n()
const router = useRouter()
const {notify} = useNotification()

const {id} = defineProps<{
  id: string
}>()

const allowed = ref(false)
const preflightCheck = ref(true)
const password = ref("")
const passwordRepeat = ref("")
const valid = ref(false)
const resettingPassword = ref(false)
const errorMessage = ref("")

const passwordForm = useTemplateRef("passwordForm")

const rules = {
  passwordNeeded: (value: string) => value !== '' || $t('password_reset.rules.password_needed'),
  repeatNotEqual: (value: string) => value === password.value || $t('password_reset.rules.passwords_not_equal'),
}

// TODO LOCALIZE THIS COMPONENT

async function resetPassword(){
  if(resettingPassword.value){
    return
  }
  //@ts-expect-error don't know how to type correctly
  const {valid} = await passwordForm.value.validate()
  if(!valid){
    return
  }
  resettingPassword.value = true
  userEndpoint.resetPasswordMail(id, password.value).then((result) => {
    resettingPassword.value = false
    if(!result?.success){
      notify({
        title: $t(`toasts.titles.error.password_reset_${result?.message}`),
        text: $t(`toasts.text.error.password_reset_${result?.message}`),
        type: "error"
      })
      return
    }

    router.push("/").then(() => {
      notify({
        title: $t(`toasts.titles.success.password_reset`),
        text: $t(`toasts.text.success.password_reset`),
        type: "success"
      })
    })
  })
}

function close(){
  if(resettingPassword.value){
    return
  }
  router.push("/")
}

onBeforeMount(() => {
  userEndpoint.resetPasswordPreflight(id).then((result) => {
    allowed.value = result?.success ?? false
    preflightCheck.value = false
    errorMessage.value = result?.message ?? ''
  })
})

</script>

<template>
  <v-row
      justify="center"
      class="fill-height mt-4"
  >
    <v-col
        cols="12"
        lg="6"
    >

      <v-card>
        <template v-slot:loader>
          <v-progress-linear
            :indeterminate="true"
            :active="preflightCheck || resettingPassword"
            color="primary"
          />
        </template>
        <v-card-title
            class="shadowed mb-3"
        >
          {{ $t('password_reset.card.title') }}
        </v-card-title>
        <v-card-text
          v-if="allowed"
        >
          <v-form
              ref="passwordForm"
              @submit.prevent
              class="fill-width"
              :disabled="preflightCheck || resettingPassword"
              v-model="valid"
          >
            <app-password-textfield
                v-model="password"
                :label="$t('password_reset.password')"
                :rules="[rules.passwordNeeded]"
                density="compact"
                variant="outlined"
                class="mb-2"
            />
            <app-password-textfield
                :label="$t('password_reset.repeat_password')"
                v-model="passwordRepeat"
                :rules="[rules.repeatNotEqual]"
                density="compact"
                variant="outlined"
            />
          </v-form>

        </v-card-text>
        <v-card-text
          v-else
          class="text-h6"
        >
          {{ $t(`password_reset.card.error.${errorMessage}`) }}
        </v-card-text>
        <v-card-actions
          class="d-flex justify-space-between"

        >
          <v-btn
            @click="close"
            :disabled="resettingPassword"
          >
            {{ $t('password_reset.card.close') }}
          </v-btn>
          <v-btn
              :disabled="preflightCheck || !valid || resettingPassword"
              :loading="resettingPassword"
              @click="resetPassword"
          >
            {{ $t('password_reset.card.reset_password') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>

</template>

<style scoped lang="scss">
:deep(.v-card-text){
  min-height: calc(100svh * 0.3);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
}

</style>