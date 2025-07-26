<script setup lang="ts">
import { ref, useTemplateRef} from "vue";
import {useI18n} from "vue-i18n";
import useAppStyling from "@/composables/useAppStyling.ts";
import useUserNameCharacterRule from "@/composables/useUserNameCharacterRule.ts";
import useEmailRule from "@/composables/useEmailRule.ts";
import {VForm} from "vuetify/components";

// TODO ALLOW USER TO LOGIN WITH USERNAME OR EMAIL
const {t} = useI18n()
const {textFieldStyling, btnStyle} = useAppStyling()
const router = useRouter()
const {userEndpoint} = useAxios()

const loading = ref(false)
const username = ref("")
const password = ref("")
const passwordRepeat = ref("")
const email = ref("")
const registerForm = useTemplateRef<VForm>("register-form")

const repeatRules = ref([
  (value: string|undefined|null) => !!value || t('register.rules.password_needed'),
  (value: string) => value === password.value || t('register.rules.passwords_not_equal')
])

const passwordRules = ref([
  (value: string|undefined|null) => !!value || t('register.rules.password_needed')
])

const {usernameCharacterRule} = useUserNameCharacterRule("register.rules.username_fmt_rule")
const usernameRules = ref([
  (value: string) => (value && value !== '') || t('register.rules.username_needed'),
  usernameCharacterRule
])

const {isValidEmailRule} = useEmailRule("register.rules.email_needed")
const emailRules = ref([
    isValidEmailRule,
])


async function register() {

  if(!registerForm.value){
    return
  }
  const {valid} = await registerForm.value.validate();
  if(!valid)
  {
    return
  }
  loading.value = true
  const payload = {
    username: username.value,
    password: password.value,
    password_confirmation: passwordRepeat.value,
    email: email.value
  }
  const { success, data, error  } = await userEndpoint.register(payload)
  if(!success){
    // TODO ERROR HANDLING
    console.log(error)
  }
  loading.value = false
  if (success) {
    reset()
    router.push("/login")
  }
}

function reset(){
  if(registerForm.value){
    registerForm.value.reset()
  }
}


</script>

<template>

    <v-card>
      <template v-slot:title>
        {{ t('register.title') }}
      </template>
      <template v-slot:subtitle>
        <span class="text-wrap">{{ t('register.subtitle') }}</span>
      </template>
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
                      :rules="usernameRules"
                      @keyup.enter="register"
                      v-bind="textFieldStyling"
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
                      :rules="emailRules"
                      @keyup.enter="register"
                      v-bind="textFieldStyling"
                  />
                </v-col>
              </v-row>
              <v-row
                  dense
              >
                <v-col>
                  <password-text-field
                      v-model="password"
                      :label="t('register.password')"
                      :rules="passwordRules"
                      @keyup.enter="register"
                  />
                </v-col>
              </v-row>
              <v-row
                  dense
              >
                <v-col>
                  <password-text-field
                      :label="t('register.repeat_password')"
                      v-model="passwordRepeat"
                      :rules="repeatRules"
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
            cols="12"
            class="d-flex flex-column justify-center align-center"
          >
            <span class="text-subtitle-1 text-center">{{t('register.existing_account')}}</span>
            <v-btn
                v-bind="btnStyle"
                variant="plain"
                varaint="small"
                color="secondary"
                to="/login"
                :text="t('register.back_to_login') "
            />

          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

</template>

<style scoped lang="scss">
.login-link{
  text-decoration: underline;
  &:hover{
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