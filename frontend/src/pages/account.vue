<script setup lang="ts">

import {useAuthStore, useConfigStore} from "@/store";
import { ref, useTemplateRef} from "vue";
import {useI18n} from "vue-i18n";
import useAppStyling from "@/composables/useAppStyling.ts";
import {ChangePasswordForm, UserUpdate} from "@/api/types/user.ts";
import {useNotification} from "@kyvg/vue3-notification";
import {storeToRefs} from "pinia";

const {t} = useI18n()

const authStore = useAuthStore()
const {userEndpoint} = useAxios()
const {textFieldStyling, btnStyle} = useAppStyling()
const {notify} = useNotification()
const configStore = useConfigStore()

const userForm = useTemplateRef('userForm')
const passwordForm = useTemplateRef('passwordResetForm')

const {smtpEnabled} = storeToRefs(configStore)
const username = ref<string>(authStore.user!.username)
const firstname = ref<string|null|undefined>(authStore.user!.first_name)
const lastname = ref<string|null|undefined>(authStore.user!.last_name)
const email = ref<string>(authStore.user!.email)
const saving = ref(false)
const passwordFormVisible = ref<boolean>(false)
const currPassword = ref<string|undefined>(undefined)
const newPassword = ref<string|undefined>(undefined)
const newPasswordRepeat = ref<string|undefined>(undefined)
const loading = ref<boolean>(false)

const passwordRules = ref([
  (value: string|null|undefined) => !!value || t('account.password.rules.old_not_empty')
])
const newPasswordRules = ref([
  (value: string|null|undefined) => !!value || t('account.password.rules.new_not_empty')
])
const newPasswordRepeatRules = ref([
  (value: string|null|undefined) => !!value || t('account.password.rules.repeat_not_empty'),
  (value: string) => value === newPassword.value || t('account.password.rules.mismatch')
])
const usernameRules = ref([
  (value: string|null|undefined) => !!value || t('account.rules.username_required')
])
const emailRules = ref([
  (value: string|null|undefined) => !!value || t('account.rules.email_required')
])

const edited = computed(() => {
  return username.value !== authStore.user!.username ||
      firstname.value !== authStore.user!.first_name ||
      lastname.value !== authStore.user!.last_name ||
      email.value !== authStore.user!.email
})
const lazySrc = computed(() => `https://api.dicebear.com/8.x/bottts-neutral/svg?seed=${username}`)
const profilePictureSrc = computed(() => lazySrc.value)
const passwordFormValid = computed(() => {
  return !!currPassword.value && !!newPassword.value && !!newPasswordRepeat.value
})

const uploadProfilePicture = () => {
  // TODO
  notify({
    type: 'info',
    title: 'coming soon'
  })
}

const reset = () => {
  username.value = authStore.user!.username
  email.value = authStore.user!.email
  lastname.value = authStore.user!.last_name
  firstname.value = authStore.user!.first_name
}

async function saveUpdatedUserdata(){
  const {valid} = await userForm.value.validate()
  if(!valid){
    return
  }
  let payload = {
    username: username.value === authStore.user!.username ? undefined : username.value,
    email: email.value === authStore.user!.email ? undefined : email.value,
    first_name: firstname.value === authStore.user!.first_name ? undefined : firstname.value,
    last_name: lastname.value === authStore.user!.last_name ? undefined : lastname.value,
  } as UserUpdate
  saving.value = true
  const {success, data, error} = await userEndpoint.updateUser(payload)
  if(!success){
    // TODO
  }
  authStore.user = data!
  reset()
  saving.value = false
}

const updatePassword = async () => {
  const {valid} = await passwordForm.value.validate()
  if(!valid){
    return
  }

  let payload = {
    current_password: currPassword.value,
    new_password: newPassword.value,
    new_password_confirmation: newPasswordRepeat.value,
  } as ChangePasswordForm

  const {success, data, error} = await userEndpoint.changePassword(payload)
  if(!success){
    // TODO
  }
  passwordForm.value.reset()
  passwordFormVisible.value = false
}

const showPasswordForm = async () => {
  passwordFormVisible.value = !passwordFormVisible.value
}

const forgotPassword = async () => {
  const {success, data, error} = await userEndpoint.resetPassword({email: authStore.user!.email})
  if(!success){
    // TODO
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
  });

};

watch(passwordFormVisible, (newValue: boolean) => {
  if(!newValue){
    passwordForm.value.reset()
  }
})


onBeforeMount(() => {
  if(!authStore.user){
    loading.value = true
    userEndpoint.self().then(({success, data, error}) => {
      if(!success){
        // TODO
      }
      authStore.user = data!
      loading.value = false
    })
  }
})


</script>

<template>

  <v-skeleton-loader
    type="image, divider, heading"
    v-if="loading"
  />

  <v-hover>
    <template v-slot:default="{isHovering, props}">
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
            cursor: isHovering ? 'pointer': undefined
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

  <v-container
      class="mt-4 mb-4"
  >
    <v-row
      justify="center"
    >
      <v-col
        lg="6"
        cols="12"
      >
        <v-form
            ref="userForm"
            @submit.prevent=""
        >
          <v-row>
            <v-col
                cols="12"
            >
              <v-text-field
                  v-bind="textFieldStyling"
                  v-model="username"
                  :label="t('account.username')"
                  :rules="usernameRules"
              >
                <template v-slot:append-inner>
                  <v-icon
                    v-if="username !== authStore.user!.username"
                    icon="mdi-refresh"
                    @click="username = authStore.user!.username"
                  />
                </template>
              </v-text-field>

            </v-col>
            <v-col
                cols="12"
            >
              <v-text-field
                  v-bind="textFieldStyling"
                  v-model="email"
                  :label="t('account.email')"
                  :rules="emailRules"
              >
                <template v-slot:append-inner>
                  <v-icon
                      v-if="email !== authStore.user!.email"
                      icon="mdi-refresh"
                      @click="email = authStore.user!.email"
                  />
                </template>
              </v-text-field>
            </v-col>
            <v-col

                cols="12"
            >
              <v-text-field
                  v-bind="textFieldStyling"
                  v-model="firstname"
                  :label="t('account.firstname')"
              >
                <template v-slot:append-inner>
                  <v-icon
                      v-if="firstname !== authStore.user!.first_name"
                      icon="mdi-refresh"
                      @click="firstname = authStore.user!.first_name"
                  />
                </template>
              </v-text-field>
            </v-col>
            <v-col
                cols="12"
            >
              <v-text-field
                  v-bind="textFieldStyling"
                  v-model="lastname"
                  :label="t('account.lastname')"
              >
                <template v-slot:append-inner>
                  <v-icon
                      v-if="lastname !== authStore.user!.last_name"
                      icon="mdi-refresh"
                      @click="lastname = authStore.user!.last_name"
                  />
                </template>
              </v-text-field>
            </v-col>

          </v-row>
        </v-form>
        <div
          class="d-flex justify-end mt-4"
        >
          <v-btn
              v-bind="btnStyle"
              :text="t('account.save')"
              @click="saveUpdatedUserdata"
              :disabled="!edited"
          />
        </div>

        <v-divider class="mt-4 mb-4" />

        <div
            class="d-flex justify-space-between align-center mb-4"
        >
          {{ t('account.password.password') }}
          <v-btn
              v-bind="btnStyle"
              variant="outlined"

              :text="!passwordFormVisible ? t('account.password.change_password') : t('account.password.hide_change_password')"
              @click="showPasswordForm"
          />
        </div>
        <v-scroll-y-transition
            @after-enter="scrollToBottom"
        >
          <v-form

            ref="passwordResetForm"
            v-if="passwordFormVisible"
          >
            <v-row>
              <v-col cols="12">
                <password-text-field
                    :label="t('account.password.current_password')"
                    v-model="currPassword"
                    :rules="passwordRules"
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
            <div
                class="d-flex justify-end mt-4 flex-wrap-reverse"
            >
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

<style scoped lang="scss">
</style>

<route>
{
  "meta": {
    "requiresAuth": true,
    "requiresHousehold": false,
    "title": 'titles.account',
  }
}
</route>