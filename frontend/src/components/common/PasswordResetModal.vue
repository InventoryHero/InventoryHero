<script setup lang="ts">
import {computed, onMounted, ref, useTemplateRef} from 'vue'
import useAxios from "@/composables/useAxios.ts";
import {AdministrationEndpoint, GeneralEndpoint, UserEndpoint} from "@/api/http";
import useTextFieldStyle from "@/composables/useAppStyling.ts";
import {useI18n} from "vue-i18n";
import PasswordResetAdminBanner from "@/components/widgets/Administration/Users/PasswordResetAdminBanner.vue";
import {useNotification} from "@kyvg/vue3-notification";

defineOptions({
  inheritAttrs: false
})

const {axios: adminEndpoint} = useAxios<AdministrationEndpoint>("administration")
const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {axios: generalEndpoint} = useAxios<GeneralEndpoint>("general")
const {t: $t} = useI18n()
const {notify} = useNotification()

const active = defineModel<boolean>('active')
const userId = defineModel<number>('userId')

const {userName="", fromAdmin=false} = defineProps<{
  userName?: string,
  fromAdmin?: boolean
}>()

const {styling: textFieldStyle} = useAppStyling()

const oldPassword = ref<string>("")
const newPassword = ref<string>("")
const newPasswordRepeat = ref<string>("")
const resettingPassword = ref<boolean>(false)
const smtpEnabled = ref<boolean>(false)
const checkingSmtpConfig = ref<boolean>(false)
const passwordForm = useTemplateRef("passwordForm")

const rules = {
  required: (value: string) => value !== '' || $t('reset_password.rules.password_needed'),
  mismatch: (value: string) => newPassword.value === value || $t('reset_password.rules.passwords_not_equal'),
}

const resetEmailText = computed(() =>{
  if(fromAdmin){
    return $t('reset_password.send_email')
  }
  return $t('reset_password.forgot_password')
})

async function savePassword(){
  const {valid} = await passwordForm.value.validate()
  if(!valid){
    return
  }
  let saveSuccessful = false
  resettingPassword.value = true

  if(fromAdmin){
    const {success} = await adminEndpoint.resetPassword(userId!.value, newPassword.value)
    saveSuccessful = success

  } else{
    const {success} = await userEndpoint.resetPassword(oldPassword.value, newPassword.value)
    saveSuccessful = success
  }
  resettingPassword.value = false
  if(!saveSuccessful){
    return
  }

  notify({
    title: $t(`toasts.titles.success.reset_password${fromAdmin ? '_admin' : ''}`),
    text: $t(`toasts.text.success.reset_password${fromAdmin ? '_admin' : ''}`),
    type: "success"
  })
  closeModal()
}

function sendEmail(){
  resettingPassword.value = true
  let user = fromAdmin ? userId.value : undefined
  userEndpoint.resetPasswordRequest(user).then(result => {
    resettingPassword.value = false
    if(result.success){
      notify({
        title: $t(`toasts.titles.success.reset_password${fromAdmin ? '_admin' : ''}_mail`),
        text: $t(`toasts.text.success.reset_password${fromAdmin ? '_admin' : ''}_mail`),
        type: "success"
      })
      closeModal()
      return;
    }
    notify({
      title: $t(`toasts.titles.warning.${result.message}`),
      text: $t(`toasts.text.warning.${result.message}`),
      type: "warning"
    })
  })
}

function closeModal(){
  passwordForm.value.reset()
  active.value = false
}

onMounted(() => {
  generalEndpoint.checkSmtp().then((enabled)=> {
    smtpEnabled.value = enabled
  })
})
</script>

<template>
  <v-dialog
      v-model="active"
      :persistent="true"
      :no-click-animation="true"
  >
    <v-expand-transition>
      <v-row
          :no-gutters="true"
          justify="center"
          class="fill-height"
          v-if="active"
      >
        <v-col
            lg="6"
            cols="12"
        >
          <v-card
              v-bind="$attrs"
              max-height="60vh"
              class="d-flex flex-column"
          >
            <template v-slot:loader>
              <v-progress-linear
                  color="primary"
                  indeterminate
                  :active="resettingPassword || checkingSmtpConfig"
              />
            </template>
            <template v-slot:append>
              <app-icon-btn
                  icon="mdi-close"
                  @click="closeModal"
              />
            </template>
            <template v-slot:title>

              <template v-if="fromAdmin">
                {{ $t("reset_password.admin_title", {username: userName}) }}
              </template>
              <template v-else>
                {{ $t('reset_password.title') }}
              </template>

            </template>
            <v-card-text>
              <password-reset-admin-banner
                :from-admin="fromAdmin"
                :smtp-enabled="smtpEnabled"
              />
              <v-form
                  ref="passwordForm"
                  @submit.prevent="(event) => event.preventDefault()"
              >
                <v-row dense>
                  <v-col>
                    <app-password-textfield
                        v-if="!fromAdmin"
                        v-bind="textFieldStyle"
                        :label="$t('reset_password.old_password')"
                        v-model="oldPassword"
                        :rules="[rules.required]"
                        disable-min-length
                    />
                  </v-col>
                </v-row>

                <v-row dense>
                  <v-col>
                    <app-password-textfield
                        v-bind="textFieldStyle"
                        :label="$t('reset_password.password')"
                        v-model="newPassword"
                        :rules="[rules.required]"
                    />
                  </v-col>
                </v-row>

                <v-row dense>
                  <v-col>
                    <app-password-textfield
                        v-bind="textFieldStyle"
                        :label="$t('reset_password.password_repeat')"
                        v-model="newPasswordRepeat"
                        disable-min-length
                        :rules="[rules.mismatch]"
                    />
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-row
                justify="center"
                justify-sm="end"
                justify-md="end"
                justify-lg="end"
                dense
              >
                <v-col
                    lg="3"
                    md="3"
                    sm="3"
                    class="d-flex justify-center justify-lg-end justify-md-end justify-sm-end"
                >
                  <v-btn
                      prepend-icon="mdi-lock-reset"
                      :text="resetEmailText"
                      @click="sendEmail"
                      :disabled="resettingPassword || checkingSmtpConfig || !smtpEnabled"
                      density="comfortable"
                      variant="outlined"
                  />
                </v-col>
                <v-col
                    lg="3"
                    md="3"
                    sm="3"
                    class="d-flex justify-center justify-lg-end justify-md-end justify-sm-end"
                >
                  <v-btn
                      prepend-icon="mdi-content-save"
                      :text="$t('reset_password.reset_password')"
                      color="green"
                      variant="elevated"
                      density="comfortable"
                      @click="savePassword"
                      :disabled="resettingPassword"
                      :loading="resettingPassword"
                  />
                </v-col>
              </v-row>

            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-expand-transition>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>