<script setup lang="ts">
import {GeneralEndpoint} from "@/api/http";
import {useI18n} from "vue-i18n";
import {computed, ref, useTemplateRef} from "vue";
import useAxios from "@/composables/useAxios.ts";
import {UserEndpoint} from "@/api/http";
import {useNotification} from "@kyvg/vue3-notification";
import useAppStyling from "@/composables/useAppStyling.ts";
import {VForm} from "vuetify/components";
import useEmailRule from "@/composables/useEmailRule.ts";


const smtpEnabled = ref(false)
const {axios: generalEndpoint} = useAxios<GeneralEndpoint>("general")
const router = useRouter()

onMounted(() => {
  generalEndpoint.checkSmtp().then((enabled: boolean) => {
    smtpEnabled.value = enabled
  })
})


const {t} = useI18n()
const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {notify} = useNotification()
const {styling} = useAppStyling()
const email = ref("")
const valid = ref(false)
const emailForm = useTemplateRef<VForm>("emailForm")
const loading = ref(false)
const sent = ref(false)
const text = computed(() => {
  return t('forgot_password.description')
})



const emailNeeded = (value: string) => !!value || t('forgot_password.rules.email_needed')
const {isValidEmailRule} = useEmailRule()

async function resetPassword(){
  if(!emailForm.value){
    return
  }
  const {valid} = await emailForm.value.validate()
  if(!valid){
    return
  }
  loading.value = true
  userEndpoint.forgotPassword(email.value).then(({success, message}) => {
    loading.value = false

    if(!success){
      if((message ?? "") === ""){
        message = "unknown_error"
      }
      if(message === "email_not_confirmed"){
        router.push("/confirmation-missing")
      }
      return
    }

    notify({
      title: t('toasts.titles.success.forgot_password_request'),
      text: t('toasts.text.success.forgot_password_request'),
      type: 'success'
    })
    sent.value = true
  })

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
            {{ t('forgot_password.title') }}
        </template>
        <v-card-subtitle
            v-if="smtpEnabled"
            class="text-wrap">
          {{text}}
        </v-card-subtitle>
        <v-card-text
        >

          <v-row
              v-if="smtpEnabled"
              class="mt-2"
              dense
              justify="center"
          >
            <v-col
                cols="12"
                lg="10"
            >
              <v-form
                  @submit.prevent="(event) => event.preventDefault()"
                  ref="emailForm"
                  v-model="valid"
                  class="mb-2"
              >
                <v-row>
                  <v-col>
                    <v-text-field
                        v-bind="styling"
                        :placeholder="t('forgot_password.email_placeholder')"
                        :label="t('forgot_password.email_label')"
                        v-model="email"
                        :rules="[emailNeeded, isValidEmailRule]"
                        @keyup.enter="resetPassword"
                    />
                  </v-col>
                </v-row>
              </v-form>
            </v-col>
          </v-row>
          <v-row
              v-if="smtpEnabled"
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
                  :text="t('forgot_password.btn')"
                  @click="resetPassword"
                  :loading="loading"
              />
            </v-col>
          </v-row>
          <v-row
              v-if="!smtpEnabled"
              class="mt-2"
              dense
              justify="center"
          >
            <v-col
                cols="12"
                lg="10"
            >
              <v-sheet
                  class="pa-4 mb-2 d-flex text-justify d-inline-block"
                  color="accent"
                  rounded="lg"
                  style="hyphens:auto;"
              >
                {{ t('forgot_password.email_disabled') }}
              </v-sheet>
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
                :text="t('forgot_password.to_login')"
                append-icon="mdi-chevron-right"
                to="/login"
            />
          </v-row>

        </v-card-text>

      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>