<script setup lang="ts">
import {useAuthStore} from "@/store";
import { ref, useTemplateRef} from "vue";
import {useI18n} from "vue-i18n";
import useAppStyling from "@/composables/useAppStyling.ts";
import useUserNameCharacterRule from "@/composables/useUserNameCharacterRule.ts";
import useEmailRule from "@/composables/useEmailRule.ts";


const authStore = useAuthStore()
const {t: $t} = useI18n()
const {styling} = useAppStyling()

const emit = defineEmits<{
  (e: 'registered'): void
}>()

const loading = ref(false)
const username = ref("")

const password = ref("")
const passwordRepeat = ref("")
const email = ref("")
const registerForm = useTemplateRef("register-form")
const rules = {
  usernameNeeded: (value: string) => (value && value !== '') || $t('login.register.rules.username_needed'),
   passwordNeeded: (value: string) => (value && value !== '') || $t('login.register.rules.password_needed'),
  repeatNotEqual: (value: string) => value === password.value || $t('login.register.rules.passwords_not_equal'),
  emailNeeded: (value: string) => (value && value !== '') || $t('login.register.rules.email_needed')
}
const {usernameCharacterRule} = useUserNameCharacterRule()
const {isValidEmailRule} = useEmailRule()
async function register() {

  //@ts-expect-error couldn't figure out how to type template ref
  const {valid} = await registerForm.value.validate();
  if(!valid)
  {
    return
  }
  loading.value=true;
  let success = await authStore.register(username.value, password.value, email.value)
  loading.value = false
  if (success) {
    reset()
    close()
  }
}

function reset(){
  password.value = "";
  passwordRepeat.value = "";
  username.value = "";
  email.value= "";
}

function close(){
  emit('registered')
}

</script>

<template>
  <v-card-text
    class="flex-1-1"
  >
    <v-form
      @submit.prevent
      ref="register-form"
    >
      <v-row
        dense
      >
        <v-col>
          <v-text-field
              :label="$t('login.register.username')"
              type="text"
              v-model="username"
              :rules="[rules.usernameNeeded, usernameCharacterRule]"
              @keyup.enter="register"
              v-bind="styling"
          />
        </v-col>
      </v-row>
      <v-row
        dense
      >
        <v-col>
          <v-text-field
              :label="$t('login.register.email')"
              type="email"
              v-model="email"
              :rules="[rules.emailNeeded, isValidEmailRule]"
              @keyup.enter="register"
              v-bind="styling"
          />
        </v-col>
      </v-row>
      <v-row
        dense
      >
        <v-col>
          <app-password-textfield
              v-model="password"
              :label="$t('login.register.password')"
              :rules="[rules.passwordNeeded]"
              @keyup.enter="register"
              v-bind="styling"
          />
        </v-col>
      </v-row>
     <v-row
      dense
     >
       <v-col>
         <app-password-textfield
             :label="$t('login.register.repeat_password')"
             v-model="passwordRepeat"
             :rules="[rules.repeatNotEqual]"
             v-bind="styling"
             @keyup.enter="register"
         />
       </v-col>
     </v-row>

    </v-form>
  </v-card-text>
  <v-card-actions class="justify-end">
    <v-btn
        :loading="loading"
        variant="elevated"
        color="green-lighten-1"
        @click="register()"
        prepend-icon="mdi-lock"
    >
      <template #prepend>
        <v-icon size="small"/>
      </template>
      {{ $t("login.register.btn") }}
    </v-btn>
  </v-card-actions>
</template>

<style scoped lang="scss">

</style>