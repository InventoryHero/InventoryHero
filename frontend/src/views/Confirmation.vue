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
    class="fill-height"
  >
    <v-col
      cols="12"
      lg="4"
      class="mt-12"
    >
      <v-card
        v-if="!requestInProgress"
        elevation="5"
      >
        <template v-slot:title>
          {{ verified ? $t('confirmation.email_confirmed') : $t('confirmation.failure')}}
        </template>
        <v-card-subtitle class="d-inline-block text-wrap">
          {{ $t('confirmation.activated')}}
        </v-card-subtitle>
        <v-card-text

        >
          <v-row
            dense
            justify="center"
            class="mb-4"
          >
            <v-col
                cols="12"
                lg="10"
                class="d-flex justify-center"

            >
              <template
                  v-if="verified"
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

              </template>
              <template
                v-else
              >
                {{ $t(`confirmation.${status}`) }}
              </template>
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
                  :text="$t('confirmation.go_to_login')"
                  to="/login"
                  :disabled="requestInProgress"
                  :loading="requestInProgress"
              />
            </v-col>
          </v-row>
        </v-card-text>
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
          {{$t('confirmation.verifying')}}
        </v-card-title>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>