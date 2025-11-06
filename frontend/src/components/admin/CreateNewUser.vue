<template>
  <v-dialog
    v-model="active"
    :height="height"
    :width="width"
    scrollable
    persistent
    no-click-animation
  >
    <v-card
      :title="t('administration.users.create_new.title')"
      :loading="loading"
    >
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="active = false"
        />
      </template>
      <v-card-text class="fill-height overflow-auto">
        <v-form
          :disabled="loading"
          submit.prevent=""
          ref="newUserForm"
          validate-on="submit lazy"
        >
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="username"
                :rules="usernameRules"
                :label="t('administration.users.create_new.username')"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="email"
                :rules="emailRules"
                :label="t('administration.users.create_new.email')"
              />
            </v-col>
            <v-col cols="12">
              <password-text-field
                v-model="password"
                :rules="passwordRules"
                :label="t('administration.users.create_new.password')"
              />
            </v-col>
            <v-col cols="12">
              <password-text-field
                v-model="passwordRepeat"
                :rules="passwordRepeatRules"
                :label="t('administration.users.create_new.repeat_password')"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="firstName"
                :label="t('administration.users.create_new.first_name')"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
                v-model="lastName"
                :label="t('administration.users.create_new.last_name')"
              />
            </v-col>
            <v-col cols="12">
              <v-checkbox-btn
                v-model="isAdmin"
                :label="t('administration.users.create_new.is_admin')"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn
          :disabled="loading"
          prepend-icon="mdi-content-save"
          :text="t('administration.users.create_new.save')"
          @click="saveUser"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { UserPublic } from '@/api/types/households'
import { AdminUserCreate } from '@/api/types/user'
import useValidationRules from '@/composables/useValidationRules'

const { mdAndUp } = useDisplay()
const { t } = useI18n()
const { textFieldStyling } = useAppStyling()
const { admin } = useAxios()
const { width, height } = useDialogSize()

const active = defineModel<boolean>('active', {
  required: true
})

const emit = defineEmits<{
  (e: 'userCreated', user: UserPublic): void
}>()

const newUserForm = useTemplateRef('newUserForm')
const username = ref<string | undefined | null>()
const email = ref<string | undefined | null>()
const password = ref<string | undefined>()
const passwordRepeat = ref<string | undefined>()
const lastName = ref<string | undefined | null>()
const firstName = ref<string | undefined | null>()
const isAdmin = ref<boolean>(false)
const loading = ref<boolean>(false)

const { usernameRules, emailRules, passwordRules, passwordRepeatRules } =
  useValidationRules(password)

const saveUser = async () => {
  const { valid } = await newUserForm.value.validate()
  if (!valid) {
    return
  }

  const newUser = {
    username: username.value,
    password: password.value,
    email: email.value,
    last_name: lastName.value,
    first_name: firstName.value,
    isAdmin: isAdmin.value
  } as AdminUserCreate

  loading.value = true
  const { success, data } = await admin.createUser(newUser)
  if (!success) {
    loading.value = false
    return
  }
  emit('userCreated', data!)
  loading.value = true
}

watch(active, (value: boolean, oldValue: boolean) => {
  if (value) {
    return
  }

  username.value = undefined
  email.value = undefined
  password.value = undefined
  passwordRepeat.value = undefined
  lastName.value = undefined
  firstName.value = undefined
  isAdmin.value = false
  loading.value = false
})
</script>

<style scoped></style>
