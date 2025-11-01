<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import useConfigStore from '@/stores/useConfigStore'
import { useTemplateRef } from 'vue'
import { VForm } from 'vuetify/components'
import { storeToRefs } from 'pinia'
import { useNotification } from '@kyvg/vue3-notification'

const { t } = useI18n()
const { textFieldStyling, btnStyle } = useAppStyling()
const route = useRoute()
const router = useRouter()
const configStore = useConfigStore()
const { auth, userEndpoint } = useAxios()
const { notify } = useNotification()

const { smtpEnabled, registrationAllowed } = storeToRefs(configStore)

const forgotPasswordDialog = ref<boolean>(false)
const username = ref<string>('')
const password = ref<string>('')
const confirmationMissingAlert = ref<boolean>(false)

const { usernameRules, passwordRules } = useValidationRules(password)

const userNameOrPasswordInvalidBanner = ref<boolean>(false)

const loginForm = useTemplateRef<VForm>('login-form')
const loading = ref(false)
const authStore = useAuthStore()

async function login() {
  if (!loginForm.value) {
    return
  }
  const { valid } = await loginForm.value.validate()
  if (!valid) {
    return
  }
  loading.value = true
  const loginFormData = new FormData()
  loginFormData.append('username', username.value)
  loginFormData.append('password', password.value)
  const { success, error } = await auth.login(loginFormData)
  if (!success) {
    if (error === 'username_or_password_incorrect') {
      userNameOrPasswordInvalidBanner.value = true
    }

    loading.value = false
    return
  }
  await authStore.whoami()
  const redirectPath = (route.query.redirect as string) || '/'
  router.replace(redirectPath)
  loginForm.value.reset()
  loading.value = false
}

const requestNewConfirmationCode = async () => {
  confirmationMissingAlert.value = false
  const { success } = await userEndpoint.requestEmailConfirmation()
  if (!success) {
    return
  } else {
    notify({
      title: t('login.notification.request_new_confirmation_code'),
      type: 'success'
    })
  }
}

onBeforeRouteLeave(() => {
  return !forgotPasswordDialog.value
})
</script>

<template>
  <forgot-password v-model:active="forgotPasswordDialog" />
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
    <template v-slot:title>
      <p class="text-wrap">
        {{ t('login.title') }}
      </p>
    </template>
    <v-card-subtitle>
      {{ t('login.subtitle') }}
    </v-card-subtitle>
    <v-card-text class="mt-4">
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
            <template v-slot:default="{ isHovering, props }">
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
      <v-expand-transition>
        <v-row
          v-if="userNameOrPasswordInvalidBanner"
          justify="center"
        >
          <v-col
            cols="12"
            class="d-flex justify-center"
          >
            <span class="text-error text-subtitle-1 text-medium-emphasis">
              {{ t('login.username_or_password_invalid') }}
            </span>
          </v-col>
        </v-row>
      </v-expand-transition>
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
      <v-divider class="mb-4 mt-4 border-opacity-25" />
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
.reset-password {
  &:hover {
    cursor: pointer;
    text-decoration: underline;
  }
}

.warning-banner {
  &:hover {
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
