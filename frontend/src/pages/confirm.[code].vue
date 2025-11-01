<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { userEndpoint } = useAxios()
const { t } = useI18n()
const router = useRouter()
const { btnStyle } = useAppStyling()

const { code = '' } = defineProps<{
  code?: string
}>()

const countdown = ref(5)
const time = ref(5)
const verified = ref(false)
const status = ref('')
const requestInProgress = ref(false)

const progressBarState = computed(() => {
  return (countdown.value - time.value) * (100 / countdown.value)
})

onMounted(() => {
  requestInProgress.value = true
  userEndpoint.confirmEmail(code).then(({ success, error }) => {
    if (!success) {
      requestInProgress.value = false
      status.value = error ?? t('confirmation.unknown_error')
      return
    }
    requestInProgress.value = false
    verified.value = success
  })
})
</script>

<template>
  <v-card
    v-if="!requestInProgress"
    elevation="5"
  >
    <template v-slot:title>
      {{
        verified ? t('confirmation.email_confirmed') : t('confirmation.failure')
      }}
    </template>
    <v-card-subtitle
      class="d-inline-block text-wrap"
      v-if="verified"
    >
      {{ t('confirmation.activated') }}
    </v-card-subtitle>
    <v-card-text class="d-flex flex-column justify-center align-center">
      <template v-if="verified">
        <v-progress-circular
          :model-value="progressBarState"
          :size="150"
          :width="8"
          color="primary"
        />
        <vue-countdown
          :time="countdown * 1000"
          :interval="1000"
          :auto-start="true"
          class="mt-2"
          v-slot="{ seconds }"
          @progress="time = $event.seconds"
          @end="router.replace('/login')"
        >
          <span class="text-wrap">
            {{ t('confirmation.redirect_in', { seconds: seconds }) }}
          </span>
        </vue-countdown>
      </template>
      <template v-else>
        {{ status }}
      </template>
    </v-card-text>
    <v-card-actions class="justify-center">
      <v-btn
        v-bind="btnStyle"
        :text="t('confirmation.go_to_login')"
        to="/login"
        :disabled="requestInProgress"
        :loading="requestInProgress"
      />
    </v-card-actions>
  </v-card>
  <v-card
    elevation="5"
    v-else
  >
    <template v-slot:loader>
      <v-progress-linear
        color="primary"
        :active="requestInProgress"
        :indeterminate="true"
      />
    </template>
    <v-card-title class="d-inline-block text-wrap">
      {{ t('confirmation.verifying') }}
    </v-card-title>
  </v-card>
</template>

<style scoped lang="scss"></style>

<route>
{
  "props": true,
  "meta": {
    "requiresAuth": false,
    "requiresHousehold": false,
    "title": 'titles.confirmation',
    "layout": "unauthorized"
  }
}
</route>
