<script setup lang="ts">
import useShareMethods from '@/composables/useShareMethods.ts'
import { HouseholdWithMemberPublic } from '@/api/types/households.ts'

const { household: householdEndpoint } = useAxios()
const { t } = useI18n()
const { width, height } = useDialogSize()

const { household } = defineProps<{
  household: HouseholdWithMemberPublic
}>()

const active = defineModel<boolean>('active', {
  required: true
})

const { textFieldStyling } = useAppStyling()

const loadingInviteCode = ref(false)
const inviteCode = ref<string>('')

const inviteLink = computed(() => {
  if (loadingInviteCode.value) {
    return t('households.invite.generating_code')
  }
  return inviteCode.value
})

function generateInviteCode() {
  loadingInviteCode.value = true
  householdEndpoint
    .createInvite(household.id)
    .then(({ success, data, error }) => {
      if (success) {
        inviteCode.value = data?.code!
      }
      loadingInviteCode.value = false
    })
}

const {
  webShareApiSupported,
  copyToClipboardIcon,
  emailShare,
  whatsAppShare,
  navigatorShare,
  copyToClipboard
} = useShareMethods(inviteLink, ref(household.name))

function share() {
  navigatorShare()
}

onMounted(() => {
  generateInviteCode()
})
</script>

<template>
  <v-dialog
    v-model="active"
    persistent
    no-click-animation
    :max-width="width"
    :max-height="height"
  >
    <v-card
      :loading="loadingInviteCode"
      :disabled="loadingInviteCode"
      :title="t('households.invite.title')"
    >
      <template v-slot:loader="{ isActive }">
        <v-progress-linear
          color="primary"
          :active="isActive"
          indeterminate
        />
      </template>
      <template v-slot:append>
        <v-icon-btn
          icon="mdi-close"
          @click="active = false"
        />
      </template>

      <v-card-text>
        <span class="text-medium-emphasis">
          {{ t('households.invite.copy_to_clipboard') }}
        </span>
        <v-text-field
          v-bind="textFieldStyling"
          class="mt-4 mb-4"
          :clearable="false"
          :loading="loadingInviteCode"
          readonly
          :model-value="inviteLink"
        >
          <template v-slot:append>
            <v-icon-btn
              :disabled="loadingInviteCode"
              variant="plain"
              @click="copyToClipboard()"
              size="large"
              class="ms-n3 me-n3"
            >
              <transition
                name="icon-morph"
                mode="out-in"
              >
                <v-icon
                  :key="copyToClipboardIcon"
                  :icon="copyToClipboardIcon"
                  size="large"
                  :color="
                    copyToClipboardIcon === 'mdi-check-bold'
                      ? 'success'
                      : undefined
                  "
                />
              </transition>
            </v-icon-btn>
          </template>
        </v-text-field>
        <div class="text-end text-medium-emphasis">
          {{ t('households.invite.or') }}
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <template v-if="webShareApiSupported">
          <v-icon-btn
            icon="mdi-share-variant"
            color="primary"
            size="large"
            @click="share"
          />
        </template>
        <template v-else>
          <s-email :share-options="emailShare">
            <v-icon-btn
              icon="mdi-email"
              variant="tonal"
              color="primary"
              size="large"
            />
          </s-email>
          <s-whats-app :share-options="whatsAppShare">
            <v-icon-btn
              variant="tonal"
              icon="mdi-whatsapp"
              color="primary"
              size="large"
            />
          </s-whats-app>
        </template>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped lang="scss">
.icon-morph-leave-active {
  transition: all 0.32s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.icon-morph-enter-active {
  transition: all 0.25s cubic-bezier(0.25, 0.8, 0.5, 1); /* faster enter */
}

.icon-morph-enter-from,
.icon-morph-leave-to {
  opacity: 0;
  transform: scale(0.5) rotate(-30deg);
  color: var(--v-theme-on-background);
}

.icon-morph-enter-to,
.icon-morph-leave-from {
  opacity: 1;
  transform: scale(1) rotate(0deg);
  color: var(--v-theme-primary);
}

@media (prefers-reduced-motion: reduce) {
  .icon-morph-enter-from,
  .icon-morph-leave-to {
    transform: none;
  }
}
</style>
