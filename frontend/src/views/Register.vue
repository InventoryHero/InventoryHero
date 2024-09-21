<script setup lang="ts">
import {useAuthStore} from "@/store";
import { ref, useTemplateRef} from "vue";
import {useI18n} from "vue-i18n";
import useAppStyling from "@/composables/useAppStyling.ts";
import useUserNameCharacterRule from "@/composables/useUserNameCharacterRule.ts";
import useEmailRule from "@/composables/useEmailRule.ts";
import {VForm} from "vuetify/components";


const authStore = useAuthStore()
const {t} = useI18n()
const {styling} = useAppStyling()
const router = useRouter()

const emit = defineEmits<{
  (e: 'registered'): void
}>()

const loading = ref(false)
const username = ref("")

const password = ref("")
const passwordRepeat = ref("")
const email = ref("")
const registerForm = useTemplateRef<VForm>("register-form")
const rules = {
  usernameNeeded: (value: string) => (value && value !== '') || t('register.rules.username_needed'),
  passwordNeeded: (value: string) => (value && value !== '') || t('register.rules.password_needed'),
  repeatNotEqual: (value: string) => value === password.value || t('register.rules.passwords_not_equal'),
  emailNeeded: (value: string) => (value && value !== '') || t('register.rules.email_needed')
}
const {usernameCharacterRule} = useUserNameCharacterRule()
const {isValidEmailRule} = useEmailRule()
async function register() {

  if(!registerForm.value){
    return
  }
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
    router.push("/login")
  }
}

function reset(){
  if(registerForm.value){
    registerForm.value?.reset()
  }
}

</script>

<template>
  <v-row
      justify="center"
      class="fill-height"
  >
    <v-col
        cols="12"
        lg="4"
        class="mt-12"
    >
      <v-card
          elevation="5"
      >
        <template v-slot:append>
          <app-icon-btn
              icon="mdi-cog"
              to="/settings"
          />
        </template>
        <template v-slot:title>
          {{ t('register.title') }}
        </template>
        <v-card-subtitle>
          {{ t('register.subtitle') }}
        </v-card-subtitle>
        <v-card-text
            class="mt-3"
        >
          <v-row
              dense
              justify="center"
          >
            <v-col
                cols="12"
                lg="10"
            >
              <v-form
                  @submit.prevent="(event) => event.preventDefault()"
                  ref="register-form"
              >
                <v-row
                    dense
                >
                  <v-col>
                    <v-text-field
                        :label="t('register.username')"
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
                        :label="t('register.email')"
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
                        :label="t('register.password')"
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
                        :label="t('register.repeat_password')"
                        v-model="passwordRepeat"
                        :rules="[rules.repeatNotEqual]"
                        v-bind="styling"
                        @keyup.enter="register"
                    />
                  </v-col>
                </v-row>

              </v-form>
            </v-col>
          </v-row>
          <v-row
              class="mt-2"
              dense
              justify="center"
          >
            <v-col
              lg="10"
            >
              <v-btn
                  class="fill-width"
                  color="primary"
                  rounded="xl"
                  :text="t('register.btn')"
                  @click="register"
                  :loading="loading"
              />
            </v-col>
          </v-row>
          <v-divider class="mb-4 mt-6 border-opacity-25"/>
          <v-row
              dense
              justify="center"

          >
            <v-col
              cols="8"
              class="d-inline-block text-break text-center"
            >
              Already got an account?
              <a
                  class="login-link"
                  @click="router.push('/login')"
              >
                {{ t('register.back_to_login') }}
              </a>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.login-link{
  text-decoration: underline;
  &:hover{
    cursor: pointer;
  }
}
</style>