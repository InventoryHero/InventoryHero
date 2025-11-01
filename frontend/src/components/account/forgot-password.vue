<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { computed, ref, useTemplateRef } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import useAppStyling from '@/composables/useAppStyling.ts'
import { VForm } from 'vuetify/components'
import useEmailRule from '@/composables/useEmailRule.ts'
// TODO ONCE EMAILS ARE IMPLEMENTED
const router = useRouter()
const { t } = useI18n()
const { userEndpoint } = useAxios()
const { notify } = useNotification()
const { textFieldStyling, btnStyle } = useAppStyling()
const { mdAndUp } = useDisplay()

const active = defineModel<boolean>('active', {
  required: true
})

const email = ref('')
const valid = ref(false)
const emailForm = useTemplateRef<VForm>('emailForm')
const loading = ref(false)

const { isValidEmailRule } = useEmailRule(
  'login.reset-password.rules.email_needed'
)

const close = () => {
  active.value = false
  emailForm.value.reset()
}

async function resetPassword() {
  if (!emailForm.value) {
    return
  }
  const { valid } = await emailForm.value.validate()
  if (!valid) {
    return
  }
  loading.value = true
  userEndpoint
    .resetPassword({
      email: email.value
    })
    .then(({ success, data, error }) => {
      loading.value = false

      if (!success) {
        return
      }

      notify({
        title: t('login.reset-password.description'),
        type: 'success',
        duration: 10000,
        closeOnClick: true
      })
      close()
    })
}

onBeforeRouteUpdate(() => {
  return false
})
</script>

<template>
  <v-dialog
    v-model="active"
    height="fit-content"
    :width="mdAndUp ? '600px' : '100%'"
  >
    <v-card elevation="5">
      <template v-slot:loader>
        <v-progress-linear
          indeterminate
          :active="loading"
          color="primary"
        />
      </template>
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="close"
        />
      </template>
      <template v-slot:title>
        <span class="text-wrap">{{ t('login.reset-password.title') }}</span>
      </template>
      <v-card-text>
        <v-row
          class="mt-2"
          dense
          justify="center"
        >
          <v-col
            cols="12"
            lg="10"
          >
            <v-form
              @submit.prevent="resetPassword"
              ref="emailForm"
              v-model="valid"
              class="mb-2"
            >
              <v-row>
                <v-col>
                  <v-text-field
                    v-bind="textFieldStyling"
                    :placeholder="t('login.reset-password.email')"
                    :label="t('login.reset-password.email')"
                    v-model="email"
                    :rules="[isValidEmailRule]"
                    @keyup.enter="resetPassword"
                  />
                </v-col>
              </v-row>
            </v-form>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn
          v-bind="btnStyle"
          variant="elevated"
          class="me-2 mb-2"
          color="primary"
          rounded="xl"
          :text="t('login.reset-password.btn')"
          @click="resetPassword"
          :loading="loading"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss"></style>
