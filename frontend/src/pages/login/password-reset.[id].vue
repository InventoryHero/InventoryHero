<script setup lang="ts">
import { onBeforeMount, ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'
import { VForm } from 'vuetify/components'

definePage({
  path: '/password-reset/:id',
  props: true,
  meta: {
    requiresAuth: false,
    requiresHousehold: false,
    title: 'titles.password_reset',
    layout: 'unauthorized'
  }
})

const { userEndpoint } = useAxios()
const { t } = useI18n()
const router = useRouter()
const { notify } = useNotification()
const { btnStyle } = useAppStyling()

const { id } = defineProps<{
  id: string
}>()

const preflightCheck = ref(true)
const password = ref('')
const passwordRepeat = ref('')
const valid = ref(false)
const resettingPassword = ref(false)
const tokenWasInvalid = ref(false)
const tokenInvalidMessage = ref<string | undefined>()

const { passwordRules, passwordRepeatRules } = useValidationRules(password, {
  validatePassword: true
})

const passwordForm = useTemplateRef<VForm>('passwordForm')

async function resetPassword() {
  if (resettingPassword.value) {
    return
  }
  if (!passwordForm.value) {
    return
  }
  const { valid } = await passwordForm.value.validate()
  if (!valid) {
    return
  }
  resettingPassword.value = true
  const { success, data, error } = await userEndpoint.resetPasswordWithToken(
    id,
    {
      new_password: password.value,
      new_password_confirmation: passwordRepeat.value
    }
  )
  if (!success) {
    resettingPassword.value = false
    return false
  }

  if (!data!.valid) {
    tokenWasInvalid.value = true
    tokenInvalidMessage.value =
      data!.reason ?? t('login.reset-password.unknown_token_error')

    resettingPassword.value = false
    return false
  }

  resettingPassword.value = false

  router.replace('/login').then(() => {
    notify({
      title: t(`login.reset-password.success`),
      type: 'success'
    })
  })
}

onBeforeMount(async () => {
  const { success, data, error } = await userEndpoint.checkPasswordResetCode(id)

  if (!success) {
    // TODO
    return
  }

  tokenWasInvalid.value = !data!.valid

  if (tokenWasInvalid.value) {
    tokenInvalidMessage.value =
      data!.reason ?? t('login.reset-password.unknown_token_error')
  }
  preflightCheck.value = false
})
</script>

<template>
  <v-skeleton-loader
    v-if="preflightCheck"
    type="card"
  />

  <v-container v-else-if="tokenWasInvalid">
    <v-alert
      type="error"
      :text="tokenInvalidMessage"
      class="mb-4"
    />
    <forgot-password @close="router.replace('/login')" />
    <div class="d-flex justify-center mt-4">
      <v-btn
        v-bind="btnStyle"
        variant="plain"
        color="secondary"
        @click="router.push('/login')"
      >
        {{ t('login.reset-password.back_to_login') }}
      </v-btn>
    </div>
  </v-container>

  <v-card
    elevation="5"
    v-else
  >
    <template v-slot:loader>
      <v-progress-linear
        :indeterminate="true"
        :active="resettingPassword"
        color="primary"
      />
    </template>
    <template v-slot:title>
      {{ t('login.reset-password.title') }}
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
            ref="passwordForm"
            @submit.prevent="resetPassword"
            :disabled="resettingPassword"
            v-model="valid"
          >
            <v-row dense>
              <v-col>
                <password-text-field
                  v-model="password"
                  :label="t('login.reset-password.password')"
                  :rules="passwordRules"
                />
              </v-col>
            </v-row>
            <v-row dense>
              <v-col>
                <password-text-field
                  :label="t('login.reset-password.repeat_password')"
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
      >
        <v-col
          lg="12"
          class="d-flex justify-center"
        >
          <v-btn
            v-bind="btnStyle"
            variant="elevated"
            color="primary"
            rounded="xl"
            :text="t('login.reset-password.btn')"
            @click="resetPassword"
            :loading="resettingPassword"
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
          class="d-flex justify-center align-center"
        >
          <v-btn
            v-bind="btnStyle"
            variant="plain"
            color="secondary"
            @click="router.push('/login')"
          >
            {{ t('login.reset-password.back_to_login') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss"></style>
