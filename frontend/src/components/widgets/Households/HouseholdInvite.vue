<script setup lang="ts">

import {Household} from "@/types";
import useAxios from "@/composables/useAxios.ts";
import {HouseholdEndpoint} from "@/api/http";
import {useAuthStore} from "@/store";
import useShareMethods from "@/composables/useShareMethods.ts";

const {axios: householdEndpoint} = useAxios<HouseholdEndpoint>("household")
const userStore = useAuthStore()
const {t} = useI18n()
const {household} = defineProps<{
  household: Household
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const {styling} = useAppStyling()

const loadingInviteCode = ref(false)
const inviteCode = ref<string>("")


const inviteLink = computed(() => {
  if(loadingInviteCode.value){
    return t('invite.generating_code')
  }
  return `${window.location.origin}/join/${inviteCode.value}`
})

function generateInviteCode(){
  loadingInviteCode.value = true
  householdEndpoint.createInviteCode(household.id).then((data) => {
    if(data.success)
    {
      inviteCode.value = data.code
    }
    loadingInviteCode.value = false
  })
}

const {
  webShareApiSupported,
  copiedConfirm,
  emailShare,
  whatsAppShare,
  navigatorShare,
  copyToClipboard
} = useShareMethods(inviteLink, ref(household.name))

function share(){
  navigatorShare()
}

onMounted(() => {
  generateInviteCode()
})

</script>

<template>
  <v-row
    justify="center"
  >
    <v-col
      cols="12"
      lg="6"
    >
      <v-snackbar
          v-model="copiedConfirm"
          :timeout="2000"
          elevation="24"
          rounded="pill"
          color="success"
          :multi-line="false"
          @click="copiedConfirm=false"

      >
        <p
            class="d-flex justify-center"
        >
          {{ $t('toasts.titles.success.copied_to_clipboard')}}
        </p>
      </v-snackbar>

      <v-card
        :loading="loadingInviteCode"
        :disabled="loadingInviteCode"
      >
        <template v-slot:loader="{ isActive }">
          <v-progress-linear
            color="primary"
            :active="isActive"
            indeterminate
          />
        </template>

        <v-card-title
            class="d-flex justify-space-between align-center"
        >
          {{ $t('invite.title') }}
          <app-icon-btn
              icon="mdi-close"
              @click="emit('close')"
          />
        </v-card-title>
        <v-card-subtitle>
          {{ $t('invite.copy_to_clipboard')}}
        </v-card-subtitle>

        <v-card-text>

          <v-text-field
            v-bind="styling"
            :clearable="false"
            :loading="loadingInviteCode"
            readonly
            :model-value="inviteLink"
          >
            <template v-slot:append>
              <app-icon-btn
                  :disabled="loadingInviteCode"
                  icon="mdi-clipboard-outline"
                  @click="copyToClipboard()"
                  size="large"
              />
            </template>
          </v-text-field>
        </v-card-text>
        <v-card-subtitle
          class="d-flex justify-end"
        >
          {{ $t('invite.or')}}
        </v-card-subtitle>
        <v-card-actions
          class="justify-end"
        >
          <template
            v-if="webShareApiSupported"
          >
            <app-icon-btn
                icon="mdi-share-variant"
                color="primary"
                size="x-large"
                class="me-2"
                @click="share"
            />
          </template>
          <template
            v-else
          >
            <s-email
              :share-options="emailShare"
            >
              <app-icon-btn
                icon="mdi-email"
                color="primary"
                size="x-large"
                class="me-1"
              />
            </s-email>
            <s-whats-app
              :share-options="whatsAppShare"
            >
              <app-icon-btn
                icon="mdi-whatsapp"
                color="primary"
                size="x-large"
                class="me-1"
              />
            </s-whats-app>
          </template>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped lang="scss">

</style>