<script setup lang="ts">

import {useAuthStore, useConfigStore} from "@/store";
import {useTemplateRef} from "vue";
import {VForm} from "vuetify/components";
import {storeToRefs} from "pinia";

const {t} = useI18n()
const {textFieldStyling, btnStyle} = useAppStyling()
const route = useRoute();
const router = useRouter();
const configStore = useConfigStore()
const {auth, userEndpoint} = useAxios()

const {smtpEnabled, registrationAllowed} = storeToRefs(configStore)
smtpEnabled.value = true

const forgotPasswordDialog = ref<boolean>(false)
const username = ref<string>("")
const password = ref<string>("")
const confirmationMissingAlert = ref<boolean>(false)



const usernameRules = ref([
  (value: string) => value !== '' || t('login.rules.username_needed')
])

const passwordRules = ref([
  (value: string) => value !== '' || t('login.rules.password_needed')
])


const loginForm = useTemplateRef<VForm>("login-form")
const loading = ref(false)
const authStore = useAuthStore()

async function login(){
  if(!loginForm.value)
  {
    return
  }
  const {valid} = await loginForm.value.validate()
  if(!valid) {
    return
  }
  loading.value = true;
  const loginFormData = new FormData()
  loginFormData.append("username", username.value)
  loginFormData.append("password", password.value)
  const {success, error} = await auth.login(loginFormData)
  if(!success){
    if(error === "email_not_confirmed") {
      confirmationMissingAlert.value = true
    }

    loading.value = false
    return
  }
  await authStore.whoami()
  const redirectPath = route.query.redirect as string || '/';
  router.replace(redirectPath)
  loginForm.value.reset()
  loading.value = false;
}

const requestNewConfirmationCode = async () => {
  confirmationMissingAlert.value = false
  const {success, error} = await userEndpoint.requestEmailConfirmation()
  if(!success){
    // TODO
  } else {
    // TODO NOTIFY SUCCESS
  }
}

onBeforeRouteLeave(() => {
  return !forgotPasswordDialog.value
})
</script>

<template>

  <forgot-password
      v-model="forgotPasswordDialog"
  />



  <v-card
      elevation="5"
      class="d-flex flex-column"
  >
    <template v-slot:loader>
      <v-progress-linear
        indeterminate
        :active="loading"
        color="primary"
      />
    </template>
    <template v-slot:append>
      <v-icon-btn
          icon="mdi-cog"
          to="/login/settings"
      />
    </template>
    <template v-slot:title>
      <p
        class="text-wrap"
      >
        {{ t('login.title') }}
      </p>
    </template>
    <v-card-subtitle>
      {{ t('login.subtitle') }}
    </v-card-subtitle>
    <v-card-text
        class="mt-4"
    >


      <v-row
          dense
          justify="center"
      >
        <v-col
          cols="12"
          lg="10"
          v-if="confirmationMissingAlert"
          class="mb-4"
        >
          <v-hover>
            <template v-slot:default="{isHovering, props}">
              <v-alert
                  v-bind="props"
                  :style="{
                    cursor: isHovering ? 'pointer' : undefined
                  }"
                  :title="t('login.confirmation_missing.title')"
                  :text="t('login.confirmation_missing.text')"
                  @click="requestNewConfirmationCode"
              />
            </template>
          </v-hover>
        </v-col>
        <v-col
            cols="12"
            lg="10"
        >
          <v-form
              ref="login-form"
              @submit.prevent="(event) => event.preventDefault()"
          >
            <v-row dense>
              <v-col>
                <v-text-field
                    :label="t('login.username')"
                    :rules="usernameRules"
                    type="text"
                    v-model="username"
                    @keyup.enter="login"
                    v-bind="textFieldStyling"
                    hide-details="auto"
                />
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <password-text-field
                    :rules="passwordRules"
                    :label="t('login.password')"
                    v-model="password"
                    @keyup.enter="login"
                />
              </v-col>
            </v-row>
          </v-form>
        </v-col>
      </v-row>
      <v-row
          class="mt-4"
          dense
          justify="center"
      >
        <v-col
          lg="10"
          class="d-flex flex-column align-center justify-center"
        >
          <v-btn
              v-bind="btnStyle"
              class="fill-width"
              rounded="xl"
              :text="t('login.btn')"
              :loading="loading"
              @click="login"
          />
          <v-btn
              v-if="smtpEnabled"
              v-bind="btnStyle"
              variant="plain"
              color="secondary"
              class="reset-password text-caption text-primary mt-2"
              @click="forgotPasswordDialog = true"
          >
            {{ t('login.forgot_password_btn') }}
          </v-btn>
        </v-col>
      </v-row>
      <v-divider class="mb-4 mt-4 border-opacity-25"/>
      <v-row
          dense
          justify="center"
          class="pa-1"
          v-if="registrationAllowed"
      >
          <v-btn
              v-bind="btnStyle"
              variant="plain"
              :text="t('login.register')"
              append-icon="mdi-chevron-right"
              to="/register"
          />
      </v-row>
    </v-card-text>
  </v-card>

</template>

<style scoped lang="scss">
.reset-password{
  &:hover{
    cursor: pointer;
    text-decoration: underline;
  }
}

.warning-banner{
  &:hover{
    cursor: pointer;
  }
}
</style>

<route>
{
  "meta": {
    "requiresAuth": false,
    "allowAuthorized": false,
    "requiresHousehold": false,
    "layout": "unauthorized",
  }
}
</route>