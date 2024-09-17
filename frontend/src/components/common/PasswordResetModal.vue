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

const {styling: textFieldStyle} = useTextFieldStyle()

const oldPassword = ref<string>("")
const newPassword = ref<string>("")
const newPasswordRepeat = ref<string>("")
const resettingPassword = ref<boolean>(false)
const smtpEnabled = ref<boolean>(false)
const checkingSmtpConfig = ref<boolean>(false)
const passwordForm = useTemplateRef("passwordForm")

const rules = {
  required: (value: string) => value !== '' || $t('administration.users.password_reset.password_needed'),
  mismatch: (value: string) => newPassword.value === value || $t('administration.users.password_reset.passwords_not_equal'),
}

const resetEmailText = computed(() =>{
  if(fromAdmin){
    return $t('administration.users.password_reset.send_email')
  }
  return $t('account.password_reset.forgot_password')
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
    title: $t(`toasts.titles.success.password_reset${fromAdmin ? '_admin' : ''}`),
    text: $t(`toasts.text.success.password_reset${fromAdmin ? '_admin' : ''}`),
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
        title: $t(`toasts.titles.success.password_reset${fromAdmin ? '_admin' : ''}_mail`),
        text: $t(`toasts.text.success.password_reset${fromAdmin ? '_admin' : ''}_mail`),
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
            <v-card-title
              class="d-flex justify-space-between align-center"
            >
              <span
                v-if="fromAdmin"
              >
                {{ $t("administration.users.password_reset.title", {username: userName}) }}
              </span>
              <span
                v-else
              >
                {{ $t('account.password_reset.title') }}
              </span>
              <v-btn
                  density="compact"
                  icon="mdi-close"
                  @click="closeModal"
              />
            </v-card-title>
            <v-card-text>
              <password-reset-admin-banner
                :from-admin="fromAdmin"
                :smtp-enabled="smtpEnabled"
              />
              <v-form
                  ref="passwordForm"
              >
                <app-password-textfield
                    v-if="!fromAdmin"
                    v-bind="textFieldStyle"
                    :label="$t('account.password_reset.old_password')"
                    class="mb-4"
                    v-model="oldPassword"
                    :rules="[rules.required]"
                    :disable-min-length="true"
                />

                <app-password-textfield
                    v-bind="textFieldStyle"
                    :label="$t('administration.users.password_reset.password')"
                    class="mb-4"
                    v-model="newPassword"
                    :rules="[rules.required]"
                />

                <app-password-textfield
                    v-bind="textFieldStyle"
                    :label="$t('administration.users.password_reset.password_repeat')"
                    class="mb-4"
                    v-model="newPasswordRepeat"
                    :rules="[rules.mismatch]"
                />
              </v-form>
            </v-card-text>
            <v-card-actions
              class="justify-space-between"
            >
              <v-btn
                  prepend-icon="mdi-cancel"
                  :text="$t('administration.users.password_reset.cancel')"
                  @click="closeModal"
                  :disabled="resettingPassword"
              />
              <div>
                <v-btn
                    prepend-icon="mdi-content-save"
                    :text="resetEmailText"
                    @click="sendEmail"
                    :disabled="resettingPassword || checkingSmtpConfig || !smtpEnabled"

                />
                <v-btn
                    prepend-icon="mdi-content-save"
                    :text="$t('administration.users.password_reset.save')"
                    @click="savePassword"
                    :disabled="resettingPassword"
                    :loading="resettingPassword"
                />
              </div>

            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-expand-transition>
  </v-dialog>
</template>

<style scoped lang="scss">

</style>