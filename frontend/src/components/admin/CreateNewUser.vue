<template>
  <v-dialog
    v-model="active"
    :height="mdAndUp ? '700px' : '100%'"
    :width="mdAndUp ? '600px' : '100%'"
    scrollable
  >
    <v-card :title="t('administration.users.create_new.title')">
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="active = fase"
        />
      </template>
      <v-card-text class="fill-height overflow-auto">
        <v-form
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
              <v-text-field
                v-bind="textFieldStyling"
                v-model="password"
                :rules="passwordRules"
                :label="t('administration.users.create_new.password')"
              />
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-bind="textFieldStyling"
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
          prepend-icon="mdi-content-save"
          :text="t('administration.users.create_new.save')"
          @click="saveUser"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import useValidationRules from '@/composables/useValidationRules'

const { mdAndUp } = useDisplay()
const { t } = useI18n()
const { textFieldStyling } = useAppStyling()

const newUserForm = useTemplateRef('newUserForm')
const username = ref<string | undefined | null>()
const email = ref<string | undefined | null>()
const password = ref<string | undefined | null>()
const passwordRepeat = ref<string | undefined | null>()
const lastName = ref<string | undefined | null>()
const firstName = ref<string | undefined | null>()
const isAdmin = ref<boolean>(false)

const { usernameRules, emailRules, passwordRules, passwordRepeatRules } =
  useValidationRules(password)

const saveUser = async () => {
  const { valid } = await newUserForm.value.validate()
  if (!valid) {
    return
  }

  console.log('New user with username: ', username.value)
}

const active = defineModel<boolean>('active', {
  required: true
})
</script>

<style scoped></style>
