<script setup lang="ts">
import {VForm} from "vuetify/components";
import {UserEndpoint} from "@/api/http";
import {useTemplateRef} from "vue";
import {useNotification} from "@kyvg/vue3-notification";

const {t} = useI18n()
const {styling} = useAppStyling()
const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {notify} = useNotification()


const formValid = ref(false)
const form = useTemplateRef<VForm>("resendEmailForm")
const username = ref<string>("")
const rules = {
  usernameNeeded: (value: string) => value !== '' || t('login.rules.username_needed'),
}


const loading = ref(false)
async function requestConfirmation(){
  if(!form.value){
    return
  }
  const {valid} = await form.value.validate()
  if(!valid){
    return
  }
  loading.value = true
  userEndpoint.resendConfirmationEmail(username.value).then(({success, message}) =>{
    loading.value = false
    if(!success){
      if((message ?? "") === ""){
        message = "unknown_error"
      }
      notify({
        title: t(`toasts.titles.error.${message}`),
        text: t(`toasts.text.error.${message}`),
        type: "error"
      })
      return
    }
    notify({
      title: t(`toasts.titles.success.resent_confirmation`),
      text: t(`toasts.text.success.resent_confirmation`),
      type: "success"
    })
  })
}
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
          class="d-flex flex-column"
      >
        <v-card-title class="d-inline-block text-wrap">
          {{ t('confirmation.not_confirmed.title')}}
        </v-card-title>
        <v-card-subtitle class="d-inline-block text-wrap">
          {{ t('confirmation.not_confirmed.subtitle')}}
        </v-card-subtitle>
        <v-card-text
          class="mt-3"
        >
          <v-row
              dense
              justify="center"
          >
            <v-col
                cols="12"
                lg="10"
            >
              <v-form
                  v-model="formValid"
                  ref="resendEmailForm"
                  @submit.prevent="(event) => event.preventDefault()"
              >
                <v-row dense>
                  <v-col>
                    <v-text-field
                        :label="$t('login.username')"
                        :rules="[rules.usernameNeeded]"
                        type="text"
                        v-model="username"
                        @keyup.enter="requestConfirmation"
                        v-bind="styling"
                        hide-details="auto"
                    />
                  </v-col>
                </v-row>
              </v-form>
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
                  class="fill-width"
                  color="primary"
                  rounded="xl"
                  :text="t('confirmation.not_confirmed.resend')"
                  :loading="loading"
                  @click="requestConfirmation"
                  :disabled="!formValid"
              />
            </v-col>
          </v-row>
          <v-divider class="mb-4 mt-6 border-opacity-25"/>
          <v-row
              dense
              justify="center"
              class="pa-1"
          >
            <v-btn
                density="compact"
                size="small"
                variant="plain"
                :text="t('confirmation.go_to_login')"
                append-icon="mdi-chevron-right"
                to="/login"
            />
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>