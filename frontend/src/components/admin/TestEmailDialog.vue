<template>
  <v-dialog
    v-model="active"
    :max-height="height"
    :max-width="width"
  >
    <v-card>
      <v-card-text>
        <v-form
          @submit.prevent="sendTestEmail"
          ref="emailForm"
        >
          <v-text-field
            v-bind="textFieldStyling"
            v-model="email"
            :rules="emailRules"
            :label="t('configuration.test_email.email')"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          v-bind="btnStyle"
          prepend-icon="mdi-email"
          :text="t('configuration.test_email.send')"
          @click="sendTestEmail"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useNotification } from '@kyvg/vue3-notification'

const { height, width } = useDialogSize()
const { t } = useI18n()
const { textFieldStyling, btnStyle } = useAppStyling()
const { admin } = useAxios()
const { emailRules } = useValidationRules()
const { notify } = useNotification()

const active = defineModel<boolean>('active', {
  required: true
})

const emailForm = useTemplateRef('emailForm')
const email = ref<string>()

const sendTestEmail = async () => {
  if (!emailForm.value) {
    return
  }

  const { valid } = await emailForm.value.validate()
  if (!valid) {
    return
  }

  const { success } = await admin.sendTestEmail(email.value!)
  // TODO react to failure, check what email on the server side can return
  if (success) {
    notify({
      title: t('configuration.test_email.sent'),
      type: 'info'
    })
  }
  active.value = false
  emailForm.value.reset()
}
</script>

<style scoped></style>
