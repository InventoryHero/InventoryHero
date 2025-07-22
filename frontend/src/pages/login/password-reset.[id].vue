<script setup lang="ts">
import {onBeforeMount, ref, useTemplateRef} from 'vue'
import {useI18n} from "vue-i18n";
import {useRouter} from "vue-router";
import {useNotification} from "@kyvg/vue3-notification";
import {VForm} from "vuetify/components";

const {userEndpoint} = useAxios()
const {t} = useI18n()
const router = useRouter()
const {notify} = useNotification()
const {btnStyle} = useAppStyling()


const {id} = defineProps<{
  id: string
}>()

const tokenValid = ref(false)
const preflightCheck = ref(true)
const password = ref("")
const passwordRepeat = ref("")
const valid = ref(false)
const resettingPassword = ref(false)

const tokenWasInvalid = ref(false)

const passwordForm = useTemplateRef<VForm>("passwordForm")


const passwordRules = ref([
  (value: string) => value !== '' || t('login.reset-password.rules.password_needed')
])
const passwordRepeatRules = ref([
  (value: string) => value !== '' || t('login.reset-password.rules.password_needed'),
  (value: string) => value === password.value || t('login.reset-password.rules.passwords_not_equal')
])


async function resetPassword(){
  if(resettingPassword.value){
    return
  }
  if(!passwordForm.value){
    return
  }
  const {valid} = await passwordForm.value.validate()
  if(!valid){
    return
  }
  resettingPassword.value = true
  const {success, data, error} = await userEndpoint.resetPasswordWithToken(id, {
    new_password: password.value,
    new_password_confirmation: passwordRepeat.value,
  })

  if(!success){
    // TODO
  }

  if(!data!.valid){
    if(data!.reason === "invalid_token"){
      tokenWasInvalid.value = true
    }
    resettingPassword.value = false
    return false
  }

  resettingPassword.value = false

  router.replace("/").then(() => {
    notify({
      title: t(`toasts.titles.success.password_reset`),
      text: t(`toasts.text.success.password_reset`),
      type: "success"
    })
  })

}

onBeforeMount(async () => {
  const {success, data, error} = await userEndpoint.checkPasswordResetCode(id)
  if(!success){
    // TODO
  }

  if(!data!.valid && data!.reason === "invalid_token"){
    tokenWasInvalid.value = true

  } else if(data!.valid){
    tokenValid.value = true
  }

  preflightCheck.value = false


})

</script>

<template>
    <v-skeleton-loader
      v-if="preflightCheck"
      type="card"
    />

    <v-container
      v-else-if="tokenWasInvalid"
    >
      <v-alert
        type="error"
        :text="t('login.reset-password.token_invalid')"
        class="mb-4"
      />
      <forgot-password
        @close="router.replace('/')"
      />
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
                ref="passwordForm"
                @submit.prevent="(event) => event.preventDefault()"
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
            class="mt-2"
            dense
            justify="center"
        >
          <v-col
            lg="10"
          >
            <v-btn
                v-bind="btnStyle"
                class="fill-width"
                color="primary"
                rounded="xl"
                :text="t('login.reset-password.btn')"
                @click="resetPassword"
                :loading="resettingPassword"
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

<style scoped lang="scss">

</style>

<route>
{
  "path": "/password-reset/:id",
  "props": true,
  "meta": {
    "requiresAuth": false,
    "requiresHousehold": false,
    "title": 'titles.password_reset',
    "layout": "unauthorized"
  }
}
</route>