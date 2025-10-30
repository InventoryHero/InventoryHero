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

const email = ref('')
const valid = ref(false)
const emailForm = useTemplateRef<VForm>('emailForm')
const loading = ref(false)
const text = computed(() => {
  return t('login.reset-password.description')
})

const emit = defineEmits(['close'])

const { isValidEmailRule } = useEmailRule(
  'login.reset-password.rules.email_needed'
)

const close = () => {
  emailForm.value.reset()
  emit('close')
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
        title: t('toasts.titles.success.login.reset-password_request'),
        text: t('toasts.text.success.login.reset-password_request'),
        type: 'success'
      })
      close()
    })
}

onBeforeMount(() => {})
</script>

<template>
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
      <span class="text-subtitle-2 text-medium-emphasis">{{ text }}</span>
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
            @submit.prevent="(event) => event.preventDefault()"
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
      <v-row
        class="mt-2"
        dense
        justify="center"
      >
        <v-col lg="10">
          <v-btn
            v-bind="btnStyle"
            class="fill-width"
            color="primary"
            rounded="xl"
            :text="t('login.reset-password.btn')"
            @click="resetPassword"
            :loading="loading"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<style scoped lang="scss"></style>
