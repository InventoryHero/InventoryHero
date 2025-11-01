<script setup lang="ts">
import { ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'
import useAppStyling from '@/composables/useAppStyling.ts'

// TODO ALLOW USER TO LOGIN WITH USERNAME OR EMAIL
const { t } = useI18n()
const { textFieldStyling, btnStyle } = useAppStyling()
const router = useRouter()
const { userEndpoint } = useAxios()

const loading = ref(false)
const username = ref('')
const password = ref('')
const passwordRepeat = ref('')
const email = ref('')
const registerForm = useTemplateRef('registerForm')

const {
  usernameAlreadyInUse,
  usernameRules,
  emailAlreadyInUse,
  emailRules,
  passwordRules,
  passwordRepeatRules
} = useValidationRules(password, { validatePassword: true })

const register = async () => {
  if (!registerForm.value) {
    return
  }
  const { valid } = await registerForm.value.validate()
  if (!valid) {
    return
  }
  loading.value = true
  const payload = {
    username: username.value,
    password: password.value,
    password_confirmation: passwordRepeat.value,
    email: email.value
  }
  const { success, error } = await userEndpoint.register(payload)
  if (!success) {
    switch (error) {
      case 'username_already_exists':
        usernameAlreadyInUse.value = true

        break
      case 'email_already_exists':
        emailAlreadyInUse.value = true
        break
      default:
      // TODO TOAST
    }
    registerForm.value.validate()

    loading.value = false
    return
  }
  loading.value = false
  if (success) {
    reset()
    router.push('/login')
  }
}

function reset() {
  if (registerForm.value) {
    registerForm.value.reset()
  }
}
watch(email, (_) => (emailAlreadyInUse.value = false))
watch(username, (_) => (usernameAlreadyInUse.value = false))
</script>

<template>
  <v-card>
    <template v-slot:title>
      {{ t('register.title') }}
    </template>
    <template v-slot:subtitle>
      <span class="text-wrap">{{ t('register.subtitle') }}</span>
    </template>
    <v-card-text class="mt-3">
      <v-row
        dense
        justify="center"
      >
        <v-col
          cols="12"
          lg="10"
        >
          <v-form
            @submit.prevent="register"
            ref="registerForm"
          >
            <v-row dense>
              <v-col>
                <v-text-field
                  :label="t('register.username')"
                  type="text"
                  v-model="username"
                  :rules="usernameRules"
                  v-bind="textFieldStyling"
                />
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <v-text-field
                  :label="t('register.email')"
                  type="email"
                  v-model="email"
                  :rules="emailRules"
                  v-bind="textFieldStyling"
                />
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <password-text-field
                  v-model="password"
                  :label="t('register.password')"
                  :rules="passwordRules"
                />
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <password-text-field
                  :label="t('register.repeat_password')"
                  v-model="passwordRepeat"
                  :rules="passwordRepeatRules"
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
          cols="12"
          class="d-flex justify-center"
        >
          <v-btn
            v-bind="btnStyle"
            color="primary"
            rounded="xl"
            :text="t('register.btn')"
            @click="register"
            :loading="loading"
          />
        </v-col>
      </v-row>
      <v-divider class="mb-4 mt-4 border-opacity-25" />
      <v-row
        dense
        justify="center"
      >
        <v-col
          cols="12"
          class="d-flex flex-column justify-center align-center"
        >
          <span class="text-subtitle-1 text-center">
            {{ t('register.existing_account') }}
          </span>
          <v-btn
            v-bind="btnStyle"
            variant="plain"
            color="secondary"
            to="/login"
            :text="t('register.back_to_login')"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss">
.login-link {
  text-decoration: underline;
  &:hover {
    cursor: pointer;
  }
}
</style>

<route>
{
  "path": "/register",
  "meta": {
    "requiresAuth": false,
    "allowAuthorized": false,
    "requiresHousehold": false,
    "title": 'titles.register',
    "layout": "unauthorized"
  }
}
</route>
