<script setup lang="ts">
import useAuthStore from '@/stores/useAuthStore'
import useConfigStore from '@/stores/useConfigStore'
import { ref, useTemplateRef } from 'vue'
import { useI18n } from 'vue-i18n'
import useAppStyling from '@/composables/useAppStyling.ts'
import { ChangePasswordForm, UserUpdate } from '@/api/types/user.ts'
import { useNotification } from '@kyvg/vue3-notification'
import { storeToRefs } from 'pinia'
import router from '@/router'
import { updateFormatted } from 'vuetify/lib/labs/VCalendar/util/timestamp.mjs'

const { t } = useI18n()

const authStore = useAuthStore()
const { userEndpoint } = useAxios()
const { textFieldStyling, btnStyle } = useAppStyling()
const { notify } = useNotification()
const configStore = useConfigStore()

const userForm = useTemplateRef('userForm')
const passwordForm = useTemplateRef('passwordResetForm')

const { smtpEnabled } = storeToRefs(configStore)
const { user } = storeToRefs(authStore)

const updated = ref({ ...user.value })

const saving = ref(false)
const passwordFormVisible = ref<boolean>(false)
const currPassword = ref<string | undefined>(undefined)
const newPassword = ref<string | undefined>(undefined)
const newPasswordRepeat = ref<string | undefined>(undefined)
const loading = ref<boolean>(false)
const currPasswordInvalid = ref<boolean>(false)

const {
  passwordRules: newPasswordRules,
  passwordRepeatRules: newPasswordRepeatRules
} = useValidationRules(newPassword, { validatePassword: true })

const currPasswordRules = ref([
  (value: string | null | undefined) =>
    !!value || t('account.password.rules.old_not_empty'),
  (value: string) =>
    !currPasswordInvalid.value || t('validation.password.curr_password_invalid')
])

const usernameRules = ref([
  (value: string | null | undefined) =>
    !!value || t('account.rules.username_required')
])
const emailRules = ref([
  (value: string | null | undefined) =>
    !!value || t('account.rules.email_required')
])

const usernameEdited = computed(
  () => updated.value?.username !== user.value?.username
)
const emailEdited = computed(() => updated.value?.email !== user.value?.email)
const firstNameEdited = computed(
  () => updated.value?.last_name !== user.value?.first_name
)
const lastNamedEdited = computed(
  () => updated.value?.last_name !== user.value?.last_name
)

const edited = computed(() => {
  return (
    usernameEdited.value ||
    firstNameEdited.value ||
    lastNamedEdited.value ||
    emailEdited.value
  )
})
const lazySrc = computed(
  () =>
    `https://api.dicebear.com/8.x/bottts-neutral/svg?seed=${user.value?.username}`
)
const profilePictureSrc = computed(() => lazySrc.value)
const passwordFormValid = computed(() => {
  return (
    !!currPassword.value && !!newPassword.value && !!newPasswordRepeat.value
  )
})

const uploadProfilePicture = () => {
  // TODO
  notify({
    type: 'info',
    title: 'coming soon'
  })
}

const reset = () => {
  updated.value = { ...user.value }
}

const resendConfirmationEmail = async () => {
  const { success } = await userEndpoint.requestEmailConfirmation()
  if (success) {
    notify({
      title: t('account.resend_confirmation_success'),
      type: 'success'
    })
  }
}

async function saveUpdatedUserdata() {
  const { valid } = await userForm.value.validate()
  if (!valid) {
    return
  }
  let payload = {
    username: !usernameEdited.value ? undefined : updated.value?.username,
    email: !emailEdited.value ? undefined : updated.value?.email,
    first_name: !firstNameEdited.value ? undefined : updated.value?.first_name,
    last_name: !lastNamedEdited.value ? undefined : updated.value?.last_name
  } as UserUpdate
  saving.value = true
  const { success, data, error } = await userEndpoint.updateUser(payload)
  if (!success) {
    saving.value = false
    return
  }
  authStore.user = data!
  reset()
  saving.value = false
}

const updatePassword = async () => {
  const { valid } = await passwordForm.value.validate()
  if (!valid) {
    return
  }

  let payload = {
    current_password: currPassword.value,
    new_password: newPassword.value,
    new_password_confirmation: newPasswordRepeat.value
  } as ChangePasswordForm

  const { success, data, error } = await userEndpoint.changePassword(payload)
  if (!success) {
    switch (error) {
      case 'wrong_password':
        currPasswordInvalid.value = true
        break
      default:
        // TODO notify?
        break
    }
    passwordForm.value.validate()
    return
  }
  notify({
    title: t('account.password_changed_successfully'),
    type: 'success'
  })
  passwordForm.value.reset()
  passwordFormVisible.value = false
}

const showPasswordForm = async () => {
  passwordFormVisible.value = !passwordFormVisible.value
}

const forgotPassword = async () => {
  const { success } = await userEndpoint.resetPassword({
    email: authStore.user!.email
  })
  if (!success) {
    return
  }
  notify({
    title: t('account.toasts.forgot-password.title'),
    text: t('account.toasts.forgot-password.text'),
    type: 'info'
  })
}

// This function stops the loop once the transition is finished
const scrollToBottom = () => {
  if (!passwordFormVisible.value) {
    return
  }
  window.scrollTo({
    top: document.documentElement.scrollHeight,
    behavior: 'smooth'
  })
}

watch(passwordFormVisible, (newValue: boolean) => {
  if (!newValue) {
    passwordForm.value.reset()
  }
})

onBeforeMount(() => {
  if (!authStore.user) {
    loading.value = true
    userEndpoint.self().then(({ success, data }) => {
      if (!success) {
        // TODO
        return
      }
      authStore.user = data!
      loading.value = false
    })
  }
})

watch(currPassword, (_) => (currPasswordInvalid.value = false))
</script>

<template>
  <v-skeleton-loader
    type="image, divider, heading"
    v-if="loading"
  />

  <template v-else>
    <v-hover>
      <template v-slot:default="{ isHovering, props }">
        <v-img
          v-bind="props"
          class="mx-auto mt-4"
          rounded="circle position-relative"
          aspect-ratio="1/1"
          height="100"
          width="100"
          cover
          :lazy-src="lazySrc"
          alt="avatar"
          :src="profilePictureSrc"
          @click="uploadProfilePicture"
          :style="{
            cursor: isHovering ? 'pointer' : undefined
          }"
        >
          <template v-slot:default>
            <v-overlay
              :model-value="!!isHovering"
              contained
              class="align-center justify-center"
              scrim="#000000"
            >
              <v-icon
                icon="mdi-camera"
                size="large"
              />
            </v-overlay>
          </template>
        </v-img>
      </template>
    </v-hover>

    <v-container class="mt-4 mb-4">
      <v-row justify="center">
        <v-col
          lg="8"
          cols="12"
        >
          <v-form
            ref="userForm"
            @submit.prevent=""
          >
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  v-model="updated.username"
                  :label="t('account.username')"
                  :rules="usernameRules"
                >
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="usernameEdited"
                      icon="mdi-refresh"
                      @click="updated.username = user?.username"
                    />
                  </template>
                  <template #prepend-inner="slotProps"></template>
                </v-text-field>
              </v-col>
              <v-col cols="12">
                <v-row>
                  <v-col
                    cols="12"
                    :md="!user?.confirmed ? '8' : '12'"
                  >
                    <v-text-field
                      v-bind="textFieldStyling"
                      v-model="updated.email"
                      :label="t('account.email')"
                      :rules="emailRules"
                    >
                      <template v-slot:append-inner>
                        <v-icon
                          v-if="emailEdited"
                          icon="mdi-refresh"
                          @click="updated.email = user?.email"
                        />
                      </template>
                    </v-text-field>
                  </v-col>
                  <v-col
                    v-if="!user?.confirmed"
                    cols="12"
                    md="4"
                    class="d-flex align-center justify-center"
                  >
                    <v-btn
                      color="warning"
                      @click="resendConfirmationEmail"
                    >
                      {{ t('account.email_not_confirmed') }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  v-model="updated.first_name"
                  :label="t('account.firstname')"
                >
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="firstNameEdited"
                      icon="mdi-refresh"
                      @click="updated.first_name = user?.first_name"
                    />
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-bind="textFieldStyling"
                  v-model="updated.last_name"
                  :label="t('account.lastname')"
                >
                  <template v-slot:append-inner>
                    <v-icon
                      v-if="lastNamedEdited"
                      icon="mdi-refresh"
                      @click="updated.last_name = user?.last_name"
                    />
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
          </v-form>
          <div class="d-flex justify-end mt-4">
            <v-btn
              v-bind="btnStyle"
              :text="t('account.save')"
              @click="saveUpdatedUserdata"
              :disabled="!edited"
            />
          </div>

          <v-divider class="mt-4 mb-4" />

          <div class="d-flex justify-space-between align-center mb-4">
            {{ t('account.password.password') }}
            <v-btn
              v-bind="btnStyle"
              variant="outlined"
              :text="
                !passwordFormVisible
                  ? t('account.password.change_password')
                  : t('account.password.hide_change_password')
              "
              @click="showPasswordForm"
            />
          </div>
          <v-scroll-y-transition @after-enter="scrollToBottom">
            <v-form
              ref="passwordResetForm"
              v-if="passwordFormVisible"
            >
              <v-row>
                <v-col cols="12">
                  <password-text-field
                    :label="t('account.password.current_password')"
                    v-model="currPassword"
                    :rules="currPasswordRules"
                  />
                </v-col>
                <v-col cols="12">
                  <password-text-field
                    :label="t('account.password.new_password')"
                    v-model="newPassword"
                    :rules="newPasswordRules"
                  />
                </v-col>
                <v-col cols="12">
                  <password-text-field
                    :label="t('account.password.new_password_repeat')"
                    v-model="newPasswordRepeat"
                    :rules="newPasswordRepeatRules"
                  />
                </v-col>
              </v-row>
              <div class="d-flex justify-end mt-4 flex-wrap-reverse">
                <v-btn
                  v-if="smtpEnabled"
                  v-bind="btnStyle"
                  variant="plain"
                  :text="t('account.password.forgot_password')"
                  @click="forgotPassword"
                />
                <v-btn
                  v-bind="btnStyle"
                  :text="t('account.password.change_password')"
                  :disabled="!passwordFormValid"
                  @click="updatePassword"
                />
              </div>
            </v-form>
          </v-scroll-y-transition>
        </v-col>
      </v-row>
    </v-container>
  </template>
</template>

<style scoped lang="scss"></style>

<route>
{
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": false,
    "title": 'titles.account',
    "layout": "default"
  }
}
</route>
