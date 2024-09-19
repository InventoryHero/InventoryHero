<script setup lang="ts">

import {useAuthStore} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {GeneralEndpoint} from "@/api/http";
import {useTemplateRef} from "vue";

const {t} = useI18n()
const {styling} = useAppStyling()

const emit = defineEmits<{
  (e: 'resetPassword'): void
}>()

const smtpEnabled = ref(false)
const {axios: generalEndpoint} = useAxios<GeneralEndpoint>("general")


function resetPassword(){
  emit('resetPassword')
}
const username = ref<string>("")
const password = ref<string>("")

const rules = {
  usernameNeeded: (value: string) => value !== '' || t('login.login.rules.username_needed'),
  passwordNeeded: (value: string) => value !== '' || t('login.login.rules.password_needed')
}


const loginForm = useTemplateRef("login-form")
const loading = ref(false)
const authStore = useAuthStore()
async function login(){
  const {valid} = await loginForm.value.validate()
  if(!valid) {
    return
  }
  loading.value = true;
  authStore.login(username.value, password.value).then(() => {
    loading.value = false;
  })
}

onMounted(() => {
  generalEndpoint.checkSmtp().then((enabled: boolean) => {
    smtpEnabled.value = enabled
  })
})
</script>

<template>
  <v-card-text
    class="flex-1-1 overflow-scroll"
  >
    <v-form

      ref="login-form"
      @submit.prevent
    >
      <v-row dense>
        <v-col>
          <v-text-field
              :label="$t('login.login.username')"
              :rules="[rules.usernameNeeded]"
              type="text"
              v-model="username"
              @keyup.enter="login"
              v-bind="styling"
              hide-details="auto"
          />
        </v-col>
      </v-row>
      <v-row dense>
        <v-col>
          <app-password-textfield
              :rules="[rules.passwordNeeded]"
              :label="$t('login.login.password')"
              v-model="password"
              :disable-min-length="true"
              @keyup.enter="login"
              v-bind="styling"
          />
        </v-col>
      </v-row>
    </v-form>
  </v-card-text>
  <v-card-actions >
    <v-btn
        v-if="smtpEnabled"
        variant="text"
        @click="resetPassword"
        :text="$t('login.login.forgot_password_btn')"
    />
    <v-spacer />
    <v-btn
        :loading="loading"
        prepend-icon="mdi-lock"
        variant="elevated"
        color="green-lighten-1"
        @click="login()"
        :text="$t('login.login.btn')"
   />
  </v-card-actions>
</template>

<style scoped lang="scss">

</style>