<script setup lang="ts">

import {useAuthStore} from "@/store";
import useAxios from "@/composables/useAxios.ts";
import {GeneralEndpoint} from "@/api/http";
import {useTemplateRef} from "vue";
import {VForm} from "vuetify/components";

const {t} = useI18n()
const {styling} = useAppStyling()
const router = useRouter()


const username = ref<string>("")
const password = ref<string>("")

const rules = {
  usernameNeeded: (value: string) => value !== '' || t('login.rules.username_needed'),
  passwordNeeded: (value: string) => value !== '' || t('login.rules.password_needed')
}


const loginForm = useTemplateRef<VForm>("login-form")
const loading = ref(false)
const authStore = useAuthStore()

async function login(){
  if(!loginForm.value)
  {
    return
  }
  const {valid} = await loginForm.value.validate()
  if(!valid) {
    return
  }
  loading.value = true;
  authStore.login(username.value, password.value).then(({success, message}) => {
    if(message === "email_not_confirmed"){
      router.push("/confirmation-missing")
    }
    loading.value = false;
    if(loginForm.value && success){
      loginForm.value.reset()
    }
  })
}



const smtpEnabled = ref(false)
const {axios: generalEndpoint} = useAxios<GeneralEndpoint>("general")
onMounted(() => {
  generalEndpoint.checkSmtp().then((enabled: boolean) => {
    smtpEnabled.value = enabled
  })
})
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
          class="d-flex flex-column"
      >
        <template v-slot:loader>
          <v-progress-linear
            indeterminate
            :active="loading"
            color="primary"
          />
        </template>
        <template v-slot:append>
          <app-icon-btn
              icon="mdi-cog"
              to="/settings"
          />
        </template>
        <template v-slot:title>
          {{ t('login.title') }}
        </template>
        <v-card-subtitle>
          {{ $t('login.subtitle') }}
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
                  ref="login-form"
                  @submit.prevent="(event) => event.preventDefault()"
              >
                <v-row dense>
                  <v-col>
                    <v-text-field
                        :label="$t('login.username')"
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
                        :label="$t('login.password')"
                        v-model="password"
                        :disable-min-length="true"
                        @keyup.enter="login"
                        v-bind="styling"

                    />
                    <div
                        class="ms-2 mt-1"
                    >
                      <a

                          v-if="smtpEnabled"
                          class="reset-password text-caption text-primary"
                          @click="router.push('/forgot-password')"
                      >
                        {{ $t('login.forgot_password_btn') }}
                      </a>
                    </div>
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
                  :text="t('login.btn')"
                  :loading="loading"
                  @click="login"
              />
            </v-col>
          </v-row>
          <v-divider class="mb-4 mt-6 border-opacity-25"/>
          <v-row
              dense
              justify="center"
              class="pa-1"
          >
              <v-btn
                  density="compact"
                  size="small"
                  variant="plain"
                  :text="t('login.register')"
                  append-icon="mdi-chevron-right"
                  to="/register"
              />
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">
.reset-password{
  &:hover{
    cursor: pointer;
    text-decoration: underline;
  }
}

.warning-banner{
  &:hover{
    cursor: pointer;
  }
}
</style>