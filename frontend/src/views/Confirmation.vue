<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {UserEndpoint} from "@/api/http";
import useAxios from "@/composables/useAxios.ts";
import { useRouter} from "vue-router";
import {useI18n} from "vue-i18n";

const {axios: userEndpoint} = useAxios<UserEndpoint>("user")
const {t: $t} = useI18n()
const router = useRouter()

const {code=""} = defineProps<{
  code?: string
}>()

const countdown = ref(5)
const time = ref(5)
const verified = ref(false)
const status = ref("")
const requestInProgress = ref(false)

const progressBarState = computed(() => {
  return (countdown.value-time.value) * (100/countdown.value)
})

onMounted(() => {
  requestInProgress.value = true
  userEndpoint.confirmEmail(code).then((result) => {
    requestInProgress.value = false
    verified.value = result.verified ?? false
    status.value = result.status
  })
})

</script>

<template>
  <v-row
    justify="center"
    class="fill-height mt-4"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <v-card>
        <template v-slot:loader>
          <v-progress-linear
              color="primary"
              :active="requestInProgress"
              :indeterminate="true"
          />
        </template>
        <template
          v-if="!requestInProgress"
        >
          <v-card-title >
            {{ verified ? $t('confirmation.email_confirmed') : $t('confirmation.failure')}}
          </v-card-title>
          <v-card-text
              v-if="verified"
              class="mt-2 d-flex flex-column justify-content-center align-center justify-center"
          >
            <v-progress-circular
                :model-value="progressBarState"
                :size="150"
                :width="8"
                color="primary"
            >
              <vue-countdown
                  :time="countdown*1000" :interval="1000" :auto-start="true"
                  v-slot="{seconds}"
                  @progress="time=$event.seconds"
                  @end="router.push('/login')"
              >
                <span class="text-wrap">
                {{ $t('confirmation.redirect_in', {seconds: seconds}) }}
              </span>
              </vue-countdown>
            </v-progress-circular>

            <span
                class="mt-4 text-h6"
            >
            {{ $t('confirmation.activated')}}
          </span>
          </v-card-text>
          <v-card-text
              v-else
          >
            {{ $t(`confirmation.${status}`) }}
          </v-card-text>
          <v-card-actions
              class="justify-end"
          >
            <v-btn
                variant="outlined"
                color="primary"
                to="/login"
                :disabled="requestInProgress"
            >
              {{ $t('confirmation.go_to_login')}}
            </v-btn>
          </v-card-actions>
        </template>
        <template v-else>
          <v-card-text
            class="d-flex justify-center"
          >
            {{ $t('confirmation.verifying') }}
          </v-card-text>
        </template>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>