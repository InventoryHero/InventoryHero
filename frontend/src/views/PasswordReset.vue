<script setup lang="ts">
import {onBeforeMount, ref, useTemplateRef} from 'vue'
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useI18n} from "vue-i18n";
import {useRouter} from "vue-router";
import {useNotification} from "@kyvg/vue3-notification";
import {VForm} from "vuetify/components";

const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {t: $t} = useI18n()
const router = useRouter()
const {notify} = useNotification()
const {styling} = useAppStyling()

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

const passwordForm = useTemplateRef<VForm>("passwordForm")

const rules = {
  passwordNeeded: (value: string) => value !== '' || $t('reset_password.rules.password_needed'),
  repeatNotEqual: (value: string) => value === password.value || $t('reset_password.rules.passwords_not_equal'),
}



async function resetPassword(){
  if(resettingPassword.value){
    return
  }
  if(!passwordForm.value){
    return
  }
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
      class="fill-height"
  >
    <v-col
        cols="12"
        lg="4"
        class="mt-12"
    >
      <v-card
        elevation="5"
      >
        <template v-slot:loader>
          <v-progress-linear
            :indeterminate="true"
            :active="preflightCheck || resettingPassword"
            color="primary"
          />
        </template>
        <template v-slot:title>
          {{ $t('reset_password.title') }}
        </template>
        <v-card-subtitle class="text-wrap">
          {{ $t('reset_password.subtitle')}}
        </v-card-subtitle>
        <v-card-text
          class="mt-3"
        >
          <v-row
              v-if="allowed"
              dense
              justify="center"
          >
            <v-col
                cols="12"
                lg="10"
            >
              <v-form
                  ref="passwordForm"
                  @submit.prevent="(event) => event.preventDefault()"
                  :disabled="preflightCheck || resettingPassword"
                  v-model="valid"
              >
                <v-row dense>
                  <v-col>
                    <app-password-textfield
                        v-model="password"
                        :label="$t('reset_password.password')"
                        :rules="[rules.passwordNeeded]"
                        v-bind="styling"
                    />
                  </v-col>
                </v-row>
                <v-row dense>
                  <v-col>
                    <app-password-textfield
                        :label="$t('reset_password.password_repeat')"
                        v-model="passwordRepeat"
                        :rules="[rules.repeatNotEqual]"
                        v-bind="styling"
                    />
                  </v-col>
                </v-row>
              </v-form>
            </v-col>
          </v-row>
          <v-row
              v-else
            dense
          >
            <v-col>
              <v-sheet
                  class="pa-4 mb-2 d-flex text-justify d-inline-block"
                  color="accent"
                  rounded="lg"
                  style="hyphens:auto;"
              >
                {{ $t(`reset_password.error.${errorMessage}`) }}
              </v-sheet>
            </v-col>
          </v-row>
          <v-row
              class="mt-2"
              dense
              justify="center"
          >
            <v-col
              lg="10"
            >
              <v-btn
                  v-if="allowed"
                  class="fill-width"
                  color="primary"
                  rounded="xl"
                  :text="$t('reset_password.reset_password')"
                  @click="resetPassword"
                  :loading="resettingPassword"
              />
              <v-btn
                  v-else
                  class="fill-width"
                  color="primary"
                  rounded="xl"
                  :text="$t('reset_password.to_reset')"
                  to="/forgot-password"
                  :loading="resettingPassword"
              />
            </v-col>
          </v-row>
          <v-divider class="mb-4 mt-6 border-opacity-25"/>
          <v-row
              dense
              justify="center"

          >
            <v-col
                cols="8"
                class="d-inline-block text-break text-center"
            >
              <v-btn
                  variant="plain"
                  @click="router.push('/login')"
              >
                {{ $t('reset_password.to_login') }}
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-text
          v-if="false"
          class="text-h6"
        >

        </v-card-text>
        <v-card-actions
            v-if="false"
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

</style>